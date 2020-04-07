import zmq
import time
import json
from game import Game


def parse_msg(msg, game):
    print("Message :")
    print(msg)
    command = msg["command"]
    if command == 'join_game':
        result_msg = game.join_game(msg["username"])
    elif command == 'start_game':
        result_msg = game.start_game()
    elif command == 'finish_game':
        result_msg = game.finish_game()
    elif command == 'play_card':
        result_msg = game.play_card(msg["player"])
        # result_msg = {'board': {'stack_dic': {'r': [], 'b': [{'color': 'b', 'value': 1, 'selected': False}], 'y': [], 'g': [], 'w': []}, 'draw_list': [{'color': 'y', 'value': 4, 'selected': False}, {'color': 'b', 'value': 1, 'selected': False}, {'color': 'w', 'value': 5, 'selected': False}, {'color': 'g', 'value': 2, 'selected': False}, {'color': 'y', 'value': 2, 'selected': False}, {'color': 'b', 'value': 2, 'selected': False}, {'color': 'y', 'value': 2, 'selected': False}, {'color': 'g', 'value': 3, 'selected': False}, {'color': 'b', 'value': 3, 'selected': False}, {'color': 'r', 'value': 1, 'selected': False}, {'color': 'y', 'value': 1, 'selected': False}, {'color': 'w', 'value': 2, 'selected': False}, {'color': 'y', 'value': 4, 'selected': False}, {'color': 'b', 'value': 1, 'selected': False}, {'color': 'w', 'value': 3, 'selected': False}, {'color': 'y', 'value': 1, 'selected': False}, {'color': 'y', 'value': 3, 'selected': False}, {'color': 'b', 'value': 5, 'selected': False}, {'color': 'y', 'value': 3, 'selected': False}, {'color': 'r', 'value': 3, 'selected': False}, {'color': 'g', 'value': 3, 'selected': False}, {'color': 'w', 'value': 2, 'selected': False}, {'color': 'r', 'value': 1, 'selected': False}, {'color': 'r', 'value': 2, 'selected': False}, {'color': 'g', 'value': 1, 'selected': False}, {'color': 'w', 'value': 1, 'selected': False}, {'color': 'r', 'value': 4, 'selected': False}, {'color': 'w', 'value': 1, 'selected': False}, {'color': 'b', 'value': 3, 'selected': False}, {'color': 'b', 'value': 2, 'selected': False}, {'color': 'b', 'value': 4, 'selected': False}, {'color': 'r', 'value': 3, 'selected': False}, {'color': 'w', 'value': 1, 'selected': False}, {'color': 'g', 'value': 5, 'selected': False}, {'color': 'y', 'value': 5, 'selected': False}, {'color': 'w', 'value': 4, 'selected': False}, {'color': 'g', 'value': 4, 'selected': False}, {'color': 'y', 'value': 1, 'selected': False}, {'color': 'b', 'value': 4, 'selected': False}, {'color': 'g', 'value': 1, 'selected': False}, {'color': 'r', 'value': 1, 'selected': False}, {'color': 'g', 'value': 2, 'selected': False}, {'color': 'w', 'value': 4, 'selected': False}, {'color': 'r', 'value': 5, 'selected': False}], 'discard_list': [], 'clues': 8, 'miss': 3}, 'team': {'enn': {'name': 'enn', 'card_list': [{'color': 'r', 'value': 4, 'selected': False}, {'color': 'g', 'value': 1, 'selected': False}, {'color': 'r', 'value': 2, 'selected': False}, {'color': 'w', 'value': 3, 'selected': False}, {'color': 'g', 'value': 4, 'selected': False}]}}, 'result': ''}
    elif command == 'give_clue':
        result_msg = game.give_clue(msg["player"], msg["current_player"])
    elif command == 'discard_card':
        result_msg = game.discard_card(msg["player"])

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
    '''
    # debug commands
    message = {'command': 'join_game', 'username': 'sd'}
    game_dic = parse_msg(message, game)
    message = {'command': 'start_game', 'username': 'sd'}
    game_dic = parse_msg(message, game)
    message = {'command': 'discard_card', 'player': {'name': 'sd', 'card_list': [{'color': 'r', 'value': 4, 'selected': True}, {'color': 'b', 'value': 4, 'selected': False}, {'color': 'y', 'value': 1, 'selected': False}, {'color': 'w', 'value': 4, 'selected': False}, {'color': 'y', 'value': 1, 'selected': False}]}}
    game_dic = parse_msg(message, game)
    print(game_dic)
    exit()
    '''

    while True:
        #  Wait for next request from client
        message = socket.recv_json()
        print("Received request: %s" % message)

        #  Parse and process message
        time.sleep(0.1)
        game_dic = parse_msg(message, game)
        print(game_dic)

        # print(json_str)
        #  Send reply back to client
        socket.send_json(game_dic)

        # publish game
        #sub_socket.send_string(json_str)


if __name__ == "__main__":
    # execute only if run as a script
    main()