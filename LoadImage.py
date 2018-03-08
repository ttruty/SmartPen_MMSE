#! python 3.5
'''
    plots the data from the clock sketch raw data
'''
import re
import os
import matplotlib.pyplot as plt
import math

regex = re.compile('\d+\.\d+\s\d+\.\d+\s\d+\s\d+')

start_time = []

fig = plt.figure()

def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy


def open_penfile(pen_file):
    with open(pen_file) as myfile:
        # read each line of the raw data file .csk
        coords = myfile.readlines()
        return coords


def make_unscored_list(path):
    new_list = []
    for root, dirs, files in os.walk(path):
        file_list = files
        for file in file_list:
            if file.endswith(".txt"):
                new_list.append(file)
    return new_list

def draw_stroke(stroke_x, stroke_y):
    ##  plt.scatter(x,y, 0.1)
    plt.plot(stroke_x, stroke_y, color='b', linestyle='-', picker=True)
    # fig = plt.gcf()

def plot_clock(path):
    ''' this plots clock from raw data
    usage: plot_clock(path)
    '''
    #fig = plt.figure()
    coord_list = []
    # clockfile_list = make_unscored_list(path)
    stroke_count = 0
    # for file in clockfile_list:
    penfile = os.path.join(path)
    coords = open_penfile(penfile)
    for i in coords:
        find = regex.findall(i)
        if "Stroke" in i:
            regex_num = re.compile('\d+')
            stroke_num = regex_num.findall(i)
            stroke_count += 1

        if "StartTime" in i:
            time = float(i.split()[1])
            start_time.append(time)
        if find != []:
            for k in find:
                cur_line = []
                # print(k)
                sp = k.split()
                # print(sp)
                cur_line.append(stroke_count)
                cur_line.append(sp)
                coord_list.append(cur_line)

    for i in range(coord_list[-1][0]):
        # deal with the individual stroke samples
        stroke = []
        print('Stroke start time = ', start_time[i])
        for j in range(len(coord_list)):
            if coord_list[j][0] == i + 1:
                stroke.append(coord_list[j])
        strkX = []
        strkY = []
        for k in stroke:

            # print(k)
            # structure of data is [stroke#, [x,y, time added to start time, pressure]]
            point = (float(k[1][0]), float(k[1][1]))
            # rotate around ordine counter clockwise 90%
            origin = (0, 0)
            angle = math.radians(0)  # 270 for the clock
            stroke_x, stroke_y = rotate(origin, point, angle)
            strkX.append(stroke_x)
            strkY.append(stroke_y)
        draw_stroke(strkX, strkY)

        # plt.pause(0.05)

    # currentAxis.add_patch(Rectangle((450,-200), 450, 200, fill=False))
    plt.axis('off')
    currentAxis = plt.gca()
    currentAxis.invert_yaxis()
    #plt.show()
    #digits = classify_digits.recog(save_file)

    return fig
    # plt.waitforbuttonpress()


# plt.show()

def make_fig(filename):
    figure = plot_clock(filename)
    return figure

