from tkinter import *
from tkinter import ttk
from tkinter import filedialog

window = Tk()
window.title("FlyVR")
window.iconbitmap("C:\\Users\\YLab\\Documents\\FlyVR\\GUI_3\\fly-shape.ico")
window.geometry('600x800')
tab_control = ttk.Notebook(window)
tab_record = ttk.Frame(tab_control)
tab_analysis = ttk.Frame(tab_control)
tab_control.add(tab_record, text="Record")
tab_control.add(tab_analysis, text="Analysis")

labelframe_FicTrac = LabelFrame(tab_record, text="FicTrac")
labelframe_FicTrac.pack(fill="both", expand="no")
left = Label(labelframe_FicTrac, text="Inside the FicTrac LabelFrame")
left.pack()

labelframe_Vizard = LabelFrame(tab_record, text="Vizard")
labelframe_Vizard.pack(fill="both", expand="no")
left = Label(labelframe_Vizard, text="Inside the Vizard LabelFrame")
left.pack()

labelframe_camera = LabelFrame(tab_record, text="Camera Control")
labelframe_camera.pack(fill="both", expand='yes')


tab_control.pack(expand=1, fill='both')
window.mainloop()
