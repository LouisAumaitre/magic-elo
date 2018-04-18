from typing import List

from magic_elo.deck import Deck


class Action:
    def __init__(self, name: str, shortcut: str, run):
        self.name = name
        self.shortcuts = [name.lower(), shortcut.lower()]
        self.run = run


class Group:
    def __init__(self, save_name='magic-elo.save'):
        self._stop = False
        self.decks = {}
        self.save_name = save_name
        self.load()

    def add_deck(self, deck):
        if deck.name.lower() in self.decks:
            print(f'there is already a deck name \'{deck.name}\'')
            return
        self.decks[deck.name.lower()] = deck
        print(f'new deck: {deck.title}')

    def run(self):
        self._stop = False
        while not self._stop:
            actions: List[Action] = []
            if len(self.decks) > 0:
                actions.append(Action('List', 'L', lambda: self.list()))
                actions.append(Action('Edit', 'E', lambda: self.edit()))
            if len(self.decks) > 1:
                actions.append(Action('Match', 'M', lambda: self.match()))
            actions.append(Action('Add', 'A', lambda: self.new_deck()))
            actions.append(Action('Stats', 'S', lambda: self.stats()))
            actions.append(Action('Quit', 'Q', lambda: self.stop()))

            message = ''
            for a in actions:
                message = message + '/' + a.name
            message = message[1:] + ' ? '

            x = input(message).lower()
            for a in actions:
                if x in a.shortcuts:
                    a.run()

    def stop(self):
        self._stop = True

    def new_deck(self):
        name = input('deck name ? ')
        while ';' in name:
            print('no \';\' in deck name')
            name = input('deck name ? ')
        colors = ['w', 'u', 'b', 'r', 'g']
        deck_colors = {}
        for c in colors:
            c_input = input(f'{c} ? ')
            if c_input != '':
                deck_colors[c] = int(c_input)
        deck = Deck(name, **deck_colors)
        self.add_deck(deck)
        self.save()

    def edit(self):
        deck = self.select_deck()
        name = input(f'deck name [{deck.name}] ? ')
        while ';' in name:
            print('no \';\' in deck name')
            name = input(f'deck name [{deck.name}] ? ')
        if name != '':
            deck.name = name
        colors = ['w', 'u', 'b', 'r', 'g']
        for c in colors:
            c_input = input(f'{c} [{deck.__getattribute__(c)}] ? ')
            if c_input != '':
                deck.__setattr__(c, int(c_input))
        self.decks[deck.name] = deck
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
            int_s = str(i + 1).rjust(3)
            print(f'{margin}{int_s}. {deck_list[i].title}')

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
                data = [
                    deck.name, deck.w, deck.u, deck.b, deck.r, deck.g, deck.elo, deck.wins, deck.nulls, deck.losses,
                    deck.coef,
                ]
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
                        deck.coef = int(data[10])
                        deck.update_coef()
                        self.add_deck(deck)
                    else:
                        print(line)

        except FileNotFoundError:
            print(f'no save named {self.save_name}')

    def stats(self):
        print(f'decks: {len(self.decks)}')
        matches = sum([d.wins + d.nulls/2 for d in self.decks.values()])
        print(f'matches: {matches}')
        colors = {'w': 0, 'u': 0, 'b': 0, 'r': 0, 'g': 0}
        elo = {'w': 0, 'u': 0, 'b': 0, 'r': 0, 'g': 0}
        for d in self.decks.values():
            for k, v in d.color_repartition.items():
                colors[k] += v
                elo[k] += d.elo * v
        total = sum(colors.values())
        color_message = ''
        elo_message = ''
        for c, v in colors.items():
            color_message += (c.upper() + ': ' + str(round(100 * v / total)) + '%; ').ljust(9)
            elo_message += (c.upper() + ': ' + str(round(elo[c] / v)) + '; ').ljust(9)
        print(color_message)
        print(elo_message)
