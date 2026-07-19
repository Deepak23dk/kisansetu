# KisanSetu - Keploy Test Recorder and Runner for Windows
# This file provides a native Windows CLI wrapper to record and test FastAPI apps 
# using the standard Keploy YAML format.

import os
import sys
import json
import time
import yaml
import httpx
import threading
import uvicorn
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

TESTS_DIR = os.path.join("keploy", "tests")

# HTTP status message mapping
STATUS_MESSAGES = {
    200: "OK",
    201: "Created",
    202: "Accepted",
    204: "No Content",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    500: "Internal Server Error",
}

# -------------------------------------------------------------
# Keploy Recording Middleware (Pure ASGI)
# -------------------------------------------------------------
class KeployRecordMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # Exclude health check
        path = scope.get("path", "")
        if path == "/health":
            await self.app(scope, receive, send)
            return

        # Intercept request body
        req_body = b""
        async def mock_receive():
            nonlocal req_body
            message = await receive()
            if message["type"] == "http.request":
                req_body += message.get("body", b"")
            return message

        # Intercept response body and status
        status_code = 200
        resp_headers = {}
        resp_body = b""

        async def mock_send(message):
            nonlocal status_code, resp_headers, resp_body
            if message["type"] == "http.response.start":
                status_code = message.get("status", 200)
                headers_list = message.get("headers", [])
                resp_headers = {}
                for k, v in headers_list:
                    try:
                        k_str = k.decode("utf-8").lower()
                        v_str = v.decode("utf-8")
                        resp_headers[k_str] = v_str
                    except Exception:
                        pass
            elif message["type"] == "http.response.body":
                resp_body += message.get("body", b"")
            
            await send(message)

        # Call app
        await self.app(scope, mock_receive, mock_send)

        # Save after call completes
        try:
            self._save_interaction(scope, req_body, status_code, resp_headers, resp_body)
        except Exception as e:
            print(f"[Keploy Recorder] Failed to save test case: {e}")

    def _save_interaction(self, scope, req_body: bytes, status_code: int, resp_headers: dict, resp_body: bytes):
        os.makedirs(TESTS_DIR, exist_ok=True)
        
        # Determine test index by counting existing files
        test_files = [f for f in os.listdir(TESTS_DIR) if f.startswith("test-") and f.endswith(".yaml")]
        test_index = len(test_files) + 1
        test_name = f"test-{test_index}"
        
        # Decode bodies
        req_body_str = req_body.decode("utf-8", errors="replace")
        resp_body_str = resp_body.decode("utf-8", errors="replace")

        # Prepare URL with query
        path = scope.get("path", "")
        query_string = scope.get("query_string", b"").decode("utf-8")
        url_with_query = path
        if query_string:
            url_with_query += f"?{query_string}"

        # Clean headers
        req_headers = {}
        for k, v in scope.get("headers", []):
            try:
                k_str = k.decode("utf-8")
                v_str = v.decode("utf-8")
                if k_str.lower() not in ["host", "user-agent", "accept-encoding"]:
                    req_headers[k_str] = v_str
            except Exception:
                pass

        # Remove volatile headers from response
        clean_resp_headers = {k: v for k, v in resp_headers.items() if k not in ["content-length", "date", "server"]}

        test_data = {
            "version": "api.keploy.io/v1beta1",
            "kind": "Http",
            "name": test_name,
            "spec": {
                "metadata": {
                    "name": path.strip("/").replace("/", "_") or "root",
                    "operation": scope["method"]
                },
                "request": {
                    "method": scope["method"],
                    "url": url_with_query,
                    "header": req_headers,
                    "body": req_body_str
                },
                "response": {
                    "status_code": status_code,
                    "header": clean_resp_headers,
                    "body": resp_body_str,
                    "status_message": STATUS_MESSAGES.get(status_code, "OK")
                }
            }
        }

        yaml_path = os.path.join(TESTS_DIR, f"{test_name}.yaml")
        with open(yaml_path, "w", encoding="utf-8") as f:
            yaml.dump(test_data, f, default_flow_style=False, sort_keys=False)
        
        print(f"[Keploy Recorder] Recorded test case: {yaml_path}")

# -------------------------------------------------------------
# CLI Commands
# -------------------------------------------------------------
def run_record():
    print("=============================================================")
    print("          KisanSetu Keploy Recorder (Windows Native)          ")
    print("=============================================================")
    print(f"Starting server in RECORD mode. Interactions will be saved to: {TESTS_DIR}")
    
    # Import the FastAPI application
    from main import app
    
    # Dynamically inject the recording middleware
    app.add_middleware(KeployRecordMiddleware)
    
    # Run server
    uvicorn.run(app, host="127.0.0.1", port=8000)

def run_test():
    print("=============================================================")
    print("           KisanSetu Keploy Test Runner (Windows)            ")
    print("=============================================================")
    
    if not os.path.exists(TESTS_DIR):
        print(f"Error: No tests found in {TESTS_DIR}. Run record mode first!")
        sys.exit(1)
        
    test_files = sorted(
        [f for f in os.listdir(TESTS_DIR) if f.startswith("test-") and f.endswith(".yaml")],
        key=lambda x: int(x.split("-")[1].split(".")[0])
    )
    
    if not test_files:
        print(f"Error: No test-X.yaml files found in {TESTS_DIR}.")
        sys.exit(1)
        
    print(f"Found {len(test_files)} test case(s) in {TESTS_DIR}.")
    
    # Clean database before testing to ensure reproducible test run
    print("Cleaning local Qdrant and SQLite databases for test isolation...")
    import shutil
    if os.path.exists("./qdrant_db"):
        try:
            shutil.rmtree("./qdrant_db")
        except Exception as e:
            print(f"Warning: Could not remove ./qdrant_db: {e}")
    if os.path.exists("./history.db"):
        try:
            os.remove("./history.db")
        except Exception as e:
            print(f"Warning: Could not remove ./history.db: {e}")
            
    # Start server in background thread
    print("Starting FastAPI server in background thread...")
    from main import app
    
    def start_server():
        # Run with warning log level to avoid polluting output
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="warning")
        
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Wait for server to boot
    time.sleep(2.0)
    print("FastAPI server started at http://127.0.0.1:8000\n")

    client = httpx.Client(base_url="http://127.0.0.1:8000", timeout=10.0)
    passed_tests = 0
    failed_tests = 0
    
    for file_name in test_files:
        file_path = os.path.join(TESTS_DIR, file_name)
        print(f"Running test case: {file_name} ... ", end="")
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                test_case = yaml.safe_load(f)
                
            spec = test_case["spec"]
            req_spec = spec["request"]
            resp_spec = spec["response"]
            
            method = req_spec["method"]
            url = req_spec["url"]
            headers = req_spec["header"]
            body = req_spec["body"]
            
            # Send HTTP request
            res = client.request(
                method=method,
                url=url,
                headers=headers,
                content=body.encode("utf-8") if body else None
            )
            
            # Assertions
            expected_status = resp_spec["status_code"]
            actual_status = res.status_code
            
            if expected_status != actual_status:
                print("FAIL")
                print(f"  -> Status code mismatch: Expected {expected_status}, got {actual_status}")
                failed_tests += 1
                continue
                
            # Compare response body (try JSON comparison if applicable)
            expected_body_str = resp_spec["body"]
            actual_body_str = res.text
            
            body_match = False
            
            # Check if it is an audio response
            is_audio = False
            expected_headers = resp_spec.get("header", {})
            for hk, hv in expected_headers.items():
                if hk.lower() == "content-type" and "audio" in hv.lower():
                    is_audio = True
                    break
            
            if is_audio:
                # For audio responses, we assert that the status code is correct and some bytes were returned
                body_match = len(res.content) > 0
                if not body_match:
                    print("FAIL")
                    print("  -> Expected audio bytes, but got empty response body.")
                    failed_tests += 1
                    continue
            else:
                try:
                    expected_json = json.loads(expected_body_str)
                    actual_json = json.loads(actual_body_str)
                    
                    # Check for key values, ignoring random/varying values like "timestamp" or UUIDs
                    # in keys that we know are dynamic
                    def clean_dynamic_keys(obj):
                        if isinstance(obj, dict):
                            # ignore timestamp and id if they exist in comparisons to prevent test flakiness
                            return {k: clean_dynamic_keys(v) for k, v in obj.items() if k not in ["timestamp", "created_at", "id"]}
                        elif isinstance(obj, list):
                            return [clean_dynamic_keys(v) for v in obj]
                        return obj
                        
                    body_match = clean_dynamic_keys(expected_json) == clean_dynamic_keys(actual_json)
                except Exception:
                    body_match = expected_body_str.strip() == actual_body_str.strip()
                
            if not body_match:
                print("FAIL")
                print(f"  -> Body mismatch:")
                print(f"     Expected: {expected_body_str}")
                print(f"     Got:      {actual_body_str}")
                failed_tests += 1
            else:
                print("PASS")
                passed_tests += 1
                
        except Exception as e:
            print("FAIL")
            print(f"  -> Execution error: {e}")
            failed_tests += 1
            
    print("\n-------------------------------------------------------------")
    print(f"Test Run Complete: {passed_tests} Passed, {failed_tests} Failed.")
    print("-------------------------------------------------------------")
    
    if failed_tests > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python keploy_windows.py record      # Start server in record mode")
        print("  python keploy_windows.py test        # Replay and assert recorded test cases")
        sys.exit(1)
        
    command = sys.argv[1].lower()
    if command == "record":
        run_record()
    elif command == "test":
        run_test()
    else:
        print(f"Unknown command: {command}")
        print("Valid commands are: record, test")
        sys.exit(1)
