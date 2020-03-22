import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QFormLayout, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import *
import server as srv

class Fenetre(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        layout_principal = QGridLayout()
        layout_tas = QGridLayout()

        # On affiche les tas de cartes
        wid_tas = QWidget()
        wid_tas.setLayout(layout_tas)

        board = srv.Board()
        board.init_draw()
        top_blanc = 0
        self.label_blanc = QLabel("Blanc :" + str(top_blanc))
        top_bleu = 0
        self.label_bleu = QLabel("Bleu :" + str(top_bleu))
        top_vert = 0
        self.label_vert = QLabel("Vert :" + str(top_vert))
        top_rouge = 0
        self.label_rouge = QLabel("Rouge :" + str(top_rouge))
        top_jaune = 0
        self.label_jaune = QLabel("Jaune :" + str(top_jaune))

        layout_tas.addWidget(self.label_blanc,1,1)
        layout_tas.addWidget(self.label_bleu,1,2)
        layout_tas.addWidget(self.label_vert,1,3)
        layout_tas.addWidget(self.label_rouge,2,1)
        layout_tas.addWidget(self.label_jaune,2,2)

        # On affiche les indices et les bombes erreurs
        wid_clue_miss = QWidget()
        layout_clue = QHBoxLayout()
        wid_clue_miss.setLayout(layout_clue)
        nb_clue = 5
        nb_miss = 3
        label_clue = QLabel("Indice :" + str(nb_clue))
        label_miss = QLabel("Erreurs :" + str(nb_miss))
        layout_clue.addWidget(label_clue)
        layout_clue.addWidget(label_miss)

        # On affiche les mains des joueurs
        list_player = ["Céline", "Simon"]
        wid_hands = QWidget()
        layout_hands = QVBoxLayout()
        wid_hands.setLayout(layout_hands)

        cartes_celine = [srv.Card('r','1'), srv.Card('r','4'), srv.Card('b','2'), srv.Card('w','5'), srv.Card('y','2')]
        celine_hand = self.hand_wid(list_player[0],cartes_celine)
        layout_hands.addWidget(celine_hand)
        cartes_simon = [srv.Card('v','2'), srv.Card('w','4'), srv.Card('b','1'), srv.Card('y','1'), srv.Card('v','4')]
        simon_hand = self.hand_wid(list_player[1],cartes_simon)
        layout_hands.addWidget(simon_hand)


        # On remplit le layout principal
        layout_principal.addWidget(wid_tas,1,1)
        layout_principal.addWidget(wid_clue_miss,2,1)
        layout_principal.addWidget(wid_hands,1,2)
        self.setLayout(layout_principal)
        self.setWindowTitle("Artifice")

    def hand_wid(self,joueur,liste_carte):
        wid_hand = QWidget()
        layout_hand = QVBoxLayout()
        wid_hand.setLayout(layout_hand)
        layout_card = QHBoxLayout()
        layout_hand.addWidget(QLabel(joueur))
        wid_cards = QWidget()
        layout_hand.addWidget(wid_cards)
        wid_cards.setLayout(layout_card)
        for carte in liste_carte:
            path_to_im = "images/" + carte.to_string()
            wid_carte = QCarte(carte)
            layout_card.addWidget(wid_carte)
        return wid_hand

    def draw_game(self):
        self.draw_board()
        return 1

    def draw_board(self, board):
        self.label_blanc = board['w']

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
        print(self.selected)
        if self.selected:
            path_to_im = "images/" + self.carte.to_string()
            pixmap = QPixmap(path_to_im)
            ButtonIcon = QIcon(pixmap)
            self.setIcon(ButtonIcon)
            self.selected = False
            print("cliqué")
        else:
            path_to_im = "images/small/" + self.carte.to_string()
            pixmap = QPixmap(path_to_im)
            ButtonIcon = QIcon(pixmap)
            self.setIcon(ButtonIcon)
            self.selected = True
            print("non cliqué")



app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)

fen = Fenetre()
fen.show()

app.exec_()