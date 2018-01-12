#!/bin/bash

/home/pi/final/speaker-recognition/src/speaker-recognition.py -n $1 -t predict -i testdata.wav -m /home/pi/final/speaker-recognition/src/mod.out
