from aiohttp import ClientSession
from fastapi import FastAPI
from typing import Optional, List, Union, Dict, Any
from pydantic import BaseModel, Field



app = FastAPI()

class AudioRequest(BaseModel):
    path: str = Field(..., description="The URL of the audio file to transcribe")
    type: int = Field(..., description="The type of the audio file (trust me its 1)")
    lang_code: str = Field(..., description="The language code of the audio file ( en or fa or ar or de or es or fr or it or ja or ko or nl or pl or pt or ru or tr or zh )")
    diarization: bool = Field(..., description="Whether to enable diarization (bool)")
    accuracy: str = Field(..., description="The accuracy of the transcription (medium or high or low)")
    referrer_url: str = Field(..., description="The referrer URL of the audio file ( /audio-to-text-converter )")
    audio_time: int = Field(..., description="The audio time of the audio file (in seconds)")
    file_name: str = Field(..., description="The file name of the audio file (Tiger Tiger.mp3)")

# @app.post("/transcribe")