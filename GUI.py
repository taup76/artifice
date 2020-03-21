import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QFormLayout, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot


class Fenetre(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        layout_principal = QGridLayout()
        layout_tas = QGridLayout()

        # On affiche les tas de cartes
        wid_tas = QWidget()
        wid_tas.setLayout(layout_tas)

        top_blanc = 0
        label_blanc = QLabel("Blanc :" + str(top_blanc))
        top_bleu = 0
        label_bleu = QLabel("Bleu :" + str(top_bleu))
        top_vert = 0
        label_vert = QLabel("Vert :" + str(top_vert))
        top_rouge = 0
        label_rouge = QLabel("Rouge :" + str(top_rouge))
        top_jaune = 0
        label_jaune = QLabel("Jaune :" + str(top_jaune))

        layout_tas.addWidget(label_blanc,1,1)
        layout_tas.addWidget(label_bleu,1,2)
        layout_tas.addWidget(label_vert,1,3)
        layout_tas.addWidget(label_rouge,2,1)
        layout_tas.addWidget(label_jaune,2,2)

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

        cartes_celine = ["r1", "r4", "b2", "w5", "y2"]
        celine_hand = self.hand_wid(list_player[0],cartes_celine)
        layout_hands.addWidget(celine_hand)
        cartes_simon= ["r2", "b4", "b1", "w1", "y4"]
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
            path_to_im = "images/" + carte
            wid_carte = QCarte(carte, path_to_im)
            layout_card.addWidget(wid_carte)
        return wid_hand

# Définition de la classe Qcarte ---------------------------
class QCarte(QPushButton):
    # Classe graphique pour representer une carte
    def __init__(self, carte, path_to_image):
        QPushButton.__init__(self)
        pixmap = QPixmap(path_to_image)
        ButtonIcon = QIcon(pixmap)
        self.setIcon(ButtonIcon)
        self.setIconSize(pixmap.rect().size())
        self.carte = carte
        self.image = path_to_image

    def __str__(self):
        return self.carte


app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)

fen = Fenetre()
fen.show()

app.exec_()