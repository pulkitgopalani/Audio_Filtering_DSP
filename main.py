import numpy as np
import matplotlib.pyplot as plt

import pyaudio as pa

def low_pass_filter(f_c, size):
    freq_filter = np.concatenate(np.zeros((size-f_c,)), np.ones((2*f_c,)), np.zeros((size-f_c,)))
    return freq_filter

def high_pass_filter(f_c, size):
    freq_filter = np.concatenate(np.ones((size-f_c,)), np.zeros((2*f_c,)), np.ones((size-f_c,)))
    return freq_filter

def band_pass_filter(f_l, f_h, size):
    freq_filter = np.concatenate(np.zeros((size-f_h,)), np.ones((f_h-f_l,)), np.zeros((2*f_l,)), np.ones((f_h-f_l,)), np.zeros((size-f_h,)))
    return freq_filter

def lccde_filter(coeffs):
    pass

def pole_zero_filter(poles, zeros):
    pass

def hear_sound():
    pass

def play_sound():
    pass


def process_real_time():

    in_stream = hear_sound()

    #Process the sound here

    out_stream = play_sound()