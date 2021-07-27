import argparse
import numpy as np
import pyaudio as pa
import matplotlib.pyplot as plt

from utils import *
from filter_util import *

FORMAT = pa.paInt16
CHUNK = 1024
CHANNELS = 1


def main(args):

    params = {"freqs": {"f_c": args.fc, "f_l": args.fl, "f_h": args.fh}}

    lccde_params = {"coeffs": {"nr": [1.0, 1.0], "dr": [1.0, 1.0]}}

    pz_params = {"pz": {"poles": [1.0, 2.0], "zeros": [3.0, 4.0]}}

    gaussian_params = {"gaussian": {"stdev": args.stdev}}

    params.update(lccde_params)
    params.update(pz_params)
    params.update(gaussian_params)

    if args.static_analysis:
        in_freqs = [1.0]  # , 2000.0, 5000.0]
        in_frames = generate_mix_freq(in_freqs, noise=args.noise)

        test_static(
            in_frames=in_frames,
            filter_type=args.filter,
            params=params,
            Fs=args.sample_rate,
        )

    elif args.prerec_file:
        in_frames = record_audio_file(
            args.prerec_file, args.sample_rate, CHUNK
        )

        test_static(
            in_frames=in_frames,
            filter_type=args.filter,
            params=params,
            Fs=args.sample_rate,
            play_audio=args.play_audio,
        )

    elif args.live_audio:
        test_dynamic(
            record_time=args.live_audio,
            filter_type=args.filter,
            params=params,
            Fs=args.sample_rate,
            play_audio=args.play_audio,
        )

    else:
        raise ValueError(
            "Please choose one option from static_analysis, pre_recorded_file, record_audio"
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
        help="Sampling rate, default: 22050.0",
    )

    parser.add_argument(
        "--live_audio",
        type=int,
        default=None,
        help="Recording live audio time, default = None",
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
        "--noise",
        action="store_true",
        help="Noise for static analysis",
    )

    parser.add_argument(
        "--play_audio",
        action="store_true",
        help="Play audio",
    )

    parser.add_argument(
        "--fc",
        type=float,
        default=1000.0,
        help="Cutoff frequency, default: 1000.0",
    )

    parser.add_argument(
        "--fl",
        type=float,
        default=4000.0,
        help="Lower cutoff frequency, default: 4000.0",
    )

    parser.add_argument(
        "--fh",
        type=float,
        default=6000.0,
        help="Upper cutoff frequency, default: 6000.0",
    )

    parser.add_argument(
        "--stdev",
        type=float,
        default=600.0,
        help="Variance for Gaussian filter, default: 600.0",
    )

    args = parser.parse_args()
    main(args)
