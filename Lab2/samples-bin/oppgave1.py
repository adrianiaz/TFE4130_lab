import numpy as np

#samplingfrekvens
#fs =  1000

#placeholder for antall sampler
#n = 10

#array for n sampler for lydsignal som mottat fra henholdsvis mic 1 & 2
#x = np.zeros(n)
#y = np.zeros(n)

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

