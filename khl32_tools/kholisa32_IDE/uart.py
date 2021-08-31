# This Python file uses the following encoding: utf-8
from PySide2 import QtWidgets
import serial
import serial.tools.list_ports
import math
import time

"""
Commands:
   debug        -> 0x30
   send game    -> 0x31



"""



class Uart:
    connection: serial.serialwin32.Serial = None
    port: str = "COM0"
    baud: int = 9600
    max_packet_size: int = 7200

    def __init__(self):
        pass

    def init():
        with open("settings.conf", "r") as conf:
            data = conf.read().split("\n")
            settings = [x.split(" ") for x in data]

            for setting in settings:
                if setting[0] == "BAUDRATE":
                    Uart.baud = int(setting[1])

                if setting[0] == "PORT":
                     Uart.port = setting[1]

    def open():
        Uart.connection = serial.Serial(port = Uart.port, baudrate = Uart.baud, timeout = 5)
        Uart.connection.write(b'\x02')
        Uart.connection.flush()
        if Uart.connection.read(1) != b'\x02':
            print("No connection made!")
            Uart.exit()
        else:
            print("Connection made succesfully!")

    def get_port_names() -> list:
        names = []
        for port in serial.tools.list_ports.comports():
            names.append(port.device)

        return names

    def exit():
        Uart.connection.write(b'\x04')
        Uart.connection.close()

    def send_command(command: bytes) -> int:
        if len(command)==1:
            Uart.connection.write(command)
            Uart.connection.flush()

        if Uart.connection.read(1) == b'\x06':
            return 1
        else:
            return 0

    def transfer_binary(binary: bytearray) -> int:
        print("Transfer started!")
        isOpen: bool = True
        if Uart.connection is None:
            Uart.open()

        if Uart.send_command(b'\x31'):
            if Uart.connection.read(1) == b'\x06':
                time.sleep(0.1)
                print("Sending total len!")
                """ Transfer total length """
                print("Len: " + str(len(binary)))
                Uart.connection.write(len(binary).to_bytes(4, "little"))
                Uart.connection.flush()
            else:
                print("Fail sending total len!")

            """ Transfer packet amount """
            n_packets = math.ceil(len(binary)/Uart.max_packet_size)+1
            if Uart.connection.read(1) == b'\x06':
                time.sleep(0.1)
                print("Sending packet amount!")
                print("Packets: " + str(n_packets))
                Uart.connection.write(n_packets.to_bytes(4, 'little'))
                Uart.connection.flush()
            else:
                print("Fail sending packet amount!")

            """ Transfer header """
            if Uart.connection.read(1) == b'\x06':
                time.sleep(0.1)
                print("Sending header")
                print(binary[:84])
                Uart.connection.write(binary[:84])
                Uart.connection.flush()
            else:
                print("Fail sending header!")

            """ Transfer data """
            start: int = 84
            stop: int = 84

            while (n_packets and 0):
                if Uart.connection.read(10) == b'\x06':
                    time.sleep(0.1)
                    start = stop
                    stop = start + Uart.max_packet_size if len(binary)-84 >= Uart.max_packet_size else len(binary)

                    """ Transfer packet length """
                    Uart.connection.write((stop-start).to_bytes(4, 'little'))
                    Uart.connection.flush()
                else:
                    pass
                if Uart.connection.read(10) == b'\x06':
                    """ Transfer packet """
                    Uart.connection.write(binary[start:stop])
                    Uart.connection.flush()

                    n_packets -= 1
                else:
                    pass

        #if not isOpen:
        Uart.exit()

        return 0

    def set_baudrate(baud: int):
        Uart.baudrate = baud

    def set_port(port: str):
        Uart.port = port
