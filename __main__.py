from magic_elo.deck import Deck
from magic_elo.group import Group

group = Group()

group.add_deck(Deck('Boros', w=1, r=1))
group.add_deck(Deck('Orzhov', w=1, b=1))

while True:
    group.do()
