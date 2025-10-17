import os
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

flow = Flow.from_client_config(
    {
        "web": {
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    },
    scopes=[
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/documents.readonly",
    ],
    redirect_uri=os.getenv("REDIRECT_URI"),
)

@router.get("/auth/login")
def auth_login():
    auth_url, _ = flow.authorization_url(prompt="consent")
    return RedirectResponse(auth_url)

'''
@router.get("/auth/callback")
def auth_callback(request: Request):
    flow.fetch_token(authorization_response=str(request.url))
    credentials = flow.credentials
    return {
        "access_token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "expires_in": credentials.expiry.isoformat(),
    }
'''

@router.get("/auth/callback")
def auth_callback(request: Request):
    try:
        flow.fetch_token(authorization_response=str(request.url))
        credentials = flow.credentials
        return {
            "access_token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "expires_in": credentials.expiry.isoformat(),
        }
    except Exception as e:
        print("❌ 토큰 교환 실패:", e)
        raise HTTPException(status_code=500, detail="토큰 교환 중 오류 발생")
