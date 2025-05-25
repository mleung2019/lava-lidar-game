from assets.prefabs.lava.lava import Lava

# When speed = 1, the lava animation from start to finish takes 1.74 seconds
LAVA_CONST = 1.74

class LavaManager:
    def __init__(self, speed):
        self.finished = False

        self.speed = speed

        self.obstacles = [] # An array of all obstacles
        self.curr_obstacles = [] # An array of all obstacles currently on screen
        self.timer = 0 # Timer for when the next wave of obstacles should arrive


    def execute(self, game):
        # Loading obstacles
        while self.timer <= 0 and len(self.obstacles) != 0:
            new_obstacle = self.obstacles.pop(0)
            
            # Add obstacle to the curr_obstacles array
            if type(new_obstacle) is Lava: 
                self.curr_obstacles.append(new_obstacle)

            # Read delay marker
            else:
                self.timer = (LAVA_CONST / self.speed) * new_obstacle

        # Drawing obstacles
        for obstacle in self.curr_obstacles:
            obstacle.execute(game)

        # Filter out obstacles that need to be despawned
        self.curr_obstacles = [obstacle for obstacle in self.curr_obstacles if not obstacle.finished]

        if len(self.obstacles) == 0 and len(self.curr_obstacles) == 0 and self.timer <= 0:
            self.finished = True

        self.timer -= game.dt