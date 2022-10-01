from pickle import TRUE
import audioplayer as ap
import time

path = "/home/kosmos/Music/buzzer.mp3"

audio = ap.AudioPlayer(path)

audio.play(False,True)