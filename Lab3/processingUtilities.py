import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz

#funksjon som tar inn to array x1 og x2 og samplingfrekvens, og gir ut tidsforsinkelsen i sekund.
def tidsforsinkelse(x,y,fs):
    #kryskorrelasjon mellom x1 og x2, tar absoluttverdi for di vi kun er interessert i positive verdier
    #Vi får her at len(crosscorr) = len(x1) + len(x2) - 1
    crosscorr = np.abs(np.correlate(x, y, mode='full'))

    #Finner indeksen i krysskorrelasjonenslisten som
    max_index_crosscorr = np.argmax(crosscorr)

    #finner den sampelforsinkelsen, altså den l-en, hvor signalene er like, altså "sampelforsinkelsen"
    sampelforsinkelse = max_index_crosscorr - (len(y)- 1)


    #tidsforsinkelsen blir da fra teorien
    tidsforsinkelse = sampelforsinkelse/fs

    return sampelforsinkelse


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