import pygame
import settings
from assets.scenes.scene import Scene

class Calibration(Scene):
    def __init__(self, cali_state=0):
        super().__init__()
        pygame.mouse.set_visible(True)

        # Instance variables 
        self.cali_state = cali_state


    def handle_events(self, game, event):
        # Left click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.cali_state == 0:
                # Left
                game.calibration[0] = game.lidar.measurement
            elif self.cali_state == 1:
                # Right
                if game.calibration[0] == game.lidar.measurement:
                    self.cali_state = -1
                game.calibration[1] = game.lidar.measurement
            else:
                game.change_states("gameplay")
            self.cali_state += 1
                

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
        if self.cali_state == 0:
            help_text = game.small_font.render("Move to the left side of the screen and click anywhere", True, settings.TEXT_COLOR)
        if self.cali_state == 1:
            help_text = game.small_font.render("Move to the right side of the screen and click anywhere", True, settings.TEXT_COLOR)

        text_rect = help_text.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2))
        game.base_surface.blit(help_text, text_rect)