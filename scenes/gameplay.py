import pygame
import settings
import cv2
import random
from assets.prefabs.lava import Lava

class Gameplay:
    def __init__(self):
        # Webcam capture feed
        self.capture = cv2.VideoCapture(0)
        # NOTE: We assume that the webcam runs at 30FPS. Our game runs at 60FPS,
        # meaning that we reuse every webcam frame once
        self.last_capture = None

        # Arrow indicator
        self.arrow = pygame.image.load("./assets/images/arrow.png").convert_alpha()
        self.arrow = pygame.transform.scale(self.arrow, (100, 100))

        # Other instance variables
        self.arrow_x = 0 # The position of the arrow
        self.obstacles = [] # An array of all current obstacles


    def handle_events(self, game, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            lava = Lava(random.randint(0, 9), random.randint(1, 4), 1)
            self.obstacles.append(lava)
                


    def execute(self, game):
        self.draw_webcam(game)
        self.draw_obstacles(game)
        self.draw_indicator(game)

        self.arrow_x = (self.arrow_x + 10) % settings.SCREEN_WIDTH

    
    def draw_webcam(self, game):
        # Grab webcam frame every 2 frames
        if game.frame_counter % 2 == 0:
            ret, frame = self.capture.read()
            if not ret:
                print("Failed to grab frame")

            # Process webcam frame
            frame = cv2.flip(frame, 1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            self.last_capture = frame_surface

        # Draw everything to base surface
        if self.last_capture:
            game.base_surface.blit(self.last_capture, (0, 0))


    def draw_indicator(self, game):
        game.base_surface.blit(self.arrow, (self.arrow_x, 180))

    
    def draw_obstacles(self, game):
        for obstacle in self.obstacles:
            obstacle.execute(game)

        # Filter out obstacles that need to be despawned
        self.obstacles = [obstacle for obstacle in self.obstacles if not obstacle.finished]