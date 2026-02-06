from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from gtts import gTTS
from gtts.lang import tts_langs
import io
import traceback

app = FastAPI(title="Voice Generator API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Voice Generator API is running", "version": "1.1.1"}

@app.get("/voices")
async def get_voices():
    """
    Return available languages/voices supported by gTTS.
    """
    try:
        langs = tts_langs()
        voices = []
        for code, name in langs.items():
            voices.append({
                "voice_id": code,
                "name": name,
                "lang": code,
                "gender": "neutral"  # gTTS is neutral
            })
        return voices
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tts")
async def generate_tts(data: dict = Body(...)):
    """
    Generate audio from text using gTTS.
    Matches Angular TtsService.generateTTS expectation.
    """
    text = data.get("text")
    lang = data.get("lang", "en")
    
    # gTTS expects 2-letter codes (e.g., 'ur' instead of 'ur-PK')
    if lang and len(lang) > 2:
        lang = lang[:2]
    
    speed = data.get("speed", "normal")
    
    # Map speed to gTTS 'slow' parameter
    slow = True if speed == "slow" else False

    if not text:
        raise HTTPException(status_code=400, detail="Text is required")

    try:
        # Generate speech
        tts = gTTS(text=text, lang=lang, slow=slow)
        
        # Save to memory buffer
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        
        return StreamingResponse(fp, media_type="audio/mpeg")
    
    except Exception as e:
        print(f"Error generating TTS: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# Backward compatibility / alias
@app.post("/generate")
async def generate_voice(data: dict = Body(...)):
    return await generate_tts(data)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
