import math
from typing import Dict, Optional


def proba(dif):
    return 1 / (1 + math.pow(10, -dif / 400))


class MatchInterface:
    @property
    def title(self):
        return NotImplementedError

    @property
    def ready(self):
        return NotImplementedError

    def update(self):
        return NotImplementedError

    @property
    def winner(self):
        return NotImplementedError


class Deck(MatchInterface):
    size = 60

    def __init__(self, name: str, colors: Dict[str, int]):
        self.name = name
        color_names = ['W', 'U', 'B', 'R', 'G']
        self.cards = {name: colors.get(name, 0) for name in color_names}

        self.elo = 1000
        self.wins = 0
        self.nulls = 0
        self.losses = 0

        self.coef = 40

    @property
    def games(self):
        return self.wins + self.nulls + self.losses

    @property
    def colors(self):
        c = ''
        if self.W:
            c += 'W'
        if self.U:
            c += 'U'
        if self.B:
            c += 'B'
        if self.R:
            c += 'R'
        if self.G:
            c += 'G'
        return c

    @property
    def title(self):
        elo = f'[ELO-{round(self.elo)}]'
        return f'{self.name.ljust(30)} {self.colors.ljust(5)} {elo.rjust(10)}'

    def win(self, opponent_elo):
        self.elo = self.elo + self.coef * (1 - proba(self.elo - opponent_elo))
        self.wins += 1
        self.update_coef()
        print(f'  {self.title}')

    def null(self, opponent_elo):
        self.elo = self.elo + self.coef * (0.5 - proba(self.elo - opponent_elo))
        self.nulls += 1
        self.update_coef()
        print(f'  {self.title}')

    def loss(self, opponent_elo):
        self.elo = self.elo + self.coef * (-proba(self.elo - opponent_elo))
        self.losses += 1
        self.update_coef()
        print(f'  {self.title}')

    def update_coef(self):
        if self.elo > 2400 or self.coef == 10:
            self.coef = 10
        elif self.games < 30:
            self.coef = 40
        else:
            self.coef = 20

    def to_data(self) -> str:
        data = [
            'D', self.name, self.W, self.U, self.B, self.R, self.G, self.elo, self.wins, self.nulls, self.losses,
            self.coef,
        ]
        return ';'.join([str(d) for d in data])

    @property
    def W(self):
        return self.cards['W']

    @property
    def U(self):
        return self.cards['U']

    @property
    def B(self):
        return self.cards['B']

    @property
    def R(self):
        return self.cards['R']

    @property
    def G(self):
        return self.cards['G']

    @property
    def total_cards(self):
        return self.W + self.U + self.B + self.R + self.G

    @property
    def w(self):
        return self.W / self.total_cards

    @property
    def u(self):
        return self.U / self.total_cards

    @property
    def b(self):
        return self.B / self.total_cards

    @property
    def r(self):
        return self.R / self.total_cards

    @property
    def g(self):
        return self.G / self.total_cards

    @property
    def color_repartition(self):
        d = {'w': self.w, 'u': self.u, 'b': self.b, 'r': self.r, 'g': self.g}
        return d

    @property
    def ready(self):
        return True

    def update(self):
        pass

    @property
    def winner(self):
        return self

    result = 'D'


def deck_from_data(line: str) -> Optional[Deck]:
    data = line.split(';')
    if len(data) >= 11:
        try:
            colors = ['W', 'U', 'B', 'R', 'G']
            card_colors = {}
            for i in range(5):
                card_colors[colors[i]] = int(data[i + 2])
            deck = Deck(data[1], card_colors)
            deck.elo = float(data[7])
            deck.wins = int(data[8])
            deck.nulls = int(data[9])
            deck.losses = int(data[10])
            deck.coef = int(data[11])
            deck.update_coef()
            return deck
        except:
            return None
    return None
