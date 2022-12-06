import pyttsx3

def playText(text,speed):
    engine = pyttsx3.init()
    engine.setProperty('rate', speed)
    engine.say(text)
    engine.runAndWait()

def createMP3(filename):
    f = open(filename)
    engine = pyttsx3.init()
    string = ''
    for line in f.readlines():
        string += ' '
        string += line
    engine.setProperty('rate', 100) 
    engine.save_to_file(string, 'speech.mp3')
    engine.runAndWait()


if __name__ == '__main__':
    # f = open('speech.txt')
    # speed = 100
    # for line in f.readlines():
    #     words = line.split(' ')
    #     for word in words:
    #         playText(word,speed)
    #         speed += 25
    createMP3('speech.txt')