import argparse
import numpy as np
import pyaudio as pa
import matplotlib.pyplot as plt

from audio_utils import (
    preproc_freq_output,
    preproc_time_input,
    plot_frames,
    play_audio_from_np,
)
from filter import AudioFilter

FORMAT = pa.paInt16
CHUNK = 1024
CHANNELS = 1


def test_static(in_frames, filter_type, freq_params, Fs, play_audio=False):
    """
    Test filters for recorded audio / static sinusoidal signals (mixture of frequencies).

    Inputs:
        in_freqs (list): List of frequencies to mix
        filter_type (str): Which filter to use
        Fs (float): Sampling frequency

    Outputs:
        out_frames (np.ndarray): Processed signal
    """

    in_fft_freqs, in_fft = preproc_time_input(in_frames, Fs)

    filter = AudioFilter(
        filter_type, params={"freqs": in_fft_freqs, "f_c": freq_params["f_c"]}
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

    if play_audio:
        play_audio_from_np(out_frames, Fs, CHUNK)


def test_dynamic(record_time, filter_type, freq_params, Fs):
    pass
