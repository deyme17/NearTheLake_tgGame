FROM python:3.12-slim

WORKDIR /lake_game_bot

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH="/lake_game_bot"

COPY . .

CMD ["python", "main.py"]
