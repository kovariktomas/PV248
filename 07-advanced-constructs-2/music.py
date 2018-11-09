import sys
import numpy as np
import wave
import struct
from math import log2, pow

def frequency_to_pitch(f, a1):
    #Zdrojpro vypocet: https://www.johndcook.com/blog/2013/06/22/how-to-convert-frequency-to-pitch/
    #pro vypocet si ze zadaneho a' nejprve spocitam middle c
    middleC = a1 * pow(2, (-21 / 12)) * 2
    h = 12 * log2(f / middleC) / log2(2)

    octave_index = int(h // 12) + 1
    pitch_index = int(h % 12)
    cents = (h % 1)
    cents = int(cents * 100)
    #prevod abych zobrazoval vždy nejbližší pitch name a co nejmene centu
    if cents >= 50:
        pitch_index += 1
        cents = 100 - cents
    #pohyb mezi octaves(mám 12 pitches)
    if pitch_index >= 12:
        pitch_index -= 12
        octave_index += 1
    #Nazvy pitches
    pitches = ['c', 'cis', 'd', 'es', 'e', 'f', 'fis', 'g', 'gis', 'a', 'bes', 'b']

    pitch = pitches[pitch_index]
    octave_char = "’"
    if octave_index < 0:
        pitch = pitch.capitalize()
        octave_char = ","

    if octave_index < 0:
        octave_index +=1
    octave_char_cnt = np.abs(octave_index)

    for i in range(octave_char_cnt):
        pitch = pitch + octave_char

    return str(pitch), str(cents)

# hodnoty na vstupu sign
def main():
    # otevreni souboru
    a1 = float(sys.argv[1])
    filename = sys.argv[2]
    wav = wave.open(filename, 'r')

    # MONO = 1 STEREO = 2
    # wav.getnchannels()
    # print("pocet kanalu: ", wav.getnchannels())
    num_channels = wav.getnchannels()

    # sampling frequency
    # print("vzorkovaci frekvence", wav.getframerate())
    sampling_frequency = wav.getframerate()

    # nframes
    # print("pocet vzorku:", wav.getnframes())
    num_frames = wav.getnframes()

    #precti vsechna data ze souboru
    # Returns byte data
    raw_data = wav.readframes(num_frames)  # Returns byte data
    fmt = str(num_frames*num_channels) + "h"
    integer_data = struct.unpack(fmt, raw_data)
    integer_data = np.array(integer_data)
    # print(integer_data)

    # prevod celeho souboru ze stereo na mono
    if (num_channels == 2):
        integer_data1 = []
        for i in range(0, len(integer_data), 2):
            integer_data1.append((integer_data[i] + integer_data[i + 1]) / 2)
        integer_data = integer_data1

    # okno ma byt posuvne po 0.1s
    # pocet oken
    windows = num_frames // sampling_frequency
    # print(windows)

    Min = -1
    Max = -1
    window_step = sampling_frequency // 10
    maxs_in_windows = []
    # cyklus pres vsechna okna po .1 sekundach a nalezeni trech maxim
    for i in range(0, (len(integer_data)-sampling_frequency), window_step):
        window_start = i
        window_end = sampling_frequency+i
        #print ("from", window_start, "to", window_end)

        # fft
        fft_data = np.fft.rfft(integer_data[window_start:window_end])

        # prevod na absoultni hodnoty
        fft_data = np.abs(fft_data)

        # vypocet prumeru
        avg = sum(fft_data) / len(fft_data)
        peak = 20 * avg

        # print(peak)
        # print(fft_data)
        fft_data1 = []
        for i in range(len(fft_data)):
            if fft_data[i]>peak:
                fft_data1.append(fft_data[i])
            else:
                fft_data1.append(0)
        clusters = []

        for i in range(1, len(fft_data1)):
            if (fft_data1[i-1]>fft_data1[i]):
                if clusters[-1]==0:
                    clusters.append(fft_data1[i-1])
                else:
                    clusters.append(0)
            else:
                clusters.append(0)

        max1 = 0
        max2 = 0
        max3 = 0
        max1_i = 0
        max2_i = 0
        max3_i = 0

        for i in range(len(clusters)):
            if clusters[i] > max1:
                max3 = max2
                max1, max2 = clusters[i], max1
                max3_i = max2_i
                max1_i, max2_i = i, max1_i
            elif clusters[i] > max2:
                max2, max3 = clusters[i], max2
                max2_i, max3_i = i, max2_i
            elif clusters[i] > max3:
                max3 = clusters[i]
                max3_i = i

        maxs_inwindow = [max1_i,  max2_i, max3_i]
        maxs_inwindow.sort()
        maxs_in_windows.append(maxs_inwindow)

    #print(maxs_in_windows)
    #sjednoceni stejnych tonu v jednom okne
    started = False
    pitches_in_windows = []
    for i in range(len(maxs_in_windows)):
        clustering_pitches = {}

        for j in range(3):
            if maxs_in_windows[i][j] != 0:
                pitch, tone = frequency_to_pitch(maxs_in_windows[i][j], a1)
                if not pitch in clustering_pitches:
                    clustering_pitches[pitch] = tone
                else:
                    if clustering_pitches[pitch] < tone:
                        clustering_pitches[pitch] = tone

        pitches_in_windows.append(clustering_pitches)

    #print (pitches_in_windows)
    # vypis intervalu a formatovani tonu
    # + sjednoceni stejnych tonu v sousednich oknech
    for i in range(len(maxs_in_windows)):
        prints = {}
        if started == False:
            print("{0:.2f}".format(0.1*i), "-", sep='', end='')
            started = True
        else:
            if len(pitches_in_windows[i-1]) == len(pitches_in_windows[i]):
                contains_all = True
                for k, v in pitches_in_windows[i-1].items():
                    if not (k in pitches_in_windows[i]):
                        contains_all = False

                if contains_all:
                    for k, v in pitches_in_windows[i - 1].items():
                        if (k in pitches_in_windows[i]):
                            pitches_in_windows[i][k] = max(v, pitches_in_windows[i][k])
                else:
                    # dokoncit tisk radku a zacit znovu
                    started = False
                    print("{0:.2f}".format(0.1 * (i+1)), sep='', end=' ')
                    if len(pitches_in_windows[i - 1])==0:
                        print("no peaks")
                    else:
                        for k, v in pitches_in_windows[i - 1].items():
                            print(k, "+", v, sep='', end=' ')
                    print("\n", sep='', end='')

            else:
                # dokoncit tisk radku a zacit znovu
                started = False
                print("{0:.2f}".format(0.1 * (i + 1)), sep='', end=' ')
                if len(pitches_in_windows[i - 1]) == 0:
                    print("no peaks")
                else:
                    for k, v in pitches_in_windows[i - 1].items():
                        print(k, "+", v, sep='', end=' ')
                print("\n", sep='', end='')

    if started:
        print("{0:.2f}".format(0.1 * (i + 1)), sep='', end=' ')
        if len(pitches_in_windows[i - 1]) == 0:
            print("no peaks")
        else:
            for k, v in pitches_in_windows[i - 1].items():
                print(k, "+", v, sep='', end=' ')
        print("\n", sep='', end='')

    wav.close()

main()
