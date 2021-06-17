FROM python:3.8.6-buster

COPY api /api
COPY ai_dj /ai_dj
COPY ai-dj.json /ai-dj.json
COPY requirements.txt /requirements.txt

ENV GOOGLE_APPLICATION_CREDENTIALS=ai-dj.json
RUN apt-get update
RUN apt-get --yes install libsndfile1
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD uvicorn api.fast:app --host 0.0.0.0 --port $PORT
