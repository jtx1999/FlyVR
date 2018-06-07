import serial
ser = serial.Serial(port="COM5", baudrate=9600)


def init_camera():
    """
    Start the experiment
    """
    ser.write('1'.encode())


def stop_camera():
    """
    End the experiment
    """
    ser.write('0'.encode())
