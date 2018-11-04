import sys
import numpy as np
import wave
import struct

#hodnoty na vstupu sign
def main():

    #otevreni souboru
    filename = sys.argv[1]
    wav = wave.open(filename, 'r')




    #MONO = 1 STEREO = 2
    #wav.getnchannels()
    #print("pocet kanalu: ", wav.getnchannels())
    num_channels = wav.getnchannels()

    #sampling frequency
    #print("vzorkovaci frekvence", wav.getframerate())
    sampling_frequency = wav.getframerate()

    #nframes
    #print("pocet vzorku:", wav.getnframes())
    num_frames = wav.getnframes()

    # okno ma byt 1s
    # pocet oken
    windows = num_frames // sampling_frequency
    #print(windows)

    min = -1
    max = -1

    #cyklus pres vsechna okna
    for i in range(windows):
        # Returns byte data
        raw_data = wav.readframes(sampling_frequency)  # Returns byte data
        fmt = str(sampling_frequency * num_channels) + "h"
        integer_data = struct.unpack(fmt, raw_data)
        integer_data = np.array(integer_data)
        #print(integer_data)

        # prevod stereo na mono
        if (num_channels == 2):
            integer_data1 = []
            for i in range(0, len(integer_data), 2):
                integer_data1.append((integer_data[i] + integer_data[i + 1]) / 2)
            integer_data = integer_data1

        #prumer
        fft_data = (np.fft.rfft(integer_data) / sampling_frequency)

        #prevod na absoultni hodnoty
        fft_data = np.abs(fft_data)

        #vypocet prumeru
        avg = sum(fft_data)/len(fft_data)
        peak = 20*avg

        #print(peak)
        #print(fft_data)
        max_actual = -1
        min_actual = -1
        for j in range(len(fft_data)):
            #porovnani amplitudy s prumerem
            if fft_data[j] > peak:
                #frekvence min peaku v okne (osa x)
                if min_actual == -1:
                    min_actual = j
                #frekvence max peaku v okne (osa x)
                if max_actual < j:
                    max_actual = j


        #print("max_in window", max_actual)
        #print("min_in window", min_actual)
        #kontrola globalniho min a max
        if min == -1:
            min = min_actual
        if min > min_actual:
            min = min_actual
        if max < max_actual:
            max = max_actual


    if not (max == -1):
        print("low:", min, "high:", max)
    else:
        print("no peaks")

    wav.close()


main()