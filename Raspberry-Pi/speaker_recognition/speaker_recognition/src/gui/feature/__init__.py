#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
import sys
import MFCC
import LPC
import numpy as np

def get_extractor(extract_func, **kwargs):
    def f(tup):
        return extract_func(*tup, **kwargs)
    return f

def mix_feature(tup):
    mfcc = MFCC.extract(tup)
    lpc = LPC.extract(tup)
    if len(mfcc) == 0:
        print >> sys.stderr, "fail to extract mfcc :", len(tup[1])
    return np.concatenate((mfcc, lpc), axis=1)
