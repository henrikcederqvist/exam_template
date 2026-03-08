class Player:
    """
    Representerar spelaren på rutnätet.
    Håller reda på spelarens position och hanterar förflyttning.
    """
    marker = "@"

    def __init__(self, x, y):
        self.pos_x = x
        self.pos_y = y

    # Flyttar spelaren. "dx" och "dy" är skillnaden
    def move(self, dx, dy):
        """Flyttar spelaren.\n
        dx = horisontell förflyttning, från vänster till höger\n
        dy = vertikal förflyttning, uppifrån och ned"""
        self.pos_x += dx
        self.pos_y += dy

    def can_move(self, dx, dy, grid):
        """
        Kontrollerar om spelaren kan gå till rutan i riktningen (dx, dy).
        Returnerar False om rutan är en vägg.
        """
        new_x = self.pos_x + dx
        new_y = self.pos_y + dy

        tile = grid.get(new_x, new_y)

        # Om rutan är en vägg → kan inte gå dit
        if tile == grid.wall:
            return False

        return True

