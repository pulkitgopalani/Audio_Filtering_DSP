import argparse
import numpy as np
import pyaudio as pa
import matplotlib.pyplot as plt

FORMAT = pa.paInt16
CHANNELS = 1

root_dir = ""


class Filter:
    def __init__(self, filter_type, params):
        self.filter_type = filter_type
        self.params = params

        self.filters = ["lowpass", "highpass", "bandpass", "lccde", "pz"]

        try:
            assert self.filter_type in self.filters

            if self.filter_type == "lowpass":
                self.filter = np.concatenate(
                    np.zeros((self.params["size"] - self.params["f_c"],)),
                    np.ones((2 * self.params["f_c"],)),
                    np.zeros((self.params["size"] - self.params["f_c"],)),
                )
            elif self.filter_type == "highpass":
                self.filter = np.concatenate(
                    np.ones((self.params["size"] - self.params["f_c"],)),
                    np.zeros((2 * self.params["f_c"],)),
                    np.ones((self.params["size"] - self.params["f_c"],)),
                )
            elif self.filter_type == "bandpass":
                self.filter = np.concatenate(
                    np.zeros((self.params["size"] - self.params["f_h"],)),
                    np.ones((self.params["f_h"] - self.params["f_l"],)),
                    np.zeros((2 * self.params["f_l"],)),
                    np.ones((self.params["f_h"] - self.params["f_l"],)),
                    np.zeros((self.params["size"] - self.params["f_h"],)),
                )
            elif self.filter_type == "lccde":
                self.filter = np.poly1d(self.params["coeffs"])
            elif self.filter_type == "pz":
                self.filter = np.poly1d(
                    self.params["pz"]["zeros"], r=True
                ) / np.poly1d(self.params["pz"]["poles"], r=True)

        except AssertionError:
            raise ValueError(
                f"Invalid filter, please choose from {self.filters}"
            )

    def __call__(self, freq_domain_input):
        try:
            assert freq_domain_input.shape == self.filter.shape
            print("----Applying filter in Frequency domain----")
            output = self.filter * freq_domain_input
            return output

        except AssertionError:
            raise ValueError("Shapes of filter and input do not match")

    def get_filter(self):
        return self.filter


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
        data_chunk = in_stream.reaAssertionErrord(chunk)
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


def process_real_time(**kwargs):

    in_data = hear_sound(
        kwargs["time"], kwargs["sample_rate"], kwargs["chunk"]
    )

    # Process the sound here
    filter = Filter(kwargs["filter_type"], kwargs["size"], kwargs["params"])

    out_data = play_sound(
        kwargs["time"], kwargs["sample_rate"], kwargs["chunk"]
    )


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
