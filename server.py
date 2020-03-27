import zmq
import time
import json
from game import Board, Player, Team

def parse_msg(msg):
    print("Message :")
    print(msg)
    command = msg["command"]
    json_str = json.dumps({})
    if command == 'join_game':
        print('TODO: join game')
        # get name and create new player
    elif command == 'start_game':
        # start only once
        # initialize player's hands
        player = msg["player"]
        main_board = Board()
        main_board.init_draw()
        main_team = Team()
        main_team.add_player(Player(player))
        main_team.init_hands(main_board)
        # Conditionnement et envoi du message vers les clients
        json_str = json.dumps({"board": main_board.to_dic(), "team": main_team.to_dic()})
        # context = zmq.Context()
        # socket = context.socket(zmq.REP)
        # socket.bind("tcp://*:5555")
        # start only once
        # initialize player's hands
    elif command == 'stop_game':
        print('TODO: stop game')
    elif command == 'draw_card':
        print('TODO: play card')
    elif command == 'give_clue':
        print('TODO: give a clue')
    elif command == 'discard_card':
        print('TODO: discard a card')
    return json_str

def main():

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    while True:
        #  Wait for next request from client
        message = socket.recv_json()
        print("Received request: %s" % message)

        #  Do some 'work'
        time.sleep(0.1)
        json_str = parse_msg(message)

        print(json_str)
        #  Send reply back to client
        socket.send_string(json_str)


if __name__ == "__main__":
    # execute only if run as a script
    main()