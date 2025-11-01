"""FastAPI servisinin authentikifasiyasını yoxlanması"""

import os
import requests

from dotenv import load_dotenv


load_dotenv()

TOKEN = os.getenv("TOKEN")
FASTAPI_URL = os.getenv("FASTAPI_URL")


def authenticate(method, endpoint, **kwargs):
    """FastAPI servisinin authentikifasiyasını yoxlama funksiyası

    Args:
        method (str): HTTP methodu (GET, POST, PUT, DELETE)
        endpoint (str): API endpointi məsələn "all" ,"/" yazmaq olmaz.
        **kwargs: kwargs
    Returns:
        response : Request olunacaq funksiya.
    """
    headers = {"Authorization": f"Bearer {TOKEN}"}
    url = f"{FASTAPI_URL}/{endpoint}"
    response = requests.request(method, url, headers=headers, **kwargs)
    return response
