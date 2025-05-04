import pygame
import settings
from assets.scenes.scene import Scene

class Calibration(Scene):
    def __init__(self):
        super().__init__()

        # Instance variables 
        self.cali_states = 0


    def handle_events(self, game, event):
        # Left click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # TODO: Use LIDAR output to finish calibration
            if self.cali_states == 0:
                # Left
                game.calibration[0] = None
            elif self.cali_states == 1:
                # Right
                game.calibration[1] = None
            else:
                game.change_states("gameplay")
            self.cali_states += 1
                

    def execute(self, game):
        self.draw_webcam(game)
        self.draw_rect(game)
        self.draw_help_text(game)


    def draw_rect(self, game):
        # Set rectangle dimensions and color
        warning_rect = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
        warning_rect.fill((0, 0, 0, 127))

        # Draw rectangle
        game.base_surface.blit(warning_rect, (0, 0))


    def draw_help_text(self, game):
        help_text = game.small_font.render("Click anywhere to start game", True, settings.TEXT_COLOR)
        if self.cali_states == 0:
            help_text = game.small_font.render("Move to the left side of the screen and click anywhere", True, settings.TEXT_COLOR)
        if self.cali_states == 1:
            help_text = game.small_font.render("Move to the right side of the screen and click anywhere", True, settings.TEXT_COLOR)

        text_rect = help_text.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2))
        game.base_surface.blit(help_text, text_rect)