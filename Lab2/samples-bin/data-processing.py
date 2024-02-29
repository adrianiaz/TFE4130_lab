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
            else 'mic-0-15.bin') 

data=(data/4096)*3.3 #scale data to volts
data=detrend(data, axis=0, type='constant') #remove DC offset

mic3 = data[:,2]
mic2 = data[:,3]
mic1 = data[:,4]

#sampleforsinkelser
n21 = oppgave1.tidsforsinkelse(mic2,mic1, fs)
n31 = oppgave1.tidsforsinkelse(mic3,mic1, fs)
n32 = oppgave1.tidsforsinkelse(mic3,mic2, fs)
print(n21)
print(n31)
print(n32) 

x = (n21 - n31 - 2*n32)
y = np.sqrt(3)*(n21 + n31)
def theta(a,b):
    theta = np.arctan2(a,b)
    return theta
angle = theta(y,x)
angle = math.degrees(angle)
print('Theta = ', angle)



N = len(data) # Number of samples, N = 31250
M = 2**15 # Number of samples, M = 32768
time_scale_ms = sample_period * np.arange(N)*1000  # Time axis [ms]


#for i in range(0,5):
#    plt.plot(time_scale_ms, data[:,i])
#plt.xlim(0,1)
#plt.title('Støysignal fra mikrofon')
#plt.xlabel('Tid [ms]')
##plt.ylabel('Amplitude [V]')
#plt.legend(['ADC1', 'ADC2', 'MIC3 - ADC3', 'MIC2 - ADC4', 'MIC1 - ADC5'])
#plt.grid()
#plt.show()