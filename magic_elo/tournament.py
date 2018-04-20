import random
from typing import List, Union

from magic_elo.deck import Deck


class Match:
    def __init__(self, parent1=None, parent2=None):
        self.deck1 = None
        self.deck2 = None
        self.result = '?'
        self.parent1 = parent1
        self.parent2 = parent2

    def update(self):
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


class MatchSingle(Match):
    def __init__(self, parent=None):
        Match.__init__(self, parent)
        self.result = 'W'

    @property
    def title(self):
        if self.deck1 is None:
            d1 = '?'.rjust(47)
            return f'{d1} ???'
        else:
            return f'{self.deck1.title} <-'


class Tournament:
    def __init__(self, decks):
        decks = sorted(decks, key=lambda x: random.random())

        self.rounds = []
        _round = self.new_round(decks)
        while _round:
            self.rounds.append(_round)
            _round = self.new_round(_round, len(self.rounds) % 2 == 1)

    def new_round(self, previous: Union[List[Match], List[Deck]], rev=False):
        if len(previous) < 2:
            return []
        nb_matches = round(len(previous) / 2 - 0.1)
        if rev:
            previous = list(reversed(previous))
        _round = [Match(previous[i * 2], previous[i * 2 + 1]) for i in range(nb_matches)]
        if len(previous) > nb_matches * 2:
            _round.append(MatchSingle(previous[-1]))
        if rev:
            return list(reversed(_round))
        else:
            return _round

    def do_match(self, deck1: Deck, deck2: Deck, result: str):
        for _round in self.rounds:
            for match in _round:
                if isinstance(match, Match):
                    if match.deck1 == deck1 and match.deck2 == deck2 and match.result == '?':
                        match.result = result.upper()
                    match.update()

    def update(self):
        for _round in self.rounds:
            for match in _round:
                if isinstance(match, Match):
                    match.update()

    def print(self, all=True):
        for i in range(len(self.rounds)):
            print(f'== ROUND {i + 1} ==')
            for m in self.rounds[i]:
                if all or isinstance(m, Deck) or m.deck1 is not None or m.deck2 is not None:
                    print(m.title)
