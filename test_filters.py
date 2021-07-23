import argparse
import numpy as np
import pyaudio as pa
import matplotlib.pyplot as plt

from utils import *
from filter import AudioFilter

FORMAT = pa.paInt16
CHUNK = 1024
CHANNELS = 1


def test_sine_mix(in_freqs, filter_type, Fs):
    """
    Test filters for static sinusoidal signals (mixture of frequencies).

    Inputs:
        in_freqs (list): List of frequencies to mix
        filter_type (str): Which filter to use
        Fs (float): Sampling frequency

    Outputs:
        out_frames (np.ndarray): Processed signal
    """

    in_frames = generate_mix_freq(in_freqs)
    in_fft_freqs, in_fft = preproc_time_input(in_frames, Fs)

    filter = AudioFilter(
        filter_type, params={"freqs": in_fft_freqs, "f_c": 500.0}
    )

    freq_output = filter(in_fft)
    out_frames = preproc_freq_output(freq_output, in_frames.size)

    plot_frames(
        {
            "Input signal": in_frames,
            "Input FFT": (
                in_fft_freqs[in_fft_freqs >= 0],
                np.abs(in_fft[: in_fft.size // 2]),
            ),
            "Output Signal": out_frames,
            "Output FFT": (
                in_fft_freqs[in_fft_freqs >= 0],
                np.abs(freq_output[: freq_output.size // 2]),
            ),
        }
    )


def test_prerec_file(in_frames, filter, Fs):
    pass


def test_live_audio(filter, Fs):
    pass
