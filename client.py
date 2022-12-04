import socket

HOST = '127.0.0.1'
PORT = 5001

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def connect_player():
    client_socket.connect((HOST, PORT))

    while True:
        message = client_socket.recv(1024).decode('utf-8')
        print(message)

        if(message == 'Player not foound. The game will start between you and the computer...'):
            start_game_between_player_and_computer()    
            break

def get_input():
    while True:
        input_number = input("Your guess: ")

        if(isinstance(int(input_number), int) and int(input_number) >= 1 and int(input_number) <= 50):
            return input_number
        else:
            print("You must enter a number between 1 and 50")


def start_game_between_player_and_computer():

    while True:
        message = client_socket.recv(1024).decode('utf-8')
        print(message)

        if(message == 'Computer has chosen a number. Try to guess it...'):
            while True:
                input_number = get_input()
                client_socket.send(input_number.encode('utf-8'))
                message = client_socket.recv(1024).decode('utf-8')
                print(message)

                if(message == 'You have guessed the number.\nDo you want to play again? (Y/N)'):
                    input_answer = input("Your answer: ")
                    client_socket.send(input_answer.encode('utf-8'))

                    if(input_answer == 'Y'):
                        start_game_between_player_and_computer()
                    else:
                        break
           
connect_player()
