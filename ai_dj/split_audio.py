from spleeter.separator import Separator
from ai_dj.params import DOWNLOADED_FOLDER, SPLIT_DATA_FOLDER
from ai_dj import gcp_storage
import os

class SpleeterSeparator():
    def __init__(self, file, stems=5):
        self.file = file
        self.separator = Separator(f'spleeter:{str(stems)}stems')
    
    def split_song(self):
        self.separator.separate_to_file(self.file, SPLIT_DATA_FOLDER)
        folder = self.file.replace(".wav", "")
        gcp_storage.upload_stems(folder)
        os.remove(f'{SPLIT_DATA_FOLDER}/{folder}')
    
# class DemucsSeparator():
#     def __init__(self, file):
#         self.file = file
        
## Test ##
if __name__=='__main__':
    file = f"{DOWNLOADED_FOLDER}/Two Scoops-Q77vdqA0hnM.wav"
    separator = SpleeterSeparator(file)
    separator.split_song()
## Test ##
