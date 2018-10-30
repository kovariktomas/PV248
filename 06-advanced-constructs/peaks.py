import sys
import re
import numpy as np
import collections
import wave
import struct
import math

#hodnoty na vstupu sign
def main():
    filename = sys.argv[1]

    wav = wave.open(filename, 'rb')

    #MONO = 1 STEREO = 2
    wav.getnchannels()
    #print("pocet kanalu: ", wav.getnchannels())
    num_channels = wav.getnchannels()

    #sampling frequency
    #print("vzorkovaci frekvence", wav.getframerate())
    sampling_frequency = wav.getframerate()

    #nframes
    #print("pocet vzorku:", wav.getnframes())
    num_frames = wav.getnframes()


    #print("pocet bitu:", wav.getsampwidth())
    sample_width = wav.getsampwidth()

    raw_data = wav.readframes(wav.getnframes())  # Returns byte data
    wav.close()

    #print(raw_data)

    #celkem vzorku
    total_samples = num_frames * num_channels

    if sample_width == 2:
        fmt = "%ih" % total_samples  # read signed 2 byte shorts
    else:
        raise ValueError("Only supports 16 bit audio formats.")
        return -1

    #prevod stereo na mono (vraci tuple)
    integer_data = struct.unpack(fmt, raw_data)

    #print("typ:", type(integer_data))


    #integer_data1 = []
    #integer_data1.append(integer_data)
    #print(integer_data1)
    if (num_channels == 2):
        integer_data1 = []
        for i in range(0, len(integer_data), 2):
            integer_data1.append((integer_data[i]+integer_data[i+1])/2)
        integer_data = integer_data1


    #zde mam integer hodnoty
    integer_data

    #okno ma byt 1s
    #pocet oken
    windows = len(integer_data) // sampling_frequency

    max_amplitude_full_sample = None
    max_i_full_sample = -1

    min_amplitude_full_sample = None
    min_i_full_sample = -1

    for w in range(windows):
        ##zpracovani jednoho okna

        #print(len(integer_data1))
        #jedno okno
        #print(len(integer_data))
        fft = np.fft.rfft(integer_data[w*sampling_frequency:w*sampling_frequency+sampling_frequency])
        #print(len(fft))
        #fft obsahuje n/2 dat
        #print("delka", len(fft))
        #average

        items = []
        for item in fft:
            items.append(np.abs(item))

        average = sum(items)/len(fft)
        #print(average)

        max_amplitude = 0
        max_i = -1

        min_amplitude = 0
        min_i = -1
        #print("delka", len(fft))
        for i in range(len(fft)):
            abs = np.abs(fft[i])
            if (abs >= average):
                if (abs > max_amplitude):
                    max_amplitude = abs
                    max_i = i
                    if (min_amplitude == 0):
                        min_amplitude = max_amplitude
                        min_i = i
                if (abs < min_amplitude):
                    min_amplitude = abs
                    min_i = i

        if min_amplitude_full_sample == None or min_amplitude_full_sample > min_amplitude:
            #print ("prepis_min")
            min_amplitude_full_sample = min_amplitude
            min_i_full_sample = min_i
        if max_amplitude_full_sample == None or max_amplitude_full_sample < max_amplitude:
            max_amplitude_full_sample = max_amplitude
            max_i_full_sample = max_i
        #print("low_amplitude:", min_amplitude, "high_amplitude:", max_amplitude)
        #print("low_amplitude xosa:", min_i, "high_amplitude xosa:", max_i)

    #print("low_amplitude:", min_amplitude_full_sample, "high_amplitude:", max_amplitude_full_sample)
    #print("low_amplitude xosa:", min_i_full_sample, "high_amplitude xosa:", max_i_full_sample)


    delka = len(fft)
    freq1 = delka-min_i_full_sample

    delka = len(fft)
    freq2 = delka - max_i_full_sample

    if not (max_i_full_sample == -1 and min_i_full_sample == -1):
        print("low: ", freq1, "high: ", freq2)
    else:
        print("no peaks")



#konec jednoho okna

main()