from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from langchain_openai import ChatOpenAI
from langserve import add_routes
import uvicorn
import os
from app.services.agents.sales_agent import sales_chain
from app.services.agents.support_agent import support_chain 
from app.services.tools.authentication import login, sign_up
from app.services.tools.data_ingestion import ingestor
from app.services.tools.scraper import get_url_data
from app.services.tools.email_extractor import get_emails
from validators.schema.validators import EmailQueryRequest, LoginSchema, SignUpSchema, URLDataRequest

app=FastAPI(
    title="Langchain Server",
    version="1.0",
    decsription="A simple API Server"
)

add_routes(
    app,
    ChatOpenAI(api_key=openai_api_key),
    path="/openai"
)  

add_routes(
    app,
    sales_chain,
    path="/sales"
)

add_routes(
    app,
    support_chain, 
    path="/support"
)

@app.post('/signup')
async def user_signup(user_data: SignUpSchema):
    return await sign_up(user_data)

@app.post('/login')
async def user_login(user_data: LoginSchema):
    return await login(user_data)

@app.post("/ingest_url_data")
def ingest_url_data(request: URLDataRequest):
    try:
        login({request.email, request.password})
        docs = get_url_data(request.url, request.index)
        return {"message": "Data ingested successfully", "documents": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest_email_data")
def ingest_email_data(request: EmailQueryRequest):
    try:
        login({request.email, request.password})
        emails = get_emails(request.query, request.index)
        return {"message": "Data ingested successfully", "emails": emails}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__=="__main__":
    uvicorn.run(app,host="localhost",port=8000)