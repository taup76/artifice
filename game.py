import random


class Card:
    def __init__(self, color=None, value=None, dic=None):
        if dic is None:
            if color is not None:
                self.color = color
            else:
                self.color = 'N'
            if value is not None:
                self.value = value
            else:
                self.value = 0
            self.selected = False
            self.revealed = 0  # note about w
        else:
            self.from_dic(dic)


    def to_string(self):
        return self.color + '' + str(self.value)

    def to_dic(self):
        return {"color": self.color, "value": self.value, "selected": self.selected, "revealed": self.revealed}

    def from_dic(self, dic):
        self.color = dic["color"]
        self.value = dic["value"]
        self.selected = dic["selected"]
        self.revealed = dic["revealed"]


class Stack:
    def __init__(self, array=None):
        if array is None:
            self.card_list = []
        else:
            self.card_list = []
            self.from_array(array)

    def to_string(self):
        str_cards = "Stack : "
        for card in self.card_list:
            str_cards += card.to_string() + " "
        return str_cards

    def append(self, card):
        self.card_list.append(card)

    def pop(self, idx):
        return self.card_list.pop(idx)

    def shuffle(self):
        random.shuffle(self.card_list)

    def unselect_all(self):
        for card in self.card_list:
            card.selected = False

    def to_array(self):
        array = []
        for card in self.card_list:
            array.append(card.to_dic())
        return array

    def from_array(self, arr):
        for dic_card in arr:
            card = Card(dic=dic_card)
            self.append(card)

    def get_length(self):
        return len(self.card_list)


class Board:
    def __init__(self, dic=None):
        if dic is None:
            self.stack_dic = {'r': Stack(), 'b': Stack(), 'y': Stack(), 'g': Stack(), 'w': Stack()}
            self.draw_list = Stack()
            self.discard_list = Stack()
            self.clues = 8
            self.miss = 0
            # self.init_draw()
        else:
            self.stack_dic = {}
            self.from_dic(dic)

    def to_string(self):
        out_str = 'stacks \n'
        for key in self.stack_dic.keys():
            out_str += key + ' '
            print(self.stack_dic[key])
            for card in self.stack_dic[key].card_list:
                out_str += card.to_string() + ' '
            out_str += '\n'
        out_str += "\n draw :" + str(len(self.draw_list)) + " cards"
        out_str += "\n discard :" + str(len(self.discard_list)) + " cards"
        out_str += "\n clues :" + str(self.clues)
        out_str += "\n miss :" + str(self.miss)
        return out_str

    def to_dic(self):
        json_stack_dic = {}
        for key in self.stack_dic.keys():
            json_stack_dic[key] = self.stack_dic[key].to_array()

        return {"stack_dic": json_stack_dic,
               "draw_list": self.draw_list.to_array(),
               "discard_list": self.discard_list.to_array(),
               "clues": self.clues,
               "miss": self.miss}

    def from_dic(self, dic):
        self.miss = dic["miss"]
        self.clues = dic["clues"]
        self.draw_list = Stack(dic["draw_list"])
        self.discard_list = Stack(dic["discard_list"])
        for key in dic["stack_dic"].keys():
            self.stack_dic[key] = Stack(dic["stack_dic"][key])

    def init_draw(self):
        for i in range(1, 6):
            rep = 2
            if i == 1:
                rep = 3
            if i == 5:
                rep = 1

            for color in self.stack_dic.keys():
                for j in range(rep):
                    self.draw_list.append(Card(color, i))
        self.draw_list.shuffle()

    def add_clue(self):
        if self.clues < 8:
            self.clues = self.clues + 1

    def take_clue(self):
        if self.clues > 0:
            self.clues = self.clues - 1

    def take_miss(self):
        self.miss = self.miss + 1

    def play_card(self, card):
        target_stack = self.stack_dic[card.color]
        if len(target_stack.card_list) + 1 == card.value:
            # if ok, add to stack
            self.stack_dic[card.color].append(card)
            # if Hanabi, add clue
            if self.stack_dic[card.color].get_length() == 5:
                self.add_clue()
        else:
            # otherwise, discard card and add miss counter
            self.discard_list.append(card)
            self.take_miss()

    def count_score(self):
        count_score = 0
        for stack in self.stack_dic:
            count_score += len(self.stack_dic[stack].card_list)
        return count_score

    def draw_empty(self):
        return len(self.draw_list.card_list) == 0


class Player:

    def __init__(self, name=None, dic=None):
        if dic is None:
            self.name = name
            self.card_list = Stack()
        else:
            self.from_dic(dic)

    def to_string(self):
        out_str = "Player " + self.name + '\n'
        for card in self.card_list:
            out_str += card.to_string() + ' '
        return out_str

    def to_dic(self):
        return {"name": self.name,
                "card_list": self.card_list.to_array()}

    def from_dic(self, dic):
        self.name = dic["name"]
        self.card_list = Stack(dic["card_list"])

    def init_hand(self, board, nb_card):
        for i in range(nb_card):
            self.draw_card(board)

    def append(self, card):
        self.card_list.append(card)

    def take(self, idx):
        return self.card_list.pop(idx)

    def draw_card(self, board):
        if len(board.draw_list.card_list) > 0:
            card = board.draw_list.pop(0)
            self.append(card)

    def play_card(self, board, idx):
        card = self.take(idx)
        # check whether card can be added to stack or not
        board.play_card(card)
        self.draw_card(board)

    def discard_card(self, board, idx):
        card = self.take(idx)
        board.discard_list.append(card)
        board.add_clue()
        self.draw_card(board)

    def receive_clue(self):
        for card in self.card_list.card_list:
            if card.selected:
                print("REVEALED!!")
                card.revealed = card.revealed + 1

    def has_selected_card(self):
        for card in self.card_list.card_list:
            if card.selected:
                return True
        return False


class Team:
    def __init__(self, dic=None):
        if dic is None:
            self.player_dic = {}
        else:
            self.player_dic = {}
            self.from_dic(dic)

    def add_player(self, player):
        if player.name in self.player_dic:
            return "Nom déjà pris"
        self.player_dic[player.name] = player
        return ""

    def init_hands(self, board):
        nb_cards = 4
        if len(self.player_dic) < 4:
            nb_cards = 5

        for player in self.player_dic:
            self.player_dic[player].init_hand(board, nb_cards)

    def unselect_all(self):
        for player in self.player_dic:
            self.player_dic[player].card_list.unselect_all()

    def to_dic(self):
        dic = {}
        for key in self.player_dic.keys():
            dic[key] = self.player_dic[key].to_dic()
        return dic

    def from_dic(self, dic):
        for key in dic.keys():
            self.player_dic[key] = Player(key, dic[key])


class Turn:

    def __init__(self, board, team):
        self.turn_count = 0
        self.last_turn = 0
        self.current_player = None
        self.endgame_message = None
        self.board = board
        self.team = team

    def to_dic(self):
        return {"turn_count": self.turn_count,
                "current_player": self.current_player,
                "endgame_message": self.endgame_message}

    def next_turn(self):
        # increment turn
        self.turn_count += 1
        # next player
        player_names = sorted(self.team.player_dic.keys())
        self.current_player = player_names[self.turn_count % len(player_names)]
        # if 3 errors
        if self.board.miss == 3:
            self.endgame_message = "Vous avez perdu !"
            return
        # if all stacks are filled
        if self.board.count_score() == 25:
            self.endgame_message = "Vous avez gagné ! \n" \
                                    + " Légendaire, petits et grands sans voix, des étoiles dans les yeux"
            return
        # if stack is empty, each player has one extra turn
        if self.board.draw_empty() and self.last_turn == 0:
            self.last_turn = self.turn_count + len(player_names)
            return
        # if stack empty and last turn has been reached
        if self.board.draw_empty() and self.turn_count > self.last_turn:
            score = self.board.count_score()
            if score <= 5:
                self.endgame_message = "Score final " + str(score)+ "/25\n Horrible, huées de la foule..."
            elif score <= 10:
                self.endgame_message = "Score final " + str(score)+ "/25\n Médiocre, à peine quelques applaudissements."
            elif score <= 15:
                self.endgame_message = "Score final " + str(score)+ "/25\n Honorable, mais ne restera pas dans les mémoires..."
            elif score <= 20:
                self.endgame_message = "Score final " + str(score)+ "/25\n Excellente, ravit la foule"
            elif score <= 25:
                self.endgame_message = "Score final " + str(score)+ "/25\n Extraordinaire, restera gravée dans les mémoires !"
            return

class Game:

    def __init__(self):
        self.is_init = False
        self.is_started = False
        self.team = None
        self.board = None
        self.turn = None

    def to_dic(self):
        return {"board": self.board.to_dic(),
                "team": self.team.to_dic(),
                "turn": self.turn.to_dic()}

    def init_game(self):
        if self.is_init:
            return "Game already initialized"

        self.board = Board()
        self.team = Team()
        self.turn = Turn(self.board, self.team)
        self.is_init = True
        return ""

    def join_game(self, player_name):
        if not self.is_init:
            self.init_game()
        if self.is_started:
            return "Le jeu est déjà lancé"
        if len(self.team.player_dic) >= 5:
            return "Nombre maximal de joueurs atteint"

        return self.team.add_player(Player(player_name))

    def start_game(self):
        if not self.is_init:
            return "Game is not initialized yet"
        if self.is_started:
            return "Game is already started"
        self.board.init_draw()
        self.team.init_hands(self.board)
        self.is_started = True

        # start first turn
        self.turn.next_turn()

        return ""

    def finish_game(self):
        self.is_init = False
        self.is_started = False
        self.team = None
        self.board = None
        self.turn = None
        return ""

    def get_player_and_card_idx(self, player_dic):
        error_msg = ""
        current_player = Player("")
        # create player from received message
        print(player_dic)
        rcvd_player = Player(dic=player_dic)

        if rcvd_player.name != self.turn.current_player:
            return "", "", "This is not your turn"

        # look for selected index
        selected_card_idx = -1
        card_list = rcvd_player.card_list.card_list

        for i in range(len(card_list)):
            print("color  " + card_list[i].color)
            print(card_list[i].selected)
            if card_list[i].selected:
                selected_card_idx = i
                break
        if selected_card_idx < 0:
            error_msg = "No card selected"

        if rcvd_player.name not in self.team.player_dic.keys():
            error_msg = "Player not in game"
        else:
            current_player = self.team.player_dic[rcvd_player.name]

        return current_player, selected_card_idx, error_msg

    def find_target_player(self):
        target_player = Player()
        error_str = ""
        for player_name in self.team.player_dic:
            player = self.team.player_dic[player_name]
            if player.has_selected_card() and (player_name != self.turn.current_player):
                target_player = player
                break
        if target_player.name is None:
            error_str = "No card selected"

        return target_player, error_str

    def play_card(self, player_dic):
        current_player, selected_card_idx, error_str = self.get_player_and_card_idx(player_dic)
        if len(error_str) > 0:
            return error_str

        current_player.play_card(self.board, selected_card_idx)
        self.team.unselect_all()
        self.turn.next_turn()
        return ""

    def give_clue(self, current_player):
        if current_player != self.turn.current_player:
            return "This is not your turn"

        # find player with selected cards
        target_player, error_str = self.find_target_player()
        if len(error_str) > 0:
            return error_str

        # if no clue left, cannot give any clue
        if self.board.clues == 0:
            return "You cannot give any more clue"

        target_player.receive_clue()
        self.board.take_clue()
        self.team.unselect_all()
        self.turn.next_turn()
        return ""

    def discard_card(self, player_dic):
        current_player, selected_card_idx, error_str = self.get_player_and_card_idx(player_dic)
        if len(error_str) > 0:
            return error_str
        current_player.discard_card(self.board, selected_card_idx)

        self.team.unselect_all()
        self.turn.next_turn()

        return ""

    def update_team(self, team_msg):
        self.team = Team(team_msg)
