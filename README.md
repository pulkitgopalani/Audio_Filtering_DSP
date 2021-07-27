## EE301 Course Project (Summer 2021)

Pulkit Gopalani  
Roll No. 180564

Audio filtering using Fourier transforms based filters.

Requirements:  
* Python 3.8 
* Numpy  
* Matplotlib  
* PyAudio

Run the following command in the `./lib/` directory:

`python main.py (--args)`  

Args are:  
  ```bash
    --filter : Filter type (default: lowpass, options: lowpass, highpass, bandpass, bandstop, gaussian, lccde, pz)
    --sample_rate: Sampling rate (default: 22050.)
    --static_analysis : For testing mixture of sinusoids
    --prerec_file : For testing pre-recorded .wav file
    --live_audio : Listening time for live filtering
    --play_audio : Playing output audio
    --noise : To add noise in static_analysis
    --stdev : Gaussian filter standard deviation
    --fc : Cutoff frequency for highpass or lowpass
    --fl, --fh: Lower and Upper cutoff frequency for band-pass filter
    
  ```
  
Please change the frequency mixture (for static analysis) directly in main.py. 
