# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 15:50:01 2024

@author: pcddi
"""

import serial
import time

class VelmaxMotor:
    def __init__(self, com_port):
        """Initialize the Velmax motor with the given COM port."""
        self.com_port = com_port

    def send_command(self, command, delay=5):
        """Send a command to the motor and wait for the specified delay."""
        ser = serial.Serial()

        ser.port = self.com_port  # Set the COM port
        ser.baudrate = 9600
        ser.bytesize = serial.EIGHTBITS
        ser.parity = serial.PARITY_NONE
        ser.stopbits = serial.STOPBITS_ONE
        ser.timeout = 5
        ser.xonxoff = False
        ser.rtscts = False
        ser.dsrdtr = False
        ser.writeTimeout = 2

        try:
            ser.open()
            print(f"Serial port {ser.port} opened successfully.")
            # Flush input and output buffers
            ser.flushInput()
            ser.flushOutput()
            
            # Send command
            ser.write(command.encode('utf-8'))  # Encode the command here
            time.sleep(delay)  # Wait for the motor to complete the movement

        except Exception as e:
            print("Error communicating: " + str(e))
        finally:
            ser.close()

    def home_motor(self, motor_number=2):
        """Move the motor to the negative limit (home position)."""
        print(f"Homing motor {motor_number} to the leftmost position...")
        command = f"F,C,I{motor_number}M0,R\r\n"  # Create command for the specified steps (already a string)
        self.send_command(command)

    def move_to_left(self, motor_number=2):
        """Move the motor to the leftmost position (home)."""
        print(f"Moving motor {motor_number} to the leftmost position...")
        self.home_motor(motor_number)

    def move_to_right(self, motor_number=2):
        """Move the motor to the rightmost position."""
        print(f"Moving motor {motor_number} to the rightmost position...")
        command = f"F,C,{motor_number}M-0,R\r\n"  # Create command for the specified steps (already a string)
        self.send_command(command)

if __name__ == "__main__":
    motor = VelmaxMotor("COM3")
    motor.move_to_left()   # Move the motor to the leftmost position
    motor.move_to_right()  # Move the motor to the rightmost position
