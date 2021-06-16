FROM python:3.8.6-buster

COPY api /api
COPY ai_dj /ai_dj
COPY requirements.txt /requirements.txt

RUN echo "upgrading pip"
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN echo "running final command"
CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
