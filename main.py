from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from Arduino import ArduinoControl
import serial
import subprocess
from subprocess import PIPE
import time
import os
from plot_helper import *
import configparser
from stopwatch import StopWatch
from threading import Thread

window = Tk()
window.title("FlyVR")
try:
    window.iconbitmap("C:\\Users\\YLab\\Documents\\FlyVR\\fly-shape.ico")
except:
    pass
window.geometry("600x800")

tab_control = ttk.Notebook(window)
tab_record = ttk.Frame(tab_control)
tab_analysis = ttk.Frame(tab_control)
tab_control.add(tab_record, text="Record")
tab_control.add(tab_analysis, text="Analysis")


def isProperFile(path, filetype):
    """
    Checks if the file is the file type wanted, pop up an error message if no
    :param path: the path of the file
    :param filetype: the file type wanted
    :return: True if the path is correct, False otherwise
    """
    l = len(filetype)
    if (type(path) == str) and (path[-l:] == filetype):
        return True
    else:
        messagebox.showerror("Error", "The selected file "+path+"\nis illegal."+"\n."+filetype+" file required")
        return False


FicTrac_path_string = StringVar()
FicTrac_path_string.set("C:/Users/YLab/Documents/FlyVR/FicTracWin64/FicTrac-PGR.exe")  # Comment this
FicTrac_configPath_string = StringVar()
FicTrac_configPath_string.set("C:/Users/YLab/Documents/FlyVR/FicTracWin64/setup-test/config.txt")


def setFicTracPath():
    """
    Function to open a file chooser and browse a file
    """
    path = filedialog.askopenfilename(title="Set FicTrac Path", filetypes=(("Programs", "*.exe"), ("All files", "*.*")))
    if path != "":
        FicTrac_path_string.set(path)


def setFicTracState(*args):
    """
    Enable or disable FicTrac according to FicTrac_state
    """
    if FicTrac_state.get():
        FicTrac_path_text.config(state=NORMAL)
        FicTrac_path_button.config(state=NORMAL)
        FicTrac_configPath_text.config(state=NORMAL)
        FicTrac_configPath_button.config(state=NORMAL)
        FicTrac_configOpen_button.config(state=NORMAL)
    else:
        FicTrac_path_text.config(state=DISABLED)
        FicTrac_path_button.config(state=DISABLED)
        FicTrac_configPath_text.config(state=DISABLED)
        FicTrac_configPath_button.config(state=DISABLED)
        FicTrac_configOpen_button.config(state=DISABLED)


def setFicTracConfigPath(*args):
    """
    Function to open a file chooser and browse a file
    """
    path = filedialog.askopenfilename(title="Set FicTrac Configuration Path",
                                      filetypes=(("Text documents", "*.txt"), ("All files", "*.*")))
    if path != "":
        FicTrac_configPath_string.set(path)


def openFicTracConfig(*args):
    """
    Open the FicTrac config file,
    Require a text file, otherwise popup an error
    """
    if isProperFile(FicTrac_configPath_string.get(), "txt"):
        subprocess.Popen(["notepad", FicTrac_configPath_string.get()], shell=True)


FicTrac_state = BooleanVar()
FicTrac_state.set(True)  # Initialized as true
FicTrac_state.trace("w", setFicTracState)

labelframe_FicTrac = LabelFrame(tab_record, text="FicTrac")
labelframe_FicTrac.pack(fill="both", expand="no")

FicTrac_frame_1 = Frame(labelframe_FicTrac)
FicTrac_frame_1.pack(fill=X)
FicTrac_state_box = ttk.Checkbutton(FicTrac_frame_1, text="Enable FicTrac", var=FicTrac_state)
FicTrac_state_box.grid(column=0, row=0, padx=5)

FicTrac_frame_2 = Frame(labelframe_FicTrac)
FicTrac_frame_2.pack(fill=X)
FicTrac_path_label = Label(FicTrac_frame_2, text="FicTrac path", width=15)
FicTrac_path_label.grid(column=0, row=1)
FicTrac_path_text = ttk.Entry(FicTrac_frame_2, width=50, textvariable=FicTrac_path_string)
FicTrac_path_text.grid(column=1, row=1)
FicTrac_path_button = ttk.Button(FicTrac_frame_2, text="Browse..", command=setFicTracPath)
FicTrac_path_button.grid(column=2, row=1)

FicTrac_configPath_label = Label(FicTrac_frame_2, text="Config path", width=15)
FicTrac_configPath_label.grid(column=0, row=2)
FicTrac_configPath_text = ttk.Entry(FicTrac_frame_2, width=50, textvariable=FicTrac_configPath_string)
FicTrac_configPath_text.grid(column=1, row=2)
FicTrac_configPath_button = ttk.Button(FicTrac_frame_2, text="Browse..", command=setFicTracConfigPath)
FicTrac_configPath_button.grid(column=2, row=2, padx=5, pady=5)
FicTrac_configOpen_button = ttk.Button(FicTrac_frame_2, text="Open config", command=openFicTracConfig)
FicTrac_configOpen_button.grid(column=3, row=2, padx=5, pady=5)

# Viard
Vizard_path_string = StringVar()
Vizard_path_string.set("C:/Vizard5/bin/winviz.exe")


def setVizardPath():
    """
    Function to open a file chooser and browse a file
    """
    path = filedialog.askopenfilename(title="Set Vizard Path", filetypes=(("Programs", "*.exe"), ("All files", "*.*")))
    if path != "":
        Vizard_path_string.set(path)


Vizard_script_string = StringVar()
Vizard_script_string.set("C:/Users/YLab/Documents/FlyVR/FicTracWin64/setup-test/gallery.py")


def setScriptPath():
    """
    Function to open a file chooser and browse a file
    """
    path = filedialog.askopenfilename(title="Set Vizard Script Path", filetypes=(("Python files", "*.py"), ("All files", "*.*")))
    if path != "":
        Vizard_script_string.set(path)


def setVizardState(*args):
    """
    Enable or disable FicTrac according to FicTrac_state
    """
    if Vizard_state.get():
        Vizard_path_text.config(state=NORMAL)
        Vizard_path_button.config(state=NORMAL)
        Vizard_script_text.config(state=NORMAL)
        Vizard_script_button.config(state=NORMAL)
        Vizard_start_button.config(state=NORMAL)
    else:
        Vizard_path_text.config(state=DISABLED)
        Vizard_path_button.config(state=DISABLED)
        Vizard_script_text.config(state=DISABLED)
        Vizard_script_button.config(state=DISABLED)
        Vizard_start_button.config(state=DISABLED)


def startVizard(*args):
    """
    Start Vizard before the experiment starts,
    so that the user can adjust the display ,etc.
    """
    if (isProperFile(Vizard_path_string.get(), "exe")) and \
            (isProperFile(Vizard_script_string.get(), "py")):  # Vizard is enabled
        subprocess.Popen(["python", "StartVizard.py",
                          Vizard_path_string.get(), Vizard_script_string.get()], shell=True)


labelframe_Vizard = LabelFrame(tab_record, text="Vizard")
labelframe_Vizard.pack(fill="both", expand="no")


Vizard_state = BooleanVar()
Vizard_state.set(True)  # Initialized as true
Vizard_state.trace("w", setVizardState)

Vizard_frame_1 = Frame(labelframe_Vizard)
Vizard_frame_1.pack(fill=X)
Vizard_state_box = ttk.Checkbutton(Vizard_frame_1, text="Enable Vizard", var=Vizard_state)
Vizard_state_box.grid(column=0, row=0, padx=5)

Vizard_frame_2 = Frame(labelframe_Vizard)
Vizard_frame_2.pack(fill=X)
Vizard_path_label = Label(Vizard_frame_2, text="Vizard path", width=15)
Vizard_path_label.grid(column=0, row=0)
Vizard_path_text = ttk.Entry(Vizard_frame_2, width=50, textvariable=Vizard_path_string)
Vizard_path_text.grid(column=1, row=0)
Vizard_path_button = ttk.Button(Vizard_frame_2, text="Browse..", command=setVizardPath)
Vizard_path_button.grid(column=2, row=0, padx=5)

Vizard_script_label = Label(Vizard_frame_2, text="Script path", width=15)
Vizard_script_label.grid(column=0, row=1)
Vizard_script_text = ttk.Entry(Vizard_frame_2, width=50, textvariable=Vizard_script_string)
Vizard_script_text.grid(column=1, row=1)
Vizard_script_button = ttk.Button(Vizard_frame_2, text="Browse..", command=setScriptPath)
Vizard_script_button.grid(column=2, row=1, padx=5, pady=5)

Vizard_start_button = ttk.Button(Vizard_frame_2, text="Start Vizard", command=startVizard)
Vizard_start_button.grid(column=0, row=2, padx=5, pady=5)


# Camera
def setArduinoState(*args):
    """
    Enable or disable FicTrac according to FicTrac_state
    """
    if Arduino_state.get():
        Arduino_port_text.config(state=NORMAL)
        Arduino_port_button.config(state=NORMAL)
    else:
        Arduino_port_text.config(state=DISABLED)
        Arduino_port_button.config(state=DISABLED)


def setArduinoPort():
    """
    Set the serial port for Arduino
    """
    global arduino
    global serial_set
    try:
        arduino = ArduinoControl(port=Arduino_port_string.get())
        serial_set = True
        messagebox.showinfo("Success", "Serial port is set successfully")
    except serial.serialutil.SerialException:
        messagebox.showerror("Error", "The port "+Arduino_port_string.get()+" is not found")


serial_set = False  # Flag to show if serial is set
Arduino_port_string = StringVar()
Arduino_port_string.set("COM3")  # Initialized as COM3
labelframe_camera = LabelFrame(tab_record, text="Camera Control")
labelframe_camera.pack(fill="both", expand="no")


Arduino_state = BooleanVar()
Arduino_state.set(True)  # Initialized as true
Arduino_state.trace("w", setArduinoState)

camera_frame_1 = Frame(labelframe_camera)
camera_frame_1.pack(fill=X)
Arduino_state_box = ttk.Checkbutton(camera_frame_1, text="Use Arduino board to control cameras", var=Arduino_state)
Arduino_state_box.grid(column=0, row=0, padx=5)

camera_frame_2 = Frame(labelframe_camera)
camera_frame_2.pack(fill=X)
Arduino_port_label = Label(camera_frame_2, text="Serial port", width=15)
Arduino_port_label.grid(column=0, row=1)
Arduino_port_text = ttk.Entry(camera_frame_2, width=10, textvariable=Arduino_port_string)
Arduino_port_text.grid(column=1, row=1)
Arduino_port_button = ttk.Button(camera_frame_2, text="Set port", command=setArduinoPort)
Arduino_port_button.grid(column=2, row=1, padx=5, pady=5)


def _startFicTrac():
    """
    A helper to start FicTrac, need to be a new thread
    """
    proc = subprocess.Popen([FicTrac_path_string.get(), FicTrac_configPath_string.get()], shell=True, stdout=PIPE)

    # while True:
    #     line = proc.stdout.readline()
    #     if b"doing frame" in line:
    #         print("Started")
    #         break
    # print("Broken")
    flag = False
    for c in iter(lambda: proc.stdout.readline(), b''):  # replace '' with b'' for Python 3
        print(c.decode()[:-1])  # -1 gets rid of the new lines
        if not flag and b"doing frame" in c:
            print("Started FicTrac")
            if Arduino_state.get() and serial_set:  # Serial is set
                arduino.init_camera()
            timing_sw.start()
            flag = True

# Experiment
def startExperiment():
    """
    Start the entire experiment
    """
    if Arduino_state.get():  # Arduino is enabled
        if not serial_set:  # Try to set arduino if not set yet
            setArduinoPort()
        if serial_set and not FicTrac_state.get():  # Serial is set
            arduino.init_camera()
        #else:  # Try to set arduino port but failed
        #    return
    #if Vizard_state.get():  # Vizard is enabled
    #    subprocess.Popen(["python", "StartVizard.py",
    #                      Vizard_path_string.get(), Vizard_script_string.get()], shell=True)
        # p = subprocess.Popen([Vizard_path_string.get(), Vizard_script_string.get()], shell=True,
        #                      stdout=PIPE, stderr=PIPE)
        # output, error = p.communicate()
        # if p.returncode != 0:  # Failed to start Vizard
        #     messagebox.showerror("Error",
        #                          "Vizard is not configured properly:\n"+output.decode("utf-8")+error.decode("utf-8"))
        #     return
    if FicTrac_state.get():  # FicTrac is enabled
        print("Starting FicTrac...")
        global t
        t = Thread(target=_startFicTrac)  # Use a thread otherwise will freeze
        t.daemon = True
        t.start()

    # TODO: start the experiment


def stopExperiment():
    """
    Stop the entire experiment
    """
    if serial_set:
        arduino.stop_camera()
    if Vizard_state.get():
        pass
    timing_sw.stop()


    # TODO: stop the experiment


time_string = StringVar()
time_string.set(0)
time_unit_string = StringVar()
time_unit_string.set("frames")

labelframe_experiment = LabelFrame(tab_record, text="Experiment Control")
labelframe_experiment.pack(fill="both", expand="yes")

experiment_frame_1 = Frame(labelframe_experiment)
experiment_frame_1.pack(fill=X)
experiment_frame_2 = Frame(labelframe_experiment)
experiment_frame_2.pack(fill=X)
experiment_frame_3 = Frame(labelframe_experiment)
experiment_frame_3.pack(fill=X)

timing_label = ttk.Label(experiment_frame_2, text="Time:")
timing_label.pack(side=LEFT, padx=5, pady=5)
timing_sw = StopWatch(experiment_frame_2, padx=5, pady=5)
timing_sw.pack(side=LEFT)

start_button = ttk.Button(experiment_frame_3, text="Start",
                          command=startExperiment)
start_button.pack(side=LEFT, padx=10, pady=5)
stop_button = ttk.Button(experiment_frame_3, text="Stop",
                         command=stopExperiment)
stop_button.pack(side=LEFT, padx=10, pady=5)

time_label = Label(experiment_frame_1, text="Record for")
time_label.grid(column=0, row=0, padx=5, pady=5)
time_text = ttk.Entry(experiment_frame_1, width=10, textvariable=time_string)
time_text.grid(column=1, row=0, pady=5)
time_dropdown = ttk.OptionMenu(experiment_frame_1, time_unit_string, "frames", "frames", "ms", "sec", "min")
time_dropdown.grid(column=2, row=0, padx=5, pady=5)
time_unit_label = Label(experiment_frame_1, text="* Specify zero to capture until manually stopped")
time_unit_label.grid(column=3, row=0)


filelist = []


def _selectFileHelper(filestr):
    """
    A helper function for file selection, used in both file and folder selection

    Sets the state of prev and next button
    """
    select_file_textbox.config(state=NORMAL)
    select_file_textbox.delete("1.0", END)
    select_file_textbox.insert("1.0", filestr)
    select_file_textbox.config(state=DISABLED)
    global plot_helper
    plot_helper = PlotHelper(plot_frame_5, filelist, average_type=plot_average_selection_int.get())
    if not plot_helper.has_next():
        plot_next_button.config(state=DISABLED)


def selectcsvFile():
    """
    Function to open a file chooser and browse files
    Then write the file names to the selected files text box
    """
    path = filedialog.askopenfilenames(title="Import files", filetypes=(("CSV files", "*.csv"), ("All files", "*.*")))
    if path == "":
        return
    global filelist
    filelist = []
    filestr = ""
    for filename in window.tk.splitlist(path):
        filelist.append(filename)
        filestr += (filename+"\n")
    _selectFileHelper(filestr)


def selectFolder():
    """
    Function to open a file chooser and browse files
    Then write the file names to the selected files text box
    """
    path = filedialog.askdirectory(title="Import Folder")
    if path == "":
        return
    global filelist
    filelist = []
    filestr = ""
    for filename in os.listdir(path):
        if ".csv" in filename:
            filelist.append(path+"/"+filename)
            filestr += (path+"/"+filename+"\n")
    _selectFileHelper(filestr)


labelframe_select = LabelFrame(tab_analysis, text="Import CSV files")
labelframe_select.pack(fill="both", expand="no")

select_frame_1 = Frame(labelframe_select)
select_frame_1.pack(fill=X, padx=5, pady=5)

select_file_button = ttk.Button(select_frame_1, text="Select File(s)", command=selectcsvFile)
select_file_button.grid(column=0, row=0, padx=10)
select_folder_button = ttk.Button(select_frame_1, text="Select Folder", command=selectFolder)
select_folder_button.grid(column=1, row=0, padx=10)

select_frame_2 = Frame(labelframe_select)
select_frame_2.pack(fill=X)

select_file_label = ttk.Label(select_frame_2, text="Selected Files:")
select_file_label.grid(column=0, row=0, padx=5)


select_frame_3 = Frame(labelframe_select)
select_frame_3.pack(fill=X, padx=5, pady=5)
select_file_scrolly = Scrollbar(select_frame_3)
select_file_scrollx = Scrollbar(select_frame_3, orient=HORIZONTAL)
select_file_textbox = Text(select_frame_3, height=5, wrap=NONE)  # No word wrap
select_file_textbox.grid(row=0, column=0, sticky="nsew")
select_file_scrolly.grid(row=0, column=1, sticky="ns")
select_file_scrollx.grid(row=1, column=0, sticky="ew")
select_file_scrolly.config(command=select_file_textbox.yview)
select_file_scrollx.config(command=select_file_textbox.xview)
select_file_textbox.config(yscrollcommand=select_file_scrolly.set, xscrollcommand=select_file_scrollx.set)
select_file_textbox.config(state=DISABLED)
select_frame_3.grid_rowconfigure(0, weight=1)
select_frame_3.grid_columnconfigure(0, weight=1)


def setupOptionWindow():
    option_window = Tk()
    option_window.wm_title("Options")

    option_window.geometry("400x300")
    option_window.attributes("-topmost", True)

    x_range_1 = StringVar()
    x_range_2 = StringVar()
    y_range_1 = StringVar()
    y_range_2 = StringVar()
    x_range_1.set(str(X_RANGE_1))
    x_range_2.set(str(X_RANGE_2))
    y_range_1.set(str(Y_RANGE_1))
    y_range_2.set(str(Y_RANGE_2))

    option_frame_1 = Frame(option_window)
    option_frame_1.pack(fill=X)
    range_x_label = ttk.Label(option_frame_1, text="x-axis range:")
    range_x_entry_1 = ttk.Entry(option_frame_1, textvariable=x_range_1, width=5)
    range_x_label_2 = ttk.Label(option_frame_1, text="-")
    range_x_entry_2 = ttk.Entry(option_frame_1, textvariable=x_range_2, width=5)
    range_y_label = ttk.Label(option_frame_1, text="y-axis range:")
    range_y_entry_1 = ttk.Entry(option_frame_1, textvariable=y_range_1, width=5)
    range_y_label_2 = ttk.Label(option_frame_1, text="-")
    range_y_entry_2 = ttk.Entry(option_frame_1, textvariable=y_range_2, width=5)
    range_x_label.grid(column=0, row=0, padx=5, pady=5)
    range_x_entry_1.grid(column=1, row=0)
    range_x_label_2.grid(column=2, row=0)
    range_x_entry_2.grid(column=3, row=0)
    range_y_label.grid(column=0, row=1, padx=5, pady=5)
    range_y_entry_1.grid(column=1, row=1)
    range_y_label_2.grid(column=2, row=1)
    range_y_entry_2.grid(column=3, row=1)

    option_window.mainloop()


SCATTER = 1
BOX = 2

labelframe_plot = LabelFrame(tab_analysis, text="Plotting")
labelframe_plot.pack(fill="both", expand="yes")
plot_frame_1 = Frame(labelframe_plot)
plot_frame_1.pack(fill=X)


plot_average_selection_int = IntVar()

plot_selection_button_1 = Radiobutton(plot_frame_1, text="Scatter Plot", variable=plot_average_selection_int,
                                      value=SCATTER, indicatoron=0)
plot_selection_button_1.grid(column=0, row=0, padx=5, pady=5)
plot_selection_button_2 = Radiobutton(plot_frame_1, text="Box Plot", variable=plot_average_selection_int,
                                      value=BOX, indicatoron=0)
plot_selection_button_2.grid(column=1, row=0, padx=5, pady=5)

plot_average_selection_int.set(SCATTER)

plot_frame_2 = Frame(labelframe_plot)
plot_frame_2.pack(fill=X)

plot_frame_21 = Frame(plot_frame_2)
plot_frame_21.pack(side=LEFT, fill=X)
plot_frame_22 = Frame(plot_frame_2)
plot_frame_22.pack(side=RIGHT, fill=X)

plot_axisx_string = StringVar()
plot_axisy_string = StringVar()
plot_axisx_caption_string = StringVar()
plot_axisy_caption_string = StringVar()
plot_title_string = StringVar()

plot_axisx_label = ttk.Label(plot_frame_21, text="x-axis:")
plot_axisy_label = ttk.Label(plot_frame_21, text="y-axis:")
plot_axisx_drop = ttk.OptionMenu(plot_frame_21, plot_axisx_string, "Time(s)", "Time(s)", "Time(frames) (Not functioning)")

plot_axisy_drop = ttk.OptionMenu(plot_frame_21, plot_axisy_string, "Speed", "Speed", "Turning")
plot_axisx_caption = ttk.Label(plot_frame_21, text="Caption:")
plot_axisy_caption = ttk.Label(plot_frame_21, text="Caption:")
plot_axisx_text = ttk.Entry(plot_frame_21, width=20, textvariable=plot_axisx_caption_string)
plot_axisy_text = ttk.Entry(plot_frame_21, width=20, textvariable=plot_axisy_caption_string)
plot_axisx_label.grid(column=0, row=0)
plot_axisy_label.grid(column=0, row=1)
plot_axisx_drop.grid(column=1, row=0)
plot_axisy_drop.grid(column=1, row=1)
plot_axisx_caption.grid(column=2, row=0)
plot_axisy_caption.grid(column=2, row=1)
plot_axisx_text.grid(column=3, row=0)
plot_axisy_text.grid(column=3, row=1)

plot_average_selection_int = IntVar()
plot_average_selection_1 = ttk.Radiobutton(plot_frame_22, text="Plot for individual fly",
                                           variable=plot_average_selection_int, value=INDIVIDUAL_PLOT)
plot_average_selection_2 = ttk.Radiobutton(plot_frame_22, text="Plot for average of all flies",
                                           variable=plot_average_selection_int, value=AVERAGE_PLOT)
plot_average_selection_1.pack(anchor=W, padx=5)
plot_average_selection_2.pack(anchor=W, padx=5)
plot_average_selection_int.set(INDIVIDUAL_PLOT)


plot_frame_3 = Frame(labelframe_plot)
plot_frame_3.pack(fill=X)
plot_title_label = ttk.Label(plot_frame_3, text="Title:")
plot_title_label.pack(side=LEFT)
plot_title_text = ttk.Entry(plot_frame_3, width=40, textvariable=plot_title_string)
plot_title_text.pack(side=LEFT)
plot_option_button = ttk.Button(plot_frame_3, text="Options...", command=setupOptionWindow)
plot_option_button.pack(side=RIGHT)

def _set_preview_label():
    """
    Sets the label of current preview
    """
    if plot_average_selection_int.get() == INDIVIDUAL_PLOT:
        plot_preview_label.config(text=plot_helper.get_file_name(plot_helper.get_index()))
    elif plot_average_selection_int.get() == AVERAGE_PLOT:
        plot_preview_label.config(text="Average of all flies")


def preview():
    if "plot_helper" not in globals():  # The file is not selected
        return
    col = INDEX_SHORT_DICT[plot_axisy_string.get()]  # Get which col to use based on user selection
    plot_helper.set_average_type(plot_average_selection_int.get())
    plot_helper.plot(0, col, plot_axisx_caption_string.get(), plot_axisy_caption_string.get(), plot_title_string.get())
    _set_preview_label()
    if plot_helper.has_next():
        plot_next_button.config(state=NORMAL)
    else:
        plot_next_button.config(state=DISABLED)
    if plot_helper.has_prev():
        plot_prev_button.config(state=NORMAL)
    else:
        plot_prev_button.config(state=DISABLED)


def prev_plot():
    if "plot_helper" not in globals():  # The file is not selected
        return
    col = INDEX_SHORT_DICT[plot_axisy_string.get()]
    plot_helper.set_average_type(plot_average_selection_int.get())
    plot_helper.plot_prev(0, col, plot_axisx_caption_string.get(), plot_axisy_caption_string.get(),
                          plot_title_string.get())
    _set_preview_label()
    if not plot_helper.has_prev():
        plot_prev_button.config(state=DISABLED)
    if plot_helper.has_next():
        plot_next_button.config(state=NORMAL)


def next_plot():
    if "plot_helper" not in globals():  # The file is not selected
        return
    col = INDEX_SHORT_DICT[plot_axisy_string.get()]
    plot_helper.set_average_type(plot_average_selection_int.get())
    plot_helper.plot_next(0, col, plot_axisx_caption_string.get(), plot_axisy_caption_string.get(),
                          plot_title_string.get())
    _set_preview_label()
    if not plot_helper.has_next():
        plot_next_button.config(state=DISABLED)
    if plot_helper.has_prev():
        plot_prev_button.config(state=NORMAL)


def save_plot():
    path = filedialog.askdirectory(title="Save in folder")
    if path == "":  # No path is selected
        return
    col = INDEX_SHORT_DICT[plot_axisy_string.get()]
    fig_size = (plot_size_width_string.get(), plot_size_height_string.get())
    plot_helper.save_file(path, extension=plot_format_string.get(), size=fig_size,
                          x=0, y=col, xc=plot_axisx_caption_string.get(), yc=plot_axisy_caption_string.get(),
                          title=plot_title_string.get())


plot_frame_4 = Frame(labelframe_plot)
plot_frame_4.pack(fill=X)
plot_preview_button = ttk.Button(plot_frame_4, text="Preview", command=preview)
plot_preview_button.pack(side=LEFT)
plot_preview_label = ttk.Label(plot_frame_4)
plot_preview_label.pack(side=LEFT)
plot_next_button = ttk.Button(plot_frame_4, text="Next", command=next_plot, width=10)
plot_next_button.pack(side=RIGHT)
plot_prev_button = ttk.Button(plot_frame_4, text="Prev", command=prev_plot, width=10, state=DISABLED)
plot_prev_button.pack(side=RIGHT)

plot_frame_5 = Frame(labelframe_plot, width=400, height=300)
plot_frame_5.pack(pady=5, fill=BOTH, expand='yes')
#canvas = Canvas(plot_frame_5, width=400, height=300)
#canvas.pack()


plot_format_string = StringVar()
plot_size_width_string = StringVar()
plot_size_width_string.set("800")
plot_size_height_string = StringVar()
plot_size_height_string.set("600")

plot_frame_6 = Frame(labelframe_plot)
plot_frame_6.pack(fill=X)
plot_format_label = ttk.Label(plot_frame_6, text="Format:")
plot_format_drop = ttk.OptionMenu(plot_frame_6, plot_format_string, "png", "png", "eps", "jpg", "pdf", "pgf", "ps",
                                  "raw", "rgba", "svg", "svgz", "tif", "tiff")
plot_size_label = ttk.Label(plot_frame_6, text="Size:")
plot_size_text_1 = ttk.Entry(plot_frame_6, width=6, textvariable=plot_size_width_string)
plot_size_label_2 = ttk.Label(plot_frame_6, text="x")
plot_size_text_2 = ttk.Entry(plot_frame_6, width=6, textvariable=plot_size_height_string)
plot_export_button = ttk.Button(plot_frame_6, text="Export plots...", command=save_plot)
plot_export_button.pack(side=RIGHT)
plot_size_text_2.pack(side=RIGHT)
plot_size_label_2.pack(side=RIGHT)
plot_size_text_1.pack(side=RIGHT)
plot_size_label.pack(side=RIGHT)
plot_format_drop.pack(side=RIGHT)
plot_format_label.pack(side=RIGHT)


labelframe_export = LabelFrame(tab_analysis, text="Export to Excel", width=600, height=50)
labelframe_export.pack(side=BOTTOM, fill=BOTH)



def loadConfig(*args):
    """
    Load the configuration of the program
    """
    Config = configparser.ConfigParser()
    path = filedialog.askopenfilename(title="Open config file", filetypes=(("INI files", "*.ini"), ("All files", "*.*")))
    Config.read(path)
    pass  # TODO: Load config


def saveConfig(*args):
    """
    Save the configuration of this program
    """
    pass  # TODO: Save config


def About(*args):
    """
    Show the about window
    """
    about = Tk()
    about.wm_title("About")
    try:
        about.wm_iconbitmap("fly-shape.ico")
    except:
        pass
    about_label = Label(about, text="The FlyVR software\nVersion 1.0\nCreated by Tianxing")
    about_label.pack(side=TOP, fill=X, pady=10, padx=50)
    about_button = ttk.Button(about, text="Okay", command=about.destroy)
    about_button.pack(pady=5)
    about.resizable(False, False)
    about.mainloop()


menu = Menu(window)
window.config(menu=menu)
filemenu = Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Load Configuration...", command=loadConfig)
filemenu.add_command(label="Save Configuration...", command=saveConfig)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit)

helpmenu = Menu(menu, tearoff=False)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About)

tab_control.pack(expand=1, fill='both')
window.mainloop()
