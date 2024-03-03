import numpy as np
import matplotlib.pyplot as plt

pulssignal = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6])
noise = np.array([0.01, 0.02, 0.03, 0.4, 0.05, 0.06])

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
    
    SNR = maxPulseAmp/np.mean(meanNoiseAmp) 
    return SNR
    
    
    