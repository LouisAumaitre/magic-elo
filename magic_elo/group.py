from magic_elo.deck import Deck


class Group:
    def __init__(self):
        self.decks = {}

    def add_deck(self, deck):
        self.decks[deck.name.lower()] = deck
        print(f'new deck: {deck.title}')

    def do(self):
        message = 'Add ? '
        if len(self.decks) > 0:
            message = 'List/' + message
        if len(self.decks) > 1:
            message = 'Match/' + message
        x = input(message)
        if x in ['M', 'm']:
            self.match()
        if x in ['L', 'l']:
            self.list()
        if x in ['A', 'a']:
            self.new_deck()

    def new_deck(self):
        name = input('deck name ? ')
        colors = ['w', 'u', 'b', 'r', 'g']
        deck_colors = {}
        for c in colors:
            deck_colors[c] = int(input(f'{c} ? '))
        deck = Deck(name, **deck_colors)
        self.add_deck(deck)

    def match(self):
        deck1 = self.select_deck()
        print(f'deck 1: {deck1.title}')
        deck2 = self.select_deck()
        print(f'deck 2: {deck2.title}')
        if deck1 is deck2:
            print('pick different decks')
            return
        x = input(f'  result: W/N/L ? ')
        if x in ['W', 'w', 'win']:
            self.win(deck1, deck2)
        if x in ['N', 'n', 'null']:
            self.null(deck1, deck2)
        if x in ['L', 'l', 'loss']:
            self.win(deck2, deck1)

    def select_deck(self) -> Deck:
        x = input('deck ? ').lower()
        try:
            int_x = int(x)
            try:
                return self.deck_list[int_x - 1]
            except IndexError:
                print('Out of index')
                self.list(margin='  ')
                return self.select_deck()
        except ValueError:
            for key in self.decks:
                if x == key:
                    return self.decks[key]
                if key.startswith(x):
                    return self.decks[key]
            print('No matching name')
            self.list(margin='  ')
            return self.select_deck()

    @property
    def deck_list(self):
        return sorted(self.decks.values(), key=lambda d: -d.elo)

    def list(self, margin=''):
        deck_list = self.deck_list
        for i in range(0, len(deck_list)):
            print(f'{margin}{i + 1}. {deck_list[i].title}')

    def win(self, deck1, deck2):
        elo_1 = deck1.elo
        deck1.win(deck2.elo)
        deck2.loss(elo_1)

    def null(self, deck1, deck2):
        elo_1 = deck1.elo
        deck1.null(deck2.elo)
        deck2.null(elo_1)
