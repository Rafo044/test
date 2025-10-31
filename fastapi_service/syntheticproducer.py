from fastapi import FastAPI
from sdv.single_table import GaussianCopulaSynthesizer
from sdv.metadata import SingleTableMetadata
import pandas as pd
import sqlite3
import threading
import time

app = FastAPI()

data = pd.read_csv('supermarket.csv')
main_columns = ['Branch', 'City','Customer type', 'Gender', 'Product line', 'Unit price', 'Quantity', 'Payment']

metadata = SingleTableMetadata()
for col in data.columns:
    if data[col].dtype == 'object':
        metadata.add_column(col, sdtype='categorical')
    else:
        metadata.add_column(col, sdtype='numerical')

model = GaussianCopulaSynthesizer(metadata)
model.fit(data)

conn = sqlite3.connect('synthetic.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS supermarket (
    Invoice_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Branch TEXT,
    City TEXT,
    Customer_type TEXT,
    Gender TEXT,
    Product_line TEXT,
    Unit_price REAL,
    Quantity INTEGER,
    Payment TEXT
)
""")

conn.commit()

def generate_data():
    while True:
        new_row = model.sample(1)[main_columns]
        new_row.columns = [c.replace(" ", "_").replace("%", "pct") for c in new_row.columns]
        new_row.to_sql('supermarket', conn, if_exists='append', index=False)
        time.sleep(1)

threading.Thread(target=generate_data, daemon=True).start()

@app.get("/latest")
def latest_data():
    df = pd.read_sql("SELECT * FROM supermarket ORDER BY Invoice_ID DESC LIMIT 1", conn)
    return df.to_dict(orient="records")
