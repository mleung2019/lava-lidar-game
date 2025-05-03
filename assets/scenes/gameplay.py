import pygame
import settings
import random
from assets.scenes.scene import Scene
from assets.prefabs.lava import Lava

class Gameplay(Scene):
    def __init__(self):
        super().__init__()

        # Other instance variables
        self.time = 0 # Survival time
        self.obstacles = [] # An array of all current obstacles
        self.arrow_x = 0 # The position of the arrow

        # Arrow indicator
        self.arrow = pygame.image.load("./assets/images/arrow.png").convert_alpha()
        self.arrow = pygame.transform.scale(self.arrow, (75, 100))


    def handle_events(self, game, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            lava = Lava(random.randint(0, 9), random.randint(1, 4), 1)
            self.obstacles.append(lava)
        # Left click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            game.change_states("calibration")
                

    def execute(self, game):
        self.draw_webcam(game)
        self.draw_obstacles(game)
        self.draw_indicator(game)
        self.draw_time(game)

        self.arrow_x = (self.arrow_x + 10) % settings.SCREEN_WIDTH
        self.time += game.dt


    def draw_indicator(self, game):
        game.base_surface.blit(self.arrow, (self.arrow_x, 180))

    
    def draw_obstacles(self, game):
        for obstacle in self.obstacles:
            obstacle.execute(game)

        # Filter out obstacles that need to be despawned
        self.obstacles = [obstacle for obstacle in self.obstacles if not obstacle.finished]


    def draw_time(self, game):
        time_text = game.medium_font.render(f"Time: {self.time:.2f}", True, settings.TEXT_COLOR)
        game.base_surface.blit(time_text, (10, 10))