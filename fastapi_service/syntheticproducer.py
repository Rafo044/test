"""
Bu bir FastAPI servisidir və məqsədi verilən csv faylına uygun sintetik verilənlər
yaratmaqdır və bunları SQLite veritabanına yazmaqdır.Servis publik və secure mode dəstəkləyir .
Public modda sərbəst giriş olunur ,secure modda isə token bazlı giriş olunur
"""

import threading
import time
import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sdv.single_table import GaussianCopulaSynthesizer
from sdv.metadata import SingleTableMetadata
import pandas as pd
from dotenv import load_dotenv


from database import create_tables

app = FastAPI()
load_dotenv()

DATA_PATH = os.getenv("DATA_PATH")
TOKEN = os.getenv("TOKEN")
data = pd.read_csv(DATA_PATH)
MAIN_COLUMNS = [
    "Branch",
    "City",
    "Customer type",
    "Gender",
    "Product line",
    "Unit price",
    "Quantity",
    "Payment",
]


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    """
    Authentifikasiya üçün token bazlı middleware .
    Args:
        request: FastAPI -in Request obyektini alır
        call_next: FastAPI -ın middleware funksiyası
    Returns:
        FastAPI Response sorgusunu qaytarır
    """
    token = request.headers.get("Authorization")
    if token != f"Bearer {TOKEN}":
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


def generate_model():
    """
    Gaussian Copula Modeli yaratmaq üçün funksiya .

    Returns:
        Gaussian Copula Modeli
    """
    metadata = SingleTableMetadata()
    for col in data.columns:
        if data[col].dtype == "object":
            metadata.add_column(col, sdtype="categorical")
        else:
            metadata.add_column(col, sdtype="numerical")
    model = GaussianCopulaSynthesizer(metadata)
    model.fit(data)
    return model


def generate_data():
    """
    Gaussian Copula Modelini sonsuz döngüdə yaradır .

    Returns:
        Gaussian Copula Modeli
    """
    while True:
        model = generate_model()
        new_row = model.sample(1)[MAIN_COLUMNS]
        new_row.columns = [
            c.replace(" ", "_").replace("%", "pct") for c in new_row.columns
        ]
        new_row.to_sql("supermarket", conn, if_exists="append", index=False)
        time.sleep(1)


conn = create_tables()
threading.Thread(target=generate_data, daemon=True).start()


@app.get("/latest")
def latest_data():
    """
    Modelin generate etdiyi son verlənləri çıxardır.

    Returns:
        Son verilənlər
    """
    df = pd.read_sql("SELECT * FROM supermarket ORDER BY Invoice_ID DESC LIMIT 1", conn)
    return df.to_dict(orient="records")


@app.get("/all")
def all_data():
    """
    Modelin generate etdiyi bütün verlənləri çıxardır.

    Returns:
        Bütün verilənlər
    """
    df = pd.read_sql("SELECT * FROM supermarket", conn)
    return df.to_dict(orient="records")
