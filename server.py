class Card :
    color = ''
    value = 0

class Stack:
    cardList = []

    def append(self, card):
        self.cardList.append(card)


def main():
    print("hello world!")
    myCard = Card()
    myCard.color ='r'
    myStack = Stack

if __name__ == "__main__":
    # execute only if run as a script
    main()