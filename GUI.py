import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QFormLayout, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import *
from PyQt5.Qt import *
from PyQt5.QtCore import QObject,pyqtSignal
from PyQt5.QtCore import QThread
import game as gm
import client
import json

# non blocking subcriber
# https://stackoverflow.com/questions/26012132/zero-mq-socket-recv-call-is-blocking


class Artifice(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.content = Fenetre()
        self.setCentralWidget(self.content)
        # self.setStyleSheet("QPushButton {border: 1px solid red;}")
        # self.setStyleSheet("QCarte:pressed {border: 1px solid red;}")
        # self.setStyleSheet("QPushButton:checked {border-style: outset; border-width: 10px;}")
        # self.setStyleSheet("QCarte:clicked {border-style: outset; border-width: 10px;}")
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
        self.setMaximumSize(self.screen().size())
        self.res_x = self.size().width()
        self.res_y = self.size().height()
        self.resize(self.res_x, self.res_y)
        self.board = gm.Board()
        self.team = gm.Team()
        self.turn = gm.Turn(self.board, self.team)
        self.username = ""

        # On affiche les mains des joueurs
        # self.list_player = self.team.player_dic.keys()
        self.wid_hands = Widget_hands()
        self.wid_hands.card_clicked.connect(self.handle_card_clicked)
        # empty_player = gm.Player()
        # for i in range(5):
        #     empty_player.append(gm.Card())
        # self.team.add_player(empty_player)
        # self.wid_hands.add_team(self.team, "")

        self.layout_principal = QHBoxLayout()

        # On affiche les boutons pour creer ou rejoindre la partie
        self.wid_buts_play = QWidget()
        self.layout_buts_play = QHBoxLayout()
        self.layout_buts_play.setContentsMargins(int(self.res_x/5), int(self.res_y/5),
                                                 int(self.res_x/5), int(self.res_y/5))
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

        # On affiche les boutons pour jouer ou defausser les cartes selectionnees, la défausse et la pioche
        self.wid_actions = QWidget()
        self.but_play = QPushButton("Jouer")
        self.but_play.clicked.connect(self.handle_but_play)
        self.but_dismiss = QPushButton("Defausser")
        self.but_dismiss.clicked.connect(self.handle_dismiss)
        self.but_give_clue = QPushButton("Renseigner")
        self.but_give_clue.clicked.connect(self.handle_give_clue)
        self.layout_actions = QHBoxLayout()
        self.layout_actions.setContentsMargins(int(self.res_x/5), int(self.res_y/5),
                                                 int(self.res_x/5), int(self.res_y/5))
        self.wid_actions.setLayout(self.layout_actions)
        self.layout_actions.addWidget(self.but_play)
        self.layout_actions.addWidget(self.but_dismiss)
        self.layout_actions.addWidget(self.but_give_clue)

        # On remplit le layout principal
        self.layout_principal.addWidget(self.wid_board, 500)
        self.wid_right_panel = QWidget()
        self.layout_right_panel = QVBoxLayout()
        self.wid_right_panel.setLayout(self.layout_right_panel)
        self.layout_right_panel.addWidget(self.wid_buts_play)
        # self.layout_principal.addWidget(self.wid_clue_miss,3,1)
        self.layout_right_panel.addWidget(self.wid_hands)
        self.layout_right_panel.addWidget(self.wid_actions)
        self.layout_principal.addWidget(self.wid_right_panel, 500)
        self.setLayout(self.layout_principal)
        self.setWindowTitle("Artifice")


    def draw_game(self):
        # print("Draw user : " + self.username)
        self.wid_hands.add_team(self.team, self.turn.current_player, self.username)
        # print("draw")
        # print(self.board.to_dic())
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
        # self.team = gm.Team(game_dic['team'])
        # self.board = gm.Board(game_dic['board'])
        # print("Launch user : " + self.username)
        # self.wid_hands.add_team(self.team, self.username)
        # self.wid_board.add_board(self.board)
        print("Initialisation du jeu OK")

    def handle_ok_join(self):
        self.username = self.popup_join.field_joueur.text()
        self.client = client.Client(self.username)
        self.sub_sock_thread = QThread()
        self.sub_listen = client.SubListener(self.client.context)
        self.sub_listen.moveToThread(self.sub_sock_thread)
        self.sub_sock_thread.started.connect(self.sub_listen.loop)
        self.sub_listen.message.connect(self.handle_message_sub)
        # self.sub_sock_thread.start()
        QTimer.singleShot(0, self.sub_sock_thread.start)
        dic_cmd = {'command':'join_game', 'username': self.username}
        message_new_game = self.client.make_message(dic_cmd)
        # self.board = gm.Board(message_new_game['board'])
        # self.team = gm.Team(message_new_game['team'])
        # self.draw_game()
        self.popup_join.close()
        self.wid_hands.clear_hands()

    def handle_message_sub(self,game_dic):
        print("Message du publisher")
        game_dic = json.loads(game_dic)
        print(game_dic)
        self.team = gm.Team(game_dic['team'])
        self.board = gm.Board(game_dic['board'])
        print('tour 1')
        self.turn = gm.Turn(self.board, self.team)
        print('tour 2')
        self.draw_game()

    def handle_but_play(self):
        print("On joue une carte")
        print(str(self.team.player_dic[self.username].to_dic()))
        dic_cmd = {'command': 'play_card', 'player': self.team.player_dic[self.username].to_dic()}
        game_dic = self.client.make_message(dic_cmd)
        print(game_dic)
        self.team = gm.Team(game_dic['team'])
        self.board = gm.Board(game_dic['board'])
        self.turn = game_dic['turn']
        print(self.turn['endgame_message'])
        if self.turn['endgame_message'] is not None:
            print('PEERDUU')
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(self.turn['endgame_message'])
            msg.setInformativeText("Nombre de tour : " + str(int((self.turn["turn_count"]-1)/len(self.team.player_dic))))
            msg.setWindowTitle("Fin de la partie")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.buttonClicked.connect(self.end_button)
            msg.exec()
        self.draw_game()

    def end_button(self):
        print("Partie terminée")
        self.but_play.setEnabled(False)
        self.but_dismiss.setEnabled(False)
        self.but_give_clue.setEnabled(False)

    def handle_dismiss(self):
        print("On défausse une carte")
        dic_cmd = {'command': 'discard_card', 'player': self.team.player_dic[self.username].to_dic()}
        game_dic = self.client.make_message(dic_cmd)
        print(game_dic)
        self.team = gm.Team(game_dic['team'])
        self.board = gm.Board(game_dic['board'])
        self.draw_game()

    def handle_give_clue(self): #TODO
        print("On donne une information")
        dic_cmd = {'command': 'give_clue', 'player': self.team.player_dic[self.username].to_dic()}
        game_dic = self.client.make_message(dic_cmd)
        print(game_dic)
        self.team = gm.Team(game_dic['team'])
        self.board = gm.Board(game_dic['board'])
        self.draw_game()

    def handle_card_clicked(self):
        dic_cmd = {'command': 'card_selected', 'team': self.team.to_dic()}
        print("card clicked 1")
        game_dic = self.client.make_message(dic_cmd)
        print("card clicked 2")

# Definition de la classe Qcarte ---------------------------
class QCarte(QPushButton):
    # Classe graphique pour representer une carte
    def __init__(self, carte=None, hidden=False):
        QPushButton.__init__(self)
        self.pixmap = QPixmap()
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
        self.set_highlight()
        self.setStyleSheet("QPushButton {border-style: outset; border-width: 0px;}")

    def __str__(self):
        return self.carte

    def set_image(self, path):
        self.pixmap = QPixmap(path)
        # self.pixmap = self.pixmap.scaled(250, 250)

        ButtonIcon = QIcon(self.pixmap)
        self.setIcon(ButtonIcon)
        self.setIconSize(self.pixmap.rect().size())
        # self.setFixedSize(self.pixmap.size())

    def on_click(self):
        mes_click_card = pyqtSignal(str)
        if self.isclickable:
            if self.selected:
                if self.hidden:
                    path_to_im = "images/hidden"
                else:
                    path_to_im = "images/" + self.carte.to_string()
                self.selected = False
                self.carte.selected = False
                self.setChecked(False)
                self.setStyleSheet("border: 0px solid red")
                self.set_highlight()
            else:
                if self.hidden:
                    path_to_im = "images/small/hidden"
                    # self.setF
                else:
                    path_to_im = "images/" + self.carte.to_string()
                self.selected = True
                self.carte.selected = True
                self.setChecked(True)
                self.set_highlight()

    def set_highlight(self):
        if self.selected:
            effect = QGraphicsDropShadowEffect()
            effect.setBlurRadius(20)
            effect.setOffset(0)
            effect.setColor(Qt.black)
            self.setGraphicsEffect(effect)
        else:
            self.setGraphicsEffect(None)


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
    card_clicked = pyqtSignal()

    def __init__(self, user = ""):
        QWidget.__init__(self)
        self.layout_hands = QVBoxLayout()
        self.setLayout(self.layout_hands)
        self.username = user
        self.team = gm.Team()

    def add_hand(self, player, current_player, team):
        self.team = team
        wid_hand = QWidget()
        layout_hand = QVBoxLayout()
        wid_hand.setLayout(layout_hand)
        layout_card = QHBoxLayout()
        wid_name = QLabel(player.name)
        if player.name == current_player:
            effect = QGraphicsDropShadowEffect()
            effect.setBlurRadius(20)
            effect.setOffset(0)
            effect.setColor(Qt.black)
            wid_name.setGraphicsEffect(effect)
        layout_hand.addWidget(wid_name)
        wid_cards = QWidget()
        layout_hand.addWidget(wid_cards)
        wid_cards.setLayout(layout_card)
        screen_size = self.screen().size()
        scr_x = screen_size.width()
        scr_y = screen_size.height()
        for carte in player.card_list.card_list:
            wid_carte = QCarte(carte, self.username == player.name)
            wid_carte.pixmap = wid_carte.pixmap.scaled(int(scr_x/12), int(scr_x/12))
            wid_carte.setIcon(QIcon(wid_carte.pixmap))
            wid_carte.setFixedSize(wid_carte.pixmap.size())
            wid_carte.clicked.connect(self.card_clicked)
            layout_card.addWidget(wid_carte)
        self.layout_hands.addWidget(wid_hand)

    # def card_selected(self):
        # print("selected 1")
        # dic_cmd = {'command':'card_selected', 'team': self.team.to_dic()}
        # print("selected 2")
        # message = self.client.make_message(dic_cmd)
        # print("selected 3")

    def add_team(self, team, user, current_player):
        self.username = user
        self.clear_hands()
        for player_name in team.player_dic.keys():
            self.add_hand(team.player_dic[player_name], current_player, team)

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
        # self.img_label.setPixmap(self.board_pixmap)
        self.layout = QFormLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.img_label)

        # On definit le layout principal
        self.layout_board = QVBoxLayout()
        self.layout_board.setSpacing(0)

        # On créé le layout pour les erreurs commises
        self.layout_error = QHBoxLayout()
        self.wid_error = QWidget()
        self.wid_error.setLayout(self.layout_error)
        self.layout_board.addWidget(self.wid_error, 1641)

        # On affiche les tas a remplir
        self.img_label.setLayout(self.layout_board)
        self.layout_tas = QHBoxLayout()
        self.wid_tas = QWidget()
        self.wid_tas.setLayout(self.layout_tas)
        self.layout_board.addWidget(self.wid_tas, 2052)

        # On affiche les indices
        self.layout_clue = QHBoxLayout()
        self.wid_clues = QWidget()
        self.wid_clues.setLayout(self.layout_clue)
        # self.layout_board.addWidget(self.wid_clues)
        self.layout_board.addWidget(self.wid_clues, 1425)

        # On affiche la pioche, la carte jouee et la defausse
        self.wid_draw_play_disc = QWidget()
        self.layout_dpd = QHBoxLayout()
        self.wid_draw_play_disc.setLayout(self.layout_dpd)
        self.wid_pioche = QLabel()
        im_pioche = QImage("images/hanabi_background_card")
        self.wid_pioche.setPixmap(QPixmap("images/hanabi_background_card"))
        self.wid_play_card = QCarte()
        self.wid_dism_stack = QCarte()
        self.layout_dpd.addWidget(self.wid_pioche)
        self.layout_dpd.addWidget(self.wid_play_card)
        self.layout_dpd.addWidget(self.wid_dism_stack)
        self.layout_board.addWidget(self.wid_draw_play_disc, 1378)

        self.resize_board()

    def resize_board(self):
        # update geometry / Voir si on peut utiliser frameGeometry
        # res_x = self.fenetre.frameGeometry().width()
        # res_y = self.fenetre.frameGeometry().height()
        res_x = self.screen().size().width()
        res_y = self.screen().size().height()
        ratio_x = 0.5
        ratio_y = 1
        p = self.board_pixmap.scaled(int(ratio_x*res_x), int(ratio_y*res_y), Qt.KeepAspectRatio)
        self.img_label.setPixmap(p)
        # self.img_label.setStyleSheet("QLabel {border-style: outset; border-width: 3px;}")

        # self.img_label.resize(p.rect().size())
        self.img_label.setFixedHeight(p.rect().size().height())
        self.img_label.setFixedWidth(p.rect().size().width())

        # print("Img_label : " + str(self.img_label.width()) + " " + str(self.img_label.height()))
        # print("p : " + str(p.width()) + " " + str(p.height()))
        self.board_x = p.width()
        self.board_y = p.height()

        # On affiche le nombre d'erreurs
        for error_i in range(self.layout_error.count()):
            # pix_error = QPixmap("images/token/token_error")
            pix_error = self.layout_error.itemAt(error_i).widget().pixmap()
            pix_error = pix_error.scaled(int(self.board_x*0.035), int(self.board_x*0.035), Qt.KeepAspectRatio)
            self.layout_error.itemAt(error_i).widget().setPixmap(pix_error)
            self.layout_error.itemAt(error_i).widget().setFixedWidth(pix_error.rect().size().width())
        self.layout_error.setContentsMargins(int(0.397 * self.board_x), int(150/6496 * self.board_y),
                                             int(0.412 * self.board_x), int(1116/6496* self.board_y))

        # On affiche les tas a remplir
        for stack_i in range(self.layout_tas.count()):
            pix_stack = self.layout_tas.itemAt(stack_i).widget().pixmap()
            pix_stack = pix_stack.scaled(int(0.19*self.board_x), int(0.32*self.board_y), Qt.KeepAspectRatio)
            self.layout_tas.itemAt(stack_i).widget().setPixmap(pix_stack)
        # self.layout_tas.setSpacing(int(self.board_x*0.011))
        self.layout_tas.setContentsMargins(int(self.board_x*0.143), int(self.board_y*0.0), int(self.board_x*0.14), int(self.board_y*0.0))

        # On affiche les indices
        for clue_i in range(self.layout_clue.count()):
            pix_clue = self.layout_clue.itemAt(clue_i).widget().pixmap()
            pix_clue = pix_clue.scaled(int(self.board_x*0.035), int(self.board_x*0.035), Qt.KeepAspectRatio)
            self.layout_clue.itemAt(clue_i).widget().setPixmap(pix_clue)
        self.layout_clue.setSpacing(int(self.board_x*0.013))
        self.layout_clue.setContentsMargins(int(self.board_x*0.292), int(724/6496*self.board_y), int(self.board_x*0.292), int(432/6496*self.board_y))

        # On affiche les elements du dpd
        pix_dpd = self.wid_pioche.pixmap()
        pix_dpd = pix_dpd.scaled(int(0.15 * self.board_x), int(0.15 * self.board_y), Qt.KeepAspectRatio)
        pix_dpd = pix_dpd.scaled(int(0.15 * self.board_x), int(0.15 * self.board_y), Qt.KeepAspectRatio)
        self.wid_pioche.setPixmap(pix_dpd)
        self.wid_pioche.setFixedSize(pix_dpd.size())
        for dpd_i in range(1,self.layout_dpd.count()):
            pix_dpd = QPixmap(self.layout_dpd.itemAt(dpd_i).widget().image)
            pix_dpd = pix_dpd.scaled(int(0.15*self.board_x), int(0.15*self.board_y), Qt.KeepAspectRatio)
            self.layout_dpd.itemAt(dpd_i).widget().setIcon(QIcon(pix_dpd))
            self.layout_dpd.itemAt(dpd_i).widget().setFixedSize(pix_dpd.size())
            self.layout_dpd.itemAt(dpd_i).widget().setStyleSheet("QCarte {border-style: outset; border-width: 3px;}")
        self.layout_dpd.setSpacing(int(self.board_x*0.01))
        lat_sp = 0.19
        self.layout_dpd.setContentsMargins(int(lat_sp*self.board_x), int(0.011*self.board_y),
                                           int(lat_sp*0.992*self.board_x), int(279/6496*self.board_y))
        # if self.fenetre.size().width > self.screen().size().width()
        #     self.fenetre.setsi

    def add_board(self, board):
        self.clear_board()
        # On affiche le nombre d'erreurs
        for error_i in range(3):
            lab_error = QLabel()
            if error_i >= board.miss:
                pix_error = QPixmap("images/token/token_transp")
            else:
                pix_error = QPixmap("images/token/token_error")
            lab_error.setPixmap(pix_error)
            self.layout_error.addWidget(lab_error)

        # On affiche les stacks
        for stack_key in board.stack_dic.keys():
            stack = board.stack_dic[stack_key]
            lab_stack = QLabel()
            if len(stack.card_list) > 0:
                carte_top = stack.card_list[-1]
                pix_stack = QPixmap("images/stack_" + carte_top.color + str(carte_top.value))
                pix_stack = pix_stack.scaled(int(0.125*self.board_x), int(0.33*self.board_y), Qt.KeepAspectRatio)
            else:
                pix_stack = QPixmap("images/empty_stack")
                pix_stack = pix_stack.scaled(int(0.125*self.board_x), int(0.33*self.board_y), Qt.KeepAspectRatio)
                print("Pas de carte " + stack_key)
            lab_stack.setPixmap(pix_stack)
            self.layout_tas.addWidget(lab_stack)
        # On affiche les indices
        for clue_i in range(8):
            lab_clue = QLabel()
            if clue_i >= board.clues:
                pix_clue = QPixmap("images/token/token_transp")
            else:
                pix_clue = QPixmap("images/token/token_clue")
            lab_clue.setPixmap(pix_clue)
            self.layout_clue.addWidget(lab_clue)
        # On affiche les piles de pioche, la carte jouee et la defausse
        # TODO ajouter la carte jouee
        self.wid_pioche = QLabel()
        default_pixmap = QPixmap("images/hidden")
        self.wid_pioche.setPixmap(default_pixmap)
        self.wid_pioche.setFixedSize(default_pixmap.size())
        painter = QPainter()
        painter.begin(self.wid_pioche.pixmap())
        painter.setPen(QColor(255, 255, 255, 190))
        painter.setFont(QFont('Decorative', 280))
        painter.drawText(self.wid_pioche.rect(), Qt.AlignCenter, str(len(board.draw_list.card_list)))
        painter.end()
        self.layout_dpd.addWidget(self.wid_pioche)
        if len(board.discard_list.card_list)>0:
            self.wid_dism_stack = QCarte(board.discard_list.card_list[-1])
        else:
            self.wid_dism_stack = QCarte()
        self.layout_dpd.addWidget(self.wid_dism_stack)
        self.wid_play_card = QCarte()
        self.layout_dpd.addWidget(self.wid_play_card)
        self.resize_board()

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
