import numpy as np
import matplotlib.pyplot as plt

pulsesignal = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
noise = np.array([0.01, 0.02, 0.03, 0.4, 0.05, 0.06])

def calculate_SNR(pulse, noise): 
    maksAmp = np.max(pulse)
    std_noise = np.std(noise)
    SNR = maksAmp/std_noise
    return SNR

def calculate_SNRdB(pulse, noise):
    SNRdB = 10*np.log10(calculate_SNR(pulse, noise))
    return SNRdB

def calc_SNR(amp, noise):
    SNR = amp/np.std(noise)
    return SNR

def calculate_SNR_fft(pulse, noise):
    pulse_fft = np.fft.fft(pulse) 
    noise_fft = np.fft.fft(noise)
    
    maxPulseAmp = np.max(np.abs(pulse_fft))
    meanNoiseAmp = np.mean(np.abs(noise_fft))
    
    SNR = maxPulseAmp/meanNoiseAmp
    return SNR
    
    
    