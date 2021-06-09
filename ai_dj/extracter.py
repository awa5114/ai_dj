from ai_dj import gcp_storage
from ai_dj.audio_features import AudioFeatureExtracter
from ai_dj.split_audio import SpleeterSeparator
import os
import shutil

from ai_dj import params

## Clean local folders
def clean_local_folders():
    local_folders = params.LOCAL_FOLDERS
    for folder in local_folders:
        if os.path.isdir(f'{params.DATA_FOLDER}/{folder}'):
                shutil.rmtree(f'{params.DATA_FOLDER}/{folder}')
        os.mkdir(f'{params.DATA_FOLDER}/{folder}/')
                
## Get youtube_link from app
def get_youtube_link():
    youtube_link = "https://www.youtube.com/watch?v=dpgqo3kH4rs"
    return youtube_link

## Extract youtube_wav file & audiofeatures + upload to the folder
def extract_features_and_upload(youtube_link):
    features_extracter = AudioFeatureExtracter()
    output_file = features_extracter.youtube_audio_features(youtube_link)
    gcp_storage.upload_youtube_wav(output_file)
    return output_file

## Split into stems
def split_into_stems(file):
    gcp_storage.get_youtube_wav(file)
    temp_file = f"{params.DOWNLOADED_FOLDER}/{file}"
    separator = SpleeterSeparator(temp_file)
    separator.split_song()

## Find 2 other songs


## Split 2 other songs into stems


## Determine which stems to mix


## Create mix from stems


## Update app



if __name__=='__main__':
    clean_local_folders()
    yt_link = get_youtube_link()
    output_file = extract_features_and_upload(yt_link)
    print(output_file)
    split_into_stems(output_file)