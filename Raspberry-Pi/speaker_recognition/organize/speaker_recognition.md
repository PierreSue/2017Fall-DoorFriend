# speaker-recognition Tutorial
It is the speaker-reconition part by training the GMM model

## Software Dependencies
- scikit-learn 
    - `pip install -U scikit-learn` <br>
- scikits.talkbox 
    - `pip install -U scikits.talkbox` <br>
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
