# KisanSetu - AI Crop Assistant (FastAPI + Mem0 + Gemini + Web UI)

KisanSetu is a fully functioning AI crop assistant backend and web UI prototype built for Indian smallholder farmers. It helps farmers:
1. **Diagnose Crop Diseases**: Using real AI (Gemini 1.5 Flash) via text and multimodal leaf image uploads, retaining persistent per-farmer conversation context across sessions using Mem0 memory.
2. **Text-to-Speech (TTS) Voice Synthesis**: Direct audio playback of the generated AI advice in English or Hindi, prototyping planned local language integrations (e.g., Gnani.ai).
3. **Mandi Market Prices**: Real-time market price lookups for 5 crops across 4 major Indian states (mocked dataset).

---

## 📂 Project Structure

* **`main.py`**: Core FastAPI application, mounts static frontend directory, implements memory retrieval/storage, price simulation, and voice streaming endpoints.
* **`advice.py`**: Interacts with the Gemini API using the `google-generativeai` SDK. Implements base64 image decoding and falls back to a keyword-matching database if keys are missing.
* **`keploy_windows.py`**: ASGI recording middleware and replay test runner designed specifically for Windows (which lacks native Keploy CLI / WSL support).
* **`frontend/index.html`**: A single-page WhatsApp-themed web interface for testing chat memory, photo uploads, audio playback, and market prices.
* **`Dockerfile` / `render.yaml`**: Deployment specifications for automated hosting platforms (Render/Railway).

---

## ⚙️ Environment Variables

Copy the sample configurations to your `.env` or environment context:

* `GEMINI_API_KEY`: Required to make live Gemini AI multimodal diagnosis calls. Get one for free from [Google AI Studio](https://aistudio.google.com/).
* `OPENAI_API_KEY`: Kept as a dummy value (`mock-openai-key-for-kisansetu`) because the Mem0 layer's OpenAI completions/embeddings are patched to run entirely locally in SQLite and Qdrant database files.

*(Note: If `GEMINI_API_KEY` is not provided, the application will gracefully run using a keyword-matching fallback database).*

---

## 🚀 Setup & Run Locally

### 1. Install Dependencies
Make sure you have Python 3.11+ installed. Run:
```bash
# Create a virtual environment
uv venv

# Install package dependencies
uv pip install -r requirements.txt
```

### 2. Start the Server
Run the FastAPI development server:
```bash
.venv\Scripts\uvicorn main:app --reload
```
Once booted, open your browser and navigate to **`http://127.0.0.1:8000`** to access the WhatsApp Web demo UI.

---

## 🧪 Testing with Keploy (Windows Native)

We use a custom Windows-native Keploy middleware and runner to record and replay tests without Docker/WSL.

### 1. Record Test Cases
Run the server in recording mode:
```bash
.venv\Scripts\python keploy_windows.py record
```
This spins up the server. Run the test requests script (`python scratch_send_requests.py` located in the brain scratch folder) or use the frontend browser. Keploy captures all endpoints (including health check, standard diagnose, base64 image uploads, memory history lookup, and TTS audio streams) into `keploy/tests/test-X.yaml`.

### 2. Replay Test Suite
To verify that all recorded tests pass under full isolation:
```bash
.venv\Scripts\python keploy_windows.py test
```
The runner will automatically clean up local databases, spin up the app in a background thread, replay the test cases using `httpx`, and verify the responses (safely ignoring dynamic values like UUIDs, timestamps, and validating binary audio streams).

---

## ☁️ Deployment (Render / Docker)

This application is ready to deploy with single-click Docker support.

### Render Blueprint Deploy
1. Push this repository to GitHub.
2. In the Render Dashboard, create a new **Blueprint** from this repository.
3. It will automatically read the `render.yaml` specification, provision a free web service running the `Dockerfile`, and prompt you to input your `GEMINI_API_KEY`.

---

## 📊 Feature Scope: What's Real vs. Mocked

| Feature | Type | Status in v2 | Technical Detail |
| :--- | :--- | :--- | :--- |
| **Disease Diagnosis** | AI | **Real** | Uses `gemini-1.5-flash` model with text + image base64. |
| **Session Memory** | Memory | **Real** | Persisted per-farmer in local Qdrant and SQLite databases via Mem0. |
| **Voice Output** | Audio | **Real** | Direct `audio/mpeg` streaming using `gTTS` library from memory. |
| **Mandi Price Recommendation**| Data | Mocked | Returns simulated price range, mandi name, and trends for 5 crops/4 states. |
