import serial
import time

class ArduinoControl(object):
    """
    Class to control the Arduino board
    """

    def __init__(self, port="COM9", baudrate=9600):

        self.ser = serial.Serial(port=port, baudrate=baudrate)

    def init_camera(self):
        """
        Start the experiment
        """
        self.ser.write('1'.encode())

    def stop_camera(self):
        """
        End the experiment
        """
        self.ser.write('0'.encode())


if __name__ == '__main__':
    arduino = ArduinoControl()
    while True:
        arduino.init_camera()
        time.sleep(2)
        arduino.stop_camera()
        time.sleep(2)
