import random

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
    stack_list = {'r': [], 'b': [], 'y': [], 'g': [], 'w': []}
    draw_list = []
    discard_list = []
    clues = 8
    miss = 3

    def init_draw(self):
        for i in range(1, 6):
            for color in self.stack_list.keys():
                self.draw_list.append(Card(color, i))
        random.shuffle(self.draw_list)

    def add_clue(self):
        self.clues = self.clues + 1

    def take_clue(self):
        self.clues = self.clues - 1

    def take_miss(self):
        self.miss = self.miss - 1

    def draw_card(self, player):
        card = self.draw_list.pop(0)
        player.append(card)

    def play_card(self, player, idx):
        card = player.take(idx)
        # check whether card can be added to stack or not
        self.stack_list.append(card)

    def discard_card(self, player, idx):
        card = player.take(idx)
        self.discard_list.append(card)
        self.add_clue()


class Player:

    def __init__(self, name):
        self.name = name
        self.card_list = []

    def init_hand(self, board, nb_card):
        for i in range(nb_card):
            board.draw_card(self)

    def append(self, card):
        self.card_list.append(card)

    def take(self, idx):
        return self.card_list.pop(idx)



def main():


    myBoard = Board()
    myBoard.init_draw()

    my_player1 = Player('Celine')
    my_player2 = Player('Simon')
    my_player1.init_hand(myBoard, 4)
    print(my_player1.name)
    print(my_player1.card_list[2].to_string())
    my_player2.init_hand(myBoard, 4)
    print(my_player2.name)
    print(my_player2.card_list[2].to_string())

    # Initialisation de la GUI

if __name__ == "__main__":
    # execute only if run as a script
    main()