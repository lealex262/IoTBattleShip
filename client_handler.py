import sys
import socket
import threading, Queue
import struct

from connected_game import game

def handle(clients, lock, queue):
    if not queue.empty() and len(clients) < 3:
        client, addr = queue.get()

        #If client wants multiple players
        clients.append((client, addr))

        player1 = None
        player2 = None
        for each_client in clients:
            if not player1:
                player1 = each_client
            elif not player2:
                player2 = each_client

        if player1 and player2:
            clients.remove(player1)
            clients.remove(player2)
            thread_game = threading.Thread(target = game, args = (player1[0], player1[1], player2[0], player2[1], lock))
            thread_game.start()
        else:
            packet = struct.pack('b27s', 27, 'Waiting for another player!')
            client.send(packet)
