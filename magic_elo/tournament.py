import random
from typing import List, Union

from magic_elo.deck import Deck, MatchInterface


class Match(MatchInterface):
    def __init__(self, parent1=None, parent2=None):
        self.deck1 = None
        self.deck2 = None
        self.result = '?'
        self.parent1 = parent1
        self.parent2 = parent2

    @property
    def ready(self):
        return self.deck1 is not None and self.deck2 is not None

    def update(self):
        ready = self.ready
        if self.parent1 is not None:
            if isinstance(self.parent1, Deck):
                self.deck1 = self.parent1
            elif self.parent1.result == 'W':
                self.deck1 = self.parent1.deck1
            elif self.parent1.result == 'L':
                self.deck1 = self.parent1.deck2
        if self.parent2 is not None:
            if isinstance(self.parent2, Deck):
                self.deck2 = self.parent2
            elif self.parent2.result == 'W':
                self.deck2 = self.parent2.deck1
            elif self.parent2.result == 'L':
                self.deck2 = self.parent2.deck2
        if not ready and self.ready:
            print(f'New match ready: {self.deck1.name} vs {self.deck2.name}')

    @property
    def title(self):
        d1 = '?'.rjust(47) if self.deck1 is None else self.deck1.title
        d2 = '?'.ljust(47) if self.deck2 is None else self.deck2.title
        res = '???'
        if self.result == 'W':
            res = '<- '
        if self.result == 'L':
            res = ' ->'
        return f'{d1} {res} {d2}'

    @property
    def winner(self):
        if self.result == 'W':
            return self.deck1
        if self.result == 'L':
            return self.deck2
        return None


def new_round(previous: List[Union[MatchInterface]]) -> List[Union[MatchInterface]]:
    if len(previous) < 2:
            return []
    pows: List[int] = [pow(2, i) for i in range(10)]
    if len(previous) in pows:
        return [Match(previous[i * 2], previous[i * 2 + 1]) for i in range(len(previous) // 2)]

    remove = len(previous) - [i for i in pows if i < len(previous)][-1]
    _round: List[Union[MatchInterface]] = [Match(previous[i * 2], previous[i * 2 + 1]) for i in range(remove)]
    _round.extend(previous[remove * 2:])
    return _round


class Tournament:
    def __init__(self, decks, random_order):
        if random_order:
            decks = sorted(decks, key=lambda x: random.random())
        else:
            decks = sorted(decks, key=lambda x: x.elo)

        self.rounds = []
        _round = new_round(decks)
        while _round:
            self.rounds.append(_round)
            _round = new_round(_round)
        self.done = False

    def do_match(self, deck1: Deck, deck2: Deck, result: str):
        for _round in self.rounds:
            for match in [m for m in _round if isinstance(m, Match)]:
                if match.deck1 == deck1 and match.deck2 == deck2 and match.result == '?':
                    match.result = result.upper()
                    print(f'Match done: {match.deck1.name} vs {match.deck2.name}')
                match.update()
        if not self.done and self.rounds[-1][0].winner:
            print(f'Tournament done: Winner is {self.rounds[-1][0].winner.name}')
            self.done = True

    def update(self):
        for _round in self.rounds:
            for match in _round:
                if isinstance(match, Match):
                    match.update()

    def print(self, print_all=True):
        for i in range(len(self.rounds)):
            round_titles = [m.title for m in self.rounds[i]
                            if print_all or (isinstance(m, Match) and (m.deck1 is not None or m.deck2 is not None))]
            if round_titles:
                print(f'== ROUND {i + 1} ==')
            for t in round_titles:
                print(t)

    def to_data(self) -> str:
        data = 'T'
        return data
