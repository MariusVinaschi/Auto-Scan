from typing import Optional
from fastapi import FastAPI

from app.models import exempleModel, returnModel

app = FastAPI()

@app.get('/isAlive')
def isAlive(): 
    return {'isAlive' : True}

@app.post('/', response_model=returnModel ,status_code=201)
async def start(params : exempleModel):
    # Put your function to start your tool here 
    return {'Text': "Test"}                                                                                                                  