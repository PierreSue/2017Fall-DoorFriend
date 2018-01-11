import speech_recognition as sr
import os
import socket
import time
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('0.0.0.0', 5000))
sock.listen(1)

wit = 'CREDENTIAL HERE'

r = sr.Recognizer()
print(r.energy_threshold)
print('Accepting connections')
while True:
    conn, addr = sock.accept()
    print('Connection from {}'.format(addr))
    data = conn.recv(1024)
    data = data.decode('utf-8')
    data = data.rstrip('\r\n')
    print('Recv: {}'.format(data))
    os.system('echo "{} is here, do you want to open the door?" | festival --tts'.format(data))
    result = '0'
    for t in range(5):
        with sr.Microphone() as source: r.adjust_for_ambient_noise(source)
        print('Say something')
        with sr.Microphone() as source: audio = r.listen(source)
        print('Wait..')
        try:
            text = r.recognize_wit(audio, key=wit)
            print('Google thinks that you said {}'.format(text))
            if text == 'yes':
                result = '1'
                break
            else:
                break
        except sr.RequestError as e:
            print('Didn\'t catch that!')
            print(e)
    conn.send(result.encode('utf-8'))
    conn.close()


