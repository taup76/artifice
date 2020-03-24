import zmq
import time
import json
from game import Board, Player, Team

def parse_msg(msg):
    command = msg["command"]
    if command == 'join_game':
        print('TODO: join game')
        # get name and create new player
    elif command == 'start_game':
        print('TODO: start game')
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

def main():
    # initialize game
    main_board = Board()
    main_team = Team()

    # initialize player 1
    main_team.add_player(Player('Celine'))
    main_team.add_player(Player('Simon'))
    main_team.add_player(Player('Loris'))
    main_team.init_hands(main_board)

    print(main_board.to_dic())
    print(main_team.to_dic())

    json_str = json.dumps({"board": main_board.to_dic(), "team": main_team.to_dic()})

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    while True:
        #  Wait for next request from client
        message = socket.recv()
        print("Received request: %s" % message)

        #  Do some 'work'
        time.sleep(1)
        print("ok")

        #  Send reply back to client
        socket.send_string(json_str)


if __name__ == "__main__":
    # execute only if run as a script
    main()