from spleeter.separator import Separator
from ai_dj.params import DOWNLOADED_FOLDER, SPLIT_DATA_FOLDER
from demucs

class SpleeterSeparator():
    def __init__(self, file, stems=4):
        self.file = file
        #self.separator = Separator(f'spleeter:{str(stems)}stems')
        self.separator = Separator('spleeter:4stems')
    
    def split_song(self):
        #self.separator.separate_to_file(self.file, SPLIT_DATA_FOLDER)
        self.separator.separate_to_file(self.file, "/Users/judithvanleersum/code/jvanleersum/ai_dj/ai_dj/data/split_audio_files/")
    
class DemucsSeparator():
    def __init__(self, file):
        self.file = file
        
## Test ##
#file = f'{DOWNLOADED_FOLDER}/Two Scoops-Q77vdqA0hnM.wav'
file = "/Users/judithvanleersum/code/jvanleersum/ai_dj/ai_dj/data/downloaded_music/Two Scoops-Q77vdqA0hnM.wav"
separator = SpleeterSeparator(file)
separator.split_song()
## Test ##
