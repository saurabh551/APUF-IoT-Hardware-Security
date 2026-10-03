# fpga_puf_uart.py
import serial
import time

PORT = "/dev/ttyUSB1"
BAUD = 9600
TIMEOUT = 5.0

class FPGA_PUF:
    def __init__(self):
        self.ser = serial.Serial(PORT, BAUD, timeout=1)
        time.sleep(1)  # allow UART to settle

    def hex_to_bytes(self, hexstr):
        return bytes.fromhex(hexstr)

    def get_response(self, challenge_hex):
        """
        Sends 64-bit challenge (8 bytes) to FPGA
        Receives 1-byte response (0 or 1)
        """
        ch_bytes = self.hex_to_bytes(challenge_hex)

        self.ser.reset_input_buffer()
        self.ser.write(ch_bytes)
        self.ser.flush()

        start = time.time()
        while (time.time() - start) < TIMEOUT:
            b = self.ser.read(1)
            if b:
                try:
                    # ASCII '0' / '1'
                    s = b.decode('ascii', errors='ignore')
                    if s in ('0', '1'):
                        return int(s)
                except:
                    pass

                # Raw byte 0x00 / 0x01
                return int.from_bytes(b, 'big')

        # Timeout
        return None

    def close(self):
        self.ser.close()
