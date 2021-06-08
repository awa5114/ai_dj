from spleeter.separator import Separator

class SpleeterSeparator:
    def __init__(self, stems=4):
        self.separator = Separator(f'spleeter:{stems}stems')
    
    def split_song(self, file, stems=4)
        separator.separate_to_file(filename, 'Downloads/')
        split_song(file)

    song_1 = "64 Ways (Dam Swindle's 65th Way Dub) feat. Mayer Hawthorne-SKUk9RUacDQ.wav"
    tempo_1, beat_frames_1, beat_times_1 = get_BPM(song_1)



    song_2 = "Kygo, Sasha Sloan - I'll Wait (Lyric Video)-ogv284C4W30.wav"
    tempo_2, beat_frames_2, beat_times_2 = get_BPM(song_2)


    sound1 = AudioSegment.from_file("Downloads/64 Ways (Dam Swindle's 65th Way Dub) feat. Mayer Hawthorne-SKUk9RUacDQ/drums.wav")
    sound2 = AudioSegment.from_file("Downloads/Kygo, Sasha Sloan - I'll Wait (Lyric Video)-ogv284C4W30/other.wav")
    combined = sound1.overlay(sound2)

    combined.export("../ai_dj/data/64_kygo_combined2.wav", format='wav')