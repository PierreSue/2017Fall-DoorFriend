# speaker-recognition Tutorial
It is the speaker-reconition part by training the GMM model

## Introduction
    The main purpose of this part is to recognize who the speaker is. Firstly, training process will take repositories name after speakers, and process the .wavs one by one as well as detect the voice activity(VAD) and extract the feature. Furthermore, train the GMM model by the MFCC features. <br>
    One step forward, if you wanna add one speaker to the model, expand command will be your first priority for you don't need to train the existing speakers again. <br>
    At last, as somebody arrive by the door, the process will automatically call the prediction function and pass the name as a parameter. The command will check the name whether it matches to the sound.

## Software Dependencies
- scikit-learn 
    - `pip install scikit-learn` <br>
- scikits.talkbox 
    - `pip install scikits.talkbox` <br>
- pyssp
    - `pypm install pyssp` <br>
- PyAudio
    - `pip install pyaudio` <br>
- numpy
    - `sudo apt install python-numpyn` <br>
- scipy
    - `sudo apt install python-scipy` <br>

## Usage
- Train (enroll a list of person named person*, and mary, with wav files under corresponding directories): <br>
    - `./speaker-recognition.py -t enroll -i "./Pierre/ ./Monmon/ ./Chiwei" -m model.out` <br>
    <br>
- Predict (predict the speaker of all wav files): <br>
    - `./speaker-recognition.py -t predict -i "./*.wav" -m model.out -n name` <br>
    <br>
- Expand (expand the existing model by several speakers) <br>
    - `./speaker-recognition.py -t expand -i "./Shangde/ " -m previous_model.out -n new_model.out` <br>
