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


class CheckRequest(BaseModel):
    event_id: str = Field(..., description="Event ID from initial transcription request")

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

        # request json 
        form = {
            "path": path,
            "type": type,
            "diarization": diarization,
            "lang_code": lang_code,
            "accuracy": accuracy
        }


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
            async with ses.post(self.start_url, json=form, headers=headers, cookies=cookies) as res:
                try:
                    res_json = await res.json(content_type=None)
                except Exception:
                    res_text = await res.text()
                    raise HTTPException(res.status, f"Invalid response: {res_text}")

                # request_status = res.get('code', 0) == 100000 and res.get('message', "failed") == "success"
                if res.status == 200 and res_json.get("code") == 100000:
                    data = res_json.get("data", {})
                    event_id = data.get("event_id")
                    if not event_id:
                        raise HTTPException(500, "Missing event_id in response")

                    return {"status": "ok", "event_id": event_id}

                else:
                    raise HTTPException(
                        res.status,
                        f"Error: {res_json.get('message', 'Unknown error')}",
                    )


    async def check_event(self, event_id: str) -> Dict[str, Any]:
        """Polls result for transcription results"""

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
        }

        timeout = ClientTimeout(total=self.timeout)

        params = {"record_id": event_id}

        async with ClientSession(timeout=timeout) as ses:
            async with ses.get(
                self.check_url,
                params=params,
                headers=headers,
                cookies=cookies,
            ) as res:
                try:
                    res_json = await res.json(content_type=None)
                except Exception:
                    res_text = await res.text()
                    raise HTTPException(res.status, f"Invalid response: {res_text}")

                # {"code": 160002, "message": "failed, please retry", "data": null}
                if res_json.get("code") == 160002:
                    return {"status": "pending", "message": "failed, please retry"}

                # {"code": 100000, "message": "success", "data": {...}}
                if res_json.get("code") == 100000:
                    data = res_json.get("data", {})
                    return {
                        "status": "ok",
                        "audio_url": data.get("audio_url"),
                        "transcript": data.get("transcript"),
                    }

                raise HTTPException(
                    res.status,
                    f"Unexpected response: {res_json}",
                )



@app.post("/transcribe")
async def transcribe(request: AudioRequest):
    ts = Transcriber()
    try:
        result = await ts.request_transcribe(
            path=request.path,
            type=request.type,
            diarization=request.diarization,
            lang_code=request.lang_code,
            accuracy=request.accuracy,
        )
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/check_event")
async def check_event(request: CheckRequest):
    ts = Transcriber()
    try:
        result = await ts.check_event(request.event_id)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


