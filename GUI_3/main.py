from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from Arduino import ArduinoControl
import serial
import subprocess
from subprocess import PIPE
import time

window = Tk()
window.title("FlyVR")
window.iconbitmap("fly-shape.ico")
window.geometry('600x800')

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
FicTrac_configPath_string = StringVar()


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


def setVizardPath():
    """
    Function to open a file chooser and browse a file
    """
    path = filedialog.askopenfilename(title="Set Vizard Path", filetypes=(("Programs", "*.exe"), ("All files", "*.*")))
    if path != "":
        Vizard_path_string.set(path)


Vizard_script_string = StringVar()


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
        subprocess.Popen(["python", "C:\\Users\\YLab\\Documents\\FlyVR\\GUI_3\\StartVizard.py",
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

# Experiment
def startExperiment():
    """
    Start the entire experiment
    """
    if Arduino_state.get():  # Arduino is enabled
        if not serial_set:  # Try to set arduino if not set yet
            setArduinoPort()
        if serial_set:  # Serial is set
            arduino.init_camera()
        else:  # Try to set arduino port but failed
            return
    if Vizard_state.get():  # Vizard is enabled
        subprocess.Popen(["python", "StartVizard.py",
                          Vizard_path_string.get(), Vizard_script_string.get()], shell=True)
        # p = subprocess.Popen([Vizard_path_string.get(), Vizard_script_string.get()], shell=True,
        #                      stdout=PIPE, stderr=PIPE)
        # output, error = p.communicate()
        # if p.returncode != 0:  # Failed to start Vizard
        #     messagebox.showerror("Error",
        #                          "Vizard is not configured properly:\n"+output.decode("utf-8")+error.decode("utf-8"))
        #     return

    # TODO: start the experiment


def stopExperiment():
    """
    Stop the entire experiment
    """
    if serial_set:
        arduino.stop_camera()
    if Vizard_state.get():
        pass
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

start_button = ttk.Button(experiment_frame_2, text="Start",
                      command=startExperiment)
start_button.pack(side=LEFT, padx=10, pady=5)
stop_button = ttk.Button(experiment_frame_2, text="Stop",
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
# TODO: timing


def loadConfig(*args):
    """
    Load the configuration of the program
    """
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
    about.wm_iconbitmap("fly-shape.ico")
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
