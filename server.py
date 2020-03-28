import zmq
import time
import json
from game import Board, Player, Team


def parse_msg(msg, game):
    print("Message :")
    print(msg)
    command = msg["command"]
    if command == 'join_game':
        result_msg = game.join_game(msg["username"])
    elif command == 'start_game':
        result_msg = game.start_game()
    elif command == 'stop_game':
        print('TODO: stop game')
    elif command == 'draw_card':
        print('TODO: play card')
    elif command == 'give_clue':
        print('TODO: give a clue')
    elif command == 'discard_card':
        print('TODO: discard a card')

    game_dic = game.to_dic()
    game_dic["result"] = result_msg
    return game_dic

def main():

    # create context for all sockets
    context = zmq.Context()

    # open request reply socket on port 5555
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    # open publisher on port 6666
    # pub_socket = context.socket(zmq.PUB)
    # socket.bind("tcp://*:6666")

    # create a game
    game = Game()

    while True:
        #  Wait for next request from client
        message = socket.recv_json()
        print("Received request: %s" % message)

        #  Parse and process message
        time.sleep(0.1)
        game_dic = parse_msg(message, game)

        print(json_str)
        #  Send reply back to client
        socket.send_json(game_dic)

        # publish game
        #sub_socket.send_string(json_str)


if __name__ == "__main__":
    # execute only if run as a script
    main()