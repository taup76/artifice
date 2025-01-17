#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
from PyQt5 import QtCore
from PyQt5.Qt import QSettings
import json



class Client:
    def __init__(self, game_dic={}, settings=QSettings()):
        self.context = zmq.Context()
        self.game_dic = game_dic
        # self.ip = "192.168.1.98"
        if settings.contains("ip_client"):
            self.ip = settings.value("ip_client")
        else:
            self.ip = "localhost"
        self.port = 5555
        self.connect_socket()

    def __str__(self):
        # TODO
        return ""

    def connect_socket(self):
        print("Connecting to hello world server…")
        #  Socket to talk to server
        self.socket = self.context.socket(zmq.REQ)
        print("tcp://" + self.ip + ":" + str(self.port))
        self.socket.connect("tcp://" + self.ip + ':' + str(self.port))
        print("Sending request")

    def make_message(self, dic_command): # commande de la forme {'command' : 'start_game' ; 'params' : ['param1', 'param2', ...]
        mes_json = "{}"
        if 'command' in dic_command:
            # mes_json = json.dumps(dic_command)
            self.socket.send_json(dic_command)
            self.message = self.socket.recv_json()
        else:
            print("Format inconnu de commande")
        return self.message


class SubListener(QtCore.QObject):
    message = QtCore.pyqtSignal(str)

    def __init__(self, context, settings = QSettings()):
        # self.context = zmq.Context()
        QtCore.QObject.__init__(self)
        self.subport = 5556
        # self.ip = "192.168.1.98"
        if settings.contains("ip_client"):
            self.ip = settings.value("ip_client")
        else:
            self.ip = "localhost"
        self.sub_socket = context.socket(zmq.SUB)
        self.sub_socket.connect("tcp://" + self.ip + ':' + str(self.subport))
        topicfilter = "message"
        self.sub_socket.setsockopt_string(zmq.SUBSCRIBE, topicfilter)
        self.running = True

    def loop(self):
        while self.running:
            sub_message = self.sub_socket.recv_string()
            sub_message = sub_message.replace("message ", "")
            self.message.emit(sub_message)

