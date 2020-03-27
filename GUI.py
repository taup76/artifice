import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QFormLayout, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import *
from PyQt5.Qt import *
from PyQt5.QtCore import QObject,pyqtSignal
import server as srv
import game as gm
import  client
import zmq, json

# non blocking subcriber
# https://stackoverflow.com/questions/26012132/zero-mq-socket-recv-call-is-blocking

class Fenetre(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.board = gm.Board()
        self.team = gm.Team()

        self.layout_principal = QGridLayout()
        # On affiche les boutons pour créer ou rejoindre la partie
        self.wid_buts_play = QWidget()
        self.layout_buts_play = QHBoxLayout()
        self.wid_buts_play.setLayout(self.layout_buts_play)
        self.but_new = QPushButton("Nouvelle partie")
        self.but_new.clicked.connect(self.open_popup_new_game)
        # self.popup_new_game = None

        self.but_join = QPushButton("Rejoindre")
        self.layout_buts_play.addWidget(self.but_new)
        self.layout_buts_play.addWidget(self.but_join)
        # self.join_game()

        # On affiche les tas de cartes
        self.wid_board = Widget_board()
        self.wid_board.add_board(self.board)

        # Ordre ['r','b','y','g','w']
        self.tas_labels = {'r': QLabel("r0"), 'b': QLabel("b0"), 'y': QLabel("y0"), 'g': QLabel("g0"), 'w': QLabel("w0")}
        self.draw_board()
        # self.layout_tas.addWidget(self.tas_labels['r'],1,1)
        # self.layout_tas.addWidget(self.tas_labels['b'],1,2)
        # self.layout_tas.addWidget(self.tas_labels['y'],1,3)
        # self.layout_tas.addWidget(self.tas_labels['g'],2,1)
        # self.layout_tas.addWidget(self.tas_labels['w'],2,2)


        # On affiche les boutons pour jouer ou défausser les cartes sélectionnées
        self.wid_actions = QWidget()
        self.but_play = QPushButton("Jouer")
        self.but_dismiss = QPushButton("Défausser")
        self.layout_actions = QHBoxLayout()
        self.wid_actions.setLayout(self.layout_actions)
        self.layout_actions.addWidget(self.but_play)
        self.layout_actions.addWidget(self.but_dismiss)

        # On affiche les mains des joueurs
        # self.list_player = ["Céline", "Simon"]
        self.list_player = self.team.player_dic.keys()
        self.wid_hands = Widget_hands()
        # self.wid_hands = QWidget()
        # self.layout_hands = QVBoxLayout()
        # self.wid_hands.setLayout(self.layout_hands)
        #
        # for joueur in self.list_player:
        #     cartes_joueur = self.team.player_dic[joueur].card_list
        #     wid_main = self.hand_wid(joueur, cartes_joueur)
        #     self.layout_hands.addWidget(wid_main)

        # On remplit le layout principal
        self.layout_principal.addWidget(self.wid_buts_play,1,1)
        self.layout_principal.addWidget(self.wid_board,2,1)
        # self.layout_principal.addWidget(self.wid_clue_miss,3,1)
        # self.layout_principal.addWidget(self.wid_actions,4,1)
        self.layout_principal.addWidget(self.wid_hands,2,2)
        self.setLayout(self.layout_principal)
        self.setWindowTitle("Artifice")

    def draw_game(self):
        print("draw 1")
        self.draw_board()
        print("draw 2")
        # self.draw_all_hands()
        print("draw 3")
        # self.show()

    def draw_board(self):
        for key in self.board.stack_dic.keys():
            print(self.board.stack_dic[key].to_string())
            print(self.board.stack_dic[key].get_length())
            if self.board.stack_dic[key].get_length() > 0:
                self.tas_labels[key].setText(self.board.stack_dic[key][-1].to_string())
            else:
                self.tas_labels = {'r': QLabel("r0"), 'b': QLabel("b0"), 'y': QLabel("y0"), 'g': QLabel("g0"), 'w': QLabel("w0")}

    def join_game(self):
        context = zmq.Context()
        #  Socket to talk to server
        print("Connecting to hello world server…")
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:5555")
        socket.send(b"Hello")
        #  Get the reply.
        message = socket.recv()
        game_dic = json.loads(message)
        self.team = gm.Team(game_dic['team'])
        self.board = gm.Board(game_dic['board'])

    def open_popup_new_game(self):
        self.popup_new_game = Popup_New()
        self.popup_new_game.but_ok.clicked.connect(self.handle_ok_new_game)
        self.popup_new_game.show()

    def handle_ok_new_game(self):
        self.username = self.popup_new_game.field_joueur.text()
        print("Nom du joueur : " + self.username)
        self.client = client.Client(self.username)
        dic_cmd = {'command':'start_game', 'player': self.username}
        self.client.connect_socket()
        message_new_game = self.client.make_message(dic_cmd)
        self.board = gm.Board(message_new_game['board'])
        self.team = gm.Team(message_new_game['team'])
        self.draw_game()
        self.popup_new_game.close()
        self.wid_hands.clear_hands()
        self.wid_hands.add_team(self.team, self.username)
        print("Initialisation du jeu OK")


# Définition de la classe Qcarte ---------------------------
class QCarte(QPushButton):
    # Classe graphique pour representer une carte
    def __init__(self, carte=None, hidden=False):
        QPushButton.__init__(self)
        self.hidden = hidden
        if carte is None:
            path_to_im = 'images/naught_b.png'
        else:
            if self.hidden:
                path_to_im = "images/hidden.png"
            else:
                path_to_im = "images/" + carte.to_string()
        self.set_image(path_to_im)
        self.carte = carte
        self.isclickable = (carte is not None)
        self.selected = False
        self.clicked.connect(self.on_click)
        self.image = path_to_im

    def __str__(self):
        return self.carte

    def set_image(self, path):
        pixmap = QPixmap(path)
        ButtonIcon = QIcon(pixmap)
        self.setIcon(ButtonIcon)
        self.setIconSize(pixmap.rect().size())


    def on_click(self):
        if self.isclickable:
            if self.selected:
                if self.hidden:
                    path_to_im = "images/hidden"
                else:
                    path_to_im = "images/" + self.carte.to_string()
                self.selected = False
            else:
                if self.hidden:
                    path_to_im = "images/small/hidden"
                else:
                    path_to_im = "images/small/" + self.carte.to_string()
                self.selected = True
            pixmap = QPixmap(path_to_im)
            ButtonIcon = QIcon(pixmap)
            self.setIcon(ButtonIcon)

class Popup_New(QWidget):
    trigger = pyqtSignal()

    def __init__(self):
        QWidget.__init__(self)
        self.layout_top = QVBoxLayout()
        self.setLayout(self.layout_top)
        self.label_setjoueur = QLabel("Nom du joueur")
        self.layout_top.addWidget(self.label_setjoueur)
        self.field_joueur = QLineEdit("")
        self.layout_top.addWidget(self.field_joueur)
        self.but_ok = QPushButton("OK")
        self.layout_top.addWidget(self.but_ok)
        self.show()

class Widget_hands(QWidget):
    def __init__(self, user = ""):
        QWidget.__init__(self)
        self.layout_hands = QHBoxLayout()
        self.setLayout(self.layout_hands)
        self.username = user

    def add_hand(self, player):
        wid_hand = QWidget()
        layout_hand = QVBoxLayout()
        wid_hand.setLayout(layout_hand)
        layout_card = QHBoxLayout()
        wid_name = QLabel(player.name)
        layout_hand.addWidget(wid_name)
        wid_cards = QWidget()
        layout_hand.addWidget(wid_cards)
        wid_cards.setLayout(layout_card)
        for carte in player.card_list.card_list:
            wid_carte = QCarte(carte, self.username == player.name)
            layout_card.addWidget(wid_carte)
        self.layout_hands.addWidget(wid_hand)

    def add_team(self, team, user):
        self.username = user
        # self.clear_hands()
        for player_name in team.player_dic.keys():
            self.add_hand(team.player_dic[player_name])

    def clear_hands(self):
        for i in reversed(range(self.layout_hands.count())):
            self.layout_hands.itemAt(i).widget().setParent(None)

class Widget_board(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        # On affiche les tas à remplir
        self.layout_board = QVBoxLayout()
        self.setLayout(self.layout_board)
        self.layout_tas = QHBoxLayout()
        self.wid_tas = QWidget()
        self.wid_tas.setLayout(self.layout_tas)
        self.layout_board.addWidget(self.wid_tas)

        # On affiche les indices et les bombes erreurs
        self.wid_clue_miss = QWidget()
        self.layout_clue = QHBoxLayout()
        self.wid_clue_miss.setLayout(self.layout_clue)
        self.label_clue = QLabel("Indice :" + str(0))
        self.label_miss = QLabel("Erreurs :" + str(0))
        self.layout_clue.addWidget(self.label_clue)
        self.layout_clue.addWidget(self.label_miss)
        self.layout_board.addWidget(self.wid_clue_miss)

    def add_board(self, board):
        self.clear_board()
        for stack_key in board.stack_dic.keys():
            stack = board.stack_dic[stack_key]
            if len(stack.card_list) > 0:
                carte_top = stack.card_list[-1]
                path = "images/" + carte_top.couleur + carte_top.valeur
                wid_carte = QCarte(carte_top)
            else:
                path = "images/naught_" + stack_key
                wid_carte = QCarte()
            wid_carte.set_image(path)
            self.layout_tas.addWidget(wid_carte)
        # On update les miss et les clues
        print("NB de clues : " + str(board.clues))
        self.label_clue = QLabel("Indices :" + str(board.clues))
        self.label_miss = QLabel("Erreurs :" + str(board.miss))
        self.layout_clue.addWidget(self.label_clue)
        self.layout_clue.addWidget(self.label_miss)

    def clear_board(self):
        for i in reversed(range(self.layout_tas.count())):
            self.layout_tas.itemAt(i).widget().setParent(None)
        self.layout_clue.itemAt(1).widget().setParent(None)
        self.layout_clue.itemAt(0).widget().setParent(None)


app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)

fen = Fenetre()
fen.show()

app.exec_()