from os import path
from pydub import AudioSegment
from pydub.playback import play
from IPython.display import Audio

def convert_mp3_to_wav(file):
    # change file extension for output file
    output_file = file.replace("mp3", "wav")    
    #convert from mp3 to wav                                                    
    sound = AudioSegment.from_mp3(file)
    sound.export(output_file, format="wav")
    return output_file