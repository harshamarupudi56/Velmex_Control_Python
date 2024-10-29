# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 13:17:13 2024

@author: pcddi
"""

import serial
import time

# Negative moves stage up 
# Positive moves stage down 
# Axis 2 to move motor vertically 
# 1 step = 0.005 mm 

class VelmexMotorController:
    def __init__(self, com_port, axis=2, home_position=0, baudrate=9600, timeout=5):
        self.com_port = com_port
        self.axis = axis  # Specify the axis (2 by default)
        self.baudrate = baudrate
        self.timeout = timeout
        self.home_position = home_position  # Define the home position (e.g., 0 steps)
        self.current_position = 0  # Track the current position of the motor
        self.ser = None  # Serial object, initialized later

    def connect(self):
        """Initialize and open the serial port."""
        self.ser = serial.Serial()
        self.ser.port = self.com_port
        self.ser.baudrate = self.baudrate
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.timeout = self.timeout
        self.ser.xonxoff = False
        self.ser.rtscts = False
        self.ser.dsrdtr = False
        self.ser.writeTimeout = 2

        try:
            self.ser.open()  # Attempt to open the serial port
            print(f"Serial port {self.ser.port} opened successfully.")
        except Exception as e:
            print(f"Error opening serial port: {e}")
            return False
        return True

    def disconnect(self):
        """Close the serial port."""
        if self.ser and self.ser.isOpen():
            self.ser.close()
            print(f"Serial port {self.ser.port} closed.")
    
    def move(self, cm, delay=5):
        """Move the motor a specified distance in centimeters on the specified axis, with delay."""
        if not self.ser or not self.ser.isOpen():
            print("Serial port not open.")
            return
        
        # Convert centimeters to steps  
        steps = int(cm * 2000)  # 1 cm = 2000 steps 
        direction = 1 if steps > 0 else -1  # Determine direction of movement
        
        try:
            # Flush input and output buffers
            self.ser.flushInput()
            self.ser.flushOutput()

            # Send command to move the motor on the specified axis
            command = f"F,C,S{self.axis}M{1000},I{self.axis}M{steps},R\r\n".encode('utf-8')
            self.ser.write(command)

            time.sleep(delay)  # Wait for the motor to complete the movement
            self.current_position += steps  # Update the current position

        except Exception as e1:
            print(f"Error communicating: {e1}")
        
        print(f"Moved: {cm} centimeters")

    def go_home(self, delay=5):
        """Move the motor back to the home position on the specified axis."""
        # Send command to move the motor on the specified axis
        command = f"F,C,I{self.axis}M0,R\r\n".encode('utf-8')
        self.ser.write(command)
        time.sleep(delay)  # Wait for the motor to complete the movement
        self.current_position = 0  # Update the current position

    def initialize(self):
        """Move to home position initially to ensure consistent starting point."""
        print(f"Homing the motor on axis {self.axis}...")
        self.go_home()  # Start by going to the home position
    
if __name__ == "__main__":
    # Initialize motor controller for axis 2
    motor = VelmexMotorController(com_port="COM3", axis=2)
    
    # Connect to the motor
    if motor.connect():
        motor.initialize()  # Home the motor initially
        time.sleep(5)
        
        motor.move(-20, delay=1)  # Move motor -20 cm on axis 2
        
        # Disconnect after operations
        motor.disconnect()

