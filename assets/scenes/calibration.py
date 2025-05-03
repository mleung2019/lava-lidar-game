import pygame
import settings
import cv2
from assets.scenes.scene import Scene

class Calibration(Scene):
    def __init__(self):
        super().__init__()


    def handle_events(self, game, event):
        # Left click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            game.change_states("gameplay")
                

    def execute(self, game):
        self.draw_webcam(game)