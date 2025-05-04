import pygame
import settings
import random
from assets.scenes.scene import Scene
from assets.prefabs.lava import Lava

class Gameplay(Scene):
    def __init__(self):
        super().__init__()

        # Instance variables
        self.obstacles = [] # An array of all current obstacles
        self.arrow_x = 0 # The position of the arrow

        # Arrow indicator
        self.arrow = pygame.image.load("./assets/images/arrow.png").convert_alpha()
        self.arrow = pygame.transform.scale(self.arrow, (75, 100))


    def handle_events(self, game, event):
        if event.type == pygame.KEYDOWN: 
            # TODO: Lava debug
            if event.key == pygame.K_SPACE:
                lava = Lava(random.randint(0, 9), random.randint(1, 3), 1)
                self.obstacles.append(lava)
            # TODO: Calibration debug
            if event.key == pygame.K_c:
                game.change_states("calibration")
            # TODO: Restart debug
            if event.key == pygame.K_r:
                game.change_states("restart")
                

    def execute(self, game):
        self.draw_webcam(game)
        self.draw_obstacles(game)
        self.draw_indicator(game)

        game.last_frame = game.base_surface.copy()
        
        self.draw_time(game)


    def draw_indicator(self, game):
        game.base_surface.blit(self.arrow, (self.arrow_x, 180))
        self.arrow_x = (self.arrow_x + 10) % settings.SCREEN_WIDTH

    
    def draw_obstacles(self, game):
        for obstacle in self.obstacles:
            obstacle.execute(game)

        # Filter out obstacles that need to be despawned
        self.obstacles = [obstacle for obstacle in self.obstacles if not obstacle.finished]


    def draw_time(self, game):
        game.time += game.dt
        time_text = game.medium_font.render(f"Time: {game.time:.2f}", True, settings.TEXT_COLOR)
        game.base_surface.blit(time_text, (10, 10))