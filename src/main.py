from unittest import result
from aiohttp import ClientSession, ClientTimeout, request
from fastapi import FastAPI, Form, HTTPException
from typing import Optional, List, Union, Dict, Any
from pydantic import BaseModel, Field
from config import Config


app = FastAPI()

class AudioRequest(BaseModel):
    path: str = Field(..., description="The URL of the audio file to transcribe")
    type: int = Field(..., description="The type of the audio file (trust me its 1)")
    lang_code: str = Field(..., description="The language code of the audio file ( en or fa or ar or de or es or fr or it or ja or ko or nl or pl or pt or ru or tr or zh )")
    diarization: bool = Field(..., description="Whether to enable diarization (bool)")
    accuracy: str = Field(..., description="The accuracy of the transcription (medium or high or low)")




class Transcriber:

    """This is where the real magic happens
    DO NOT TOUCH OR YOU WILL BE FIRED ( i always wanted to say this )"""

    def __init__(self) -> None:

        self.start_url: str = Config.START_URL
        self.check_url: str = Config.CHECK_URL
        self.timeout: int = 60


    async def request_transcribe(
        self,
        path: str,
        type: int = 1,
        diarization: bool = False,
        lang_code: str = "en",
        accuracy: str = "medium",
        
    ) -> Dict[str, Any]:

        # request params 
        form = {
            "path": path,
            "type": type,
            "diarization": diarization,
            "lang_code": lang_code,
            "accuracy": accuracy
        }

        #TODO; request headers

        timeout = ClientTimeout(total=self.timeout)
        async with ClientSession(timeout=timeout) as ses:
            async with ses.post(self.start_url, params=form, headers=None) as res:
                request_status = res.get('code', 0) == 100000 and res.get('message', "failed") == "success"
                if res.status == 200 and request:
                    #TODO; handle the ok res
                    pass
                else:
                    res_text = res.text()
                    raise HTTPException(res.status, f"We got an error: {res_text}")



@app.post("/transcribe")

#TODO 
# Add file -> url

async def transcribe(request: AudioRequest):
    pass
