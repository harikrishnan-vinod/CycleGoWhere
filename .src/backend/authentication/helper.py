import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()

auth_token = {
    "token": None,
    "expires_at": 0
}

def get_onemap_token():
    """Fetch and cache the OneMap token"""
    current_time = time.time()

    if auth_token["token"] and current_time < auth_token["expires_at"]:
        return auth_token["token"]

    print("Fetching new OneMap token...")

    url = "https://www.onemap.gov.sg/api/auth/post/getToken"
    payload = {
        "email": os.environ["ONEMAP_EMAIL"],
        "password": os.environ["ONEMAP_EMAIL_PASSWORD"]
    }

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        raise Exception("Failed to get OneMap token")

    data = response.json()
    token = data["access_token"]

    auth_token["token"] = token
    auth_token["expires_at"] = current_time + 24 * 60 * 60  # 24-hour expiry

    print (token)

    return token