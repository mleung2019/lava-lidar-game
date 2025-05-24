class LavaManager:
    def __init__(self):
        self.finished = False

        self.obstacles = [] # An array of all current obstacles
        # Controls obstacle timing 
        self.sequence = 0

    def execute(self, game):
        for obstacle in self.obstacles:
            if self.sequence >= obstacle.sequence:
                obstacle.execute(game)
                self.sequence = obstacle.sequence

        # Filter out obstacles that need to be despawned
        self.obstacles = [obstacle for obstacle in self.obstacles if not obstacle.finished]

        if len(self.obstacles) == 0:
            self.finished = True