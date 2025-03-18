import httpx
import json
import jwt
import os
import reflex as rx

from dotenv import load_dotenv
from loguru import logger
from typing import Callable, Iterable

load_dotenv()
jwt_key = os.getenv("jwt_key")
api_url = os.getenv("api_url")
api_key = os.getenv("api_key")

class BaseState(rx.State):
    user_id: str
    user_is_loading: bool = False

    access_token: str = rx.Cookie(
        name="access_token",
        same_site="strict",
        secure=True
    )

    refresh_token: str = rx.Cookie(
        name="refresh_token",
        same_site="strict",
        secure=True
    )

    @rx.var
    def user_claims(self) -> dict:
        try:
            if self.access_token:
                claims = jwt.decode(
                    self.access_token,
                    jwt_key,
                    audience="authenticated",
                    algorithms=["HS256"]
                )
                return claims
            else:
                return {}
        except Exception as e:
            return {}
        
    @rx.var
    def user_claims_id(self) -> str | None:
        return self.user_claims.get("sub")
    
    @rx.var
    def user_claims_authenticated(self) -> bool:
        if self.user_claims:
            return True if self.user_claims.get("aud") == "authenticated" else False
        else:
            return False
        
    def user_login(self, auth_data: dict) -> Callable:
        try:
            self.user_is_loading = True
            email = auth_data.get("email")
            password = auth_data.get("password")
            if email and password:
                tokens = login_to_supabase(email, password)
                self.access_token = tokens.get("access_token")
            else:
                self.user_is_loading = False
                return rx.toast.error("Both fields are required.")
            
            self.user_is_loading = False
            
        except Exception as e:
            return rx.toast(str(e))
        self.user_is_loading = False

def login_to_supabase(email: str, password: str) -> dict:
    logger.debug("Attempting to login...")
    url = f"{api_url}/auth/v1/token"
    params = {
        "grant_type": "password"
    }
    headers = {
        "apikey": api_key,
        "Content-Type": "application/json"
    }
    data = {
        "email": email,
        "password": password
    }
    response = httpx.post(
        url=url,
        params=params,
        headers=headers,
        data=json.dumps(data)
    )
    if response.is_success:
        logger.debug("Logged in via user/pass.")
        payload = json.loads(response.content)
        return payload
    else:
        error = json.loads(response.text)
        raise Exception(error.get("msg"))