import socket
import random
from time import sleep

HOST = '127.0.0.1'
PORT = 5001

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(2)

clients_sockets = []
clients_addresses = []

def register_player(socket, address):
    clients_sockets.append(socket)
    clients_addresses.append(address)
    send_message(socket, 'You are connected')
    send_message(socket, 'Waiting for any other player to connect...')

def send_message_to_all(message):
    for client_socket in clients_sockets:
        send_message(client_socket, message)

def send_message(client_socket, message) :
    client_socket.send(message.encode('utf-8'))

def connect_players():
    while True:    
        client_socket, client_address = server_socket.accept()

        register_player(client_socket, client_address)

        server_socket.settimeout(5)

        try:
            client_socket, client_address = server_socket.accept()

            register_player(client_socket, client_address)

            sleep(2)

            send_message_to_all("Player found. Game is starting...")
            
            start_game_between_two_players()
            break

        except socket.timeout:
            send_message(clients_sockets[0], 'Player not foound. The game will start between you and the computer...')

            start_game_between_player_and_computer()
            break

def send_score():
    print('Sending score...')

def start_game_between_player_and_computer():
    print('Game is starting between player and computer...')
    client_socket = clients_sockets[0]
    
    send_message(client_socket, 'Computer is choosing a number between 1 and 50...')
    random_number = random.randint(1, 50)
    sleep(1)
    send_message(client_socket, 'Computer has chosen a number. Try to guess it...')

    while True:
        message = client_socket.recv(1024).decode('utf-8')
        number = int(message)

        if message == 'EXIT':
            break

        if(number == random_number):
            send_message(client_socket, 'You have guessed the number.\nDo you want to play again? (Y/N)')
            message = client_socket.recv(1024).decode('utf-8')

            if(message == 'Y'):
                start_game_between_player_and_computer()
            else:
                send_score()
            break
        elif(number > random_number):
            send_message(client_socket, 'The number is lower than the one you have chosen.')

        elif(number < random_number):
            send_message(client_socket, 'The number is higher than the one you have chosen.')


def start_game_between_two_players():
    print('Game is starting between two players...')



connect_players()
