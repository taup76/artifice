import zmq
import time
import json
from game import Board, Player, Team

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


    myBoard = Board()

    my_player1 = Player('Celine')
    my_player2 = Player('Simon')
    my_player1.init_hand(myBoard, 4)
    my_player2.init_hand(myBoard, 4)
    for i in range(4):
        my_player2.play_card(myBoard, 0)
    print(my_player1.to_string())
    print(my_player2.to_string())
    print(myBoard.to_string())

if __name__ == "__main__":
    # execute only if run as a script
    main()