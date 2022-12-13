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

player_vs_computer_game_scores = []
player_vs_player_game_scores = []


def register_player(socket, address):
    clients_sockets.append(socket)
    clients_addresses.append(address)
    print("Player connected...")
    send_message(socket, 'You are connected')
    send_message(socket, 'Waiting for any other player to connect...')


def send_message_to_all(message):
    for client_socket in clients_sockets:
        send_message(client_socket, message)


def send_message(client_socket, message):
    client_socket.send(message.encode('utf-8'))


def connect_players():
    print("Waiting for players to connect...")

    while True:    
        client_socket, client_address = server_socket.accept()

        register_player(client_socket, client_address)

        server_socket.settimeout(5)

        try:
            client_socket, client_address = server_socket.accept()

            register_player(client_socket, client_address)
            sleep(1)

            send_message_to_all("Player found. Game is starting...")
            server_socket.settimeout(None)
            start_game_between_two_players()
            break

        except socket.timeout:
            send_message(clients_sockets[0], 'Player not found. The game will start between you and the computer...')
            server_socket.settimeout(None)
            start_game_between_player_and_computer()
            break

def send_score(client_socket):
    best_score = min(player_vs_computer_game_scores)
    send_message(client_socket, 'Your best score is: ' + str(best_score))


def try_parse_int(value):
    try:
        return (int(value), True)
    except ValueError:
        return (value, False)


def handle_confirm_answer(message, client_socket, nr_of_tries):
    while True:
        if(message.upper() == 'EXIT'):
            handle_player_exit(client_socket)
            connect_players()
            return False
        
        if(message.upper() == 'Y'):
            player_vs_computer_game_scores.append(nr_of_tries)
            start_game_between_player_and_computer()

        elif(message.upper() == 'N'):
            player_vs_computer_game_scores.append(nr_of_tries)
            send_score(client_socket)
            handle_player_exit(client_socket)
            connect_players()
            return False

        else:
            send_message(client_socket, 'You must enter Y or N')


def handle_message(message, client_socket):
    while True:
        if(message.upper() == 'EXIT'):
            handle_player_exit(client_socket)
            connect_players()
            return False
        else:
            result = try_parse_int(message)

            if(result[1]):
                return handle_guess_message(result[0], client_socket)

            else:
                send_message(client_socket, 'You must enter a number between 1 and 50')
                message = client_socket.recv(1024).decode('utf-8')


def handle_player_exit(client_socket):
    clients_sockets.pop(0)
    player_vs_computer_game_scores.clear()
    client_socket.close()
    print('Player has exited the game. Server is waiting for new connections...')


def handle_players_exit():
    for client_socket in clients_sockets:
        client_socket.close()
        
    clients_sockets.clear()

    print('Player 1 has exited the game. Server is waiting for new connections...')
    print('Player 2 has exited the game. Server is waiting for new connections...')


def handle_guess_message(number, client_socket):
    while True:
        if(number > 0 and number < 51):
            return number
        else:
            send_message(client_socket, 'You must enter a number between 1 and 50')


def start_game_between_player_and_computer():
    print('Game is starting between player and computer...')

    client_socket = clients_sockets[0]
    nr_of_tries = 0

    send_message(client_socket, 'Computer is choosing a number between 1 and 50...\nComputer has chosen a number. Try to guess it...')
    random_number = random.randint(1, 50)

    while True:
        message = client_socket.recv(1024).decode('utf-8')
        number = handle_message(message, client_socket)

        if(number == False):
            break

        nr_of_tries += 1

        if(number == random_number):
            send_message(client_socket, 'You have guessed the number.\nDo you want to play again? (Y/N)')
            
            message = client_socket.recv(1024).decode('utf-8')
            confirm = handle_confirm_answer(message, client_socket, nr_of_tries)

            if(confirm == False):
                break

        elif(number > random_number):
            send_message(client_socket, 'The number is lower than the one you have chosen.')

        elif(number < random_number):
            send_message(client_socket, 'The number is higher than the one you have chosen.')


def start_game_between_two_players():
    nr_of_tries = 0
    print('Game is starting between two players...')

    client_socket_1 = clients_sockets[0]
    client_socket_2 = clients_sockets[1]

    send_message(client_socket_1, 'You will choose a number between 1 and 50.')
    send_message(client_socket_2, 'You will guess the number chosen by player 1.')

    message = client_socket_1.recv(1024).decode('utf-8')
    result = try_parse_int(message)
    number_choosen_by_player_1 = 0

    if(result[1]):
        number_choosen_by_player_1 = result[0]

    send_message(client_socket_2, 'Player 1 has chosen a number. Try to guess it...')

    while True:
        message = client_socket_2.recv(1024).decode('utf-8')
        number = int(message)
        nr_of_tries += 1

        if(number == number_choosen_by_player_1):
            send_message(client_socket_2, 'You have guessed the number.\nDo you want to play again? (Y/N)')
            send_message(client_socket_1, 'Player 2 has guessed the number.\nDo you want to play again? (Y/N)')
            
            message1 = client_socket_2.recv(1024).decode('utf-8')
            message2 = client_socket_1.recv(1024).decode('utf-8')

            if(message1.upper() == 'Y' and message2.upper() == 'Y'):
                player_vs_player_game_scores.append(nr_of_tries)
                start_game_between_two_players()
                break
            else:
                player_vs_player_game_scores.append(nr_of_tries)
                send_message_to_all("Not enough players to start a new game.\n" + "Best Score: " + str(min(player_vs_player_game_scores)))
                handle_players_exit()
                connect_players()
                break
            
        elif(number > number_choosen_by_player_1):
            send_message(client_socket_1, "Player 2 chose a number lower than the one you have chosen.")
            send_message(client_socket_2, 'The number is lower than the one you have chosen.')

        elif(number < number_choosen_by_player_1):
            send_message(client_socket_1, "Player 2 chose a number higher than the one you have chosen.")
            send_message(client_socket_2, 'The number is higher than the one you have chosen.')
    

connect_players()
