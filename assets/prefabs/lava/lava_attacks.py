import settings
from assets.prefabs.lava.lava_manager import LavaManager
from assets.prefabs.lava.lava import Lava

class LeftandRight(LavaManager):
    def __init__(self, speed):
        super().__init__()

        left = Lava(0, settings.GRID_SIZE // 2, speed, 0)
        right = Lava(settings.GRID_SIZE // 2, settings.GRID_SIZE // 2, speed, 1)

        self.obstacles = [left, right]

class InBetweens(LavaManager):
    def __init__(self, speed):
        super().__init__()

        for i in range(settings.GRID_SIZE):
            lava = None
    
            if i % 2 == 0:
                lava = Lava(i, 1, speed, 0)
            else:
                lava = Lava(i, 1, speed, 1)
    
            self.obstacles.append(lava)