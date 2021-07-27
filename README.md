## EE301 Course Project (Summer 2021)

Audio filtering using Fourier transforms based filters.

Requirements:  
* Python 3.8 
* Numpy  
* Matplotlib  
* PyAudio

Run the following command in the `DSP_Project/lib/` directory:

`python main.py (--args)`  

Args are:  
  ```bash
    --filter : Filter type (default: lowpass, options: lowpass, highpass, bandpass, lccde, pz)
    --sample_rate: Sampling rate (default: 22050.)
    --static_analysis : For testing mixture of sinusoids
    --prerec_file : For testing pre-recorded .wav file
    --record_audio : For live filtering
    --play_audio : Playing output audio
  ```
  
Please change the frequency mixture (for static analysis) directly in main.py. 
