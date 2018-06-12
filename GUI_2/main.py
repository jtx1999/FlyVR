from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from random import randint

from GUI_2.Arduino import ArduinoControl
import subprocess
from subprocess import PIPE
import os
import serial


class Fly(BoxLayout):
    def __init__(self, **kwargs):
        super(Fly, self).__init__(orientation='vertical', **kwargs)
        self.lyt1 = BoxLayout(orientation='horizontal')
        self.lyt2 = BoxLayout(orientation='horizontal')
        self.textinput = TextInput(text="COM3", multiline=False)
        self.lyt1.add_widget(self.textinput)
        self.btn0 = Button(text="Set port", on_press=self.setSerial)
        self.lyt1.add_widget(self.btn0)
        self.add_widget(self.lyt1)
        self.btn3 = Button(text="Config", on_press=self.setConfig)
        self.lyt1.add_widget(self.btn3)
        self.btn1 = Button(text="Start", on_press=self.startCam)
        self.lyt2.add_widget(self.btn1)
        self.btn2 = Button(text="Stop", on_press=self.stopCam)
        self.lyt2.add_widget(self.btn2)
        self.add_widget(self.lyt2)
        self.serial = False  # The serial port is not set


    def setSerial(self, instance=None, port=None):
        """
        Set the serial communication with the arduino board, pop up a window
        if failed
        """
        if port is None:
            port = self.textinput.text
        try:
            self.arduino = ArduinoControl(port=port)
            self.serial = True
        except serial.serialutil.SerialException:
            self.popupError("Error", "The port "+port+" cannot be found")


    def startCam(self, instance):
        """
        Start the experiment
        """
        if not self.serial:
            self.setSerial()
        if self.serial:
            self.arduino.init_camera()

        wd1 = "C:\\Users\\YLab\\Documents\\FlyVR\\FicTracWin64\\fictrac_example_test"
        subprocess.Popen(['..\\FicTrac.exe', 'config.txt'], cwd=wd1, shell=True)
        #subprocess.run('cd "C:\\FicTracWin64\\setup_test"')
        #subprocess.run("..\FicTrac config.txt")

    def stopCam(self, instance):
        """
        Stop the experiment
        """

        if self.serial:
            self.arduino.stop_camera()

    def popupError(self, title, message):
        """
        Pop up a window with the title and message
        """
        layout = GridLayout(cols=1, padding=10)
        popupLabel = Label(text=message)
        closeButton = Button(text="Close", size_hint=(1, 0.3))
        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)
        popup = Popup(title=title,
                      content=layout, auto_dismiss=False,
                      size_hint=(None, None), size=(400, 400))
        popup.open()
        closeButton.bind(on_release=popup.dismiss)

    def setConfig(self, instance=None):
        """
        Set the configuration of FicTrac
        """
        wd1 = "C:\\Users\\YLab\\Documents\\FlyVR\\FicTracWin64\\fictrac_example_test"
        subprocess.Popen(['notepad', 'config.txt'], stdout=PIPE, stderr=PIPE, cwd=wd1)


class FlyVRApp(App):
    def build(self):

        fly = Fly()

        return fly


if __name__ == '__main__':
    FlyVRApp().run()
