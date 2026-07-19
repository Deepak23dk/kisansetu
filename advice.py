# KisanSetu - Crop Disease Advice Module (Gemini AI & Stub Fallback)
import os
import base64
import logging
import google.generativeai as genai

logger = logging.getLogger("KisanSetu.advice")

# Keep the keyword-based database as a local fallback when API keys are not available
DISEASE_DATABASE = {
    "tomato": {
        "keywords": ["tomato", "tamatar", "yellow spots", "spots", "wilt", "curl", "blight", "peela", "dhabba", "patti"],
        "advice": (
            "Diagnosis: Suspected Tomato Early Blight or Tomato Leaf Curl Virus.\n"
            "Recommended Action:\n"
            "1. Spray organic Neem Oil (2-3 ml per liter of water) to control whitefly vectors.\n"
            "2. Remove and destroy infected lower leaves to stop fungal spores from spreading.\n"
            "3. Maintain proper spacing between plants and practice crop rotation next season."
        )
    },
    "rice": {
        "keywords": ["rice", "chawal", "dhan", "brown spots", "blast", "burn", "dhabba", "sukha"],
        "advice": (
            "Diagnosis: Suspected Rice Blast or Brown Spot Disease.\n"
            "Recommended Action:\n"
            "1. Apply Copper Oxychloride (2.5g per liter of water) or Tricyclazole.\n"
            "2. Ensure proper spacing to enable air circulation and reduce humidity.\n"
            "3. Avoid excessive nitrogen fertilizer, which makes the crop more susceptible to blast."
        )
    },
    "wheat": {
        "keywords": ["wheat", "gehun", "gehu", "rust", "yellow rust", "powdery", "mildew", "rusting", "safed"],
        "advice": (
            "Diagnosis: Suspected Wheat Rust (Yellow/Brown Rust) or Powdery Mildew.\n"
            "Recommended Action:\n"
            "1. Spray Propiconazole 25% EC (1 ml per liter of water) upon first appearance of rust pustules.\n"
            "2. Use certified rust-resistant seed varieties (e.g., HD 3086 or DBW 187) for the next sowing.\n"
            "3. Apply balanced NPK fertilizers and avoid over-irrigation."
        )
    }
}

DEFAULT_ADVICE = (
    "Diagnosis: Inconclusive disease patterns.\n"
    "Recommended Action:\n"
    "1. Keep the soil moisture balanced and clear any surrounding weeds.\n"
    "2. Monitor the leaves for changes in spots or pest populations over the next 2-3 days.\n"
    "3. Visit your nearest Krishi Vigyan Kendra (KVK) or consult a local agricultural officer with a leaf sample."
)

def get_advice_stub(message: str, language: str = "en") -> str:
    """Keyword-based fallback stub."""
    msg_lower = message.lower() if message else ""
    for crop, data in DISEASE_DATABASE.items():
        if any(keyword in msg_lower for keyword in data["keywords"]):
            advice = data["advice"]
            if language.lower() in ["hi", "hindi"]:
                advice = f"[Translated to Hindi]: {advice}"
            return advice
    return DEFAULT_ADVICE

def get_advice_real(
    message: str = None,
    image_base64: str = None,
    image_media_type: str = None,
    language: str = "en",
    remembered_context: list = None
) -> str:
    """
    Diagnoses crop disease using the official Gemini API (gemini-1.5-flash).
    Supports multimodal inputs (text and/or image).
    Integrates Mem0 context memories.
    Falls back to `get_advice_stub` if GEMINI_API_KEY is not configured.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        logger.warning("GEMINI_API_KEY not found in environment. Falling back to get_advice_stub.")
        return f"[Fallback Stub Advice]\n{get_advice_stub(message or '', language)}"

    # Configure Gemini API
    genai.configure(api_key=api_key)
    # Using gemini-2.5-flash for fast, multimodal execution
    model = genai.GenerativeModel("gemini-2.5-flash")

    # 1. Build prompt with memory history context
    history_str = ""
    if remembered_context:
        history_str = "Prior farmer interaction history (use this context to ensure you address previous issues or follow-ups):\n"
        for idx, mem in enumerate(remembered_context, 1):
            history_str += f"- {mem}\n"
        history_str += "\n"

    # Farmer's input text
    query_str = f"Farmer query/description: {message}\n" if message else "Farmer uploaded an image with no text description.\n"

    # Guidelines
    instructions = (
        f"You are KisanSetu, an expert agricultural AI assistant helping smallholder farmers in India.\n"
        f"Respond in language: {language}.\n\n"
        f"Task:\n"
        f"Analyze the crop leaf/issue described or shown. Respond with:\n"
        f"1. A likely disease or issue diagnosis.\n"
        f"2. 2-3 concrete and practical treatment steps (both organic and chemical if possible).\n"
        f"3. A recommendation on whether the case looks severe enough to warrant contacting the local KVK (Krishi Vigyan Kendra).\n\n"
        f"Formatting: Keep it extremely concise, clear, and action-oriented (maximum 3-5 sentences). "
        f"Format with bullet points so it is highly readable as a WhatsApp text message."
    )

    prompt = f"{history_str}{query_str}\n{instructions}"

    # 2. Build contents payload
    contents = []
    if image_base64 and image_media_type:
        try:
            # Clean base64 if data URI prefix was included
            if "," in image_base64:
                image_base64 = image_base64.split(",", 1)[1]
            image_bytes = base64.b64decode(image_base64)
            contents.append({
                "mime_type": image_media_type,
                "data": image_bytes
            })
        except Exception as e:
            logger.error(f"Failed to decode base64 image: {e}")
            return f"Error: Failed to process uploaded image. Details: {str(e)}"

    contents.append(prompt)

    # 3. Call model
    try:
        logger.info("Calling Gemini API...")
        response = model.generate_content(contents)
        logger.info("Gemini API call completed successfully.")
        return response.text.strip()
    except Exception as e:
        logger.error(f"Error calling Gemini API: {e}")
        return f"Error: Gemini API call failed. Details: {str(e)}"
