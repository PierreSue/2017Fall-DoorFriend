# speaker-recognition Tutorial
It is the speaker-reconition part by training the GMM model

## Usage
-Train (enroll a list of person named person*, and mary, with wav files under corresponding directories):
    -`./speaker-recognition.py -t enroll -i "./Pierre/ ./Monmon/ ./Chiwei" -m model.out`
-Predict (predict the speaker of all wav files):
    -.`/speaker-recognition.py -t predict -i "./*.wav" -m model.out -n name`
-Expand (expand the existing model by several speakers)
    -`./speaker-recognition.py -t expand -i "./Shangde/ " -m previous_model.out -n new_model.out`
