from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from random import randint
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from GUI_2.Arduino import init_camera, stop_camera
import subprocess
import os


class Fly(GridLayout):
    def __init__(self, **kwargs):
        super(Fly, self).__init__(**kwargs)
        self.cols = 2
        self.btn1 = Button(text="Start", on_press=self.start)
        self.add_widget(self.btn1)
        self.btn2 = Button(text="Stop", on_press=self.stop)
        self.add_widget(self.btn2)

    def start(self, instance):
        init_camera()
        #subprocess.check_call(['..\FicTrac', 'config.txt'], cwd="C:/FicTracWin64/setup_test")
        #subprocess.run('cd "C:\\FicTracWin64\\setup_test"')
        #subprocess.run("..\FicTrac config.txt")

    def stop(self, instance):
        stop_camera()


class FlyVRApp(App):
    def build(self):

        fly = Fly()

        return fly


if __name__ == '__main__':
    FlyVRApp().run()
