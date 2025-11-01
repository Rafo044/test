FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .

#RUN pip install torch==2.2.0+cpu torchvision==0.17.0+cpu torchaudio==2.2.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

RUN pip install --no-cache-dir -r requirements.txt

COPY syntheticproducer.py .
COPY supermarket.csv .
CMD ["uvicorn", "syntheticproducer:app", "--host", "0.0.0.0", "--port", "8000"]
