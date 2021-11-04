import logging
import time
from argparse import ArgumentParser
from datetime import datetime

import serial

# LoRaWAN IoT Sensor Demo
# Using REYAX RYLR896 transceiver modules
# Author: Gary Stafford
# Requirements: python3 -m pip install –user -r requirements.txt
# To Run: python3 ./rasppi_lora_receiver.py –tty /dev/ttyAMA0 –baud-rate 115200

# constants
ADDRESS = 115
NETWORK_ID = 6

#WILL NOT USE PASSWORD
#PASSWORD = "92A0ECEC9000DA0DCF0CAAB0ABA2E0EF"


def main():
    logging.basicConfig(filename='output.log', filemode='w', level=logging.DEBUG)
    payload = ""

    print("Connecting to REYAX RYLR896 transceiver module…")
    serial_conn = serial.Serial(
        port="/dev/serial0",
        baudrate=115200,
        timeout=5,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )

    if serial_conn.isOpen():
        
        print("Serial Port is Open")
        
        set_lora_config(serial_conn)
        check_lora_config(serial_conn)
        
        
        connect_to_camera(serial_conn)
        
        
        wait_read(serial_conn)
        
        #CONNECTION SET UP, ENTER STANBY MODE
        
        standby_mode(serial_conn)
        
        
        

def set_lora_config(serial_conn):
    # configures the REYAX RYLR896 transceiver module

    serial_conn.write(str.encode("AT+ADDRESS=" + str(ADDRESS) + "\r\n"))
    serial_payload = (serial_conn.readline())
    print("Address set?", serial_payload.decode(encoding="utf-8"))

    serial_conn.write(str.encode("AT+NETWORKID=" + str(NETWORK_ID) + "\r\n"))
    serial_payload = (serial_conn.readline())
    print("Network Id set?", serial_payload.decode(encoding="utf-8"))
    
    #NOT USING PASSWORD
    #serial_conn.write(str.encode("AT+CPIN=" + PASSWORD + "\r\n"))
    #time.sleep(1)
    #serial_payload = (serial_conn.readline())
    #print("AES-128 password set?", serial_payload.decode(encoding="utf-8"))


def check_lora_config(serial_conn):
    serial_conn.write(str.encode("AT?\r\n"))
    serial_payload = (serial_conn.readline())
    print("Module responding?", serial_payload.decode(encoding="utf-8"))

    serial_conn.write(str.encode("AT+ADDRESS?\r\n"))
    serial_payload = (serial_conn.readline())
    print("Address:", serial_payload.decode(encoding="utf-8"))

    serial_conn.write(str.encode("AT+NETWORKID?\r\n"))
    serial_payload = (serial_conn.readline())
    print("Network id:", serial_payload.decode(encoding="utf-8"))

    serial_conn.write(str.encode("AT+IPR?\r\n"))
    serial_payload = (serial_conn.readline())
    print("UART baud rate:", serial_payload.decode(encoding="utf-8"))

    serial_conn.write(str.encode("AT+BAND?\r\n"))
    serial_payload = (serial_conn.readline())
    print("RF frequency", serial_payload.decode(encoding="utf-8"))

    serial_conn.write(str.encode("AT+CRFOP?\r\n"))
    serial_payload = (serial_conn.readline())
    print("RF output power", serial_payload.decode(encoding="utf-8"))

    serial_conn.write(str.encode("AT+MODE?\r\n"))
    serial_payload = (serial_conn.readline())
    print("Work mode", serial_payload.decode(encoding="utf-8"))

    serial_conn.write(str.encode("AT+PARAMETER?\r\n"))
    serial_payload = (serial_conn.readline())
    print("RF parameters", serial_payload.decode(encoding="utf-8"))

#     serial_conn.write(str.encode("AT+CPIN?\r\n"))
#     serial_payload = (serial_conn.readline())
#     print("AES128 password of the network",
#           serial_payload.decode(encoding="utf-8"))

def connect_to_camera(serial_conn):
    print("Try to connect to camera")
    send("CONNECT", serial_conn)

def send(message, serial_conn, address=116):
    length = len(str(message))
    send_command = "AT+SEND=" + str(address) + "," + str(length) + "," + str(message) + "\r\n"
    serial_conn.write(str.encode(send_command))
    serial_payload = (serial_conn.readline())
    print("Send message: " + send_command)
    print("Message sent?", serial_payload.decode(encoding="utf-8"))
    #self.AT_command(f"AT+SEND={address},{length},{message}\r\n")


def wait_read(serial_conn):
    while True:
        serial_payload = serial_conn.readline()  # read data from serial port
        if len(serial_payload) > 0:
            try:
                payload = serial_payload.decode(encoding="utf-8")
                print(payload)
                
                command = payload.split(',')[-3]
                
                if command == "SUCCESS":
                    break 
                
            except UnicodeDecodeError:  # receiving corrupt data?
                logging.error("UnicodeDecodeError: {}".format(serial_payload))
            except IndexError:
                logging.error("IndexError: {}".format(payload))
            except ValueError:
                logging.error("ValueError: {}".format(payload))
                
                
def standby_mode(serial_conn):
    while True:
        user_input = input("ENTER COMMAND: ")
        
        if user_input == "1":
            send("UP", serial_conn)
            wait_read(serial_conn)
        elif user_input == "2":
            send("DOWN", serial_conn)
            wait_read(serial_conn)
        elif user_input == "3":
            send("LIGHT", serial_conn)
            wait_read(serial_conn)
        

if __name__ == "__main__":
    main()