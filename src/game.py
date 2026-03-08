"""
Ett rutnätsbaserat spel där spelaren samlar föremål markerade med (?).
Föremålen ger poäng och sparas i en lista som spelaren kan visa.
Spelaren måste undvika fällor, kan placera bomber och måste samla alla föremål
för att aktivera utgången och vinna spelet.
"""

from .status import print_status
from .grid import Grid
from .player import Player
from . import pickups

# Räknar hur många items som finns på kartan (ej exit)
def count_items_on_grid(grid):
    count = 0
    for y in range(grid.height):
        for x in range(grid.width):
            tile = grid.get(x, y)
            if isinstance(tile, pickups.Item) and not isinstance(tile, pickups.Exit):
                count += 1
    return count

# Globala spelvariabler
picked_items = 0
active_bomb = None   # (x, y)
bomb_timer = 0
player = Player(18, 6)
score = 0
inventory = []

# Skapa spelvärlden
g = Grid()
g.set_player(player)
g.make_walls()
g.make_inner_walls()
pickups.randomize(g)

total_items = count_items_on_grid(g)
#print("DEBUG: total_items =", total_items)

def place_traps(n=3):
    import random
    for _ in range(n):
        while True:
            x = g.get_random_x()
            y = g.get_random_y()
            if g.is_empty(x, y):
                g.set(x, y, pickups.Trap())
                break

# Slumpa ut tre fällor på tomma rutor
place_traps(3)

# Slumpar ut en exit på en tom ruta
def place_exit():
    import random
    while True:
        x = g.get_random_x()
        y = g.get_random_y()
        if g.is_empty(x, y):
            g.set(x, y, pickups.Exit())
            break

place_exit()

# Grace period: spelaren tar ingen skada i X steg
grace_steps = 0
turn_counter = 0

import random

def spawn_new_pickup():
    empty_tiles = []

    for y in range(g.height):
        for x in range(g.width):
            tile = g.get(x, y)

            # Do NOT overwrite the Exit tile
            if getattr(tile, "symbol", None) == "E":
                continue

            if g.is_empty(x, y):
                empty_tiles.append((x, y))

    if not empty_tiles:
        return

    x, y = random.choice(empty_tiles)
    new_item = pickups.random_item()
    g.set(x, y, new_item)

    global total_items
    total_items += 1
    #print("DEBUG: total_items increased to", total_items)

    print("A new plant has grown somewhere on the map!")

# Lägger ut en bomb på spelarens position om ingen redan finns
def place_bomb():
    global active_bomb, bomb_timer

    if active_bomb is not None:
        print("You already placed a bomb!")
        return

    x = player.pos_x
    y = player.pos_y

    g.set(x, y, pickups.Bomb())
    active_bomb = (x, y)
    bomb_timer = 3

    print("Bomb placed! It will explode in 3 turns.")

# Bomben exploderar i ett 3x3 område runt spelaren och kan skada spelaren.
def explode_bomb():
    global active_bomb, bomb_timer, score

    if active_bomb is None:
        return

    bx, by = active_bomb
    print("BOOM! The bomb explodes!")

    for dy in [-1, 0, 1]:
        for dx in [-1, 0, 1]:
            x = bx + dx
            y = by + dy

            if 0 <= x < g.width and 0 <= y < g.height:

                # Spräng inte bort utgången
                tile = g.get(x, y)
                if isinstance(tile, pickups.Exit):
                    continue

                if x == player.pos_x and y == player.pos_y:
                    score -= 20
                    print("You were caught in the explosion! -20 points.")

                g.set(x, y, g.empty)

    active_bomb = None
    bomb_timer = 0

# Flyttar spelaren och hanterar allt som kan hända under ett steg
def move_player(dx, dy):
    global score, grace_steps, turn_counter, picked_items

    if player.can_move(dx, dy, g):
        target_x = player.pos_x + dx
        target_y = player.pos_y + dy

        maybe_item = g.get(target_x, target_y)
        #print("DEBUG: Stepped on:", maybe_item, type(maybe_item))
        player.move(dx, dy)

        # Exit placeras slumpmässigt men är inaktiv tills alla items är plockade
        if getattr(maybe_item, "symbol", None) == "E":
            if picked_items == total_items:
                print("You reached the exit and won the game!")
                exit()
            else:
                print("The exit is inactive. Collect all items first.")
                return

        turn_counter += 1

        global bomb_timer
        if bomb_timer > 0:
            bomb_timer -= 1
            if bomb_timer == 0:
                explode_bomb()

        # Var 25:e turn växer en ny planta
        if turn_counter % 25 == 0:
            spawn_new_pickup()

        if grace_steps > 0:
            grace_steps -= 1
            print(f"Grace period active: {grace_steps} steps left.")
        else:
            score -= 1

        if isinstance(maybe_item, pickups.Trap):
            score -= 10
            print("You stepped on a trap! -10 points.")
            return

        if isinstance(maybe_item, pickups.Item) and getattr(maybe_item, "symbol", None) != "E":
            score += maybe_item.value
            print(f"You found a {maybe_item.name}, +{maybe_item.value} points.")
            inventory.append(maybe_item)
            g.clear(player.pos_x, player.pos_y)

            picked_items += 1
            print("DEBUG: picked_items =", picked_items)

            grace_steps = 5
            print("Grace period started: 5 free steps!")


moves = {
    "w": (0, -1), # upp
    "s": (0, 1),  # ner
    "a": (-1, 0), # vänster
    "d": (1, 0),  # höger
}

command = "a"

# Visar en lista över alla insamlade växter/frukter
def print_inventory():
    print("Inventory:")
    if len(inventory) == 0:
        print("  (empty)")
    else:
        for item in inventory:
            print(" -", item.name)


# Huvudloop: kör spelet tills spelaren trycker Q eller X
while not command.casefold() in ["q", "x"]:
    print_status(g, score, grace_steps)

    command = input("Use WASD to move, I for inventory, B to place bomb, Q/X to quit: ")
    command = command.casefold()[:1]

    if command in moves:
        dx, dy = moves[command]
        move_player(dx, dy)

    elif command == "i":
        print_inventory()

    elif command == "b":
        place_bomb()

# Hit kommer vi när while-loopen slutar
print("Thank you for playing!")
