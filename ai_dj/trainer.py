import youtube_dl
from ai_dj import gcp_storage, params
from ai_dj import audio_features
from ai_dj.mix_rating import load_audio_features, get_wave_data, get_mix_features, get_mix_tracks, get_stem_info
from ai_dj.audio_features import get_BPM, computeKeyCl, min_max_freq, mean_amplitude, z_cross
from ai_dj.download_youtube import download_wav_and_metadata
from ai_dj.split_audio import split_tracks
import librosa
import numpy as np
import pandas as pd
import os
import shutil
from google.cloud import storage
from tensorflow.python.lib.io import file_io
import io
import pandas as pd
import pickle

from ai_dj import params

## Get youtube_link from app
def get_youtube_link():
    youtube_link = "https://www.youtube.com/watch?v=SKUk9RUacDQ"
    return youtube_link

## Extract youtube_wav file & audiofeatures + upload to the folder
def extract_wav_from_yt_link(youtube_link):
    title, output_filename = download_wav_and_metadata(youtube_link)
    gcp_storage.upload_youtube_wav(output_filename)
    return title, output_filename

def get_audio_features_db():
    f = io.BytesIO(
            file_io.read_file_to_string(
                f'gs://ai_dj_batch627_data/data/audio_features/audio_features_track_names.csv',
                binary_mode=True))
    audio_feature_track_names = np.load(f, allow_pickle=True)
    audio_feature_track_names = pd.DataFrame(audio_feature_track_names)
    audio_feature_track_names.columns=["name", "youtube_link", "audio_features_file"]
    return audio_feature_track_names

def get_audio_features(name):
    f = io.BytesIO(
            file_io.read_file_to_string(
                f'gs://ai_dj_batch627_data/data/audio_features/{name}.npy',
                binary_mode=True))
    audio_features_df = np.load(f, allow_pickle=True)
    audio_features_df = pd.DataFrame(audio_features_df)
    audio_features_df.columns=["name", "output_file_mp3", "BPM", "key", 
                                    "wave_original", "mean_aplitude_original", "z_cross_original", "min_freq_original", "max_freq_original", "range_freq_original",
                                    "wave_bass", "mean_aplitude_bass", "z_cross_bass", "min_freq_bass", "max_freq_bass", "range_freq_bass",
                                    "wave_drums", "mean_aplitude_drums", "z_cross_drums", "min_freq_drums", "max_freq_drums", "range_freq_drums",
                                    "wave_vocals", "mean_aplitude_vocals", "z_cross_vocals", "min_freq_vocals", "max_freq_vocals", "range_freq_vocals",
                                    "wave_other", "mean_aplitude_other", "z_cross_other", "min_freq_other", "max_freq_other", "range_freq_other",
                                    "wave_mixed", "mean_aplitude_mixed", "z_cross_mixed", "min_freq_mixed", "max_freq_mixed", "range_freq_mixed", "beat_times"
                                    ]
    return audio_features_df

def update_new_audio_features(output_filename, title):
    file_path = f'{params.DOWNLOADED_FOLDER}/{output_filename}'
    y, sr = librosa.load(file_path, sr=44100)
    bpm = get_BPM(y, sr)
    key = computeKeyCl(file_path)
    max_freq_original, min_freq_original, range_freq_original = min_max_freq(y, sr)
    mean_aplitude_original = mean_amplitude(y)
    z_cross_original = z_cross(y)
    audio_files = [output_filename]
    print("ready to split files")
    mix_data = split_tracks(audio_files, 4)
    wave_bass = mix_data[output_filename]["prediction"]["bass"][:,0]
    max_freq_bass, min_freq_bass, range_freq_bass = min_max_freq(wave_bass, sr)
    mean_aplitude_bass = mean_amplitude(wave_bass)
    z_cross_bass = z_cross(wave_bass)
    wave_drums = mix_data[output_filename]["prediction"]["drums"][:,0]
    max_freq_drums, min_freq_drums, range_freq_drums = min_max_freq(wave_drums, sr)
    mean_aplitude_drums = mean_amplitude(wave_drums)
    z_cross_drums = z_cross(wave_drums)
    wave_vocals = mix_data[output_filename]["prediction"]["vocals"][:,0]
    max_freq_vocals, min_freq_vocals, range_freq_vocals = min_max_freq(wave_vocals, sr)
    mean_aplitude_vocals = mean_amplitude(wave_vocals)
    z_cross_vocals = z_cross(wave_vocals)
    wave_other = mix_data[output_filename]["prediction"]["other"][:,0]
    max_freq_other, min_freq_other, range_freq_other = min_max_freq(wave_other, sr)
    mean_aplitude_other = mean_amplitude(wave_other)
    z_cross_other = z_cross(wave_other)
    wave_mixed = wave_bass + wave_drums + wave_vocals + wave_other
    max_freq_mixed, min_freq_mixed, range_freq_mixed = min_max_freq(wave_mixed, sr)
    mean_aplitude_mixed = mean_amplitude(wave_mixed)
    z_cross_mixed = z_cross(wave_mixed)
    beat_times = mix_data[output_filename]["beat_times"]
    
    new_song = pd.DataFrame(columns=["name", "output_file_mp3", "BPM", "key", 
                                        "wave_original", "mean_aplitude_original", "z_cross_original", "min_freq_original", "max_freq_original", "range_freq_original",
                                        "wave_bass", "mean_aplitude_bass", "z_cross_bass", "min_freq_bass", "max_freq_bass", "range_freq_bass",
                                        "wave_drums", "mean_aplitude_drums", "z_cross_drums", "min_freq_drums", "max_freq_drums", "range_freq_drums",
                                        "wave_vocals", "mean_aplitude_vocals", "z_cross_vocals", "min_freq_vocals", "max_freq_vocals", "range_freq_vocals",
                                        "wave_other", "mean_aplitude_other", "z_cross_other", "min_freq_other", "max_freq_other", "range_freq_other",
                                        "wave_mixed", "mean_aplitude_mixed", "z_cross_mixed", "min_freq_mixed", "max_freq_mixed", "range_freq_mixed", "beat_times"
                                        ])
    new_song_dict = {"name": title,
                     "output_file_mp3": output_filename,
                     "BPM": bpm,
                     "key": key,
                     "wave_original": y,
                     "mean_aplitude_original": mean_aplitude_original,
                     "z_cross_original": z_cross_original,
                     "min_freq_original": min_freq_original, 
                     "max_freq_original": max_freq_original,
                     "range_freq_original": range_freq_original,
                     "wave_bass": wave_bass,
                     "mean_aplitude_bass": mean_aplitude_bass, 
                     "z_cross_bass": z_cross_bass, 
                     "min_freq_bass": min_freq_bass, 
                     "max_freq_bass": max_freq_bass, 
                     "range_freq_bass": range_freq_bass,
                     "wave_drums": wave_drums,
                     "mean_aplitude_drums": mean_aplitude_drums, 
                     "z_cross_drums": z_cross_drums, 
                     "min_freq_drums": min_freq_drums, 
                     "max_freq_drums": max_freq_drums, 
                     "range_freq_drums": range_freq_drums,
                     "wave_vocals": wave_vocals, 
                     "mean_aplitude_vocals": mean_aplitude_vocals, 
                     "z_cross_vocals": z_cross_vocals, 
                     "min_freq_vocals": min_freq_vocals, 
                     "max_freq_vocals": max_freq_vocals, 
                     "range_freq_vocals": range_freq_vocals,
                     "wave_other": wave_other,
                     "mean_aplitude_other": mean_aplitude_other, 
                     "z_cross_other": z_cross_other, 
                     "min_freq_other": min_freq_other, 
                     "max_freq_other": max_freq_other, 
                     "range_freq_other": range_freq_other,
                     "wave_mixed": wave_mixed,
                     "mean_aplitude_mixed": mean_aplitude_mixed, 
                     "z_cross_mixed": z_cross_mixed, 
                     "min_freq_mixed": min_freq_mixed, 
                     "max_freq_mixed": max_freq_mixed, 
                     "range_freq_mixed": range_freq_mixed, 
                     "beat_times": beat_times
                    }
    new_song = new_song.append(new_song_dict, ignore_index=True)
    return new_song

def mix_tracks(new_song, other_song):
    mix_tracks_rating_df = pd.DataFrame()
    while len(mix_tracks_rating_df) < 1:
        mix_tracks_df = new_song
        mix_tracks_df.append(other_song.sample(1), ignore_index=True)
        wave_data, bpm_avg = get_wave_data(mix_tracks_df)
        mix_df = get_mix_features(mix_tracks_df)
        result, stems = get_mix_tracks(wave_data, bpm_avg)
        if len(result[0]) == len(result[1]) == len(result[2]) == len(result[3]):
            mix_df = get_stem_info(mix_df, result, stems)
            mixed_song = mix_df["mix"][0]
            mix_tracks_rating_df = mix_tracks_rating_df.append(mix_df, ignore_index=True)
        else:
            continue
    return mixed_song, mix_tracks_rating_df

if __name__=='__main__':
    youtube_link = get_youtube_link()
    audio_feature_track_names = get_audio_features_db()
    if not youtube_link in audio_feature_track_names["youtube_link"]:
        title, output_filename = extract_wav_from_yt_link(youtube_link)
        print(title)
        new_song = update_new_audio_features(output_filename, title)
        np.save(
         file_io.FileIO(
             f'gs://ai_dj_batch627_data/data/audio_features/{title}.npy',
             'w'), new_song)
        track_info = {"name": title, 
                      "youtube_link": youtube_link,
                      "audio_features_file": f'gs://ai_dj_batch627_data/data/audio_features/{title}.npy'
                      }
        audio_feature_track_names.append(track_info, ignore_index=True)
        np.save(
         file_io.FileIO(
             f'gs://ai_dj_batch627_data/data/audio_features/audio_features_track_names.csv',
             'w'), audio_feature_track_names)
    else:
        name = audio_feature_track_names[audio_feature_track_names["youtube_link"] == youtube_link]["name"].values[0]
        print(name)
        new_song = get_audio_features(name)
    other_name = audio_feature_track_names.sample(1)["name"].values[0]
    print(other_name)
    other_song = get_audio_features(other_name)
    audio_files = [name, other_song]
    model = pickle.load(open("pipeline.pkl","rb"))
    predicted_rating = 0
    while predicted_rating < 5:
        mixed_song, mix_tracks_rating_df = mix_tracks(new_song, other_song)
        predicted_rating = model.predict(mix_tracks_rating_df)
        print(predicted_rating)
    final_mix = mixed_song
    
    #if rating submitted, add to rated_mixes.csv
    #run linear_model
     