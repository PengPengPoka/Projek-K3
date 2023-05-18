from playsound import playsound
from threading import Thread
 
def play_music():
    playsound('aman.mpeg')
 
# Play Music on Separate Thread (in background)
music_thread = Thread(target=play_music)
music_thread.start()

i=0
while i<10:
    print(i)
    i+=1
 
print("Does playsound block the main thread?")
user_input = input("What is your guess?: ")
print("You guessed: " + user_input)