from ai_dj.download_youtube import YoutubeDownloader
import numpy as np
import pandas as pd
import librosa
from scipy.signal import spectrogram
from pyACA.ToolComputeHann import ToolComputeHann
from pyACA.FeatureSpectralPitchChroma import FeatureSpectralPitchChroma
from pyACA.ToolPreprocAudio import ToolPreprocAudio
from pyACA.ToolReadAudio import ToolReadAudio
from ai_dj.params import DOWNLOADED_FOLDER
from os import path

class AudioFeatureExtracter:

    def __init__(self, file):
        self.file = file
        
    def get_BPM(self, sr=44100):
        y, sr = librosa.load(self.file, sr=sr)

        # Run the default beat tracker
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        #print('Estimated tempo: {:.2f} beats per minute'.format(tempo))

        # Convert the frame indices of beat events into timestamps
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        return tempo, beat_frames, beat_times

    def computeKey(self, afAudioData, f_s, afWindow=None, iBlockLength=4096, iHopLength=2048):

        # compute window function for FFT
        if afWindow is None:
            afWindow = ToolComputeHann(iBlockLength)

        assert(afWindow.shape[0] == iBlockLength), "parameter error: invalid window dimension"

        # key names
        cKeyNames = np.array(['C Maj', 'C# Maj', 'D Maj', 'D# Maj', 'E Maj', 'F Maj', 'F# Maj', 'G Maj', 'G# Maj', 'A Maj', 'A# Maj', 'B Maj',
                            'c min', 'c# min', 'd min', 'd# min', 'e min', 'f min', 'f# min', 'g min', 'g# min', 'a min', 'a# min', 'b min'])

        # template pitch chroma (Krumhansl major/minor), normalized to a sum of 1
        t_pc = np.array([[6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88],
                        [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17]])
        t_pc = t_pc / t_pc.sum(axis=1, keepdims=True)

        # pre-processing
        afAudioData = ToolPreprocAudio(afAudioData, iBlockLength)

        # in the real world, we would do this block by block...
        [f, t, X] = spectrogram(afAudioData,
                                f_s,
                                afWindow,
                                iBlockLength,
                                iBlockLength - iHopLength,
                                iBlockLength,
                                False,
                                True,
                                'spectrum')

        #  scale the same as for matlab
        X = np.sqrt(X / 2)

        # compute instantaneous pitch chroma
        v_pc = FeatureSpectralPitchChroma(X, f_s)

        # average pitch chroma
        v_pc = v_pc.mean(axis=1)
        # compute manhattan distances for modes (major and minor)
        d = np.zeros(t_pc.shape)
        v_pc = np.concatenate((v_pc, v_pc), axis=0).reshape(2, 12)
        for i in range(0, 12):
            d[:, i] = np.sum(np.abs(v_pc - np.roll(t_pc, i, axis=1)), axis=1)

        # get unwrapped key index
        iKeyIdx = d.argmin()

        cKey = cKeyNames[iKeyIdx]

        return (cKey)

    def computeKeyCl(self):
        
        [f_s, afAudioData] = ToolReadAudio(self.file)
        # afAudioData = np.sin(2*np.pi * np.arange(f_s*1)*440./f_s)

        cKey = self.computeKey(afAudioData, f_s)
        #print("detected key: ", cKey)
        
        return cKey
    
if __name__=='__main__':
    
    yt_link = 'https://www.youtube.com/watch?v=ogv284C4W30'
    youtubedl = YoutubeDownloader(yt_link)
    title, song_id, output_filename, yt_link = youtubedl.download_metadata()
    
    audio_feature_extracter = AudioFeatureExtracter(f'{DOWNLOADED_FOLDER}/{output_filename}')
    tempo, beat_frames, beat_times = audio_feature_extracter.get_BPM()
    key = audio_feature_extracter.computeKeyCl()
    new_song_dict = {"song_id":song_id,
                    "youtube_link":yt_link,
                    "output_file": output_filename,
                    "title": title, 
                    "BPM": tempo, 
                    "key": key, 
                    "beat_frames": beat_frames, 
                    "beat_times": beat_times}
    df = pd.DataFrame(columns=new_song_dict.keys())
    df = df.append(new_song_dict, ignore_index=True)
    
    if path.exists("ai_dj/data/audio_features.csv"):
        df.to_csv("ai_dj/data/audio_features.csv", mode='a', header=False)
    else:
        df.to_csv("ai_dj/data/audio_features.csv")