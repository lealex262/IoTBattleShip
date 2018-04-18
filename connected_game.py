# Handles client and server interactions
# Should be opened in a new thread
import random
import struct
import sys
import thread

def game(client1, addr1, client2, addr2, clients, lock):
    # send client the initial state
    packet1 = struct.pack('b26s', 26, 'Game Starting!\nYour Turn!')
    client1.send(packet1)
    packet2 = struct.pack('b38s', 38, 'Game Starting!\nWaiting for Player1...')
    client2.send(packet2)

    message_receiver = [client1, client2]
    count = 0
    while True:
        client = message_receiver[count % 2]
        receive_packet = client.recv(1024)
        if receive_packet:
            #unpack and get client_guess
            m = struct.unpack_from(b'b',receive_packet)
            m = struct.unpack_from(b'b'+str(m[0])+'s',receive_packet)
            client_guess = m[1]

            # If Hit
            if my_game.invalidGuess(client_guess):
                send_packet = struct.pack('b31s', 31, 'Error! Please guess one letter!')
                client.send(send_packet)

            # If Miss
            else:
                #do the guess operation
                result = my_game.guess(client_guess)

                #check if the client has won
                #TODO: send you lose to the other client
                if my_game.win():
                    send_packet = struct.pack('b'+str(35 + len(my_game.word))+'s', 35 + len(my_game.word), 'The word was ' + my_game.word +'\nYou Win!\nGame Over!')
                    client.send(send_packet)
                    message_receiver[(count + 1) % 2].send(send_packet)
                    break
                #check if game over
                elif my_game.gameOver():
                    send_packet = struct.pack('b'+str(35 + len(my_game.word))+'s', 35 + len(my_game.word), 'The word was ' + my_game.word +'\nYou lost\nGame Over!')
                    client.send(send_packet)
                    message_receiver[(count + 1) % 2].send(send_packet)
                    break
                #print corret and waiting message to the player
                elif result is True:
                    send_packet = struct.pack('b' + str(37+len(str(2-count % 2))) + 's', 35+len(str(2-count % 2)), 'Correct!\nWaiting on Player ' + str(2-count % 2) + '...')
                    client.send(send_packet)
                #print incorrect and waiting message to the player
                elif result is False:
                    send_packet = struct.pack('b' + str(39+len(str(2-count % 2))) + 's', 37+len(str(2-count % 2)), 'Incorrect!\nWaiting on Player ' + str(2-count % 2) + '...')
                    client.send(send_packet)
                #switch to another player
                count += 1
                #return your turn and incorrectGuesses to the other player
                turn_packet = struct.pack('b10s', 10, 'Your Turn!')
                message_receiver[count % 2].send(turn_packet)
                send_packet = struct.pack('bbb'+ str(my_game.word_length + len(my_game.incorrectGuesses)) + 's', 0, my_game.word_length, len(my_game.incorrectGuesses), ''.join(my_game.hiddenWord) + ''.join(my_game.incorrectGuesses))
                message_receiver[count % 2].send(send_packet)

    client1.close()
    client2.close()             # Close the connection
    thread.exit()
