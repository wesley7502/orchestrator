# Orchestrator
EECS 571 project: a real-time multimodal speech synthesis tool, uses visual input (head motion) to control speech prosody (e.g. speed).

be sure to install opencv by using

```pip install opencv-contrib-python```

and for tts

```pip install -r requirements.txt```

To run the object tracking software, use
```python3 .\object_track.py --tracker csrt```

To run the tts, use
```python3 .\orchestrator.py```

The sound file will be played automatically, or can be found in ./output/result/LJSpeech

