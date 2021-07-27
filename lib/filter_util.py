import numpy as np
from numpy.lib.npyio import save
from numpy.testing._private.utils import integer_repr
import pyaudio as pa
import matplotlib.pyplot as plt
import wave

from utils import (
    preproc_freq_output,
    preproc_time_input,
    plot_frames,
    play_audio_from_np,
)
from audio_filter import AudioFilter

FORMAT = pa.paInt16
CHUNK = 1024
CHANNELS = 1


def test_static(in_frames, filter_type, params, Fs, play_audio=False):
    """
    Test filters for recorded audio / static sinusoidal signals (mixture of frequencies).

    Inputs:
        in_freqs (list): List of frequencies to mix
        filter_type (str): Type of filter to use
        Fs (float): Sampling frequency

    Outputs:
        out_frames (np.ndarray): Processed signal
    """

    in_fft_freqs, in_fft = preproc_time_input(in_frames, Fs)

    filter = AudioFilter(filter_type, in_fft_freqs, params=params)

    plt.xlabel("Frequency")
    plt.ylabel("|H(z)|")
    plt.plot(
        in_fft_freqs[in_fft_freqs >= 0],
        filter.filter[: filter.filter.size // 2],
    )
    plt.savefig("../assets/plots/filter.jpg")
    plt.close()

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
        play_audio_from_np(out_frames, Fs)


def test_dynamic(
    record_time,
    filter_type,
    params,
    Fs,
    play_audio,
    save_dir="../assets/audio/processed.wav",
):
    """
    Test filter for live audio streaming.

    Inputs:
        record_time (int): Time in seconds for which to record audio and filter
        filter_type (str): Type of filter to use
        Fs (float): Sampling frequency

    Outputs:
        out_frames (np.ndarray): Processed signal (also saved to save_dir)
    """

    chunk = 2 ** 16

    p = pa.PyAudio()

    in_stream = p.open(
        format=FORMAT,
        rate=int(Fs),
        channels=CHANNELS,
        frames_per_buffer=chunk,
        input=True,
    )

    out_stream = p.open(
        format=FORMAT,
        rate=int(Fs),
        channels=CHANNELS,
        output=True,
    )

    out_frames_np = []
    out_frames_bytes = []

    for step in range((record_time * int(Fs)) // chunk):
        in_frame = np.frombuffer(in_stream.read(chunk), dtype="int16")

        in_fft_freqs, in_fft = preproc_time_input(in_frame, Fs)

        filter = AudioFilter(filter_type, in_fft_freqs, params)

        freq_output = filter(in_fft)
        out_frame_np = preproc_freq_output(freq_output, in_frame.size).astype(
            np.int16
        )

        out_frames_np.append(out_frame_np)
        out_frames_bytes.append(out_frame_np.tobytes())

        if play_audio:
            byte = out_frame_np.tobytes()
            out_stream.write(byte)

        plot_frames(
            {
                "Input signal": in_frame,
                "Input FFT": (
                    in_fft_freqs[in_fft_freqs >= 0],
                    np.abs(in_fft[: in_fft.size // 2]),
                ),
                "Output Signal": out_frame_np,
                "Output FFT": (
                    in_fft_freqs[in_fft_freqs >= 0],
                    np.abs(freq_output[: freq_output.size // 2]),
                ),
            }
        )

    # write_audio(save_dir, int(Fs), np.array(out_frames))

    wav_file = wave.open(save_dir, "wb")
    wav_file.setnchannels(1)
    wav_file.setsampwidth(pa.get_sample_size(pa.paInt16))
    wav_file.setframerate(int(Fs))
    wav_file.writeframes(np.array(out_frames_np).tobytes())
    wav_file.close()

    in_stream.stop_stream()
    in_stream.close()
    out_stream.stop_stream()
    out_stream.close()
    p.terminate()

    return out_frames_np


'''
def record_live_audio(record_time, sample_rate, chunk):
    """
    To record sound input from live audio input.

    Inputs:
        record_time (int): Time for which sound is recorded.
        sample_rate (int): sampling rate parameter for processing
        chunk (int): chunk parameter for processing

    Outputs:
        np_frames (np.ndarray): input frames as numpy array.
    """

    p = pa.PyAudio()

    in_stream = p.open(
        format=FORMAT,
        rate=sample_rate,
        channels=CHANNELS,
        frames_per_buffer=chunk,
        input=True,
    )

    byte_frames = []
    int_frames = []

    print("----Recording Audio----")

    for _ in range((record_time * sample_rate) / chunk):
        data_chunk = in_stream.read(chunk)
        byte_frames.append(data_chunk)

        for chunk in byte_frames:
            int_frames.append(int(chunk))

    np_frames = np.array(int_frames)

    in_stream.stop_stream()
    in_stream.close()

    return np_frames
'''
