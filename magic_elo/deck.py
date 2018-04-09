def proba(dif):
    return 1 / (1 + 10 ^ (-dif / 400))


class Deck:
    size = 60

    def __init__(self, name: str, w: float=0, u: float=0, b: float=0, r: float=0, g: float=0):
        self.name = name
        self.w = w
        self.u = u
        self.b = b
        self.r = r
        self.g = g

        total = w + u + b + r + g
        assert total == 1

        self.elo = 1000
        self.wins = 0
        self.null = 0
        self.defeat = 0

        self.coef = 40

    @property
    def games(self):
        return self.wins + self.null + self.defeat

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
        return f'{self.name} ({self.colors}) [ELO-{self.elo}]'

    def win(self, opponent_elo):
        self.elo = self.elo + self.coef * (1 - proba(self.elo - opponent_elo))
        self.update_coef()

    def null(self, opponent_elo):
        self.elo = self.elo + self.coef * (0.5 - proba(self.elo - opponent_elo))
        self.update_coef()

    def loss(self, opponent_elo):
        self.elo = self.elo + self.coef * (-proba(self.elo - opponent_elo))
        self.update_coef()

    def update_coef(self):
        if self.elo > 2400 or self.coef == 10:
            self.coef = 10
        elif self.games < 30:
            self.coef = 40
        else:
            self.coef = 20
