import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, find_peaks, freqz

#text-to-array
def txt_to_arr(file_path):
    # Read data from the text file
    data = np.loadtxt(file_path)
    return data


#funksjon som tar inn ett array data og samplingfrekvens, og spytter ut absoluttverdi av autokorrelasjon
def autocorrelate(data):
    #Vi får her at len(crosscorr) = len(x1) + len(x2) - 1
    auto_signal = np.abs(np.correlate(data, data, mode='full'))
    return auto_signal

def get_peaks(data):
    #Finner indeksen i krysskorrelasjonenslisten som
    peaks, _ = find_peaks(data)
    return peaks

#Bandpassfilters
def butter_bandpass(lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a
def butter_bandpass_filter(data, lowcut, highcut, fs, order=4):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

#SNR

def calculate_SNR(puls, noise): 
    maksAmp = np.max(puls)
    std_noise = np.std(noise)
    SNR = maksAmp/std_noise
    return SNR

def calculate_SNRdB(puls, noise):
    SNRdB = 10*np.log10(calculate_SNR(puls, noise))
    return SNRdB

def calc_SNR(amp, noise):
    SNR = amp/np.std(noise)
    return SNR

def calculate_SNR_fft(puls, noise):
    puls_fft = np.fft.fft(puls) 
    noise_fft = np.fft.fft(noise)
    
    maxPulseAmp = np.max(np.abs(puls_fft))
    meanNoiseAmp = np.mean(np.abs(noise_fft))
    
    SNR = maxPulseAmp/meanNoiseAmp
    return SNR
    
    