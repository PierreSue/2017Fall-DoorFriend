#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
import argparse
import sys
import glob
import os
import itertools
import time
import scipy.io.wavfile as wavfile

sys.path.append(os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'gui'))
from gui.interface import ModelInterface
from gui.utils import read_wav
from filters.silence import remove_silence

import RPi.GPIO as GPIO

def get_args():
    desc = "Speaker Recognition "
    epilog = """

Examples:
    Train (enroll a list of person named person*, and mary, with wav files under corresponding directories):
    ./speaker-recognition.py -t enroll -i "./Pierre/ ./Monmon/ ./Chiwei" -m model.out

    Predict (predict the speaker of all wav files):
    ./speaker-recognition.py -t predict -i "./*.wav" -m model.out -n name

    Expand (expand the existing model by several speakers)
    ./speaker-recognition.py -t expand -i "./Shangde/ " -m previous_model.out -n new_model.out
"""

    parser = argparse.ArgumentParser(description=desc,epilog=epilog,
                                    formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-t', '--task',
                       help='Task to do. Either "enroll", "predict", or expand',
                       required=True)

    parser.add_argument('-i', '--input',
                       help='Input Files(to predict) or Directories(to enroll)',
                       required=True)

    parser.add_argument('-m', '--model',
                       help='Model file to save(in enroll) or use(in predict)',
                       required=True)
    
    parser.add_argument('-n', '--index',
                       help='Index to compare or new model',
                       required=False)

    ret = parser.parse_args()
    return ret

def task_enroll(input_directory, output_model):
    m = ModelInterface()
    for k in input_directory.strip().split():
        input_dirs = [os.path.expanduser(k)]
    for d in input_directory:
        dirs = itertools.chain(*(glob.glob(d)))
    for d in dirs:
        if os.path.isdir(d):
            dirs = [d]
    files = []
    if len(dirs) == 0:
        print "No valid directory found!"
        sys.exit(1)
    for d in dirs:
        label = os.path.basename(d.rstrip('/'))

        wavs = glob.glob(d + '/*.wav')
        if len(wavs) == 0:
            print "No wav file found in {0}".format(d)
            continue
        print "Label {0} has files {1}".format(label, ','.join(wavs))
        for wav in wavs:
            fs, signal = read_wav(wav)
            m.enroll(label, fs, signal)

    m.train()
    m.dump(output_model)

def task_predict(input_files, input_model, index):
    m = ModelInterface.load(input_model)
    for f in glob.glob(os.path.expanduser(input_files)):
        fs, signal = read_wav(f)
        label = m.predict(fs, signal)
        print f, '->', label
        if label == index:
            sys.exit(1)
        else:
            sys.exit(2)

def task_expand(input_directory, input_model, output_model):
    m = ModelInterface.load(input_model)
    for k in input_dirs.strip().split():
        input_dirs = [os.path.expanduser(k)]
    for d in input_directory:
        dirs = itertools.chain(*(glob.glob(d)))
    for f in dirs:
        if(os.path.isdir(d)):
            dirs = [d]
    files = []
    if len(dirs) == 0:
        print "No valid directory found!"
        sys.exit(1)
    for d in dirs:
        label = os.path.basename(d.rstrip('/'))

        wavs = glob.glob(d + '/*.wav')
        if len(wavs) == 0:
            print "No wav file found in {0}".format(d)
            continue
        print "Label {0} has files {1}".format(label, ','.join(wavs))
        for wav in wavs:
            fs, signal = read_wav(wav)
            m.enroll(label, fs, signal)

    m.train()
    m.dump(output_model)

if __name__ == '__main__':
    global args
    args = get_args()

    task = args.task
    if task == 'enroll':
        task_enroll(args.input, args.model)
    elif task == 'predict':
        task_predict(args.input, args.model, args.index)
    elif task == 'expand':
        task_expand(args.input, args.model, args.index)
