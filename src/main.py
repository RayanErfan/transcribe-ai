from unittest import result
from aiohttp import ClientSession, ClientTimeout, request
from fastapi import FastAPI, Form, HTTPException
from typing import Optional, List, Union, Dict, Any
from pydantic import BaseModel, Field
from config import Config
from utils import Hash

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


        # Headers
        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://notegpt.io",
            "Referer": "https://notegpt.io/audio-to-text-converter",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:144.0) Gecko/20100101 Firefox/144.0",
        }
        hash_obj = Hash()

        random_userid = hash_obj.hash(digest_size=33)
        cookies = {
            "anonymous_user_id": random_userid,
            "is_first_visit": "true",
            # for now cf clearance not needed, #TODO; add cf anticaptcha later if needed
        }

        timeout = ClientTimeout(total=self.timeout)
        async with ClientSession(timeout=timeout) as ses:
            async with ses.post(self.start_url, params=form, headers=headers, cookies=cookies) as res:
                request_status = res.get('code', 0) == 100000 and res.get('message', "failed") == "success"
                if res.status == 200 and request:

                    res_json = await res.json()
                    event_id = res_json['data']['event_id'] if res_json['data']['event_id'] else None
                    # format response
                    return {
                        "status": "ok",
                        "event_id":  event_id 
                    }
                else:
                    res_text = await res.text()
                    raise HTTPException(res.status, f"We got an error: {res_text}")



@app.post("/transcribe")

#TODO 
# Add file -> url

async def transcribe(request: AudioRequest):
    pass
