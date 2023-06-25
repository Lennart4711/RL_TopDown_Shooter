class Bullet:
    def __init__(self, pos, players: list):
        self.pos = pos
        self.players = players

    def move(self, change):
        self.pos += change

        for player in self.players:
            if np.linalg.norm(self.pos - player.pos) < 10:
                player.hit()


class Bullet2:
    def __init__(self, pos):
        self.pos = pos

    def move(self, change, players):
        self.pos += change

        for player in players:
            if np.linalg.norm(self.pos - player.pos) < 10:
                player.hit()
