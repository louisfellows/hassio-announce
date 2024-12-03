from typing import Union
from fastapi import FastAPI, Response
from pydantic import BaseModel
from subprocess import call

class PlayRequest(BaseModel):
    uri: str

app = FastAPI()
        
@app.post("/", status_code=204)
def play_announcement(play_req: PlayRequest, response: Response):
    
    if (play_req.uri is None):
        response.status_code = 405
        return
    
    try:   
        call(["aplay", play_req.uri])
    except:
        response.status_code = 500
        return {"Could not play file " + play_req.uri }
        
    return