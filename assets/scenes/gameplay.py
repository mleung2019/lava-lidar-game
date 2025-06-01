import pygame
import settings
import random
from assets.scenes.scene import Scene
from assets.prefabs.lava.lava_attacks import *

class Gameplay(Scene):
    def __init__(self):
        super().__init__()
        pygame.mouse.set_visible(False)

        # Arrow indicator
        self.arrow = pygame.image.load("./assets/images/arrow.png").convert_alpha()
        self.arrow = pygame.transform.scale(self.arrow, (75, 100))
        
        # Current attack
        self.curr_attack = Wait(1)

        # All attacks
        self.attacks = [
            LeftAndRight,
            FullLeft,
            FullRight, 
            CenterOut, 
            ThreeRotate, 
            Drizzle, 
            MouseHole,
            Homing,
            MovingDrizzle,
        ]

        # Speed
        self.speed = 1
        self.speed_timer = 10



    def handle_events(self, game, event):
        if event.type == pygame.KEYDOWN: 
            # Calibration debug
            if event.key == pygame.K_c:
                game.change_states("calibration")
            # Restart debug
            if event.key == pygame.K_r:
                game.change_states("restart")
                

    def execute(self, game):
        self.generate_attacks(game)
        self.draw_webcam(game)
        self.draw_attacks(game)
        self.draw_indicator(game)

        game.last_frame = game.base_surface.copy()
        
        self.draw_time(game)


    def generate_attacks(self, game):
        if self.curr_attack.finished:
            rand_attack = random.choice(self.attacks)
            self.curr_attack = rand_attack(self.speed)

        if self.speed_timer <= 0:
            self.speed_timer = 10
            self.speed += 0.1

            print("Speed increased to " + str(self.speed))      

        self.speed_timer -= game.dt


    def draw_indicator(self, game):
        # Offset the arrow indicator by 38 pixels to center it
        game.base_surface.blit(self.arrow, (game.lidar_parse() - 38, 180))


    def draw_attacks(self, game):
        self.curr_attack.execute(game)


    def draw_time(self, game):
        game.time += game.dt
        game.best_time = max(game.time, game.best_time)

        time_text = game.medium_font.render(f"Time: {game.time:.2f}", True, settings.TEXT_COLOR)
        game.base_surface.blit(time_text, (10, 10))