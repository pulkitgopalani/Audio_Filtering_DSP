import argparse
import numpy as np
import pyaudio as pa
import matplotlib.pyplot as plt

from utils import *
from test_filters import *

FORMAT = pa.paInt16
CHUNK = 1024
CHANNELS = 1

"""
TODO: 
    0. (Done) Bytes -- np.array conversions
    1. (Done) Test on static input
    2. (Done) Test on pre-recorded file
    3. Test H(z) filters
    4. Test on live audio
    5. Check callback function in pyaudio
       for real time processing
"""


def main(args):

    freq_params = {"f_c": 4000.0, "f_l": 4000.0, "f_h": 6000.0}

    if args.static_analysis:
        in_freqs = [10.0, 200.0, 500.0, 2000.0, 5000.0]
        in_frames = generate_mix_freq(in_freqs)

        test_static(
            in_frames=in_frames,
            filter_type=args.filter,
            freq_params=freq_params,
            Fs=args.sample_rate,
        )

    elif args.prerec_file:
        in_frames = record_prerec_audio(
            args.prerec_file, args.sample_rate, CHUNK
        )

        test_static(
            in_frames=in_frames,
            filter_type=args.filter,
            freq_params=freq_params,
            Fs=args.sample_rate,
            play_audio=args.play_audio,
        )

    elif args.record_audio:
        test_dynamic(
            record_time=args.record_audio,
            filter_type=args.filter,
            freq_params=freq_params,
            Fs=args.sample_rate,
        )

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
        "--prerec_file",
        type=str,
        default=None,
        help="Prerecorded sound file location, default = None",
    )

    parser.add_argument(
        "--static_analysis",
        action="store_true",
        help="Static analysis",
    )

    parser.add_argument(
        "--play_audio",
        action="store_true",
        help="Play audio",
    )

    args = parser.parse_args()
    main(args)
