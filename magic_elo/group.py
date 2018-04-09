from magic_elo.deck import Deck


class Group:
    def __init__(self, save_name='magic-elo.save'):
        self.decks = {}
        self.save_name = save_name

    def add_deck(self, deck):
        if deck.name.lower() in self.decks:
            print(f'there is already a deck name \'{deck.name}\'')
            return
        self.decks[deck.name.lower()] = deck
        print(f'new deck: {deck.title}')

    def run(self):
        stop = False
        while not stop:
            message = 'Add/Quit ? '
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
            if x in ['Q', 'q']:
                stop = True

    def new_deck(self):
        name = input('deck name ? ')
        while ';' in name:
            print('no \';\' in deck name')
            name = input('deck name ? ')
        colors = ['w', 'u', 'b', 'r', 'g']
        deck_colors = {}
        for c in colors:
            deck_colors[c] = int(input(f'{c} ? '))
        deck = Deck(name, **deck_colors)
        self.add_deck(deck)
        self.save()

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
        self.save()

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

    def save(self):
        with open(self.save_name, 'w') as f:
            for deck in self.deck_list:
                data = [deck.name, deck.w, deck.u, deck.b, deck.r, deck.g, deck.elo, deck.wins, deck.nulls, deck.losses]
                txt = ';'.join([str(d) for d in data])
                f.write(txt + '\n')

    def load(self):
        try:
            with open(self.save_name, 'r') as f:
                for line in f.readlines():
                    data = line.split(';')
                    if len(data) >= 10:
                        deck = Deck(data[0], int(data[1]), int(data[2]), int(data[3]), int(data[4]), int(data[5]))
                        deck.elo = float(data[6])
                        deck.wins = int(data[7])
                        deck.nulls = int(data[8])
                        deck.losses = int(data[9])
                        deck.update_coef()
                        self.add_deck(deck)
                    else:
                        print(line)

        except FileNotFoundError:
            print(f'no save named {self.save_name}')
