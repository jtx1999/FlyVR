from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from GUI_3.Arduino import ArduinoControl
import serial

window = Tk()
window.title("FlyVR")
window.iconbitmap("C:\\Users\\YLab\\Documents\\FlyVR\\GUI_3\\fly-shape.ico")
window.geometry('600x800')

tab_control = ttk.Notebook(window)
tab_record = ttk.Frame(tab_control)
tab_analysis = ttk.Frame(tab_control)
tab_control.add(tab_record, text="Record")
tab_control.add(tab_analysis, text="Analysis")

FicTrac_path_string = StringVar()

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
        FicTrac_config_button.config(state=NORMAL)
        FicTrac_path_text.config(state=NORMAL)
        FicTrac_path_button.config(state=NORMAL)
    else:
        FicTrac_config_button.config(state=DISABLED)
        FicTrac_path_text.config(state=DISABLED)
        FicTrac_path_button.config(state=DISABLED)


FicTrac_state = BooleanVar()
FicTrac_state.set(True)  # Initialized as true
FicTrac_state.trace("w", setFicTracState)

labelframe_FicTrac = LabelFrame(tab_record, text="FicTrac")
labelframe_FicTrac.pack(fill="both", expand="no")

FicTrac_state_box = Checkbutton(labelframe_FicTrac, text="Enable FicTrac", var=FicTrac_state)
FicTrac_state_box.grid(column=0, row=0)

FicTrac_path_label = Label(labelframe_FicTrac, text="FicTrac path")
FicTrac_path_label.grid(column=0, row=1)
FicTrac_path_text = Entry(labelframe_FicTrac, width=50, textvariable=FicTrac_path_string)
FicTrac_path_text.grid(column=1, row=1)
FicTrac_path_button = Button(labelframe_FicTrac, text="Browse..", command=setFicTracPath)
FicTrac_path_button.grid(column=2, row=1)

FicTrac_config_button = Button(labelframe_FicTrac, text="Config FicTrac")
FicTrac_config_button.grid(column=0, row=2)

# Viard
Vizard_path_string = StringVar()


def setVizardPath():
    """
    Function to open a file chooser and browse a file
    """
    path = filedialog.askopenfilename(title="Set Vizard Path", filetypes=(("Programs", "*.exe"), ("All files", "*.*")))
    if path != "":
        Vizard_path_string.set(path)


def setVizardState(*args):
    """
    Enable or disable FicTrac according to FicTrac_state
    """
    if Vizard_state.get():
        Vizard_path_text.config(state=NORMAL)
        Vizard_path_button.config(state=NORMAL)
    else:
        Vizard_path_text.config(state=DISABLED)
        Vizard_path_button.config(state=DISABLED)


labelframe_Vizard = LabelFrame(tab_record, text="Vizard")
labelframe_Vizard.pack(fill="both", expand="no")


Vizard_state = BooleanVar()
Vizard_state.set(True)  # Initialized as true
Vizard_state.trace("w", setVizardState)

Vizard_state_box = Checkbutton(labelframe_Vizard, text="Enable Vizard", var=Vizard_state)
Vizard_state_box.grid(column=0, row=0)

Vizard_path_label = Label(labelframe_Vizard, text="Vizard path")
Vizard_path_label.grid(column=0, row=1)
Vizard_path_text = Entry(labelframe_Vizard, width=50, textvariable=Vizard_path_string)
Vizard_path_text.grid(column=1, row=1)
Vizard_path_button = Button(labelframe_Vizard, text="Browse..", command=setVizardPath)
Vizard_path_button.grid(column=2, row=1)


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

Arduino_state_box = Checkbutton(labelframe_camera, text="Use Arduino board to control cameras", var=Arduino_state)
Arduino_state_box.grid(column=0, row=0)

Arduino_port_label = Label(labelframe_camera, text="Serial port")
Arduino_port_label.grid(column=0, row=1)
Arduino_port_text = Entry(labelframe_camera, width=10, textvariable=Arduino_port_string)
Arduino_port_text.grid(column=1, row=1)
Arduino_port_button = Button(labelframe_camera, text="Set port", command=setArduinoPort)
Arduino_port_button.grid(column=2, row=1)

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

    # TODO: start the experiment


def stopExperiment():
    """
    Stop the entire experiment
    """
    if serial_set:
        arduino.stop_camera()

    # TODO: stop the experiment


labelframe_experiment = LabelFrame(tab_record, text="Experiment Control")
labelframe_experiment.pack(fill="both", expand="yes")
start_button = Button(labelframe_experiment, text="Start", bg="green", font=("Arial", 30),
                      command=startExperiment)
start_button.pack(side=LEFT)
stop_button = Button(labelframe_experiment, text="Stop", bg="red", font=("Arial", 30),
                     command=stopExperiment)
stop_button.pack(side=LEFT)


tab_control.pack(expand=1, fill='both')
window.mainloop()
