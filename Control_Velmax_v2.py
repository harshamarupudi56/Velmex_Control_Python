#!/usr/bin/python

import serial
import time

def move_velmax_motor(com_port, steps, delay=5):
    """Move Velmax motor a specified number of steps.
    
    Args:
        com_port (str): The COM port to which the Velmex motor is connected.
        steps (int): The number of steps to move the motor.
        delay (int, optional): Time to wait for the motor to complete the movement. Default is 5 seconds.
    """
    
    # Initialization and open the port
    ser = serial.Serial()

    ser.port = com_port  # Set the COM port
    ser.baudrate = 9600
    ser.bytesize = serial.EIGHTBITS  # Number of bits per byte
    ser.parity = serial.PARITY_NONE  # Set parity check: no parity
    ser.stopbits = serial.STOPBITS_ONE  # Number of stop bits
    ser.timeout = 5  # Timeout for read operations (in seconds)
    ser.xonxoff = False  # Disable software flow control
    ser.rtscts = False  # Disable hardware (RTS/CTS) flow control
    ser.dsrdtr = False  # Disable hardware (DSR/DTR) flow control
    ser.writeTimeout = 2  # Timeout for writing (in seconds)

    try:
        ser.open()  # Attempt to open the serial port
        print(f"Serial port {ser.port} opened successfully.")
    except Exception as e:
        print("Error opening serial port: " + str(e))
        return

    if ser.isOpen():
        try:
            # Flush input and output buffers
            ser.flushInput()
            ser.flushOutput()
            
            # Send command to trigger motor 2 move the specified number of steps
            command = f"F,C,I2M{steps},R\r\n".encode('utf-8')  # Create command for the specified steps
            ser.write(command)  # Send command
            
            time.sleep(delay)  # Give the device time to process the command (increase if needed)

            ser.close()  # Close the serial port after communication
            print("Moved successfully.")

        except Exception as e1:
            print("Error communicating: " + str(e1))
        finally:
            ser.close()  # Ensure the serial port is closed on exit
    else:
        print("Cannot open serial port.")

#Negative moves to right, positive moves left 
if __name__ == "__main__":
    move_velmax_motor("COM3", 8000) 

