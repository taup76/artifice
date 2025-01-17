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
    elif command == 'give_clue':
        result_msg = game.give_clue(msg["target_player"], msg["clue"])
    elif command == 'discard_card':
        result_msg = game.discard_card(msg["player"])
    elif command == 'card_selected':
        result_msg = game.update_team(msg["team"])
    else:
        result_msg = "Fonction serveur non definie"

    if command != 'finish_game':
        game_dic = game.to_dic()
    else:
        game_dic = {}
    game_dic["result"] = result_msg
    return game_dic

def main():

    # create context for all sockets
    context = zmq.Context()

    # open request reply socket on port 5555
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    # open publisher on port 6666
    pub_socket = context.socket(zmq.PUB)
    pub_socket.bind("tcp://*:5556")

    # create a game
    game = Game()

    # debug commands
    # message = {'command': 'join_game', 'username': 'sd'}
    # game_dic = parse_msg(message, game)
    # message = {'command': 'join_game', 'username': 'fn'}
    # game_dic = parse_msg(message, game)
    # message = {'command': 'join_game', 'username': 'ping'}
    # game_dic = parse_msg(message, game)
    # message = {'command': 'join_game', 'username': 'pong'}
    # game_dic = parse_msg(message, game)
    # message = {'command': 'join_game', 'username': 'ieng'}
    # game_dic = parse_msg(message, game)
    # message = {'command': 'start_game', 'username': 'sd'}
    # game_dic = parse_msg(message, game)
    # # message = {'command': 'discard_card', 'player': {'name': 'sd', 'card_list': [{'color': 'r', 'value': 4, 'selected': True}, {'color': 'b', 'value': 4, 'selected': False}, {'color': 'y', 'value': 1, 'selected': False}, {'color': 'w', 'value': 4, 'selected': False}, {'color': 'y', 'value': 1, 'selected': False}]}}
    # # game_dic = parse_msg(message, game)
    # print(game_dic)
    # exit()


    while True:
        #  Wait for next request from client
        message = socket.recv_json()
        print("Received request: %s" % message)

        #  Parse and process message
        time.sleep(0.1)
        game_dic = parse_msg(message, game)
        print(game_dic)

        #  Send reply back to client
        socket.send_json(game_dic)

        # publish game
        pub_socket.send_string("%s %s" % ("message", json.dumps(game_dic)))


if __name__ == "__main__":
    # execute only if run as a script
    main()