import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QFormLayout, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import *
from PyQt5.Qt import *
from PyQt5.QtCore import QObject,pyqtSignal
from PyQt5.QtGui import QScreen
import game as gm
import  client

# non blocking subcriber
# https://stackoverflow.com/questions/26012132/zero-mq-socket-recv-call-is-blocking

class Artifice(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.content = Fenetre()
        self.setCentralWidget(self.content)
        # self.setFixedSize(self.screen().size())
        # self.setBaseSize(self.screen().size())

        menubar = self.menuBar()
        menu = menubar.addMenu('File')
        db_action = menu.addAction("Open file")
        db_action.setStatusTip("Select a file to use as a database")
        # db_action.triggered.connect(self.open_new_db)

        self.statusBar().showMessage("Ready")

class Fenetre(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.res_x = self.size().width()
        self.res_y = self.size().height()
        self.resize(self.res_x, self.res_y)
        self.board = gm.Board()
        self.team = gm.Team()
        self.username = ""

        # On affiche les mains des joueurs
        self.list_player = self.team.player_dic.keys()
        self.wid_hands = Widget_hands()

        self.layout_principal = QGridLayout()

        # On affiche les boutons pour creer ou rejoindre la partie
        self.wid_buts_play = QWidget()
        self.layout_buts_play = QHBoxLayout()
        self.wid_buts_play.setLayout(self.layout_buts_play)
        self.but_join = QPushButton("Rejoindre le serveur")
        self.but_join.clicked.connect(self.open_popup_join)

        self.but_launch = QPushButton("Demarrer la partie")
        self.but_launch.clicked.connect(self.handle_launch)
        self.layout_buts_play.addWidget(self.but_join)
        self.layout_buts_play.addWidget(self.but_launch)

        # On affiche le plateau
        self.wid_board = Widget_board(self)
        self.wid_board.add_board(self.board)

        # Ordre ['r','b','y','g','w']
        # self.tas_labels = {'r': QLabel("r0"), 'b': QLabel("b0"), 'y': QLabel("y0"), 'g': QLabel("g0"), 'w': QLabel("w0")}
        # self.draw_game()


        # On affiche les boutons pour jouer ou defausser les cartes selectionnees, la défausse et la pioche
        self.wid_actions = QWidget()
        self.but_play = QPushButton("Jouer")
        self.but_play.clicked.connect(self.handle_but_play)
        self.but_dismiss = QPushButton("Defausser")
        self.but_dismiss.clicked.connect(self.handle_dismiss)
        # self.wid_pioche = QLabel(str(0))
        # self.wid_dism_stack = QCarte()
        self.layout_actions = QHBoxLayout()
        self.wid_actions.setLayout(self.layout_actions)
        self.layout_actions.addWidget(self.but_play)
        self.layout_actions.addWidget(self.but_dismiss)
        # self.layout_actions.addWidget(self.wid_pioche)
        # self.layout_actions.addWidget(self.wid_dism_stack)


        # On remplit le layout principal
        self.layout_principal.addWidget(self.wid_buts_play,1,2)
        # self.layout_principal.addWidget(self.wid_clue_miss,3,1)
        self.layout_principal.addWidget(self.wid_board,1,1,3,1)
        self.layout_principal.addWidget(self.wid_hands,2,2)
        self.layout_principal.addWidget(self.wid_actions,3,2)
        self.setLayout(self.layout_principal)
        self.setWindowTitle("Artifice")

    def draw_game(self):
        self.wid_hands.add_team(self.team, self.username)
        print("draw")
        print(self.board.to_dic())
        self.wid_board.add_board(self.board)

    def join_game(self):
        dic_cmd = {'username': self.username}
        message = self.client.make_message(dic_cmd)
        # message = self.client.socket.recv()
        # game_dic = json.loads(message)
        self.team = gm.Team(message['team'])
        self.board = gm.Board(message['board'])

    def open_popup_join(self):
        self.popup_join = Popup_join()
        self.popup_join.but_ok.clicked.connect(self.handle_ok_join)
        self.popup_join.show()

    def handle_launch(self):
        dic_cmd = {'command':'start_game', 'username': self.username}
        game_dic = self.client.make_message(dic_cmd)
        self.team = gm.Team(game_dic['team'])
        self.board = gm.Board(game_dic['board'])

        self.wid_hands.add_team(self.team, self.username)
        self.wid_board.add_board(self.board)
        print("Initialisation du jeu OK")

    def handle_ok_join(self):
        self.username = self.popup_join.field_joueur.text()
        self.client = client.Client(self.username)
        dic_cmd = {'command':'join_game', 'username': self.username}
        message_new_game = self.client.make_message(dic_cmd)
        self.board = gm.Board(message_new_game['board'])
        self.team = gm.Team(message_new_game['team'])
        self.draw_game()
        # self.draw_board()
        self.popup_join.close()
        self.wid_hands.clear_hands()

    def handle_but_play(self):
        print("On joue une carte")
        dic_cmd = {'command': 'play_card', 'player': self.team.player_dic[self.username].to_dic()}
        game_dic = self.client.make_message(dic_cmd)
        print(game_dic)
        self.team = gm.Team(game_dic['team'])
        self.board = gm.Board(game_dic['board'])
        self.draw_game()

    def handle_dismiss(self):
        print("On défausse une carte")
        dic_cmd = {'command': 'discard_card', 'player': self.team.player_dic[self.username].to_dic()}
        game_dic = self.client.make_message(dic_cmd)
        print(game_dic)
        self.team = gm.Team(game_dic['team'])
        self.board = gm.Board(game_dic['board'])
        self.draw_game()

# Definition de la classe Qcarte ---------------------------
class QCarte(QPushButton):
    # Classe graphique pour representer une carte
    def __init__(self, carte=None, hidden=False):
        QPushButton.__init__(self)
        self.hidden = hidden
        if carte is None:
            path_to_im = 'images/hanabi_background_card.png'
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
        self.setStyleSheet("QPushButton {border-style: outset; border-width: 0px;}")

    def __str__(self):
        return self.carte

    def set_image(self, path):
        pixmap = QPixmap(path)
        pixmap = pixmap.scaled(250, 250)
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
                self.carte.selected = False
            else:
                if self.hidden:
                    path_to_im = "images/small/hidden"
                else:
                    path_to_im = "images/small/" + self.carte.to_string()
                self.selected = True
                self.carte.selected = True
            pixmap = QPixmap(path_to_im)
            pixmap = pixmap.scaled(220, 200)
            ButtonIcon = QIcon(pixmap)
            self.setIcon(ButtonIcon)

class Popup_join(QWidget):
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
        self.layout_hands = QVBoxLayout()
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
        self.clear_hands()
        for player_name in team.player_dic.keys():
            self.add_hand(team.player_dic[player_name])

    def clear_hands(self):
        for i in reversed(range(self.layout_hands.count())):
            self.layout_hands.itemAt(i).widget().setParent(None)

class Widget_board(QWidget):
    def resizeEvent(self, event):
        self.resize_board()

    def __init__(self, fenetre):
        QWidget.__init__(self)
        # fenetre principale
        self.fenetre = fenetre

        # image du plateau
        self.img_label = QLabel()
        self.board_pixmap = QPixmap("images/hanabi_board")
        #self.img_label.setPixmap(self.board_pixmap)
        self.layout = QFormLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.img_label)

        # On definit le layout principal
        self.layout_board = QVBoxLayout()

        # On créé le layout pour les erreurs commises
        self.layout_error = QHBoxLayout()
        self.wid_error = QLabel()
        self.wid_error.setLayout(self.layout_error)
        self.layout_board.addWidget(self.wid_error)

        # On affiche les tas a remplir
        self.img_label.setLayout(self.layout_board)
        self.layout_tas = QHBoxLayout()
        self.wid_tas = QWidget()
        self.wid_tas.setLayout(self.layout_tas)
        self.layout_board.addWidget(self.wid_tas)

        # On affiche les indices
        self.layout_clue = QHBoxLayout()
        self.wid_clues = QWidget()
        self.wid_clues.setLayout(self.layout_clue)
        self.layout_board.addWidget(self.wid_clues)
        self.layout_board.addWidget(self.wid_clues)

        # On affiche la pioche, la carte jouee et la defausse
        self.wid_draw_play_disc = QWidget()
        self.layout_dpd = QHBoxLayout()
        self.wid_draw_play_disc.setLayout(self.layout_dpd)
        self.wid_pioche = QCarte()
        self.wid_pioche.setText("0")
        self.wid_play_card = QCarte()
        self.wid_dism_stack = QCarte()
        self.layout_dpd.addWidget(self.wid_pioche)
        self.layout_dpd.addWidget(self.wid_play_card)
        self.layout_dpd.addWidget(self.wid_dism_stack)
        self.layout_board.addWidget(self.wid_draw_play_disc)

        self.resize_board()

    def resize_board(self):
        # update geometry
        res_x = self.fenetre.frameGeometry().width()
        res_y = self.fenetre.frameGeometry().height()
        ratio_x = 0.5
        ratio_y = 1
        p = self.board_pixmap.scaled(int(ratio_x*res_x), int(ratio_y*res_y), Qt.KeepAspectRatio)
        self.img_label.setPixmap(p)

        self.img_label.resize(int(ratio_x*res_x), int(ratio_y*res_y))

        self.board_x = p.width()
        self.board_y = p.height()

        # On affiche le nombre d'erreurs
        for error_i in range(self.layout_error.count()):
            pix_error = QPixmap("images/token/token_error")
            pix_error = pix_error.scaled(int(self.board_x*0.035), int(self.board_x*0.035), Qt.KeepAspectRatio)
            self.layout_error.itemAt(error_i).widget().setPixmap(pix_error)
        self.layout_error.setSpacing(int(0.005 * self.board_x))
        self.layout_error.setContentsMargins(int(0.412 * self.board_x), int(0.0 * self.board_y),
                                             int(0.412 * self.board_x), int(0.0 * self.board_y))

        # On affiche les tas a remplir
        for stack_i in range(self.layout_tas.count()):
            pix_stack = QPixmap("images/empty_stack")
            pix_stack = pix_stack.scaled(int(0.19*self.board_x), int(0.32*self.board_y), Qt.KeepAspectRatio)
            self.layout_tas.itemAt(stack_i).widget().setPixmap(pix_stack)
        self.layout_tas.setSpacing(int(self.board_x*0.011))
        self.layout_tas.setContentsMargins(int(self.board_x*0.143), int(self.board_y*0.0), int(self.board_x*0.143), int(self.board_y*0.0))

        # On affiche les indices
        for stack_i in range(self.layout_clue.count()):
            pix_clue = QPixmap("images/token/token_clue")
            pix_clue = pix_clue.scaled(int(self.board_x*0.035), int(self.board_x*0.035), Qt.KeepAspectRatio)
            self.layout_clue.itemAt(stack_i).widget().setPixmap(pix_clue)
        self.layout_clue.setSpacing(int(self.board_x*0.013))
        self.layout_clue.setContentsMargins(int(self.board_x*0.292), int(self.board_y*0.0), int(self.board_x*0.292), int(self.board_y*0.0))

        # On affiche les elements du dpd
        for dpd_i in range(self.layout_dpd.count()):
            pix_dpd = QPixmap("images/hanabi_background_card") # TODO a remplacer par naught
            pix_dpd = pix_dpd.scaled(int(0.19*self.board_x), int(0.15*self.board_y), Qt.KeepAspectRatio)
            self.layout_dpd.itemAt(dpd_i).widget().setIcon(QIcon(pix_dpd))
        self.layout_dpd.setSpacing(int(self.board_x*0.011))
        self.layout_dpd.setContentsMargins(int(self.board_x*0.143), int(self.board_y*0.0), int(self.board_x*0.143), int(self.board_y*0.0))



    def add_board(self, board):
        self.clear_board()
        # On affiche le nombre d'erreurs
        for error_i in range(board.miss):
            lab_error = QLabel()
            pix_error = QPixmap("images/token/token_error")
            pix_error = pix_error.scaled(25, 25, Qt.KeepAspectRatio)
            lab_error.setPixmap(pix_error)
            self.layout_error.addWidget(lab_error)

        # On affiche les stacks
        for stack_key in board.stack_dic.keys():
            stack = board.stack_dic[stack_key]
            lab_stack = QLabel()
            if len(stack.card_list) > 0:
                carte_top = stack.card_list[-1]
                path = "images/stack_" + carte_top.color + str(carte_top.value)
                wid_stack = QLabel()
                stack_im = QPixmap(path)
                wid_stack.setPixmap(path)
                wid_stack.resize(stack_im.width(), stack_im.height())
                # self.layout_tas.addWidget(wid_stack)
                pix_stack = QPixmap("images/stack_" + carte_top.color + str(carte_top.value))
            else:
                pix_stack = QPixmap("images/empty_stack")
                pix_stack = pix_stack.scaled(int(0.125*self.board_x), int(0.33*self.board_y), Qt.KeepAspectRatio)
                print("Pas de carte " + stack_key)
            lab_stack.setPixmap(pix_stack)
            self.layout_tas.addWidget(lab_stack)
        # On affiche les indices
        for i in range(board.clues):
            lab_clue = QLabel()
            pix_clue = QPixmap("images/token/token_clue")
            # pix_clue = pix_clue.scaled(25, 25, Qt.KeepAspectRatio)
            lab_clue.setPixmap(pix_clue)
            self.layout_clue.addWidget(lab_clue)
        # self.layout_clue.setSpacing(int(7/802*self.board_x))
        # self.layout_clue.setContentsMargins(int(0.3*self.board_x), int(0.01*self.board_y), int(0.3*self.board_x), int(0*self.board_y) )
        # self.layout_clue.addWidget(self.label_miss)
        # On affiche les piles de pioche, la carte jouee et la defausse
        # TODO ajouter la carte jouee
        self.wid_pioche = QCarte()
        self.wid_pioche.setText(str(len(board.draw_list.card_list)))
        self.layout_dpd.addWidget(self.wid_pioche)
        self.wid_play_card = QCarte()
        self.layout_dpd.addWidget(self.wid_play_card)
        if len(board.discard_list.card_list)>0:
            self.wid_dism_stack = QCarte(board.discard_list.card_list[-1])
        else:
            self.wid_dism_stack = QCarte()
            # self.wid_dism_stack.setFixedSize(155,155)
        self.layout_dpd.addWidget(self.wid_dism_stack)

    def clear_board(self):
        for i in reversed(range(self.layout_error.count())):
            self.layout_error.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.layout_tas.count())):
            self.layout_tas.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.layout_clue.count())):
            self.layout_clue.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.layout_dpd.count())):
            self.layout_dpd.itemAt(i).widget().setParent(None)


app = QApplication.instance()
if not app:
    app = QApplication(sys.argv)

# screen_resolution = app.desktop().screenGeometry()
# res_x, res_y = screen_resolution.width(), screen_resolution.height()
# fen = Fenetre()
# fen.show()
artif = Artifice()
artif.show()
app.exec_()