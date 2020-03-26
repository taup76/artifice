#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
import json


class Client:
    def __init__(self, joueur = "", socket = zmq.Context(), game_dic = {}):
        self.socket = socket
        self.game_dic = game_dic
        self.ip = "localhost"
        self.port = 5555
        self.joueur = joueur

    def __str__(self):
        # TODO
        return ""

    def connect_socket(self):
        print("Connecting to hello world server…")
        context = zmq.Context()
        #  Socket to talk to server
        self.socket = context.socket(zmq.REQ)
        print("tcp://" + self.ip + ":" + str(self.port))
        self.socket.connect("tcp://" + self.ip + ':' + str(self.port))
        print("Sending request")
        # self.socket.send_string(self.joueur)
        # self.message = self.socket.recv() # Mettre un watchdog
        # print("Received reply [ %s ]" % self.message)
        # self.game_dic = json.loads(self.message)

    def make_message(self, dic_command): # commande de la forme {'command' : 'start_game' ; 'params' : ['param1', 'param2', ...]
        mes_json = "{}"
        print("Message client")
        print(dic_command)
        if 'command' in dic_command:
            # mes_json = json.dumps(dic_command)
            self.socket.send_json(dic_command)
            self.message = self.socket.recv_json()
            # print("Message recu :")
            # print(self.message)
        else:
            print("Format inconnu de commande")
        return self.message

# context = zmq.Context()
#
# #  Socket to talk to server
# print("Connecting to hello world server…")
# socket = context.socket(zmq.REQ)
# socket.connect("tcp://localhost:5555")
#
#
# #  Do 10 requests, waiting each time for a response
# for request in range(10):
#     print("Sending request %s …" % request)
#     socket.send(b"Hello")
#
#     #  Get the reply.
#     message = socket.recv()
#     print("Received reply %s [ %s ]" % (request, message))
#     game_dic = json.loads(message)
#     print(game_dic)