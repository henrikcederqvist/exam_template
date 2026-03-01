from .grid import Grid
from .player import Player
from . import pickups

#test

player = Player(18, 6)
score = 0
inventory = []

g = Grid()
g.set_player(player)
g.make_walls()
pickups.randomize(g)


# TODO: flytta denna till en annan fil
def print_status(game_grid):
    """Visa spelvärlden och antal poäng."""
    print("--------------------------------------")
    print(f"You have {score} points.")
    print(game_grid)

def move_player(dx, dy):
    global score

    if player.can_move(dx, dy, g):
        target_x = player.pos_x + dx
        target_y = player.pos_y + dy

        maybe_item = g.get(target_x, target_y)
        player.move(dx, dy)

        if isinstance(maybe_item, pickups.Item):
            score += maybe_item.value
            print(f"You found a {maybe_item.name}, +{maybe_item.value} points.")
            g.clear(player.pos_x, player.pos_y)


moves = {
    "w": (0, -1), # upp
    "s": (0, 1),  # ner
    "a": (-1, 0), # vänster
    "d": (1, 0),  # höger
}

command = "a"

# Loopa tills användaren trycker Q eller X.
while not command.casefold() in ["q", "x"]:
    print_status(g)

    command = input("Use WASD to move, Q/X to quit. ")
    command = command.casefold()[:1]

    if command in moves:
        dx, dy = moves[command]
        move_player(dx, dy)


# Hit kommer vi när while-loopen slutar
print("Thank you for playing!")
