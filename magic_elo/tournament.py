import random
from enum import Enum
from typing import List, Union, Dict

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
        if not ready and self.ready and self.result == '?':
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

    first_round = len(previous) - [i for i in pows if i < len(previous)][-1]
    _round: List[Union[MatchInterface]] = [Match(previous[i * 2], previous[i * 2 + 1]) for i in range(first_round)]
    _round.extend(previous[first_round * 2:])
    return _round


class OrderMode(Enum):
    Same = 'same'
    Random = 'random'
    Elo = 'elo'


class Tournament:
    def __init__(self, decks, order: OrderMode=OrderMode.Same):
        if order == OrderMode.Random:
            self.decks = sorted(decks, key=lambda x: random.random())
        elif order == OrderMode.Elo:
            self.decks = sorted(decks, key=lambda x: x.elo)
        else:
            self.decks = decks

        self.rounds = []
        _round = new_round(self.decks)
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
        rounds_data = []
        for r in self.rounds:
            rounds_data.append(''.join([m.result for m in r]))
        decks_data = ';'.join([d.name.lower() for d in self.decks])
        data = ['T', '/'.join(rounds_data), decks_data]
        return ';;'.join(data)


def tournament_from_data(line: str, provided_decks: Dict[str, Deck]) -> Tournament:
    _, rounds_join, decks_join = line.split(';;')
    deck_names = decks_join.split(';')
    deck_list = [provided_decks[name.lower()] for name in deck_names]
    tournament = Tournament(deck_list, OrderMode.Same)
    rounds_data = rounds_join.split('/')
    for i in range(len(tournament.rounds)):
        t_round = tournament.rounds[i]
        for j in range(len(t_round)):
            result = rounds_data[i][j]
            if result != Deck.result:
                try:
                    t_round[j].result = result
                except AttributeError:
                    print(f'WARNING: cannot set result \'{result}\' to {t_round[i].title}')
    return tournament
