# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 13:17:13 2024

@author: pcddi
"""

import serial
import time

class VelmaxMotor:
    def __init__(self, com_port):
        """Initialize the Velmax motor with the given COM port."""
        self.com_port = com_port
        self.total_movement = 0  # Track the total movement

    def move_motor(self, steps, delay=5):
        """Move Velmax motor a specified number of steps.
        
        Args:
            steps (int): The number of steps to move the motor.
            delay (int, optional): Time to wait for the motor to complete the movement. Default is 5 seconds.
        """
        # Initialization and open the port
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
                # Flush input and output buffers
                ser.flushInput()
                ser.flushOutput()
                
                # Send command to move the specified number of steps
                command = f"F,C,I2M{steps},R\r\n".encode('utf-8')
                ser.write(command)
                
                time.sleep(delay)  # Wait for the motor to complete the movement

                # Update the total movement
                self.total_movement += steps
                print(f"Moved successfully. Total movement: {self.total_movement}")

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
            self.total_movement = 0  # Reset total movement to zero after returning
            print("Returned to zero position.")
        else:
            print("Already at zero position.")

if __name__ == "__main__":
    motor = VelmaxMotor("COM3")
    motor.move_motor(-10000)  # Move the motor by 10000 steps
    motor.move_motor(5000)    # Move the motor by another 5000 steps
    motor.return_to_zero()    # Return to the zero position
