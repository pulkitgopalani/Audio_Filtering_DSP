import numpy as np
import pyaudio as pa
import matplotlib.pyplot as plt

FORMAT = pa.paInt16
CHANNELS = 1


def hear_sound(record_time, sample_rate, chunk):
    p = pa.PyAudio()

    in_stream = p.open(
        format=FORMAT,
        rate=sample_rate,
        channels=CHANNELS,
        frames_per_buffer=chunk,
        input=True,
    )

    frames = []

    print("----Recording Audio----")

    for _ in range((record_time * sample_rate) / chunk):
        data_chunk = in_stream.read(chunk)
        frames.append(data_chunk)

    in_stream.stop_stream()
    in_stream.close()

    return frames


def play_sound(audio, sample_rate, chunk):
    p = pa.PyAudio()

    out_stream = p.open(
        format=FORMAT,
        rate=sample_rate,
        channels=CHANNELS,
        frames_per_buffer=chunk,
        output=True,
    )

    print("----Playing Audio----")

    for data_chunk in audio:
        out_stream.write(data_chunk)

    out_stream.stop_stream()
    out_stream.close()
    p.terminate()

    return audio


def plot_frames(frames):
    plt.plot(np.arange(frames.shape[-1], frames))
    plt.show()


def preproc_and_fft_input(in_frames):
    pass


def preproc_and_ifft_output(freq_output):
    pass
