import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import collections
import struct

filename = sys.argv[1]

spf = wave.open(filename,'r')

#Extract Raw Audio from Wav File
signal = spf.readframes(-1)

signal = np.fromstring(signal, 'Int16')
if (spf.getnchannels() == 2):
    integer_data1 = []
    for i in range(0, len(signal), 2):
        integer_data1.append((signal[i] + signal[i + 1]) / 2)
    signal = integer_data1


print(max(signal))

#fft = np.fft.rfft(signal[0:44100])

#signal = fft





plt.figure(1)
plt.title('Signal Wave...')
plt.plot(signal)
plt.show()