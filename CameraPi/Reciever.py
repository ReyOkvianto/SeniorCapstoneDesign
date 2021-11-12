import logging
import time
from argparse import ArgumentParser
from datetime import datetime
import RPi.GPIO as GPIO
import board
import digitalio
from adafruit_motor import stepper
import serial

# LoRaWAN IoT Sensor Demo
# Using REYAX RYLR896 transceiver modules
# Author: Gary Stafford
# Requirements: python3 -m pip install –user -r requirements.txt
# To Run: python3 ./rasppi_lora_receiver.py –tty /dev/ttyAMA0 –baud-rate 115200

# constants
ADDRESS = 116
NETWORK_ID = 6
CONNECTION_SET = False

GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers
RELAIS_1_GPIO = 17
GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode
GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # out

DELAY = 0.01
STEPS = 200

# To use with a Raspberry Pi:
coils = (
     digitalio.DigitalInOut(board.D19),  # A1
     digitalio.DigitalInOut(board.D26),  # A2
     digitalio.DigitalInOut(board.D20),  # B1
     digitalio.DigitalInOut(board.D21),  # B2
)

for coil in coils:
    coil.direction = digitalio.Direction.OUTPUT

motor = stepper.StepperMotor(coils[0], coils[1], coils[2], coils[3], microsteps=None)

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
        set_lora_config(serial_conn)
        check_lora_config(serial_conn)
        
        wait_read(serial_conn)
        

            # time.sleep(2) # transmission frequency set on IoT device

def set_lora_config(serial_conn):
    # configures the REYAX RYLR896 transceiver module

    serial_conn.write(str.encode("AT+ADDRESS=" + str(ADDRESS) + "\r\n"))
    serial_payload = (serial_conn.readline())
    print("Address set?", serial_payload.decode(encoding="utf-8"))

    serial_conn.write(str.encode("AT+NETWORKID=" + str(NETWORK_ID) + "\r\n"))
    serial_payload = (serial_conn.readline())
    print("Network Id set?", serial_payload.decode(encoding="utf-8"))


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

def send(message, serial_conn, address=115):
    length = len(str(message))
    send_command = "AT+SEND=" + str(address) + "," + str(length) + "," + str(message) + "\r\n"
    serial_conn.write(str.encode(send_command))
    serial_payload = (serial_conn.readline())
    print("Send message: " + send_command)
    print("Message sent?", serial_payload.decode(encoding="utf-8"))

def wait_read(serial_conn):
    while True:
        serial_payload = serial_conn.readline()  # read data from serial port
        if len(serial_payload) > 0:
            try:
                payload = serial_payload.decode(encoding="utf-8")
                print(payload)
                
                command = payload.split(',')[-3]
                
                if command == "CONNECT":
                    CONNECTION_SET = True
                    send("SUCCESS", serial_conn)
                    
                elif command == "UP":
                    print("MOVE CAMERA UP")
                    move_camera_up()
                    send("SUCCESS", serial_conn)
                    
                elif command == "DOWN":
                    print("MOVE CAMERA DOWN")
                    move_camera_down()
                    send("SUCCESS", serial_conn)
                    
                elif command == "LIGHT":
                    print("TOGGLE LIGHT")
                    toggle_light()
                    send("SUCCESS", serial_conn)
                    
            except UnicodeDecodeError:  # receiving corrupt data?
                logging.error("UnicodeDecodeError: {}".format(serial_payload))

            except IndexError:
                logging.error("IndexError: {}".format(payload))
            except ValueError:
                logging.error("ValueError: {}".format(payload))
                

def toggle_light():
    GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # out
    time.sleep(0.5)
    GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # on
    print("TOGGLED LIGHT")
    
def move_camera_down():
    print("MOVE MOTOR DOWN")
    for step in range(STEPS):
        motor.onestep(style=stepper.DOUBLE)
        time.sleep(DELAY)
        
def move_camera_up():
    print("MOVE MOTOR UP")
    for step in range(STEPS):
        motor.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
        time.sleep(DELAY)

if __name__ == "__main__":
    main()