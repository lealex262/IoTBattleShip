import sys
import socket
import struct
import serial

if len(sys.argv) != 3:
    print("Incorrect Arguments")
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
    print ("Something's wrong with %s:%d. Exception is %s" % (address, port, e))
    sock.close()
    sys.exit()

# receive "ready to start" message
start_message = sock.recv(1024)
print start_message

# Init Game State
map = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 0], \
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0], \
    [0, 1, 0, 0, 0, 0, 0, 0, 1, 0], \
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0], \
    [0, 0, 0, 1, 1, 1, 0, 0, 1, 0], \
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0], \
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0], \
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], \
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
hit = 0
enemy_hit = 0
previous_aimed = list()

def your_turn():
    print "Your Turn"
    print "Target Row"
    input = raw_input()
    message = input.split('/')[0]
    print "Target Column"
    input = raw_input()
    message += input.split('/')[0]
    previous_aimed.append(message)
    message += str(hit) + str(0)
    sock.send(message)

while True:
    print "Your Map"
    for i in range(len(map)):
        print map[i]
    print "Previous aimed at"
    print previous_aimed
    print "You were hit " + str(enemy_hit) + " times"

    #receive server's packet
    receive_packet = sock.recv(1024)
    if receive_packet:
        print receive_packet

        if not "Game" in receive_packet:
            # Check if you win
            if receive_packet[3] == '1':
                print "Victory"
                break

            # Check if you hit them
            if receive_packet[2] == '1':
                print "Enemy Hit"
            else:
                print "You missed"

            # Check if you were hit
            x = int(receive_packet[0])
            y = int(receive_packet[1])
            if map[y][x] == 1:
                print "You were hit"
                map[y][x] = 0
                enemy_hit += 1
                hit = 1
            else:
                hit = 0

            # Check if you lose
            if enemy_hit >= 17:
                print "Defeat"
                sock.send("0001")
                break

        your_turn()

# Finished Game
sock.close
