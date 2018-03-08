import matplotlib
import numpy as np
import pandas as pd
from numpy import arange, sin, pi
import math
import csv
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import os
from datetime import datetime
import sys
import ParsePenTxt as graph
import matplotlib.pyplot as plt
from matplotlib import transforms
matplotlib.use('TkAgg')

class MainGui:
    def __init__(self, master):
        self.master = master
        master.wm_title("Digital MMSE Processing")
        icon = resource_path("penticon.ico")
        master.wm_iconbitmap(icon)

        # list variables
        self.strokes_var = StringVar()
        self.pent_var = StringVar()
        self.stroke_selected = []
        self.rotation_degree = 90
        self.rot = transforms.Affine2D().rotate_deg(self.rotation_degree)

        self.widget = None

        # frames
        self.menu_left = Frame(self.master, width=150, bg="#ababab")
        self.menu_left_upper = Frame(self.menu_left, width=150, height=150)
        self.menu_left_lower = Frame(self.menu_left, width=150, )
        self.button_frame = Frame(self.menu_left_lower)

        self.menu_right = Frame(self.master, width=150, bg="#ababab")
        self.menu_right_top = Frame(self.menu_right, width=150, height=100)
        self.menu_right_middle = Frame(self.menu_right, width=150, height=100 )
        self.menu_right_bottom = Frame(self.menu_right, width=150, height=100 )
        self.canvas_frame = Frame(self.master, width=600, height=400)

        # left menus
        self.left_label = Label(self.menu_left_upper, text="Unsorted Strokes")
        self.left_label.pack()

        self.stroke_listbox = Listbox(self.menu_left_upper, selectmode='multiple')
        self.stroke_listbox.pack()
        self.stroke_listbox.bind('<<ListboxSelect>>', self.onselect)

        # self.stroke_listbox = Listbox(self.menu_left_lower)
        # self.stroke_listbox.pack()

        # buttons
        self.select_file = Button(self.button_frame, text="Select an image", command=self.select_image)
        self.select_file.pack(fill=X)
        self.button_frame.pack(side='left')

        self.move2pent = Button(self.button_frame, text='Move to Pentagon', command=self.move_to_pent)
        self.move2pent.pack(fill=X)
        self.button_frame.pack(side='left')

        self.move2sentence = Button(self.button_frame, text='Move to Sentence', command=self.move_to_sentence)
        self.move2sentence.pack(fill=X)
        self.button_frame.pack(side='left')

        self.move2pent = Button(self.button_frame, text='Move to RA Data', command=self.move_to_ra)
        self.move2pent.pack(fill=X)
        self.button_frame.pack(side='left')

        self.reset_button = Button(self.button_frame, text='Reset Strokes', command=self.reset)
        self.reset_button.pack(fill=X)
        self.button_frame.pack(side='left')

        self.rotate_button = Button(self.button_frame, text='Rotate', command=self.rotate)
        self.rotate_button.pack(fill=X)
        self.button_frame.pack(side='left')

        self.quit_button = Button(self.button_frame, text='Quit', command=self._quit)
        self.quit_button.pack(fill=X)
        self.button_frame.pack(side='left')

        self.save_button = Button(self.button_frame, text='Save', command=self.save)
        self.save_button.pack(fill=X)
        self.button_frame.pack(side='left')

        self.menu_left_upper.pack(side="top", fill="both", expand=True)
        self.menu_left_lower.pack(side="top", fill="both", expand=True)

        # right area
        self.menu_right_top.pack(side="top", fill="both", expand=True)
        self.menu_right_middle.pack(side="top", fill="both", expand=True)
        self.menu_right_bottom.pack(side="top", fill="both", expand=True)

        self.pentagon_label = Label(self.menu_right_top, text="Pentagon Strokes")
        self.pentagon_label.pack()
        self.pent_listbox = Listbox(self.menu_right_top, selectmode='multiple')
        self.stroke_listbox.bind('<<ListboxSelect>>', self.onselect)
        self.pent_listbox.pack()

        self.sentence_label = Label(self.menu_right_middle, text="Sentence Strokes")
        self.sentence_label.pack()
        self.sentence_listbox = Listbox(self.menu_right_middle, selectmode='multiple')
        self.sentence_listbox.pack()

        self.ra_label = Label(self.menu_right_bottom, text="RA Data Strokes")
        self.ra_label.pack()
        self.ra_listbox = Listbox(self.menu_right_bottom, selectmode='multiple')
        self.ra_listbox.pack()

        self.some_title_frame = Frame(self.master, bg="#dfdfdf")
        self.file_label = Label(self.some_title_frame, text="Select a file", bg="#dfdfdf")
        self.file_label.pack()

        # status bar
        self.status_frame = Frame(self.master, height=100)
        self.projID_info = Entry(self.status_frame)
        self.proj_label = Label(self.status_frame, text="Enter Project ID")

        self.staff_info = Entry(self.status_frame)
        self.staff_label = Label(self.status_frame, text="Enter Staff ID")

        self.proj_label.grid(row=0, column=0, columnspan=1, sticky="sw", padx=5)
        self.projID_info.grid(row=0, column=2, columnspan=1, sticky="sw", padx=5)

        self.staff_label.grid(row=0, column=3, columnspan=1, sticky="s", padx=5)
        self.staff_info.grid(row=0, column=4, columnspan=1, sticky="s", padx=5)

        # place gui on frames
        self.menu_left.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.menu_right.grid(row=0, column=3, rowspan=4, sticky="ne")
        self.some_title_frame.grid(row=0, column=1, sticky="ew")
        self.status_frame.grid(row=3, column=0, columnspan=4, sticky="sw")
        self.canvas_frame.grid(row=1, column=1, columnspan=2, sticky="ew")

        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(1, weight=1)


    def rotate(self):
        """callback from the rotate button, rotates the canvase 90 degress and resets"""
        self.reset()
        if self.rotation_degree < 360:
            self.rotation_degree += 90
        else:
            self.rotation_degree = 90

        self.rot = transforms.Affine2D().rotate_deg(self.rotation_degree)
        self.make_canvas(self.path)
        # self.make_canvas(self.path)
        # print(self.rotation_degree)

    def make_canvas(self, filename):
        """shapes and draws the canvas on the scene, remeber to clear using f.clf for cleaner
        look when changing stroke color"""
        self.base = plt.gca().transData

        self.stroke_listbox.delete(0, END)

        if self.widget:
            self.widget.destroy()
            self.widget = None
        try:
            self.f.clf()  # cleans the canvas
        except AttributeError as e:
            print(e)
        self.f, self.stroke_data = graph.make_fig(filename, self.rotation_degree)  # r'C:\Users\KinectProcessing\Documents\Anoto\Anotopgc\150.846.10.15_Anoto Forms Solution_27_11_2017_08.40.26.739.txt')
        self.load_strokes()

        # DrawingArea
        self.canvas = FigureCanvasTkAgg(self.f, self.canvas_frame)
        # self.canvas.show()
        self.widget = self.canvas.get_tk_widget()

        # tool bar // causes an padding issues in canvas
        # self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.canvas_frame)
        # self.toolbar.update()
        # #self.canvas._tkcanvas.grid(row=2, column=1)
        # self.widget.pack(side=TOP, fill=BOTH,  expand=0)

        # pick events
        self.canvas.mpl_connect('key_press_event', self.on_key_event)
        self.f.canvas.mpl_connect('pick_event', self.onpick_stroke)
        self.widget.pack(fill=BOTH)


    def onselect(self, event):
        # Note here that Tkinter passes an event object to onselect()
        self.base = plt.gca().transData

        #w = event.widget
        #index = w.curselection()
        # print(index)

        # self.reset()

        if self.stroke_listbox.curselection() == ():
            return

        # get tuple of selected indices
        selection = self.stroke_listbox.curselection()
        # print(selection)

        full_stroke_list = self.stroke_listbox.get(0, END)
        # print(full_stroke_list)
        # merge w/o duplicates
        result_index = sorted(list(set(selection)))
        #print(result_index)
        result_list = [full_stroke_list[i] for i in result_index]
        neg_list = [i for i in full_stroke_list if i not in result_list]
        # print(result_list)
        # print(neg_list)
        for i in neg_list:
            stroke_index = int(i[1]) - 1
            unchosen_strokes = (self.stroke_data.iloc[stroke_index]['data'])
            ydata = [x[0] for x in unchosen_strokes]
            xdata = [x[1] for x in unchosen_strokes]
            plt.plot(xdata, ydata, '-', color="b", linewidth=1, transform=self.rot + self.base)

        for i in result_list:
            stroke_index = int(i[1]) - 1
            chosen_strokes = (self.stroke_data.iloc[stroke_index]['data'])
            ydata = [x[0] for x in chosen_strokes]
            xdata = [x[1] for x in chosen_strokes]
            plt.plot(xdata, ydata, '-', color="g", linewidth=4, transform=self.rot + self.base)
        self.f.canvas.draw()

    def move_to_pent(self, only_one_item=False):
        """Moves the selected strokes to the pent bin"""
        if self.stroke_listbox.curselection() == ():
            return

        # get tuple of selected indices
        selection = self.stroke_listbox.curselection()
        self.make_selection(selection, self.pent_listbox, "red") # shows the stroke as red when moved

    def move_to_sentence(self, only_one_item=False):

        if self.stroke_listbox.curselection() == ():
            return

        selection = self.stroke_listbox.curselection()
        # get tuple of selected indices
        self.make_selection(selection, self.sentence_listbox, "red")

    def move_to_ra(self, only_one_item=False):

        if self.stroke_listbox.curselection() == ():
            return

        selection = self.stroke_listbox.curselection()
        # get tuple of selected indices
        self.make_selection(selection, self.ra_listbox, "red")

    def make_selection(self, selection, move_to, color):
        full_stroke_list = self.stroke_listbox.get(0, END)

        # merge w/o duplicates
        result_index = sorted(list(set(selection)))
        # print(result_index)
        result_list = [full_stroke_list[i] for i in result_index]
        unsorted = [i for j, i in enumerate(full_stroke_list) if j not in result_index]

        self.stroke_listbox.delete(0, END)  # clear listbox
        self.stroke_listbox.insert(END, *unsorted)
        move_to.insert(END, *result_list)

        for i in result_list:
            stroke_index = int(i[1]) - 1
            pentagon_strokes = (self.stroke_data.iloc[stroke_index]['data'])
            ydata = [x[0] for x in pentagon_strokes]
            xdata = [x[1] for x in pentagon_strokes]
            plt.plot(xdata, ydata, '-', color=color, transform=self.rot + self.base)
        self.f.canvas.draw()


    def load_strokes(self):
        stroke_number = 0
        strokes = []

        for i in (self.stroke_data['data']):
            self.stroke_listbox.insert(END, ("Stroke", str(stroke_number + 1)))
            strokes.append((stroke_number + 1))
            stroke_number += 1
        # print(strokes)

    def on_key_event(self, event):
        # print('you pressed %s' % event.key)
        key_press_handler(event, self.canvas) #(event, canvas, toolbar=None)

    def onpick_stroke(self, event):
        self.base = plt.gca().transData
        ind = event.ind

        line = event.artist
        xdata, ydata = line.get_data()
        select_location = np.array([xdata[ind], ydata[ind]]).T

        # print('Stroke: ', ind)
        # print('on pick line:', select_location)

        match_x = float(select_location[0][0])
        match_y = float(select_location[0][1])
        # print("Location", match_x, match_y)
        count = 0

        for i in (self.stroke_data['data']):
            # this finds which stroke is clicked on needs work
            for sublist in i:
                if sublist[1] == match_x and sublist[0] == match_y:
                    # print("Found it!", sublist)
                    # print("Found in stroke", str(count + 1))
                    self.pick_stroke(count)
                    self.stroke_selected.append(count)
                    # print(xdata, ydata)
                    plt.gca()
                    plt.plot(xdata, ydata, 'r', linewidth=5, transform=self.rot + self.base)
                    self.f.canvas.draw()
                    break
            count += 1


        for i in self.stroke_selected:
            self.stroke_listbox.selection_set(i)

    def pick_stroke(self, stroke_number):
        self.stroke_listbox.selection_clear(0, END)
        self.stroke_listbox.selection_set(stroke_number)
        # print(self.stroke_data.iloc[stroke_number])

    def reset(self):
        try:
            self.stroke_selected = []
            self.reset_canvas()

            stroke_number = 0
            strokes = []

            self.stroke_listbox.delete(0, END)  # clear listbox
            self.pent_listbox.delete(0, END)  # clear listbox
            self.sentence_listbox.delete(0, END)  # clear listbox
            self.ra_listbox.delete(0, END)  # clear listbox

            for i in (self.stroke_data['data']):
                self.stroke_listbox.insert(END, ("Stroke", str(stroke_number + 1)))
                strokes.append((stroke_number + 1))
                stroke_number += 1
                # print(strokes)
        except AttributeError as e:
            print(e)

    def reset_canvas(self):
        try:
            # self.canvas.get_tk_widget().delete("all")
            self.f.clf()
            if self.widget:
                self.widget.destroy()
            self.make_canvas(self.path)
        except AttributeError as e:
            print(e)

    def distance(self, p0, p1):
        return math.sqrt((p0[0] - p1[0]) ** 2 + (p0[1] - p1[1]) ** 2)

    def calc_stroke_dist(self, coordinate_list):
        total_distance = 0
        for i in range(len(coordinate_list)):
            if i < len(coordinate_list) - 1:
                # print(coordinate_list[i])
                dist = self.distance(coordinate_list[i], coordinate_list[i+1])
                total_distance += dist
        return total_distance

    def select_image(self):
        if self.widget:
            self.widget.destroy()
        self.path = filedialog.askopenfilename()
        # ensure a file path was selected
        if len(self.path) > 0:
            file_name = os.path.basename(self.path)
            self.file_label['text'] = file_name
            self.projID_info.delete(0, 'end')
            self.reset()
            self.make_canvas(self.path)

    def save(self):
        print(self.stroke_listbox)
        if self.projID_info.get() == "":
            self.projID_info.config(background="red")
            messagebox.showinfo("Error", "Please enter a valid project ID")
            self.projID_info.config(background="white")
            return


        new_df = self.stroke_data
        # print(self.stroke_data)
        sorted_pent_list = self.pent_listbox.get(0, END)
        sorted_sent_list = self.sentence_listbox.get(0, END)
        sorted_ra_list = self.ra_listbox.get(0, END)

        # print(sorted_pent_list)
        for i in sorted_pent_list:
            # print(i)
            total_time = 0
            sample_points = []
            force = []
            df_index_of_stroke = int(i[1]) - 1
            new_df.loc[df_index_of_stroke, "label"] = 'Pentagon'
            data = self.stroke_data['data'].loc[df_index_of_stroke]
            for j in data:
                total_time += j[2]
                sample_points.append((j[0], j[1]))
                force.append(j[3])

            new_df.loc[df_index_of_stroke, "Stroke Time"] = total_time
            new_df.loc[df_index_of_stroke, "Number of Samples"] = len(data)

            new_df.at[df_index_of_stroke, "Points"] = 0
            new_df["Points"] = new_df["Points"].astype(object)
            new_df.at[df_index_of_stroke, "Points"] = sample_points

            new_df.at[df_index_of_stroke, "Force"] = 0
            new_df["Force"] = new_df["Force"].astype(object)
            new_df.at[df_index_of_stroke, "Force"] = force

            # fig1 = plt.figure()
            # ax1 = fig1.add_subplot(111)
            # ax1.plot(force)
            new_df.at[df_index_of_stroke, "Stroke Distance"] = \
                self.calc_stroke_dist(new_df.at[df_index_of_stroke, "Points"])

        # print(sorted_sent_list)
        for i in sorted_sent_list:
            total_time = 0
            sample_points = []
            force = []
            df_index_of_stroke = int(i[1]) - 1
            new_df.loc[df_index_of_stroke, "label"] = 'Sentence'
            data = self.stroke_data['data'].loc[df_index_of_stroke]
            for j in data:
                total_time += j[2]
                sample_points.append((j[0], j[1]))
                force.append(j[3])
            new_df.loc[df_index_of_stroke, "Stroke Time"] = total_time
            new_df.loc[df_index_of_stroke, "Number of Samples"] = len(data)

            new_df.at[df_index_of_stroke, "Points"] = 0
            new_df["Points"] = new_df["Points"].astype(object)
            new_df.at[df_index_of_stroke, "Points"] = sample_points

            new_df.at[df_index_of_stroke, "Force"] = 0
            new_df["Force"] = new_df["Force"].astype(object)
            new_df.at[df_index_of_stroke, "Force"] = force

            # fig1 = plt.figure()
            # ax1 = fig1.add_subplot(111)
            # ax1.plot(force)
            # fig1.savefig('stroke_force' + str(i))

            new_df.at[df_index_of_stroke, "Stroke Distance"] = self.calc_stroke_dist(
                new_df.at[df_index_of_stroke, "Points"])

        # print(sorted_ra_list)
        for i in sorted_ra_list:
            total_time = 0
            sample_points = []
            force = []
            df_index_of_stroke = int(i[1]) - 1
            new_df.loc[df_index_of_stroke, "label"] = 'Ra_Data'
            data = self.stroke_data['data'].loc[df_index_of_stroke]
            for j in data:
                total_time += j[2]
                force.append(j[3])
                sample_points.append((j[0], j[1]))
            new_df.loc[df_index_of_stroke, "Stroke Time"] = total_time
            new_df.loc[df_index_of_stroke, "Number of Samples"] = len(data)

            new_df.at[df_index_of_stroke, "Points"] = 0
            new_df["Points"] = new_df["Points"].astype(object)
            new_df.at[df_index_of_stroke, "Points"] = sample_points

            new_df.at[df_index_of_stroke, "Force"] = 0
            new_df["Force"] = new_df["Force"].astype(object)
            new_df.at[df_index_of_stroke, "Force"] = force
            #
            # fig1 = plt.figure()
            # ax1 = fig1.add_subplot(111)
            # ax1.plot(force)
            # fig1.savefig('stroke_force' + str(i))

            new_df.at[df_index_of_stroke, "Stroke Distance"] = self.calc_stroke_dist(
                new_df.at[df_index_of_stroke, "Points"])

        # print(new_df)
        starttime = self.stroke_data['DateTime'][0]
        t = datetime.strptime(starttime, "%a, %d %b %Y %H:%M:%S")
        t = t.strftime("%Y%m%d-%H%M%S")
        outfile = self.projID_info.get() + "_" + t + "_mmse.csv"
        #output = os.path.join(r'C:\Users\KinectProcessing\Documents\Anoto\mmse_output', outfile)
        save_path = os.getcwd()
        save_path = save_path + r'\MMSE_output'
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        output = (os.path.join(save_path, outfile))

        try:
            os.remove(output)
        except OSError:
            pass

        with open(output, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Proj ID", "=\"" + self.projID_info.get() + "\""])
            writer.writerow(["Filename", self.file_label['text']])
            writer.writerow(["Starttime", starttime])
            writer.writerow(["Process Time", str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))])
            writer.writerow(["Staff ID", self.staff_info.get()])
            writer.writerow(" ")

            new_df.to_csv(f)

    def _quit(self):
        root.quit()     # stops mainloop
        root.destroy()  # this is necessary on Windows to prevent Fatal Python Errorgg: PyEval_RestoreThread:NULL tstate


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

root = Tk()
my_gui = MainGui(root)
root.mainloop()

