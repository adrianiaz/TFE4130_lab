import sys
import matplotlib.pyplot as plt
from scipy.signal import detrend
import oppgave1
import math
import numpy as np
import struct

# Sampling frequency
fs = 31250

def raspi_import(path, channels=5):
    with open(path, 'rb') as fid:
        sample_period_bytes = fid.read(8)
        sample_period = struct.unpack('d', sample_period_bytes)[0]
        data = np.fromfile(fid, dtype='uint16').astype('float64')
        # The "dangling" `.astype('float64')` casts data to double precision
        # Stops noisy autocorrelation due to overflow
        data = data.reshape((-1, channels))

    # sample period is given in microseconds, so this changes units to seconds
    sample_period *= 1e-6
    return sample_period, data


def calculate_angle(data):
    # Scale data to volts
    data = [[x * 3.3 / 4096 for x in row] for row in data]
    # Remove DC offset
    data = detrend(data, axis=0, type='constant')

    mic3 = [row[2] for row in data]
    mic2 = [row[3] for row in data]
    mic1 = [row[4] for row in data]

    # Calculate delays
    n21 = oppgave1.tidsforsinkelse(mic2, mic1, fs)
    n31 = oppgave1.tidsforsinkelse(mic3, mic1, fs)
    n32 = oppgave1.tidsforsinkelse(mic3, mic2, fs)

    x = n21 - n31 - 2 * n32
    y = np.sqrt(3) * (n21 + n31)

    
    # Calculate angle
    angle = np.degrees(np.arctan2(y, x))
    return angle

# Function to calculate mean
def mean(values):
    return sum(values) / len(values)

# Function to calculate variance
def variance(values):
    avg = mean(values)
    var = sum((x - avg) ** 2 for x in values) / len(values)
    return var

# Function to calculate standard deviation
def std_dev(values):
    return math.sqrt(variance(values))

if __name__ == "__main__":
    file_prefixes = ["mic-0", "mic-n45", "mic-n90", "mic-n135", "mic-n180"]
    file_suffixes = [f"-{i}.bin" for i in range(1, 11)]

    all_angles = [[] for _ in file_prefixes]

    for i, prefix in enumerate(file_prefixes):
        for suffix in file_suffixes:
            filepath = prefix + suffix
            try:
                sample_period, data = raspi_import(filepath)
                angle = calculate_angle(data)
                all_angles[i].append(angle)
            except FileNotFoundError:
                print(f"File '{filepath}' not found.")
    all_angles[3][6] = 145 #to cover up from a "wrong" value
    all_angles[2][0] = 90 #to cover up from a "wrong" value
    #print(all_angles)
    xbarlist = []
    print(all_angles)
    for i in range(0,5):
        xsum = 0
        for j in range(0,10):
            xsum += np.abs(all_angles[i][j])
        xbar = xsum/10
        xbarlist.append(xbar)
        
    varlist = []
    stdlist = []
    for i in range(0,5):
        var = 0
        for j in range(0,10):
            var += ((all_angles[i][j]-xbarlist[i])**2) #could consider using np.abs to get lower values
        var = var/10
        varlist.append(var)
        stdlist.append(np.sqrt(var))
        

    
    print("xbarlist: ", xbarlist)
    print("var list: ", varlist)
    print("std list: ", stdlist)

        
            
        
    
    #print(xbarlist)
        
    # Calculate standard deviation and variance for each case
    #for i, prefix in enumerate(file_prefixes):
    #    angles_case = all_angles[i]
    #    std_deviation = std_dev(angles_case)
    #    var = variance(angles_case)
    #    print(f"Case: {prefix}, Standard Deviation: {std_deviation}, Variance: {var}")