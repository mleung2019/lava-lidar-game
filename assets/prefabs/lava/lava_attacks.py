import settings
import random
from assets.prefabs.lava.lava_manager import LavaManager
from assets.prefabs.lava.lava import Lava

class LeftandRight(LavaManager):
    def __init__(self, speed):
        speed *= 1.2

        super().__init__(speed)

        offset = int(settings.GRID_SIZE * 0.8)

        left = Lava(0, offset, speed)
        right = Lava(settings.GRID_SIZE - offset, offset, speed)

        self.obstacles = [left, 1, right]


class InBetweens(LavaManager):
    def __init__(self, speed):
        super().__init__(speed)

        pos = [i for i in range(settings.GRID_SIZE) if i % 3 == 0]
        first_lava = [Lava(i, 3, speed) for idx, i in enumerate(pos) if idx % 2 == 0]
        second_lava = [Lava(i, 3, speed) for idx, i in enumerate(pos) if idx % 2 == 1]

        self.obstacles = first_lava + [0.75] + second_lava


class ThreeRotate(LavaManager):
    def __init__(self, speed):
        super().__init__(speed)

        first_lava = [Lava(i, 1, speed) for i in range(settings.GRID_SIZE) if i % 3 == 0]
        second_lava = [Lava(i, 1, speed) for i in range(settings.GRID_SIZE) if i % 3 == 1]
        third_lava = [Lava(i, 1, speed) for i in range(settings.GRID_SIZE) if i % 3 == 2]

        self.obstacles = first_lava + [0.5] + second_lava + [0.5] + third_lava


class Drizzle(LavaManager):
    def __init__(self, speed):
        super().__init__(speed)

        random_pos = list(range(settings.GRID_SIZE))
        random.shuffle(random_pos)
        random_pos = random_pos[:len(random_pos) // 2]

        for i in random_pos:
            self.obstacles += [Lava(i, 1, speed), 0.1]