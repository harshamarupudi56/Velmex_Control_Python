# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 14:57:39 2024

@author: pcddi
"""

import serial
import time

class VelmaxMotor:
    def __init__(self, com_port):
        """Initialize the Velmax motor with the given COM port."""
        self.com_port = com_port
        self.total_movement = 0  # Track the total movement
        self.encoder_position = 0  # Track the current encoder position
        self.is_homed = False  # Track whether the motor is homed

    def read_encoder(self):
        """Read the current position from the encoder."""        
        print(f"Current Encoder Position: {self.encoder_position}")  # Print the position

    def move_motor(self, steps, delay=5):
        """Move Velmax motor a specified number of steps."""
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
        except Exception as e:
            print("Error opening serial port: " + str(e))
            return

        if ser.isOpen():
            try:
               
                ser.flushInput()
                ser.flushOutput()
                
                command = f"F,C,I2M{steps},R\r\n".encode('utf-8')
                ser.write(command)
                
                time.sleep(delay)  

                self.total_movement += steps
                self.encoder_position += steps  
                print(f"Moved successfully. Total movement: {self.total_movement}")
                self.read_encoder()  #
            except Exception as e1:
                print("Error communicating: " + str(e1))
            finally:
                ser.close()
        else:
            print("Cannot open serial port.")

    def return_to_zero(self, delay=5):
        """Return the motor to the zero position by moving the total distance back."""
        if self.total_movement != 0:
            self.move_motor(-self.total_movement, delay)
            self.total_movement = 0  
            self.encoder_position = 0  
            print("Returned to zero position.")
        else:
            print("Already at zero position.")

    def home_motor(self):
        """Homing procedure to find the home position."""
        print("Homing motor...")
        while not self.is_homed:
            self.move_motor(-100) 
            self.read_encoder()           
            if self.encoder_position <= 0:  
                self.is_homed = True
                self.total_movement = 0  
                self.encoder_position = 0  
                print("Homing complete.")
                break

if __name__ == "__main__":
    motor = VelmaxMotor("COM3")
    motor.home_motor()  # Home the motor
    motor.move_motor(10000) # Move the motor by 10000 steps
    motor.move_motor(5000)  # Move the motor by another 5000 steps
    motor.return_to_zero()  # Return to the zero position
