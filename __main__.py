from magic_elo.deck import Deck
from magic_elo.group import Group

group = Group()
group.load()

group.add_deck(Deck('Boros', w=1, r=1))
group.add_deck(Deck('Orzhov', w=1, b=1))
group.add_deck(Deck('Simic', u=1, g=1))
group.add_deck(Deck('Azorius', w=1, u=1))

group.run()
