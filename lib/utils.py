from typing import Tuple
import numpy as np
import pyaudio as pa
import matplotlib.pyplot as plt
import wave
from scipy.io.wavfile import read

from audio_filter import AudioFilter

FORMAT = pa.paInt16
CHANNELS = 1

# ---------------------------- AUDIO UTILS ----------------------------#


def record_audio_file(prerec_file, sample_rate, chunk):
    """
    To record sound input from file.

    Inputs:
        loc (str): File from which sound is recorded.
        sample_rate (int): sampling rate parameter for processing
        chunk (int): chunk parameter for processing

    Outputs:
        np_frames (np.ndarray): input frames as numpy array.
    """

    soundfile = read(prerec_file)
    in_frames = np.array(soundfile[1], dtype=float)

    return in_frames


def play_audio_from_np(out_frames, sample_rate):
    """
    To play given frames as audio.

    Inputs:
        audio (np.ndarray): numpy array of frames to play as audio.
        sample_rate (int): sampling rate parameter for processing.
        chunk (int): chunk parameter for processing

    Outputs:
        None
    """

    p = pa.PyAudio()

    out_frames = np.round(out_frames).astype(np.int16)

    out_stream = p.open(
        format=FORMAT,
        rate=int(sample_rate),
        channels=len(out_frames.shape),
        output=True,
    )

    print("----Playing Audio----")

    out_stream.write(out_frames.tobytes())

    out_stream.stop_stream()
    out_stream.close()
    p.terminate()


# ---------------------------- PLOT & FFT UTILS ----------------------------#


def plot_frames(frame_dict, n_cols=2, filename="../assets/plots/signals.jpg"):
    """
    Plot frames as matplotlib plot.

    Inputs:
        frames (np.ndarray): Frames (signal) to plot

    Outputs:
        None
    """

    frames = list(frame_dict.values())
    titles = list(frame_dict)

    fig, axes = plt.subplots(
        len(frames) // n_cols, n_cols, constrained_layout=True
    )

    pos = 0
    for row in axes:
        for col in row:
            if isinstance(frames[pos], Tuple):
                col.plot(frames[pos][0], frames[pos][1])
            else:
                col.plot(frames[pos])

            col.set_title(titles[pos])
            pos += 1

    fig.savefig(filename)
    plt.close()


def generate_mix_freq(freqs, noise=False):
    """
    Generate frequency mixture of sine waves of freqeuncies in freqs

    Inputs:
        freqs (list): list of frequencies
        size (int): size of sample

    Outputs:
        result (np.ndarray): Sum of sine-waves of all frequencies in freqs.
    """

    Fs = 22050
    T = 4
    range = np.arange(T * Fs) / Fs
    result = np.zeros_like(range)

    for freq in freqs:
        sin_freq = np.sin(2 * np.pi * freq * range)
        result += sin_freq

    if noise:
        result += np.random.randn(result.size)

    return result


def next_2_pow(n):
    return 2 ** (np.ceil(np.log2(n)))


def preproc_time_input(in_frames, Fs):
    """
    Preprocess the input signal and obtain its (zero-centered) FFT.

    Inputs:
        in_frames (np.ndarray): input signals in time domain in form of np.array

    Outputs:
        freq_output (np.ndarray): frequency domain (FFT) output for given input.
    """

    input_fft = np.fft.fft(in_frames, n=int(next_2_pow(in_frames.shape[-1])))
    fft_freqs = np.fft.fftfreq(n=len(input_fft), d=1 / Fs)
    return fft_freqs, input_fft


def preproc_freq_output(freq_output, size):
    """
    Preprocess the frequency domain output signal and obtain its time domain signal.

    Inputs:
        freq_output (np.ndarray): output signals in frequency domain in form of np.array

    Outputs:
        freq_output (np.ndarray): time domain (IFFT) output for given input.
    """

    ifft = np.fft.ifft(freq_output)[:size].real

    return ifft
