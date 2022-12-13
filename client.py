import socket

HOST = '127.0.0.1'
PORT = 5001

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def connect_player():
    client_socket.connect((HOST, PORT))

    while True:
        message = client_socket.recv(1024).decode('utf-8')
        print(message)

        if(message == 'Player not found. The game will start between you and the computer...'):
            start_game_between_player_and_computer()
            break

        elif(message == 'Player found. Game is starting...'):
            start_game_between_two_players()          
            break

def try_parse_int(value):
    try:
        return (int(value), True)
    except ValueError:
        return (value, False)


def get_guess_input():
    while True:
        input_number = input("Your guess: ")

        if(input_number.upper() == 'EXIT'):
            handle_player_exit()
        else:
            result = try_parse_int(input_number)

            if(result[1] and result[0] > 0 and result[0] < 51):
                return result[0]
            else:
                print("You must enter a number between 1 and 50")


def get_answer_input():
    while True:
        input_answer = input("Your answer: ")

        if(input_answer.upper() == 'EXIT'):
            handle_player_exit()

        elif(input_answer.upper() == 'Y' or input_answer.upper() == 'N'):
            return input_answer
        else:
            print("You must enter Y or N")


def send_message(client_socket, message):
    client_socket.send(message.encode('utf-8'))


def handle_guess_message():
    input_number = get_guess_input()
    send_message(client_socket, str(input_number))

    message = client_socket.recv(1024).decode('utf-8')
    return message


def handle_confirm_answer(callback, type_of_game = ""):

    while True:
        message = get_answer_input().upper()

        if(message == 'Y'):
            send_message(client_socket, message)

            if(type_of_game == 'pvp'):
                message = client_socket.recv(1024).decode('utf-8')
                print(message)
                print(message)
                handle_player_exit()

            callback()

        elif(message == 'N'):
            send_message(client_socket, message)
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
            handle_player_exit()
    
        else:
            print("You must enter Y or N")


def handle_player_exit():
    send_message(client_socket, 'EXIT')
    client_socket.close()
    print('You have exited the game.')
    exit(0)

def start_game_between_player_and_computer():
    while True:
        message = client_socket.recv(1024).decode('utf-8')
        print(message)

        if(message == 'Computer is choosing a number between 1 and 50...\nComputer has chosen a number. Try to guess it...'):
            while True:
                message = handle_guess_message()
                print(message)

                if(message == 'You have guessed the number.\nDo you want to play again? (Y/N)'):
                    handle_confirm_answer(start_game_between_player_and_computer)



def start_game_between_two_players():
    while True:
        message = client_socket.recv(1024).decode('utf-8')
      
        if(message == 'You will choose a number between 1 and 50.'):
            play_role_1(message)
            break

        if(message == 'You will guess the number chosen by player 1.'):
            play_role_2(message)
            break

def play_role_1(message):
    print(message)

    choise = input("Your choise: ")

    send_message(client_socket, choise)

    while True:
        message = client_socket.recv(1024).decode('utf-8')
        print(message)

        if(message == 'Player 2 has guessed the number.\nDo you want to play again? (Y/N)'):
            handle_confirm_answer(start_game_between_two_players, "pvp")


def play_role_2(message):
    print(message)

    message = client_socket.recv(1024).decode('utf-8')
    print(message)

    while True:
        message = handle_guess_message()
        print(message)

        if(message == 'You have guessed the number.\nDo you want to play again? (Y/N)'):
            handle_confirm_answer(start_game_between_two_players, "pvp")


connect_player()