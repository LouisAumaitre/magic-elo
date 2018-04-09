import math


def proba(dif):
    return 1 / (1 + math.pow(10, -dif / 400))


class Deck:
    size = 60

    def __init__(self, name: str, w=0, u=0, b=0, r=0, g=0):
        self.name = name
        total = w + u + b + r + g
        self.w = w / total
        self.u = u / total
        self.b = b / total
        self.r = r / total
        self.g = g / total

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
        if self.w:
            c += 'W'
        if self.u:
            c += 'U'
        if self.b:
            c += 'B'
        if self.r:
            c += 'R'
        if self.g:
            c += 'G'
        return c

    @property
    def title(self):
        return f'{self.name} ({self.colors}) [ELO-{round(self.elo)}]'

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
