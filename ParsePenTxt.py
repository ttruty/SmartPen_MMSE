"""
This loads in the txt converted from the PCG file downloaded from anoto
The PCG is converted to text using ps script ExtractTxtFromPcg

the format of the file is:
Pen id: AJX-AAP-J76-5G
Number of pages: 1
Page address: 150.846.10.15#0
Page bounds: 0 0 9998 9998
Number of strokes: 14
StrokeID: 1
Number of samples: 12
Color: 41 0 139
StartTime: 1511793607.823
673.0000 33.0000 0 0
672.6250 32.7500 26 0
672.5000 32.7500 14 20
672.5000 33.1250 13 50
672.5000 33.7500 13 62
672.5000 36.1250 14 70
672.6250 39.1250 13 74
672.8750 42.2500 13 76
674.3750 46.0000 40 78
679.3750 39.6250 40 86
685.5000 31.5000 14 82
692.6250 24.0000 13 56
StrokeID: 2
Number of samples: 8
Color: 41 0 139
StartTime: 1511793611.666
224.7500 210.2500 0 0
225.1250 210.1250 13 16
224.7500 211.0000 27 62
222.5000 221.3750 26 74
221.2500 229.8750 14 78
221.1250 241.8750 26 84
221.5000 242.7500 14 66
222.3750 242.1250 13 0
...
"""

import pandas as pd
import re
import os
from collections import OrderedDict
from itertools import groupby
from operator import itemgetter
import matplotlib.pyplot as plt
from matplotlib import transforms
# from datetime import datetime, timedelta
import time
import math


# file = r'C:\Users\KinectProcessing\Documents\Anoto\Anotopgc\150.846.10.15_Anoto Forms ' \
#        r'Solution_27_11_2017_08.40.26.739.txt '
regex_sample_data = re.compile('\d+\.\d+\s\d+\.\d+\s\d+\s\d+')

# matplotlib defs
fig = plt.figure()

def rotation(rotation_degree):
    rot = transforms.Affine2D().rotate_deg(rotation_degree) # make sure this matches in GUI
    return rot


def readfile(txt_file):
    """
    read the raw txt_file and output that data as a list of lines
    :param txt_file:
    :return data:
    """
    with open(txt_file) as textile:
        # read each line of the raw data file .csk
        data = textile.readlines()
        data = [x.rstrip('\n') for x in data]
        return data


def stroke_samples(data):
    """
    parse each line in the txt and add to df
    returns a list of  stokes samples [stroke count, [sample x, sample y, timing info, force]
    :param data:
    :return sample_list, start_time:
    """
    start_time = {}
    sample_list = []
    stroke_count = 0
    for i in data:

        found_sample = regex_sample_data.findall(i)

        if "Stroke" in i:
            regex_num = re.compile('\d+')  # find the stroke number
            stroke_num = regex_num.findall(i)  # unused for now but cant be used later
            stroke_count += 1

        if "StartTime" in i:
            s_time = float(i.split()[1])
            start_time[stroke_count] = s_time

        if found_sample:
            for k in found_sample:
                line = []
                sp = k.split()
                sp = [float(x) for x in sp]
                # print(sp)
                line.append(stroke_count)
                line.append(sp)
                sample_list.append(line)
    return sample_list, start_time


def create_df(stroke_data, time_data, rotation_degree):
    """
    creates a dataframe from the list stroke data and time info
    :param stroke_data:
    :param time_data:
    :param rotation_degree:
    :return: figure
    :return: full df
    """
    base = plt.gca().transData

    # print(time_data)
    single_strokes = [[y for x, y in g] for k, g in groupby(stroke_data, key=itemgetter(0))]

    full_stroke_df = pd.DataFrame()

    # individual stroke plot and data frame
    for i in single_strokes:
        full_stroke_df = full_stroke_df.append([[i]], ignore_index=True)
        one_stroke_df = pd.DataFrame(i, columns=['x', 'y', 'time', 'force'])
        one_stroke_df = one_stroke_df.apply(pd.to_numeric, errors='ignore')
        rot = rotation(rotation_degree)
        plt.plot(one_stroke_df['y'], one_stroke_df['x'], color='b', linestyle='-', picker=True, transform=rot+base)

    plt.axis('off')
    # print(list(time_data.values()))
    full_stroke_df['StartTimes'] = list(time_data.values())
    full_stroke_df['DateTime'] = [time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(i)) for i in list(time_data.values())]
    full_stroke_df = full_stroke_df.apply(pd.to_numeric, errors='ignore')
    full_stroke_df.columns = ['data', 'StartTimes', 'DateTime']
    return fig, full_stroke_df


def make_fig(file, rotation_degree):
    raw_data = readfile(file)
    strokes, times = stroke_samples(raw_data)
    figure, df = create_df(strokes, times, rotation_degree)
    #print(df)
    return figure, df
