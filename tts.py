import pyttsx3

def playText(text,speed):
    engine = pyttsx3.init()
    engine.setProperty('rate', speed)
    engine.say(text)
    engine.runAndWait()

if __name__ == '__main__':
    f = open('speech.txt')
    speed = 100
    for line in f.readlines():
        playText(line,speed)
        speed += 25