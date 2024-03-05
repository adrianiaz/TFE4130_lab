import numpy as np
import matplotlib.pyplot as plt
import processingUtilities as pu
from scipy.signal import detrend

#Set global variables
fs = 30  # Sampling frequency
lowcut = 1  # Lower cutoff frequency
highcut = fs/2 - 1 # Upper cutoff frequency, set according to nyquist theorem, -1 to be below nyquist freq
order = 8  # Filter order

file_path = "postprocessing/transfinger3.txt"  # Path file to txt samplefile

# Create a test signal
t = np.arange(0, 1, 1/fs)  # 1 second of data
signal = np.sin(2 * np.pi * 30 * t) + 0.5 * np.sin(2 * np.pi * 200 * t) # 1 second of data


def main():

    #0. create data file from txt-file
    data_array = pu.txt_to_arr(file_path)

    #0.5. divide it up into its component channels. every index of the list represents the sample number
    red = []
    green = []
    blue = []
    for row in data_array:
        red.append(row[0])
        green.append(row[1])
        blue.append(row[2])
    
    #make seperate rgb channels
    red = np.array(red)
    green = np.array(green)
    blue = np.array(blue)
    data_array_channel = np.array([red],[green],[blue]) #values are given in a unit of intensity
    print("data array channel: ", data_array_channel)

    #Do processing for every channel of color
    for channel in range(len(data_array_channel)):
        color = ["red", "green", "blue"]

        signal = data_array_channel[channel] 
        t = np.arange(0, len(signal)/fs, 1/fs)
        
        
        data_autocorr_signal = pu.autocorrelate(signal)
        t_autocorr = np.arange(0, len(data_autocorr_signal)/fs, 1/fs)

        #1. apply filter
        signal_filtered = pu.butter_lowpass_filter(signal,lowcut, fs, order) #apply filter
        
        #2. autocorrelate signal with itself
        data_autocorr_filtered = pu.autocorrelate(signal_filtered)

        t_autocorr_filtered = np.arange(0, len(data_autocorr_filtered)/fs, 1/fs)

        #3. find the tops in the autocorrelated signals, and the time between tops
        peaks = pu.get_peaks(data_autocorr_filtered)

        print(peaks)
         # Plot original and filtered signals
        plt.figure(figsize=(12, 6))

        plt.subplot(4, 1, 1)
        plt.plot(t, signal, label='Raw Signal')
        plt.title('Original Signal - {}'.format(color[channel]))
        plt.xlabel('Time (seconds)')
        plt.ylabel('Amplitude')
        plt.legend()

        plt.subplot(4, 1, 2)
        plt.plot(t, np.real(signal_filtered), label='Filtered Signal')
        plt.title('Filtered Signal')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Amplitude')
        plt.legend()

        plt.subplot(4, 1, 3)
        plt.plot(t_autocorr, data_autocorr_signal, label='unfiltered Signal')
        plt.title('autocorr raw signal')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Amplitude')
        plt.legend()

        plt.subplot(4, 1, 4)
        plt.plot(t_autocorr_filtered, data_autocorr_filtered, label='Filtered Signal')
        plt.title('autocorr filtered signal')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Amplitude')
        plt.legend()

        plt.tight_layout()
        plt.show()

        #4. vil ha (#of peaks)/((antall samples i målt intervall)/fs) = [BPS], ganger med 60 for å få BPM

main()
