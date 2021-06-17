import youtube_dl
from ai_dj import gcp_storage, params
from ai_dj.mix_rating import load_audio_features, get_wave_data, get_mix_features, get_mix_tracks, get_stem_info
from ai_dj.audio_features import get_BPM, computeKeyCl, min_max_freq, mean_amplitude, z_cross
from ai_dj.download_youtube import download_wav_and_metadata
from ai_dj.split_audio import split_tracks
import librosa
import os
import shutil
from google.cloud import storage
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

def mix_tracks(new_song, audio_features_df):
    mix_tracks_rating_df = pd.DataFrame()
    while len(mix_tracks_rating_df) < 1:
        mix_tracks_df = new_song
        mix_tracks_df.append(audio_features_df.sample(1), ignore_index=True)
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
    #check existing database
    #load names_yt_link csv
    #if yt link not in csv:
    title, output_filename = extract_wav_from_yt_link(youtube_link)
    print(title)
    new_song = update_new_audio_features(output_filename, title)
    #else:
    #get audio_features.npy
    #get random other name from names_yt_link csv
    #get audio_features.npy from other track
    #append audio_files with each rows from the songs
    model = pickle.load(open("pipeline.pkl","rb"))
    predicted_rating = 0
    while predicted_rating < 5:
        mixed_song, mix_tracks_rating_df = mix_tracks(new_song, audio_features_df)
        predicted_rating = model.predict(mix_tracks_rating_df)
    final_mix = mixed_song
    
    #if rating submitted, add to rated_mixes.csv
    #run linear_model
     