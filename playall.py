from os import listdir
from os.path import isfile, join
from playsound import playsound
output_path = './output/result/LJSpeech'
files = set([f for f in listdir(output_path) if isfile(join(output_path, f))])

while True:
    new_files = set([f for f in listdir(output_path) if isfile(join(output_path, f))])
    newf = new_files - files
    
    if newf:
        files = new_files
        f = './output/result/LJSpeech' + '/' + newf.pop()
        playsound(f)
        print(f)
