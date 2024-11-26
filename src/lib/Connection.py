import serial


class Connection(serial.Serial):
    def __init__(self, port, baudrate):
        super().__init__(port, baudrate)
        self.port = port
        self.baudrate = baudrate

    def connect(self):
        self.open()
        return self.is_open

    def disconnect(self):
        self.close()
        return not self.is_open
