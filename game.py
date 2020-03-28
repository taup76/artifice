import random


class Card:
    def __init__(self, color=None, value=None, dic=None):
        if dic is None:
            self.color = color
            self.value = value
            self.selected = False
        else:
            self.from_dic(dic)

    def to_string(self):
        return self.color + '' + str(self.value)

    def to_dic(self):
        return {"color": self.color, "value": self.value}

    def from_dic(self, dic):
        self.color = dic["color"]
        self.value = dic["value"]


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
            self.miss = 3
            self.init_draw()
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
            self.stack_dic["key"] = Stack(dic["stack_dic"][key])

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
        self.miss = self.miss - 1

    def play_card(self, card):
        target_stack = self.stack_dic[card.color]
        if len(target_stack) + 1 == card.value:
            # if ok, add to stack
            self.stack_dic[card.color].append(card)
        else:
            # otherwise, discard card and add miss counter
            self.discard_list.append(card)
            self.take_miss()


class Player:

    def __init__(self, name, dic=None):
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
        card = board.draw_list.pop(0)
        self.append(card)

    def play_card(self, board, idx):
        card = self.take(idx)
        # check whether card can be added to stack or not
        board.play_card(card)

    def discard_card(self, board, idx):
        card = self.take(idx)
        self.discard_list.append(card)
        board.add_clue()


class Team:
    def __init__(self, dic=None):
        if dic is None:
            self.player_dic = {}
        else:
            self.player_dic = {}
            self.from_dic(dic)

    def add_player(self, player):
        self.player_dic[player.name] = player

    def init_hands(self, board):
        nb_cards = 4
        if len(self.player_dic) < 4:
            nb_cards = 5

        for player in self.player_dic:
            self.player_dic[player].init_hand(board, nb_cards)

    def to_dic(self):
        dic = {}
        for key in self.player_dic.keys():
            dic[key] = self.player_dic[key].to_dic()
        return dic

    def from_dic(self, dic):
        for key in dic.keys():
            self.player_dic[key] = Player(key, dic[key])

class Game:
    def __init__(self):
        self.is_init = False
        self.is_started = False
        self.team = None
        self.board = None

    def to_dic(self):
        return {"board": self.board.to_dic(), "team": self.team.to_dic()}

    def init_game(self):
        if self.is_init:
            return "Game already initialized"

        self.board = Board()
        self.team = Team()
        self.is_init = True
        return ""

    def join_game(self, player_name):
        if not self.is_init:
            self.init_game()
        if self.is_started:
            return "Game is already started"
        if len(self.team.player_dic) >= 5:
            return "Cannot add any more player"

        self.team.add_player(Player(player_name))
        return ""

    def start_game(self):
        if not self.is_init:
            return "Game is not initialized yet"
        if self.is_started:
            return "Game is already started"
        self.board.init_draw()
        self.team.init_hands(self.board)
        self.is_started = True
        return ""

    def finish_game(self):
        self.is_init = False
        self.is_started = False
        self.team = None
        self.board = None
        return ""

    def play_card(self, username, card_idx):
        return ""

    def give_clue(self, username, card_idx_list):
        return ""

    def discard_card(self, username, card_idx):
        return ""
