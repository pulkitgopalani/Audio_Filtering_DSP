import os
import argparse
import numpy as np
import pyaudio as pa
import matplotlib.pyplot as plt

FORMAT = pa.paInt16
CHUNK = 1024
REC_TIME = 5
CHANNELS = 1
SAMPLE_RATE = 44100

root_dir = ""


def hear_sound():
    pass


def play_sound():
    pass


def low_pass_filter(f_c, size):
    filter = np.concatenate(
        np.zeros((size - f_c,)), np.ones((2 * f_c,)), np.zeros((size - f_c,))
    )
    print("Filter used: {}".format(filter))

    return filter


def high_pass_filter(f_c, size):
    filter = np.concatenate(
        np.ones((size - f_c,)), np.zeros((2 * f_c,)), np.ones((size - f_c,))
    )
    print("Filter used: {}".format(filter))

    return filter


def band_pass_filter(f_l, f_h, size):
    filter = np.concatenate(
        np.zeros((size - f_h,)),
        np.ones((f_h - f_l,)),
        np.zeros((2 * f_l,)),
        np.ones((f_h - f_l,)),
        np.zeros((size - f_h,)),
    )
    print("Filter used: {}".format(filter))

    return filter


def lccde_filter(coeffs):
    filter = np.poly1d(coeffs)
    print("Filter used: {}".format(filter))

    return filter


def pole_zero_filter(poles, zeros):
    filter = np.poly1d(zeros, r=True) / np.poly1d(poles, r=True)
    print("Filter used: {}".format(filter))

    return filter


def process_real_time():

    in_stream = hear_sound()

    # Process the sound here

    out_stream = play_sound()


def main(args):
    # do stuff
    pass


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--filter",
        type=str,
        default="low_pass",
        help="Type of filter, options: low_pass, high_pass, band_pass, pole_zero, lccde",
    )
    parser.add_argument(
        "--time", type=int, default=5, help="Time to record, default: 5 sec"
    )
    parser.add_argument(
        "--pre-recorded",
        action="store_true",
        help="To use prerecorded sound as test",
    )
    parser.add_argument(
        "--pre-recorded-audio",
        type="str",
        default="./audio.wav",
        help="Prerecorded sound file location, default = audio.wav",
    )

    args = parser.parse_args()
    main(args)
