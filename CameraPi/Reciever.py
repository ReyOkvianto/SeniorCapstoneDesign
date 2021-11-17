import logging
import time
from argparse import ArgumentParser
from datetime import datetime
import RPi.GPIO as GPIO
import board
import digitalio
from adafruit_motor import stepper
import serial
import drivers

## LoRa constants
ADDRESS = 116
NETWORK_ID = 6
CONNECTION_SET = False

## Relay setups
GPIO.setmode(GPIO.BCM) # GPIO Numbers instead of board numbers

## Setup camera power relay
CAMERA_RELAY_GPIO = 17
GPIO.setup(CAMERA_RELAY_GPIO, GPIO.OUT) # GPIO Assign mode
GPIO.output(CAMERA_RELAY_GPIO, GPIO.LOW) # out


## Setup FPV power relay
FPV_RELAY_GPIO = 27
GPIO.setup(FPV_RELAY_GPIO, GPIO.OUT) # GPIO Assign mode
GPIO.output(FPV_RELAY_GPIO, GPIO.LOW) # out


## Setup camera light relay
LIGHT_RELAY_GPIO = 22
GPIO.setup(LIGHT_RELAY_GPIO, GPIO.OUT) # GPIO Assign mode
GPIO.output(LIGHT_RELAY_GPIO, GPIO.LOW) # out

## Setup motor configuration
DELAY = 0.01
STEPS = 200
coils = (
     digitalio.DigitalInOut(board.D19),  # A1
     digitalio.DigitalInOut(board.D26),  # A2
     digitalio.DigitalInOut(board.D20),  # B1
     digitalio.DigitalInOut(board.D21),  # B2
)

for coil in coils:
    coil.direction = digitalio.Direction.OUTPUT

motor = stepper.StepperMotor(coils[0], coils[1], coils[2], coils[3], microsteps=None)


## Setup display
display = drivers.Lcd()

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
        
        #Wait to connect to the controller
        wait_connection(serial_conn)
        
        
        #Once connected succesfully, power up rest of system
        power_up_system()
        
        
        #Once everything is powered up wait for next commands
        wait_read(serial_conn)
        

            # time.sleep(2) # transmission frequency set on IoT device

def set_lora_config(serial_conn):
    # configures the REYAX RYLR896 transceiver module
    display.lcd_display_string("Setting up LoRa!", 1)
    
    #Set up lora address
    while True:
        serial_conn.write(str.encode("AT+ADDRESS=" + str(ADDRESS) + "\r\n"))
            
        serial_payload = serial_conn.readline()  # read data from serial port
        if len(serial_payload) > 0:
            try:
                
                print("Address set?", serial_payload.decode(encoding="utf-8"))
                
                if serial_payload.decode(encoding="utf-8") == "+OK\r\n":
                    display.lcd_display_string("Address set?" + serial_payload.decode(encoding="utf-8"), 2)
                    break
                
            except UnicodeDecodeError:  # receiving corrupt data?
                logging.error("UnicodeDecodeError: {}".format(serial_payload))

            except IndexError:
                logging.error("IndexError: {}".format(payload))
            except ValueError:
                logging.error("ValueError: {}".format(payload))

    #Set up network id
    while True:
        serial_conn.write(str.encode("AT+NETWORKID=" + str(NETWORK_ID) + "\r\n"))
            
        serial_payload = serial_conn.readline()  # read data from serial port
        if len(serial_payload) > 0:
            try:
                
                print("Network Id set?", serial_payload.decode(encoding="utf-8"))
                
                if serial_payload.decode(encoding="utf-8") == "+OK\r\n":
                    display.lcd_display_string("Network Id set?" + serial_payload.decode(encoding="utf-8"), 3)
                    break
            except UnicodeDecodeError:  # receiving corrupt data?
                logging.error("UnicodeDecodeError: {}".format(serial_payload))

            except IndexError:
                logging.error("IndexError: {}".format(payload))
            except ValueError:
                logging.error("ValueError: {}".format(payload))
                
    time.sleep(5)
    display.lcd_clear()


def check_lora_config(serial_conn):
    serial_conn.write(str.encode("AT?\r\n"))
    serial_payload = (serial_conn.readline())
    print("ModulLIGHT_RELAY_GPIOe responding?", serial_payload.decode(encoding="utf-8"))

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

def wait_connection(serial_conn):
    display.lcd_display_string("Connecting...", 1)
    while True:
        serial_payload = serial_conn.readline()  # read data from serial port
        if len(serial_payload) > 0:
            #try:
            payload = serial_payload.decode(encoding="utf-8")
            print(payload)
            
            command = payload.split(',')[-3]
            
            if command == "CONNECT":
                display.lcd_display_string("CONNECTED!!!", 2)
                send("CONNECTION CONFIRMED", serial_conn)
                time.sleep(5)
                display.lcd_clear()
                return
                

def power_up_system():
    start_up_camera()
    start_up_FPV()
    

def start_up_camera():
    GPIO.output(CAMERA_RELAY_GPIO, GPIO.HIGH) # out
    print("START UP CAMERA")
    

def start_up_FPV():
    GPIO.output(FPV_RELAY_GPIO, GPIO.HIGH) # out
    print("START UP FPV")
    

def wait_read(serial_conn):
    connection = CONNECTION_SET
    display.lcd_display_string("Waiting...", 1)
    while True:
        #Keep trying to confirm connected until command received
        if not connection:
            send("CONNECTION CONFIRMED", serial_conn)
            
        serial_payload = serial_conn.readline()  # read data from serial port
        if len(serial_payload) > 0:
            try:
                
                payload = serial_payload.decode(encoding="utf-8")
                print(payload)
                
                command = payload.split(',')[-3]
                
                if command == "UP":
                    connection = True
                    print("MOVE CAMERA UP")
                    display.lcd_display_string("MOVE CAMERA UP!!!", 2)
                    move_camera_up()
                    send("SUCCESS", serial_conn)
                    display.lcd_clear()
                    
                elif command == "DOWN":
                    connection = True
                    print("MOVE CAMERA  DOWN")
                    display.lcd_display_string("!!", 2)
                    move_camera_down()
                    send("SUCCESS", serial_conn)
                    display.lcd_clear()
                    
                elif command == "LIGHT":
                    connection = True
                    print("TOGGLE LIGHT")
                    display.lcd_display_string("TOGGLE LIGHT!!!", 2)
                    toggle_light()
                    send("SUCCESS", serial_conn)
                    display.lcd_clear()
                
                elif command == "CONNECT":
                    connection = False
                    print("CONNECTION SET")
                    display.lcd_display_string("CONNECTED AGAIN!!!", 2)
                    send("CONNECTION CONFIRMED", serial_conn)
                    display.lcd_clear()
                    
            except UnicodeDecodeError:  # receiving corrupt data?
                logging.error("UnicodeDecodeError: {}".format(serial_payload))

            except IndexError:
                logging.error("IndexError: {}".format(payload))
            except ValueError:
                logging.error("ValueError: {}".format(payload))
                

def toggle_light():
    GPIO.output(LIGHT_RELAY_GPIO, GPIO.HIGH) # out
    time.sleep(0.5)
    GPIO.output(LIGHT_RELAY_GPIO, GPIO.LOW) # on
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