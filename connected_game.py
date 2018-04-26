# Handles client and server interactions
# Should be opened in a new thread
import random
import struct
import sys
import thread

def game(client1, addr1, client2, addr2, lock):
    # send client the initial state
    packet1 = struct.pack('b26s', 26, 'Game Starting!\nYour Turn!')
    client1.send(packet1)
    packet2 = struct.pack('b38s', 38, 'Game Starting!\nWaiting for Player1...')
    client2.send(packet2)

    message_receiver = [client1, client2]
    count = 0
    while True:
        client1 = message_receiver[count % 2]
        client2 = message_receiver[(count + 1) % 2]
        receive_packet = client1.recv(1024)
        if receive_packet:
            client2.send(receive_packet)

            #switch to another player
            count += 1


    client1.close()
    client2.close()             # Close the connection
    thread.exit()
