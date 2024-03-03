import numpy as np
import matplotlib.pyplot as plt
import processingUtilities as pu

#Set global variables
lowcut = 10.0  # Lower cutoff frequency
highcut = 50.0  # Upper cutoff frequency
fs = 31250  # Sampling frequency
order = 4  # Filter order


def main():
    # Create a test signal
    t = np.arange(0, 1, 1/fs)  # 1 second of data
    signal = np.sin(2 * np.pi * 30 * t) + 0.5 * np.sin(2 * np.pi * 200 * t) # 1 second of data

    #1. bandpass-filter
    data_bndpass = pu.butter_bandpass_filter(signal,lowcut, highcut, fs)

    #2. autocorrelate signal with itself
    data_autocorr = pu.autocorrelate(data_bndpass)

    #3. find the tops in the autocorrelated signals, and the time between tops
    peaks = pu.get_peaks(data_autocorr)

    #forventer størst peak for l=0
    print(peaks)

    #vil finne antal samples mellom hver peak, aka. differansen mellom hver peak i lista peaks.

    #for å finne tiden dette tilsvarer, bruker man sampeldifferanse/fs

    

main()
