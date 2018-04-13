import sys
import socket
import threading, Queue

# from connected_game import game, game2
# from client_handler import handle, handleTwoPlayer

if not(len(sys.argv) == 2 or len(sys.argv) == 3):
    print("Incorrect Arguments")
    sys.exit()

#Handle clients
global clients
clients = []
global queue
queue = Queue.Queue()
global lock
lock = threading.Lock()

#Handle Two Players
thread2 = threading.Thread(target = handleTwoPlayer, args = (clients, lock))
thread2.start()

# Setup Socktet
sock = socket.socket()
if (len(sys.argv) == 3):
    host = sys.argv[2]
else:
    host = socket.gethostname()
port = int(sys.argv[1])

#Bind & Listen
sock.bind((host, port))
sock.listen(5)                 # Now wait for client connection.


while True:
   client, addr = sock.accept()     # Establish connection with client.
   print 'Got connection from', addr
   queue.put((client, addr))

   threadMain = threading.Thread(target = handle, args = (clients, lock, queue))
   threadMain.start()
