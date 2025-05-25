import settings
import random
from assets.prefabs.lava.lava_manager import LavaManager
from assets.prefabs.lava.lava import Lava

class Wait(LavaManager):
    def __init__(self, speed):
        super().__init__(speed)

        self.obstacles = [0.75]


class LeftandRight(LavaManager):
    def __init__(self, speed):
        speed *= 0.8

        super().__init__(speed)

        offset = int(settings.GRID_SIZE * 0.8)
        left = Lava(0, offset, speed)
        right = Lava(settings.GRID_SIZE - offset, offset, speed)

        self.obstacles = [left, 1, right]


class FullLeft(LavaManager):
    def __init__(self, speed):
        speed *= 0.7

        super().__init__(speed)

        offset = int(settings.GRID_SIZE * 0.9)
        left = Lava(0, offset, speed)

        self.obstacles = [left]


class FullRight(LavaManager):
    def __init__(self, speed):
        speed *= 0.7

        super().__init__(speed)

        offset = int(settings.GRID_SIZE * 0.9)
        right = Lava(settings.GRID_SIZE - offset, offset, speed)

        self.obstacles = [right]


class CenterOut(LavaManager):
    def __init__(self, speed):
        speed *= 0.9
        
        super().__init__(speed)

        center_width = int(settings.GRID_SIZE * 0.67)
        offset = int(settings.GRID_SIZE * 0.17)

        middle = Lava(offset, center_width, speed)
        outer_left = Lava(0, offset * 2, speed)
        outer_right = Lava(settings.GRID_SIZE - (offset * 2), offset * 2, speed)

        self.obstacles = [middle] + [0.9] + [outer_left] + [outer_right]


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
        random_pos = random_pos[:int(len(random_pos) * 0.8)]

        for i in random_pos:
            self.obstacles.append(Lava(i, 1, speed))
            self.obstacles.append(0.1)


class MouseHole(LavaManager):
    def __init__(self, speed):
        speed *= 0.7

        super().__init__(speed)

        random_pos = list(range(settings.GRID_SIZE - 1))

        hole_1 = random.choice(random_pos)
        hole_2 = hole_1 + 1

        continuous = 0
        for i in range(settings.GRID_SIZE):
            if i != hole_1:
                continuous += 1
            else:
                if continuous != 0:
                    self.obstacles.append(Lava(0, continuous, speed))

                if continuous == 0 or hole_2 != settings.GRID_SIZE - 1:
                    self.obstacles.append(Lava(hole_2+1, settings.GRID_SIZE, speed))


class Homing(LavaManager):
    def __init__(self, speed):
        super().__init__(speed)

        width = int(settings.GRID_SIZE * 0.34)

        first_lava = [Lava(-1, width, speed)]
        second_lava = [Lava(-1, width, speed)]
        third_lava = [Lava(-1, width, speed)]

        self.obstacles = first_lava + [0.5] + second_lava + [0.5] + third_lava