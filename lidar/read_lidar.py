import serial
import serial.tools.list_ports
import settings

class ReadLidar:
    def __init__(self, port, baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.measurement = 0


    @staticmethod
    def list_arduino_ports():
        ports = serial.tools.list_ports.comports()
        arduino_ports = []

        for port in ports:
            if "usbserial" in port.device:
                arduino_ports.append(port.device)

        return arduino_ports


    def open_port(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)

            print(f"Opened serial port {self.port} at {self.baudrate} baud")
        except serial.SerialException as e:
            print(f"Failed to open serial port: {e}")


    def close_port(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print(f"Closed serial port {self.port}")


    def read_lidar(self):
        if not self.ser or not self.ser.is_open:
            print("Serial port not open")
            return
        try:
            while self.measurement != -1:
                if self.ser.in_waiting > 0:
                    line = self.ser.readline().decode('utf-8', errors='replace').strip()
                    if line.isnumeric():
                        self.measurement = int(line)
                    else:
                        self.measurement = -2
                
        except KeyboardInterrupt:
            print("Stopping read due to keyboard interrupt.")
        except Exception as e:
            print(f"Error reading from serial: {e}")
        finally:
            self.close_port()