import logging
import time
from argparse import ArgumentParser
from datetime import datetime
from threading import *
import RPi.GPIO as GPIO

import serial


class LoRaController(Thread):

    # constants
    Address = 115
    Network = 6
    Port = "/dev/serial0"
    Serial = None
    
    ## Relay setups
    GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers

    ## Setup FPV power relay
    FPV_RELAY_GPIO = 17
    GPIO.setup(FPV_RELAY_GPIO, GPIO.OUT) # GPIO Assign mode
    GPIO.output(FPV_RELAY_GPIO, GPIO.LOW) # out


    def __init__(self):
        logging.basicConfig(filename='output.log', filemode='w', level=logging.DEBUG)
        
        Thread.__init__(self)

        print("Connecting to REYAX RYLR896 transceiver module…")
        self.Serial = serial.Serial(
            port="/dev/serial0",
            baudrate=115200,
            timeout=0.25,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )

        if self.Serial.isOpen():
            print("Serial port set up completed succesfully!") 

            #Set up and check lora connection
            self.set_lora_config()  
            self.check_lora_config()
            self.connect_to_camera()


    def set_lora_config(self):
        # configures the REYAX RYLR896 transceiver module

        self.Serial.write(str.encode("AT+ADDRESS=" + str(self.Address) + "\r\n"))
        serial_payload = (self.Serial.readline())
        print("Address set?", serial_payload.decode(encoding="utf-8"))

        self.Serial.write(str.encode("AT+NETWORKID=" + str(self.Network) + "\r\n"))
        serial_payload = (self.Serial.readline())
        print("Network Id set?", serial_payload.decode(encoding="utf-8"))


    def check_lora_config(self):
        # checks the configuration of the lora
        
        self.Serial.write(str.encode("AT?\r\n"))
        serial_payload = (self.Serial.readline())
        print("Module responding?", serial_payload.decode(encoding="utf-8"))

        self.Serial.write(str.encode("AT+ADDRESS?\r\n"))
        serial_payload = (self.Serial.readline())
        print("Address:", serial_payload.decode(encoding="utf-8"))

        self.Serial.write(str.encode("AT+NETWORKID?\r\n"))
        serial_payload = (self.Serial.readline())
        print("Network id:", serial_payload.decode(encoding="utf-8"))

        self.Serial.write(str.encode("AT+IPR?\r\n"))
        serial_payload = (self.Serial.readline())
        print("UART baud rate:", serial_payload.decode(encoding="utf-8"))

        self.Serial.write(str.encode("AT+BAND?\r\n"))
        serial_payload = (self.Serial.readline())
        print("RF frequency", serial_payload.decode(encoding="utf-8"))

        self.Serial.write(str.encode("AT+CRFOP?\r\n"))
        serial_payload = (self.Serial.readline())
        print("RF output power", serial_payload.decode(encoding="utf-8"))

        self.Serial.write(str.encode("AT+MODE?\r\n"))
        serial_payload = (self.Serial.readline())
        print("Work mode", serial_payload.decode(encoding="utf-8"))

        self.Serial.write(str.encode("AT+PARAMETER?\r\n"))
        serial_payload = (self.Serial.readline())
        print("RF parameters", serial_payload.decode(encoding="utf-8"))

    def connect_to_camera(self):
        connection = False
        while not connection: 
            print("Try to connect to camera")
            self.send("CONNECT")

            connection = self.wait_read()
            
            self.start_up_FPV()
            
    def start_up_FPV(self):
        GPIO.output(self.FPV_RELAY_GPIO, GPIO.HIGH) # out
        time.sleep(0.5)
        GPIO.output(self.FPV_RELAY_GPIO, GPIO.LOW) # on
        print("START UP FPV")

    def send(self, message, address=116):
        length = len(str(message))
        send_command = "AT+SEND=" + str(address) + "," + str(length) + "," + str(message) + "\r\n"
        self.Serial.write(str.encode(send_command))
        serial_payload = (self.Serial.readline())
        print("Send message: " + send_command)
        print("Message sent?", serial_payload.decode(encoding="utf-8"))

    def wait_read(self):
        start = datetime.now()
        while True:
            serial_payload = self.Serial.readline()  # read data from serial port
            if len(serial_payload) > 0:
                try:
                    payload = serial_payload.decode(encoding="utf-8")
                    print(payload)
                    
                    command = payload.split(',')[-3] if len(payload.split(',')) > 2 else None
                    
                    if command == "SUCCESS":
                        return True
                        
                    
                except UnicodeDecodeError:  # receiving corrupt data?
                    logging.error("UnicodeDecodeError: {}".format(serial_payload))
                except IndexError:
                    logging.error("IndexError: {}".format(payload))
                except ValueError:
                    logging.error("ValueError: {}".format(payload))

            if (datetime.now() - start).total_seconds() > 5: 
                return False
                    
                    
    def standby_mode(self, get_command, set_text):
        start = None
        while True:
            command = get_command()
            if command == "MOVE CAMERA UP":
                self.send("UP")
                if self.wait_read(): 
                    start = datetime.now()
                    set_text("Camera Moved Up")
                else:
                    start = datetime.now()
                    set_text("Error: Camera Not Responding, Try again")
            elif command == "MOVE CAMERA DOWN":
                self.send("DOWN")
                if self.wait_read():
                    start = datetime.now()
                    set_text("Camera Moved Down")
                else:
                    start = datetime.now()
                    set_text("Error: Camera Not Responding, Try again")
            elif command == "TOGGLE LIGHT":
                self.send("LIGHT")
                if self.wait_read():
                    start = datetime.now()
                    set_text("Light Toggled")
                else:
                    start = datetime.now()
                    set_text("Error: Camera Not Responding, Try again")
            
            if start and (datetime.now() - start).total_seconds() > 5: 
                set_text("")
                
        