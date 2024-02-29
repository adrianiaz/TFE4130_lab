import numpy as np
import sys
import matplotlib.pyplot as plt
from scipy.signal import get_window
from scipy.signal import detrend
import oppgave1
import math

#Sampling frequency
fs = 31250

def raspi_import(path, channels=5):

    with open(path, 'r') as fid:
        sample_period = np.fromfile(fid, count=1, dtype=float)[0]
        data = np.fromfile(fid, dtype='uint16').astype('float64')
        # The "dangling" `.astype('float64')` casts data to double precision
        # Stops noisy autocorrelation due to overflow
        data = data.reshape((-1, channels))

    # sample period is given in microseconds, so this changes units to seconds
    sample_period *= 1e-6
    return sample_period, data


# Import data from bin file
if __name__ == "__main__":
    sample_period, data = raspi_import(sys.argv[1] if len(sys.argv) > 1
            else 'mic-90gr-1.bin')

data=(data/4096)*3.3 #scale data to volts
data=detrend(data, axis=0, type='constant') #remove DC offset

mic3 = data[:,2]
mic2 = data[:,3]
mic1 = data[:,4]


#sampleforsinkelser
n21 = oppgave1.tidsforsinkelse(mic2,mic1, fs)
n31 = oppgave1.tidsforsinkelse(mic3,mic1, fs)
n32 = oppgave1.tidsforsinkelse(mic3,mic2, fs)



krysskorr21 = np.correlate(mic2, mic1, mode='full')
krysskorr31 = np.correlate(mic3, mic1, mode='full')
krysskorr32 = np.correlate(mic3, mic2, mode='full')
Autokorr = np.correlate(mic1,mic1, mode = 'full')

# Create time axis
time_axis = np.arange(-len(mic1) + 1, len(mic1))

# Plot cross-correlations
plt.plot(time_axis, krysskorr21, label='Cross-correlation 21')
plt.plot(time_axis, krysskorr31, label='Cross-correlation 31')
plt.plot(time_axis, krysskorr32, label='Cross-correlation 32')
plt.plot(time_axis, Autokorr, label = 'Autokorrelasjon  ')

plt.title('Cross-Correlation Results')
plt.xlabel('Time Lag')
plt.ylabel('Cross-Correlation Value')
plt.legend()
plt.xlim(-10,10)
plt.grid()
plt.show()
# for i in range(0,5):
#     plt.plot(time_scale_ms, data[:,i])
# #plt.xlim(0,1)
# plt.title('Støysignal fra mikrofon')
# plt.xlabel('Tid [ms]')
# plt.ylabel('Amplitude [V]')
# plt.legend(['ADC1', 'ADC2', 'MIC3 - ADC3', 'MIC2 - ADC4', 'MIC1 - ADC5'])
# plt.grid()
# plt.show()