# 2017Fall-DoorFriend
It's a friend that recognizes you and your other friends!

## Directory structure
    - RPi: The code that should be run in RPi
    - Arduino: The Arduino sketch

## Use case
Imagine that you are busy cooking a great dinner for your party, and your friend is arriving at your house. Your friend pushes the bell, but you can't open the door with the dirty hands! Now the Door Friend comes to save your day. It can recognize you and your friends' faces and voices and open the door accordingly.

## Project structure
![The structure graph](https://i.imgur.com/jKUtGx1.png)<br />

We use a Raspberry Pi to perform individual speaker / face recognition. Another Raspberry Pi is used as an in-house home assistant. An Arduino is used to control the behavior of the door and the OLED display used to greet the user outside. Also we use an LED strip to aid the face recognition in the night.

The two RPi's communicate through a TCP socket. The voice assistant acts as a server. When an user is identified successfully, the RPi outside will open a connection and notifies the indoor RPi of the arriving friend. The voice assistant then asks the home owner whether he/she wants to open the door. After receiving a response, it sends the result back to the outdoor RPi.

The RPi outside communicates with Arduino by simple pulled up GPIOs. The lines are pulled up to 3.3V, and the RPi pulls it down to 0V to notify Arduino of events.

## Face recognition
We use OpenCV to implement face detection and face recognition. In order to use OpenCV for face recognition, we install "opencv_contrib". For face detection, we use "haarcascade_frontalface_alt.xml". For face recognition, we use LBPH recognizer. Before the face recognition, we pre-train the recognizer and save it as "recognizer.xml" for future use. So when recognizing the faces, the program doesn't have to train the faces again. The program then takes a photo every second and process it. If the face hasn't been found in the image or hasn't been recognized, the program will continue to take photos. Once the face is recognized, it will execute speeker recognition program and send the name of the face to it.
### haar cascade classifier
Use edged features, line features, and four-rectangle features to describe and detect the features on the face. Furthermore, use cascade of classifiers to determine a region is a face or not. The reason for cascading classifier is for efficiency. Because once the face doesn't pass one of the classifiers, this region will be determined as "no face".
### LBPH recognizer
LBPH mean "local binary pattern histogram". It is a type of texture spectrum model. We use it because it is very efficiency and common.

## speaker-recognition Tutorial
It is the speaker-reconition part by training the GMM model

### Introduction
   The main purpose of this part is to recognize who the speaker is. Firstly, training process will take repositories name after speakers, and process the .wavs one by one as well as detect the voice activity(VAD) and extract the feature. Furthermore, train the GMM model by the MFCC features. <br>
   One step forward, if you wanna add one speaker to the model, expand command will be your first priority for you don't need to train the existing speakers again. <br>
   At last, as somebody arrive by the door, the process will automatically call the prediction function and pass the name as a parameter. The command will check the name whether it matches to the sound.

### Software Dependencies
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

### Usage
- Train (enroll a list of person named person*, and mary, with wav files under corresponding directories): <br>
    - `./speaker-recognition.py -t enroll -i "./Pierre/ ./Monmon/ ./Chiwei" -m model.out` <br>
    <br>
- Predict (predict the speaker of all wav files): <br>
    - `./speaker-recognition.py -t predict -i "./*.wav" -m model.out -n name` <br>
    <br>
- Expand (expand the existing model by several speakers) <br>
    - `./speaker-recognition.py -t expand -i "./Shangde/ " -m previous_model.out -n new_model.out` <br>


## Wiring
### Communication between RPi <-> Arduino
Pull these pins up to 3.3V with a resistor.
- Connect the grounds together
- Open pin RPi 13 <-> Arduino 8
- Alarm pin RPi 11 <-> Arduino 9
- Speak notify pin RPi 15 <-> Arduino 7
- Busy notify pin RPi 7 <-> Arduino A2
### Ultrasonic Sensor
- VCC <-> 5V
- TRIG <-> Arduino A0
- ECHO <-> Arduino A1
### Fingerprint Reader
- VCC <-> 5V
- TX <-> Arduino 11
- RX <-> Arduino 10
### OLED Display
- VCC <-> 5V
- SCL <-> Arduino A5
- SDA <-> Arduino A4
### Other Peripherals
- Magnetic lock (driven by ULN2803) <-> Arduino 2
- LED Strip (driven by ULN2803) <-> Arduino 3
- Buzzer / Green LED / Red LED <-> Arduino 3 / 4 / 5

## Software installation
### Arduino part
You should first have `U8glib`, `Ultrasonic`, `Adafruit_Fingerprint` installed. Then compile `arduino_door_lock.ino` and upload it to your Arduino.

### Raspberry Pi part
OpenCV should be installed first. You can refer to the link under `Refereneces` section. Also we have a writeup here: <https://github.com/NTUEE-ESLab/2017Fall-DoorFriend/blob/master/OpenCV_INSTALL.md>  
The speaker regocnition part requires `pyssp`, `scikits.talkbox`, `scikit-learn`, `numpy`, `scipy`, `PyAudio`.

## Future improvements
- Make the enrollment process smoother
- The owner can lock the door manually

## References
- Installing OpenCV on RPi 3: <https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/>
- OpenCV face detection: <http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_objdetect/py_face_detection/py_face_detection.html>
- OpenCV face recognition: <https://www.superdatascience.com/opencv-face-recognition/>
- U8glib display driver: <https://github.com/olikraus/u8glib>
- ULN2803 datasheet: <http://www.ti.com/lit/ds/symlink/uln2803a.pdf>
