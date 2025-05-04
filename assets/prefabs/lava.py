import pygame
import settings

class Lava:
    def __init__(self, pos, width, speed):
        ratio = settings.SCREEN_WIDTH / settings.GRID_SIZE
        self.loops = 3
        self.finished = 0
        self.opacity = 127
        self.pos_x = pos * ratio
        self.width = width * ratio
        self.speed = speed

        # Caution indicator
        self.caution = pygame.image.load("./assets/images/caution.png").convert_alpha()
        self.caution = pygame.transform.scale(self.caution, (200, 200))
    

    def execute(self, game):
        self.draw_lava_anim(game)
        
        
    def draw_lava_anim(self, game):
        # Set rectangle dimensions and color
        warning_rect = pygame.Surface((self.width, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
        warning_rect.fill((255, 0, 0, self.opacity))

        # Draw rectangle
        game.base_surface.blit(warning_rect, (self.pos_x, 0))

        # Draw indicator 
        icon_pos_x = ((self.pos_x * 2) + self.width) // 2
        icon_pos_y = settings.SCREEN_HEIGHT // 2
        indicator = self.caution

        # Counter
        if self.loops > 0:
            indicator = game.big_font.render(f"{self.loops}", True, settings.TEXT_COLOR)
        # Caution
        else:
            # Blend caution for correct opacity
            self.caution.set_alpha(min(self.opacity * 2, 255))
        
        indicator_rect = indicator.get_rect(center=(icon_pos_x, icon_pos_y))
        game.base_surface.blit(indicator, indicator_rect)

        # Update opacity
        self.opacity -= self.speed * game.dt * 300
        
        # Blinking effect
        if self.opacity <= 0:
            self.loops -= 1
            # Reset blinking effect
            if self.loops > 0:
                self.opacity = 127
            elif self.loops == 0:
                self.opacity = 255
                self.speed *= 2
            # Despawn
            else:
                self.finished = 1