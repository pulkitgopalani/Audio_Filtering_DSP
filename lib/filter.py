import argparse
import numpy as np
import pyaudio as pa
import matplotlib.pyplot as plt


class AudioFilter:
    """
    Class for audio filter.
    """

    def __init__(self, filter_type, freqs, params):
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
        self.freqs = freqs
        self.params = params
        self.filter = None
        self.filters = ["lowpass", "highpass", "bandpass", "lccde", "pz"]
        eps = 1e-4

        try:
            assert self.filter_type in self.filters

            if self.filter_type == "lowpass":
                self.filter = np.where(
                    np.abs(self.freqs) < self.params["freqs"]["f_c"],
                    1.0,
                    0.0,
                )

            elif self.filter_type == "highpass":
                self.filter = np.where(
                    np.abs(self.freqs) > self.params["freqs"]["f_c"],
                    1.0,
                    0.0,
                )

            elif self.filter_type == "bandpass":
                self.filter = np.where(
                    np.logical_and(
                        (np.abs(self.freqs) > self.params["freqs"]["f_l"]),
                        (np.abs(self.freqs) < self.params["freqs"]["f_h"]),
                    ),
                    1.0,
                    0.0,
                )

            elif self.filter_type == "lccde":
                nr = np.poly1d(self.params["coeffs"]["nr"])
                dr = np.poly1d(self.params["coeffs"]["dr"])
                self.filter = nr(np.exp(1j * 2 * np.pi * self.freqs)) / (
                    dr(np.exp(1j * 2 * np.pi * self.freqs)) + eps
                )

            elif self.filter_type == "pz":
                nr = np.poly1d(self.params["pz"]["zeros"], r=True)
                dr = np.poly1d(self.params["pz"]["poles"], r=True)
                self.filter = nr(np.exp(1j * 2 * np.pi * self.freqs)) / (
                    dr(np.exp(1j * 2 * np.pi * self.freqs)) + eps
                )

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
