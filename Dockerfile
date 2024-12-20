FROM python:3.9

WORKDIR /lake_game_bot

COPY requirements.txt ./
RUN pip3 install -r requirements.txt && rm -rf /root/.cache/pip

ENV PYTHONPATH="${PYTHONPATH}:/lake_game_bot"

COPY . .

CMD ["python", "./main.py"]

