from socket import socket
import socket
import audioplayer as ap

def playAudio(audio):
    audio.play(False,False)

safe = "aman.mpeg"
unsafe = "tidak aman.mpeg"
audio_safe = ap.AudioPlayer(safe)
audio_unsafe = ap.AudioPlayer(unsafe)

host = "127.0.0.1"
port = 65432
so = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
so.connect((host,port))
data = so.recv(1024)

while True:
    print(data)
    if int(data.decode()) == 0:
        playAudio(audio_safe)
    elif int(data.decode()) == 1:
        playAudio(audio_unsafe)
