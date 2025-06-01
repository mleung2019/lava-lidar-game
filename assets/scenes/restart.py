import pygame
import settings
import cv2
from assets.scenes.scene import Scene

class Restart(Scene):
    def __init__(self):
        super().__init__()
        pygame.mouse.set_visible(True)
        
        # Instance variables
        self.opacity = 0
        self.anim_finished = False


    def handle_events(self, game, event):
        # Left click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            game.change_states("gameplay")
        # Right click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            game.change_states("calibration")
    

    def execute(self, game):
        self.draw_last_frame(game)
        self.draw_fade_anim(game)
  
        if self.anim_finished:
            self.draw_info_text(game)
        

    def draw_last_frame(self, game):
        game.base_surface.blit(game.last_frame, (0, 0))

    
    def draw_fade_anim(self, game):
        # Set rectangle dimensions and color
        warning_rect = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
        warning_rect.fill((0, 0, 0, self.opacity))

        # Draw rectangle
        game.base_surface.blit(warning_rect, (0, 0))

        # Update opacity
        self.opacity += game.dt * 300
        
        # Rectangle fade in effect
        if self.opacity >= 127:
            self.opacity = 127
            self.anim_finished = True


    def draw_info_text(self, game):
        texts = [f"Survival time: {game.time:.2f}", f"Best time: {game.best_time:.2f}", "Click anywhere to restart", "(right click to recalibrate)"]

        for i, text in enumerate(texts):
            info_text = game.small_font.render(text, True, settings.TEXT_COLOR)
            info_rect = info_text.get_rect(center=(settings.SCREEN_WIDTH // 2, (settings.SCREEN_HEIGHT // 2) + (i * 75) - 150))
            game.base_surface.blit(info_text, info_rect)