import numpy as np
import pyaudio as pa
import matplotlib.pyplot as plt

FORMAT = pa.paInt16
CHANNELS = 1


def record_live_sound(record_time, sample_rate, chunk):
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


def play_sound(audio, sample_rate, chunk):
    """
    To play given frames as audio.

    Inputs:
        audio (np.ndarray): numpy array of frames to play as audio.
        sample_rate (int): sampling rate parameter for processing.
        chunk (int): chunk parameter for processing

    Outputs:
        None
    """

    """
    TODO: Convert audio from np.array to bytes.
    """

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


def record_audio_file(loc, sample_rate, chunk):
    """
    To record sound input from file.

    Inputs:
        loc (str): File from which sound is recorded.
        sample_rate (int): sampling rate parameter for processing
        chunk (int): chunk parameter for processing

    Outputs:
        np_frames (np.ndarray): input frames as numpy array.
    """

    """
    TODO: Convert audio from np.array to bytes.
    """

    pass


def plot_frames(frames):
    """
    Plot frames as matplotlib plot.

    Inputs:
        frames (np.ndarray): Frames (signal) to plot

    Outputs:
        None
    """

    """
    TODO: Convert audio from np.array to bytes.
    """

    plt.plot(np.arange(frames.shape[-1], frames))
    plt.show()


def preproc_time_input(in_frames):
    """
    Preprocess the input signal and obtain its (zero-centered) FFT.

    Inputs:
        in_frames (np.ndarray): input signals in time domain in form of np.array

    Outputs:
        freq_output (np.ndarray): frequency domain (FFT) output for given input.
    """

    """
    TODO: Convert audio from np.array to bytes.
    """

    pass


def preproc_freq_output(freq_output):
    """
    Preprocess the input signal and obtain its (zero-centered) FFT.

    Inputs:
        freq_output (np.ndarray): output signals in frequency domain in form of np.array

    Outputs:
        freq_output (np.ndarray): time domain (FFT) output for given input.
    """

    """
    TODO: Convert audio from np.array to bytes.
    """

    pass
