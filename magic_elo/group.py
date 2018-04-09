import sys


class Group:
    def __init__(self):
        self.decks = []

    def add_deck(self, deck):
        self.decks.append(deck)

    def do(self):
        print(f'Match, List, Add')
        for line in sys.stdin:
            if line in ['M', 'm']:
                self.match()
            if line in ['L', 'l']:
                self.list()
            if line in ['A', 'a']:
                self.new_deck()
            break

    def new_deck(self):
        pass

    def match(self):
        print('deck 1 ?')
        for line in sys.stdin:
            deck1 = self.decks[int(line) - 1]
            break
        print('deck 2 ?')
        for line in sys.stdin:
            deck2 = self.decks[int(line) - 1]
            break
        print(f'match: {deck1.title} vs {deck2.title}')
        print(f'  result: W/N/L ?')
        for line in sys.stdin:
            if line in ['W', 'w', 'win']:
                self.win(deck1, deck2)
            if line in ['N', 'n', 'null']:
                self.null(deck1, deck2)
            if line in ['L', 'l', 'loss']:
                self.win(deck2, deck1)
            break

    def list(self):
        self.decks = sorted(self.decks, key=lambda d: -d.elo)
        for i in range(0, len(self.decks)):
            print(f'{i}. {self.decks[i].title}')

    def win(self, deck1, deck2):
        elo_1 = deck1.elo
        deck1.win(deck2.elo)
        deck2.loss(elo_1)

    def null(self, deck1, deck2):
        elo_1 = deck1.elo
        deck1.null(deck2.elo)
        deck2.null(elo_1)
