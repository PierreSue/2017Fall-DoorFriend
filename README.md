# 2017Fall-DoorFriend
It's a friend that recognizes you and your other friends!

## Directory structure
    - RPi: The code that should be run in RPi
    - Arduino: The Arduino sketch

## Use case
Imagine that you are busy cooking a great dinner for your party, and your friend is arriving at your house. Your friend pushes the bell, but you can't open the door with the dirty hands! Now the Door Friend comes to save your day. It can recognize you and your friends' faces and voices and open the door accordingly.

## Project structure
![The structure graph](https://i.imgur.com/fTyPmXD.png)
We use a Raspberry Pi to perform individual speaker / face recognition. An Arduino is used to control the behavior of the door and the OLED display used to greet the user outside. Also we use an LED strip to aid the face recognition in the night.

## Wiring

## Software installing
### Arduino part
You should first have `U8glib` installed. Then compile `arduino_door_lock.ino` and upload it to your Arduino.

### Raspberry Pi part
OpenCV should be installed first. You can refer to the link under `Refereneces` section. 
`scikit-learn` `scikits.talkbox` `pyssp` `PyAudio` `numpy` `scipy` should be installed for speaker recognition.

## Future improvements
- Have an additional RPi inside to notify user of arriving friends
- Make the enrollment process smoother
- The owner can lock the door manually

## References
- Installing OpenCV on RPi 3: <https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/>
- OpenCV face detection: <http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_objdetect/py_face_detection/py_face_detection.html>
- OpenCV face recognition: <https://www.superdatascience.com/opencv-face-recognition/>
- U8glib display driver: <https://github.com/olikraus/u8glib>
- ULN2803 datasheet: <http://www.ti.com/lit/ds/symlink/uln2803a.pdf>
- Speaker Recognition: <https://github.com/ppwwyyxx/speaker-recognition>
