import random

class Grid:
    """
    Representerar spelplanen som ett rutnät.
    Hanterar väggar, tomma rutor, spelaren och placering av objekt.
    """
    width = 36
    height = 12
    empty = "."  # Tecken för en tom ruta
    wall = "■"   # Tecken för en ogenomtränglig vägg

    def __init__(self):
        """Skapar ett nytt rutnät fyllt med tomma rutor."""
        # Spelplanen lagras i en lista av listor. Vi använder "list comprehension" för att sätta tecknet för "empty" på varje plats på spelplanen.
        self.data = [[self.empty for y in range(self.width)] for z in range(
            self.height)]


    def get(self, x, y):
        """Returnerar innehållet på positionen (x, y)."""
        return self.data[y][x]

    def set(self, x, y, value):
        """Sätter innehållet på positionen (x, y) till value."""
        self.data[y][x] = value

    def set_player(self, player):
        """Registrerar spelaren så att den kan ritas ut på kartan."""
        self.player = player

    def clear(self, x, y):
        """Tar bort ett föremål från positionen (x, y)."""
        self.set(x, y, self.empty)

    def __str__(self):
        """Gör så att vi kan skriva ut spelplanen med print(grid)"""
        xs = ""
        for y in range(len(self.data)):
            row = self.data[y]
            for x in range(len(row)):
                if x == self.player.pos_x and y == self.player.pos_y:
                    xs += "@"
                else:
                    tile = row[x]

                    # ⭐ NY KOD: använd tile.symbol om det finns
                    if hasattr(tile, "symbol"):
                        xs += tile.symbol
                    else:
                        xs += str(tile)

            xs += "\n"
        return xs

    def make_walls(self):
        """Skapar väggar runt hela spelplanens ytterkanter."""
        for i in range(self.height):
            self.set(0, i, self.wall)
            self.set(self.width - 1, i, self.wall)

        for j in range(1, self.width - 1):
            self.set(j, 0, self.wall)
            self.set(j, self.height - 1, self.wall)

    def make_inner_walls(self):
        """Skapar några fördefinierade inre väggar."""

        for x in range(2, 11):
            self.set(x, 2, self.wall)

        for x in range(2, 11):
            if x != 6:  # öppning i mitten
                self.set(x, 6, self.wall)

        for y in range(2, 7):
            self.set(2, y, self.wall)

        for y in range(2, 7):
            self.set(10, y, self.wall)

    # Används i filen pickups.py
    def get_random_x(self):
        """Slumpa en x-position på spelplanen"""
        return random.randint(0, self.width-1)

    def get_random_y(self):
        """Slumpa en y-position på spelplanen"""
        return random.randint(0, self.height-1)


    def is_empty(self, x, y):
        """Returnerar True om det inte finns något på aktuell ruta"""
        return self.get(x, y) == self.empty

