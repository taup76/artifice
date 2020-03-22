import random
#import zmq


class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def to_string(self):
        return self.color + '' + str(self.value)


class Stack:
    card_list = []

    def append(self, card):
        self.card_list.append(card)


class Board:
    def __init__(self):
        self.stack_list = {'r': [], 'b': [], 'y': [], 'g': [], 'w': []}
        self.draw_list = []
        self.discard_list = []
        self.clues = 8
        self.miss = 3
        self.init_draw()

    def to_string(self):
        out_str = 'stacks \n'
        for key in self.stack_list.keys():
            out_str += key + ' '
            for card in self.stack_list[key]:
                out_str += card.to_string() + ' '
            out_str += '\n'
        out_str += "\n draw :" + str(len(self.draw_list)) + " cards"
        out_str += "\n discard :" + str(len(self.discard_list)) + " cards"
        out_str += "\n clues :" + str(self.clues)
        out_str += "\n miss :" + str(self.miss)
        return out_str

    def init_draw(self):
        for i in range(1, 6):
            rep = 2
            if i == 1:
                rep = 3
            if i == 5:
                rep = 1

            for color in self.stack_list.keys():
                for j in range(rep):
                    self.draw_list.append(Card(color, i))
        random.shuffle(self.draw_list)

    def add_clue(self):
        if self.clues < 8:
            self.clues = self.clues + 1

    def take_clue(self):
        if self.clues > 0:
            self.clues = self.clues - 1

    def take_miss(self):
        self.miss = self.miss - 1

    def play_card(self, card):
        target_stack = self.stack_list[card.color]
        if len(target_stack) + 1 == card.value:
            # if ok, add to stack
            self.stack_list[card.color].append(card)
        else:
            # otherwise, discard card and add miss counter
            self.discard_list.append(card)
            self.take_miss()


class Player:

    def __init__(self, name):
        self.name = name
        self.card_list = []

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

    def to_string(self):
        out_str = "Player " + self.name + '\n'
        for card in self.card_list:
            out_str +=  card.to_string() + ' '
        return out_str



def main():

    myBoard = Board()

    my_player1 = Player('Celine')
    my_player2 = Player('Simon')
    my_player1.init_hand(myBoard, 4)
    my_player2.init_hand(myBoard, 4)
    for i in range(4):
        my_player2.play_card(myBoard, 0)
    print(my_player1.to_string())
    print(my_player2.to_string())
    print(myBoard.to_string())

if __name__ == "__main__":
    # execute only if run as a script
    main()