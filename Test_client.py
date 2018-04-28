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

while True:
    #receive server's packet
    receive_packet = sock.recv(1024)
    if receive_packet:
        ## m = struct.unpack_from(b'b',receive_packet)
        ## #if it is only message packet
        ## if m[0] != 0:
        ##     m = struct.unpack_from(b'b'+str(m[0])+'s',receive_packet)
        ##     print m[1]
        ##     # if it is invalid guess
        ##     if 'Error' in m[1]:
        ##         print 'Letter to guess: ',
        ##         client_guess = raw_input()
        ##         send_packet = struct.pack('b'+str(len(client_guess))+'s', len(client_guess), client_guess)
        ##         sock.send(send_packet)
        ##     # if the game is over
        ##     elif 'Over' in m[1]:
        ##         break
        ## else:
        ##     # unpack the client's packet
        ##     m = struct.unpack_from(b'bbb', receive_packet)
        ##     word_length = m[1]
        ##     num_incorrect = m[2]
        ##     m = struct.unpack_from(b'bbb'+str(word_length + num_incorrect)+'s', receive_packet)
        ##     return_string = m[3]
        ##     print return_string[:word_length]
        ##     print "Incorrect Guesses: " + return_string[word_length:]
        ##     print
        ##     print 'Letter to guess: ',
        ## 
        ##     # input guess word and send the client packet to the server
        ##     client_guess = raw_input()
        ##     send_packet = struct.pack('b'+str(len(client_guess))+'s', len(client_guess), client_guess)
            print "receive Packet - " + receive_packet
            message = raw_input()
            sock.send(message.split('/')[0])

# Finished Game
sock.close
