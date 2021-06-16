from ai_dj import gcp_storage, neighbour_songs
from ai_dj.audio_features import AudioFeatureExtracter
from ai_dj.split_audio import SpleeterSeparator
import os
import shutil
from google.cloud import storage
import pandas as pd

from ai_dj import params

## Get youtube_link from app
def get_youtube_link():
    youtube_link = "https://www.youtube.com/watch?v=xF-UznUkhP8"
    return youtube_link

## Extract youtube_wav file & audiofeatures + upload to the folder
def extract_features_and_upload(youtube_link):
    features_extracter = AudioFeatureExtracter()
    output_file, bpm, key = features_extracter.youtube_audio_features(youtube_link)
    gcp_storage.upload_youtube_wav(output_file)
    return output_file, bpm, key

