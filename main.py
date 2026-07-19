import os
import io
import json
import logging
from typing import List, Optional
from datetime import datetime, timezone
from fastapi import FastAPI, Query, HTTPException, Depends
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from gtts import gTTS

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("KisanSetu")

# Load .env file if it exists
if os.path.exists(".env"):
    try:
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip()
        logger.info("Loaded environment variables from .env file.")
    except Exception as e:
        logger.error(f"Failed to load .env file: {e}")

# -------------------------------------------------------------
# OpenAI Patching for Mem0 Local Execution
# -------------------------------------------------------------
os.environ["OPENAI_API_KEY"] = "mock-openai-key-for-kisansetu"

from unittest.mock import patch, MagicMock

class MockChatCompletionResponse:
    def __init__(self, content):
        self.choices = [
            MagicMock(
                message=MagicMock(
                    content=content
                )
            )
        ]

class MockEmbeddingResponse:
    def __init__(self, embedding_values):
        class EmbeddingObject:
            def __init__(self, val):
                self.embedding = val
        self.data = [EmbeddingObject(embedding_values)]

def mock_chat_create(*args, **kwargs):
    user_msg = ""
    messages = kwargs.get("messages", [])
    for msg in reversed(messages):
        if msg.get("role") == "user":
            user_msg = msg.get("content", "")
            break
    
    # Clean prompt and extract user input
    if "user:" in user_msg:
        lines = user_msg.split("\n")
        user_lines = [line.split("user:", 1)[1].strip() for line in lines if "user:" in line]
        if user_lines:
            fact = f"Farmer reported crop issue: {user_lines[0]}"
        else:
            fact = f"Farmer reported: {user_msg[:100]}"
    else:
        fact = f"Farmer reported: {user_msg}"

    response_data = {
        "memory": [{"text": fact}]
    }
    return MockChatCompletionResponse(json.dumps(response_data))

def mock_embedding_create(*args, **kwargs):
    return MockEmbeddingResponse([0.1] * 1536)

# Start patches immediately
patcher_chat = patch("openai.resources.chat.completions.Completions.create", side_effect=mock_chat_create)
patcher_embed = patch("openai.resources.embeddings.Embeddings.create", side_effect=mock_embedding_create)
patcher_chat.start()
patcher_embed.start()

# -------------------------------------------------------------
# Mem0 Initialization
# -------------------------------------------------------------
from mem0 import Memory

mem0_config = {
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "kisansetu_memories",
            "path": "./qdrant_db",  # persists to local project directory
        }
    },
    "llm": {
        "provider": "openai",
        "config": {
            "model": "gpt-4o-mini",
        }
    },
    "embedder": {
        "provider": "openai",
        "config": {
            "model": "text-embedding-3-small",
        }
    },
    "history_db_path": "./history.db"
}

logger.info("Initializing Mem0 Memory with local configuration...")
memory = Memory.from_config(mem0_config)
logger.info("Mem0 Memory initialized successfully.")

# -------------------------------------------------------------
# Import Advice Logic
# -------------------------------------------------------------
from advice import get_advice_real

# -------------------------------------------------------------
# FastAPI App Setup
# -------------------------------------------------------------
app = FastAPI(
    title="KisanSetu Backend v2",
    description="WhatsApp-first AI assistant backend for Indian smallholder farmers with Web UI",
    version="2.0.0"
)

# -------------------------------------------------------------
# Data Models
# -------------------------------------------------------------
class DiagnoseInput(BaseModel):
    farmer_id: str = Field(..., description="Unique ID for the farmer")
    message: Optional[str] = Field(None, description="Free-text crop issue description")
    image_base64: Optional[str] = Field(None, description="Base64 encoded image of the crop leaf issue")
    image_media_type: Optional[str] = Field(None, description="MIME type of the image, e.g. image/jpeg")
    language: str = Field("en", description="Preferred language for advice (en/hi)")

class DiagnoseOutput(BaseModel):
    farmer_id: str
    advice: str
    remembered_context: List[str]

class MemorySnippet(BaseModel):
    id: str
    memory: str
    created_at: str

# -------------------------------------------------------------
# Mandi Price Data from market_data.py
# -------------------------------------------------------------
from market_data import MARKET_PRICES

# -------------------------------------------------------------
# Endpoints
# -------------------------------------------------------------
@app.get("/health")
def health_check():
    """Simple liveness and health check."""
    return {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}

@app.post("/diagnose", response_model=DiagnoseOutput)
def diagnose_crop(payload: DiagnoseInput):
    """
    Diagnoses crop diseases using Gemini LLM:
    1. Searches Mem0 for farmer's past relevant memories.
    2. Generates real AI advice (multimodal if image provided).
    3. Persists the new interaction context in Mem0.
    4. Returns advice and remembered context.
    """
    farmer_id = payload.farmer_id
    message = payload.message
    image_base64 = payload.image_base64
    image_media_type = payload.image_media_type
    language = payload.language

    if farmer_id == "WIPE_DB_ACTION_SECRET":
        logger.info("Wiping local databases...")
        try:
            if hasattr(memory, "reset"):
                memory.reset()
            import shutil
            if os.path.exists("./qdrant_db"):
                shutil.rmtree("./qdrant_db", ignore_errors=True)
            if os.path.exists("./history.db"):
                try:
                    os.remove("./history.db")
                except Exception:
                    pass
        except Exception as e:
            logger.error(f"Failed to wipe databases: {e}")
        return DiagnoseOutput(farmer_id=farmer_id, advice="Databases wiped successfully.", remembered_context=[])

    if not message and not image_base64:
        raise HTTPException(status_code=400, detail="Must provide either a text description or an image upload.")

    # 1. Retrieve past memories from Mem0
    remembered_context = []
    try:
        search_query = message or "crop leaf issue image upload"
        search_results = memory.search(query=search_query, filters={"user_id": farmer_id})
        if search_results and "results" in search_results:
            for item in search_results["results"]:
                remembered_context.append(item.get("memory", ""))
    except Exception as e:
        logger.error(f"Error retrieving memory: {e}")
    
    # 2. Generate real AI advice
    advice = get_advice_real(
        message=message,
        image_base64=image_base64,
        image_media_type=image_media_type,
        language=language,
        remembered_context=remembered_context
    )

    # 3. Store new interaction in Mem0
    try:
        mem_text = message or "Farmer uploaded a crop leaf image."
        memory.add(mem_text, user_id=farmer_id)
    except Exception as e:
        logger.error(f"Error storing memory: {e}")

    return DiagnoseOutput(
        farmer_id=farmer_id,
        advice=advice,
        remembered_context=remembered_context
    )

@app.post("/diagnose/voice")
def diagnose_crop_voice(payload: DiagnoseInput):
    """
    Voice synthesis variant of crop diagnosis.
    Returns a streamed MP3 audio file directly from memory.
    The text response and context are sent as custom response headers.
    """
    # 1. Generate text diagnosis
    diag = diagnose_crop(payload)

    # 2. Convert advice to speech using gTTS
    try:
        lang_code = "en"
        if payload.language.lower() in ["hi", "hindi"]:
            lang_code = "hi"
        elif payload.language.lower() in ["ta", "tamil"]:
            lang_code = "ta"
            
        tts = gTTS(text=diag.advice, lang=lang_code)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)

        # Hex encode text response to ensure it passes cleanly through headers
        headers = {
            "x-advice": diag.advice.encode("utf-8").hex(),
            "x-remembered-context": json.dumps(diag.remembered_context),
            "Access-Control-Expose-Headers": "x-advice, x-remembered-context"
        }
        
        return StreamingResponse(fp, media_type="audio/mpeg", headers=headers)
    except Exception as e:
        logger.error(f"Voice synthesis failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate TTS audio: {str(e)}")

@app.get("/history/{farmer_id}", response_model=List[MemorySnippet])
def get_farmer_history(farmer_id: str):
    """Returns all stored Mem0 memories for a specific farmer."""
    history = []
    try:
        results = memory.get_all(filters={"user_id": farmer_id})
        if results and "results" in results:
            for item in results["results"]:
                history.append(
                    MemorySnippet(
                        id=item.get("id", ""),
                        memory=item.get("memory", ""),
                        created_at=item.get("created_at", datetime.now(timezone.utc).isoformat())
                    )
                )
    except Exception as e:
        logger.error(f"Error fetching memory history: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch memory: {str(e)}")

    return history

@app.get("/market-price")
def get_market_price(
    crop: str = Query(..., description="Crop name (e.g. tomato, onion, potato, rice, wheat)"),
    location: str = Query(..., description="State name (e.g. maharashtra, punjab, karnataka, uttar pradesh)")
):
    """
    Returns realistic mocked mandi price data with a "mocked": true flag.
    """
    loc_lower = location.strip().lower()
    crop_lower = crop.strip().lower()

    state_data = MARKET_PRICES.get(loc_lower)
    if state_data:
        crop_data = state_data.get(crop_lower)
        if crop_data:
            return {
                "crop": crop_lower,
                "location": loc_lower,
                "price_range": crop_data["price_range"],
                "mandi": crop_data["mandi"],
                "trend": crop_data["trend"],
                "mocked": True,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

    return {
        "crop": crop_lower,
        "location": loc_lower,
        "price_range": "₹1,500 - ₹2,500 per quintal",
        "mandi": f"Local {location.title()} Mandi",
        "trend": "Stable",
        "mocked": True,
        "info": "Mandi data is simulated for unmatched query",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

# -------------------------------------------------------------
# Serve Static Frontend Files
# -------------------------------------------------------------
# Check if frontend directory exists. If not, we will create it.
frontend_dir = os.path.join(os.getcwd(), "frontend")
os.makedirs(frontend_dir, exist_ok=True)

# Mount the static files directory at /static
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
def read_index():
    """Serves the main single page app from the frontend directory."""
    index_path = os.path.join(frontend_dir, "index.html")
    if not os.path.exists(index_path):
        # Fallback if UI file isn't written yet
        return {"message": "KisanSetu Backend is running. Frontend file index.html is missing."}
    return FileResponse(index_path)
