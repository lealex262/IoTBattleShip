import sys
import socket
import struct
import serial
import time

# Connect to mbed
try:
    ser = serial.Serial(
        port='COM6',\
        baudrate=9600,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
        timeout=None
        )
except Exception as e:
    print "Serial port failed to connect"
    sys.exit()

if len(sys.argv) != 3:
    print "Incorrect Arguments"
    sys.exit()

# Create a socket object
sock = socket.socket()

# Host
if sys.argv[1] == "local":
    # Get local machine name
    host = socket.gethostname()
else:
    host = sys.argv[1]

# Port Number - Reserve for your service.
port = int(sys.argv[2])

# Connect to Game Server
try:
    sock.connect((host, port))
except Exception as e:
    print("Something's wrong with %s:%d. Exception is %s" % (address, port, e))
    sock.close()
    sys.exit()

# receive "ready to start" message
start_message = sock.recv(1024)
print start_message
if 'another' in start_message:
    # player 1
    ser.write('abcd')
else:
    #player 2
    ser.write('efgh')

while True:
    #receive server's packet
    receive_packet = sock.recv(1024)
    if receive_packet:
        if not "Game" in receive_packet:
            print receive_packet
            ser.write(receive_packet)

        # Send packet
        time.sleep(0.1)
        message = ser.read(4)
        print "message = " + message
        sock.send(message)

# Finished Game
sock.close
ser.close()
