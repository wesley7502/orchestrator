'''
Python file to combine the TTS and the movement tracking
https://www.olivieraubert.net/vlc/python-ctypes/doc/
'''
import time
from os import add_dll_directory
add_dll_directory('C:\Program Files\VideoLAN\VLC')
import vlc
from tracker import Tracker
from tts import createMP3

def main_loop():
    global prev_time
    media_player = vlc.MediaPlayer()
    media = vlc.Media("speech.mp3")
    media_player.set_media(media)
    track = Tracker()

    # give the user 7 seconds to setup tracking
    time.sleep(7)
    media_player.play()
    while(True):
        current_time = time.time()

        # if the time hits 5 seconds, get the x/y values
        if current_time - prev_time >= 2:
            prev_time = current_time

            values = track.get_values()
            x = values[0]

            speed = x/125

            print(speed)
            #pause(media_player)
            media_player.set_rate(speed)

if __name__ == '__main__':
    global prev_time
    createMP3('speech.txt')
    prev_time = time.time()
    main_loop()
