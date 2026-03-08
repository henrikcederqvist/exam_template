
class Item:
    """
    Representerar ett föremål som spelaren kan plocka upp.
    Varje föremål har ett namn, ett poängvärde och en symbol som visas på kartan.
    """
    def __init__(self, name, value=20, symbol="?"):
        self.name = name
        self.value = value
        self.symbol = symbol

    def __str__(self):
        return self.symbol


# Lista över alla möjliga föremål som kan slumpas ut på kartan
pickups = [
    Item("carrot"),
    Item("apple"),
    Item("strawberry"),
    Item("cherry"),
    Item("watermelon"),
    Item("radish"),
    Item("cucumber"),
    Item("orange")
]

def randomize(grid):
    """
    Placerar ut alla föremål i listan 'pickups' på slumpmässiga tomma rutor.
    Varje föremål placeras exakt en gång.
    """
    for item in pickups:
        while True:
            # slumpa en position tills vi hittar en som är ledig
            x = grid.get_random_x()
            y = grid.get_random_y()
            if grid.is_empty(x, y):
                grid.set(x, y, item)
                break  # avbryt while-loopen, fortsätt med nästa varv i for-loopen

import random

def random_item():
    """Returnerar ett slumpmässigt föremål från listan 'pickups'."""
    return random.choice(pickups)

class Exit(Item):
    """
    Representerar utgången. Den är inaktiv tills spelaren har samlat alla föremål.
    """
    def __init__(self):
        super().__init__("Exit", value=0, symbol="E")

class Trap:
    """
    En fälla som skadar spelaren när den kliver på den.
    """
    symbol = "T"
    name = "Trap"
    value = -10

class Bomb:
    """
    En bomb som spelaren kan placera med B. Den exploderar efter några turer.
    """
    symbol = "B"
    name = "Bomb"