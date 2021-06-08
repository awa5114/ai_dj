from ai_dj.params import MIXED_AUDIO_FOLDER, SPLIT_DATA_FOLDER
from pydub import AudioSegment

class AudioMixer:
    def __init__(self):
        pass
    
    def mix_stems(self, file_1, file_2):
        sound1 = AudioSegment.from_file(file_1)
        sound2 = AudioSegment.from_file(file_2)
        combined = sound1.overlay(sound2)
        combined.export(f"{MIXED_AUDIO_FOLDER}64_kygo_combined2.wav", format='wav')
    
## Test ##
file_1 = f"{SPLIT_DATA_FOLDER}64 Ways (Dam Swindle's 65th Way Dub) feat. Mayer Hawthorne-SKUk9RUacDQ/drums.wav"
file_2 = f"{SPLIT_DATA_FOLDER}Kygo, Sasha Sloan - I'll Wait (Lyric Video)-ogv284C4W30/other.wav"
mixer = AudioMixer()
mixer.mix_stems(file_1, file_2)
## Test ##