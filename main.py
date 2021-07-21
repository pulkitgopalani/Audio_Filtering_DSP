import argparse
import numpy as np
from numpy.core.numeric import outer
import pyaudio as pa
import matplotlib.pyplot as plt

from utils import *
from filter import AudioFilter

FORMAT = pa.paInt16
CHANNELS = 1


def filter_signal(**kwargs):
    """
    Function to filter a signal using a given filter type.

    Inputs:
        record_audio (bool): Whether to record audio. If False, preset_frames should not be None
        preset_frames (np.ndarray): Test static signals defined by preset_frames
        filter_type (str): Filter type to use
        params (dict): Dict of params relevant to filter, refer AudioFilter docstring for details
        time (int): Time for which to record
        sample_rate (int): Sampling rate parameter
        play_audio (bool): Whether to play the resultant signal as audio

    Outputs:
        out_frames (np.ndarray): Resultant signal after filtering.
    """

    if kwargs["record_audio"]:
        in_frames = hear_sound(
            kwargs["time"], kwargs["sample_rate"], kwargs["chunk"]
        )
    else:
        in_frames = kwargs["preset_frames"]

    freq_input = preproc_and_fft_input(in_frames)

    filter = AudioFilter(kwargs["filter_type"], kwargs["params"])

    freq_output = filter(freq_input)
    out_frames = preproc_and_ifft_output(freq_output)

    if kwargs["play_audio"]:
        play_sound(out_frames, kwargs["sample_rate"], kwargs["chunk"])
    else:
        plot_frames(out_frames)

    return out_frames


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
        "--chunk",
        type=int,
        default=1024,
        help="Chunk parameter, default: 1024",
    )

    parser.add_argument(
        "--sample_rate",
        type=int,
        default=44100,
        help="Sampling rate, default: 44100",
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
