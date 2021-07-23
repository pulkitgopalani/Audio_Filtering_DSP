import argparse
import numpy as np
import pyaudio as pa
import matplotlib.pyplot as plt

from utils import *
from test_filters import *
from filter import AudioFilter

FORMAT = pa.paInt16
CHUNK = 1024
CHANNELS = 1

"""
TODO: 
    0. Bytes -- np.array conversions
    1. (Done) Test on static input
    2. Test on pre-recorded file
    3. Test on live audio
    4. Check callback function in pyaudio
       for real time processing
"""


def main(args):

    if args.static_analysis:
        in_freqs = [10.0, 200.0, 500.0, 2000.0, 5000.0]
        test_sine_mix(
            in_freqs=in_freqs, filter_type=args.filter, Fs=args.sample_rate
        )

    elif args.pre_recorded_file:
        test_prerec_file(
            prerec_file=args.pre_recorded_file,
            filter_type=args.filter,
            Fs=args.sample_rate,
        )

    elif args.record_audio:
        test_live_audio(record_time=args.record_audio, Fs=args.sample_rate)

    else:
        raise ValueError(
            f"Please choose one option from static_analysis, pre_recorded_file, record_audio"
        )


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--filter",
        type=str,
        default="lowpass",
        help="Type of filter, options: lowpass, highpass, bandpass, polezero, lccde",
    )

    parser.add_argument(
        "--sample_rate",
        type=float,
        default=22050.0,
        help="Sampling rate, default: 44100",
    )

    parser.add_argument(
        "--record_audio",
        type=int,
        default=None,
        help="Recording audio time, default = None",
    )

    parser.add_argument(
        "--pre_recorded_file",
        type=str,
        default=None,
        help="Prerecorded sound file location, default = None",
    )

    parser.add_argument(
        "--static_analysis",
        action="store_true",
        help="Static analysis",
    )

    args = parser.parse_args()
    main(args)
