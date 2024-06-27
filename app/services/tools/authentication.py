from fastapi import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from firebase_admin import credentials, auth
import firebase_admin
from validators.schema.validators import LoginSchema, SignUpSchema
import pyrebase
from dotenv import load_dotenv
import os

if not firebase_admin._apps:
    firebase_admin.initialize_app()

if not firebase_admin._apps:
    cred_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY_PATH")
    cred = credentials.Certificate(cred_path) #get your service account keys from firebase
    firebase_admin.initialize_app(cred)


firebaseConfig = {
  "apiKey": os.getenv("FIREBASE_API_KEY"),
  "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
  "projectId": os.getenv("FIREBASE_PROJECT_ID"),
  "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
  "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
  "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
  "appId": os.getenv("FIREBASE_APP_ID"),
  "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID")
};

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

async def sign_up(user_data: SignUpSchema):
    email = user_data.email
    password = user_data.password

    try:
        user = auth.create_user_with_email_and_password(
            email=email,
            password=password
        )
        return JSONResponse(content={"message": f"User account created successfully for user {user}"},
                            status_code=201)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Account already created for the email {email}, error: {e}"
        )

async def login(user_data: LoginSchema):
    email = user_data.email
    password = user_data.password

    try:
        user = auth.sign_in_with_email_and_password(
            email=email,
            password=password
        )
        return JSONResponse(content={"message": f"User successfully logged in: {user}"},
                            status_code=200)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Account already created for the email {email}, error: {e}"
        )