import serial.tools.list_ports


def get_serial_ports():
    serial_ports = [port.device for port in serial.tools.list_ports.comports()]

    if not serial_ports:
        return ["No se encontraron puertos"]

    return serial_ports
