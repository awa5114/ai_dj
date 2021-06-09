from google.cloud import storage
from ai_dj.params import BUCKET_NAME, MP3_DATA_FOLDER, TEMP_DATA_FOLDER

def get_mp3(file):
    storage_client = storage.Client()

    bucket = storage_client.bucket(BUCKET_NAME)
    source_blob_name = f'{MP3_DATA_FOLDER}/{file}'
    print(source_blob_name)
    blob = bucket.blob(source_blob_name)
    destination_file_name = f'{TEMP_DATA_FOLDER}/{file}'
    print(destination_file_name)
    blob.download_to_filename(destination_file_name)
    
    print(
        "Blob {} downloaded to {}.".format(
            source_blob_name, destination_file_name
        )
    )

## TEST ##
# file = "1156133 Roberto Auser - Caravan (Original Mix).mp3"
# get_mp3(file)
## TEST ##