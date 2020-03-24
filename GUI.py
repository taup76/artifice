import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QFormLayout, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import *
import server as srv
import game as gm
import zmq, json

# non blocking subcriber
# https://stackoverflow.com/questions/26012132/zero-mq-socket-recv-call-is-blocking

class Fenetre(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.layout_principal = QGridLayout()
        self.layout_tas = QGridLayout()

        # On affiche le bouton pour rejoindre la partie
        self.but_join = QPushButton("Rejoindre")
        self.join_game()
        # self.but_join.clicked.connect(self.join_game)

        # On affiche les tas de cartes
        self.wid_tas = QWidget()
        self.wid_tas.setLayout(self.layout_tas)

        # Ordre ['r','b','y','g','w']
        self.tas_labels = {'r': QLabel("r0"), 'b': QLabel("b0"), 'y': QLabel("y0"), 'g': QLabel("g0"), 'w': QLabel("w0")}

        self.layout_tas.addWidget(self.tas_labels['r'],1,1)
        self.layout_tas.addWidget(self.tas_labels['b'],1,2)
        self.layout_tas.addWidget(self.tas_labels['y'],1,3)
        self.layout_tas.addWidget(self.tas_labels['g'],2,1)
        self.layout_tas.addWidget(self.tas_labels['w'],2,2)

        # On affiche les indices et les bombes erreurs
        self.wid_clue_miss = QWidget()
        self.layout_clue = QHBoxLayout()
        self.wid_clue_miss.setLayout(self.layout_clue)
        self.label_clue = QLabel("Indice :" + str(self.board.clues))
        self.label_miss = QLabel("Erreurs :" + str(self.board.miss))
        self.layout_clue.addWidget(self.label_clue)
        self.layout_clue.addWidget(self.label_miss)

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
        self.wid_hands = QWidget()
        self.layout_hands = QVBoxLayout()
        self.wid_hands.setLayout(self.layout_hands)

        for joueur in self.list_player:
            cartes_joueur = self.team.player_dic[joueur].card_list
            wid_main = self.hand_wid(joueur, cartes_joueur)
            self.layout_hands.addWidget(wid_main)

        # On remplit le layout principal
        self.layout_principal.addWidget(self.but_join,1,1)
        self.layout_principal.addWidget(self.wid_tas,2,1)
        self.layout_principal.addWidget(self.wid_clue_miss,3,1)
        self.layout_principal.addWidget(self.wid_actions,4,1)
        self.layout_principal.addWidget(self.wid_hands,2,2)
        self.setLayout(self.layout_principal)
        self.setWindowTitle("Artifice")

    def hand_wid(self,joueur,stack_carte):
        wid_hand = QWidget()
        layout_hand = QVBoxLayout()
        wid_hand.setLayout(layout_hand)
        layout_card = QHBoxLayout()
        layout_hand.addWidget(QLabel(joueur))
        wid_cards = QWidget()
        layout_hand.addWidget(wid_cards)
        wid_cards.setLayout(layout_card)
        for carte in stack_carte.card_list:
            path_to_im = "images/" + carte.to_string()
            wid_carte = QCarte(carte)
            layout_card.addWidget(wid_carte)
        return wid_hand

    def draw_game(self):
        self.draw_board()
        self.draw_all_hands()

    def draw_board(self):
        for key in self.board.stack_dic.keys():
            print(self.board.to_string())
            if self.board.stack_dic[key].get_length() > 0:
                self.tas_labels[key].setText(self.board.stack_dic[key][-1].to_string())
            else:
                self.tas_labels[key].setText("0")

    def draw_hand(self, joueur):
        print("TODO")

    def draw_all_hands(self):
        for joueur in self.list_player:
            self.draw_hand(self, joueur)

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


# Définition de la classe Qcarte ---------------------------
class QCarte(QPushButton):
    # Classe graphique pour representer une carte
    def __init__(self, carte):
        QPushButton.__init__(self)
        path_to_im = "images/" + carte.to_string()
        pixmap = QPixmap(path_to_im)
        ButtonIcon = QIcon(pixmap)
        self.setIcon(ButtonIcon)
        self.setIconSize(pixmap.rect().size())
        self.carte = carte
        self.image = path_to_im
        self.selected = False
        self.clicked.connect(self.on_click)

    def __str__(self):
        return self.carte

    def on_click(self):
        if self.selected:
            path_to_im = "images/" + self.carte.to_string()
            pixmap = QPixmap(path_to_im)
            ButtonIcon = QIcon(pixmap)
            self.setIcon(ButtonIcon)
            self.selected = False
        else:
            path_to_im = "images/small/" + self.carte.to_string()
            pixmap = QPixmap(path_to_im)
            ButtonIcon = QIcon(pixmap)
            self.setIcon(ButtonIcon)
            self.selected = True


app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)

fen = Fenetre()
fen.show()

app.exec_()