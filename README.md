# orchestrator
EECS 571 project

This project is a real time TTS device.

be sure to install opencv by using

```pip install opencv-contrib-python```

and for tts

```pip install -r requirements.txt```

if it failed, which happens to me, just install it separately and install the latest version

To run the object tracking software, use
```python3 .\object_track.py --tracker csrt```

To run the tts, use
```python3 .\orchestrator.py```

You can alter the text and duration parameter in orchestrator.py
The sound file will be played automatically, or can be found in ./output/result/LJSpeech

Next step: stream gesture into orchestrator
