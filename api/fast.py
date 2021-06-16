from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from ai_dj import params
from google.cloud import storage
import soundfile
import io

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.get("/")
def index(filename):
    storage_client = storage.Client()
    bucket = storage_client.bucket(params.BUCKET_NAME)
    blob = bucket.blob(f'data/audio_wav/{filename}')
    blob = blob.download_as_string()

    data, sr = soundfile.read(io.BytesIO(blob))
    return {
        "data":data[:,0].tolist(),
        "sr":sr
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

