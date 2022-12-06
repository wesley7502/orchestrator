'''
Python file to combine the TTS and the movement tracking
'''
import time
import object_track

def main_loop():
    global prev_time    
    # give the user 7 seconds to setup tracking
    time.sleep(7)
    while(True):
        current_time = time.time()

        # if the time hits 5 seconds, get the x/y values
        if current_time - prev_time >= 5:
            prev_time = current_time



if __name__ == '__main__':
    global prev_time
    prev_time = time.time()
    object_track.track_object()
