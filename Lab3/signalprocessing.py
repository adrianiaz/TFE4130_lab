import numpy as np
import matplotlib.pyplot as plt
import processingUtilities as pu

#Set global variables
lowcut = 10.0  # Lower cutoff frequency
highcut = 50.0  # Upper cutoff frequency
fs = 1000.0  # Sampling frequency
order = 4  # Filter order

# Create a test signal
t = np.arange(0, 1, 1/fs)  # 1 second of data
  # 1 second of data
signal = np.sin(2 * np.pi * 30 * t) + 0.5 * np.sin(2 * np.pi * 200 * t)

#1. bandpass-filter
#2. autocorrelate signal with itself
#3. find the tops in the autocorrelated signals, and the time between tops

# Plot the original and filtered signals
plt.figure(figsize=(10, 6))
plt.plot(t, signal, label='Original Signal')
#plt.plot(t, filtered_signal, label='Filtered Signal')
plt.title('Butterworth Bandpass Filter')
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.legend()
plt.show()
