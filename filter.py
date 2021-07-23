import argparse
import numpy as np
import pyaudio as pa
import matplotlib.pyplot as plt


class AudioFilter:
    """
    Class for audio filter.
    """

    def __init__(self, filter_type, params):
        """
        Initialize filter based on filter_type and params.

        Inputs:
            filter_type (str): Type of filter to initialize, possible types: "lowpass", "highpass", "bandpass", "lccde", "pz"
            params (dict): Various params relevant to the filter type:
            {
                cutoff frequency (f_c) for (lowpass, highpass),
                upper (f_h) and lower (f_l) cutoff for (bandpass),
                coefficients (coeffs) for (lccde),
                poles and zeros (as a dict pz = {'poles':[], 'zeros':[]} for (pz)
            }

        Outputs:
            None
        """

        self.filter_type = filter_type
        self.params = params

        self.filters = ["lowpass", "highpass", "bandpass", "lccde", "pz"]

        try:
            assert self.filter_type in self.filters

            if self.filter_type == "lowpass":
                self.filter = np.concatenate(
                    [
                        np.zeros((self.params["size"] - self.params["f_c"],)),
                        np.ones((2 * self.params["f_c"],)),
                        np.zeros((self.params["size"] - self.params["f_c"],)),
                    ]
                )

            elif self.filter_type == "highpass":
                self.filter = np.concatenate(
                    [
                        np.ones(
                            (self.params["size"] // 2 - self.params["f_c"],)
                        ),
                        np.zeros((2 * self.params["f_c"],)),
                        np.ones(
                            (self.params["size"] // 2 - self.params["f_c"],)
                        ),
                    ]
                )

            elif self.filter_type == "bandpass":
                self.filter = np.concatenate(
                    [
                        np.zeros(
                            (self.params["size"] // 2 - self.params["f_h"],)
                        ),
                        np.ones((self.params["f_h"] - self.params["f_l"],)),
                        np.zeros((2 * self.params["f_l"],)),
                        np.ones((self.params["f_h"] - self.params["f_l"],)),
                        np.zeros(
                            (self.params["size"] // 2 - self.params["f_h"],)
                        ),
                    ]
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

    def __call__(self, freq_input):
        """
        __call__ method for AudioFilter class. Applies self.filter on given input.

        Inputs:
            freq_domain_input (np.ndarray): Frequency domain input for filter.

        Outputs:
            output (np.ndarray): Frequency domain output for given freq_domain_input and self.filter.
        """

        try:
            assert freq_input.shape == self.filter.shape
            output = self.filter * freq_input
            return output

        except AssertionError:
            raise ValueError(
                f"Shapes of filter {self.filter.shape} and input {freq_input.shape} do not match"
            )

    def get_filter(self):
        """
        Returns the filter as self.filter.
        """

        return self.filter
