from typing import Any, Optional
from pydantic import BaseModel

class URLDataRequest(BaseModel):
    url: str
    index: str
    email:str
    password:str

class EmailQueryRequest(BaseModel):
    query: str
    index: str
    email:str
    password:str
    
class SignUpSchema(BaseModel):
    email:str
    password:str

    class Config:
        schema_extra ={
            "example":{
                "email":"sample@gmail.com",
                "password":"samplepass123"
            }
        }


class LoginSchema(BaseModel):
    email:str
    password:str

    class Config:
        schema_extra ={
            "example":{
                "email":"sample@gmail.com",
                "password":"samplepass123"
            }
        }