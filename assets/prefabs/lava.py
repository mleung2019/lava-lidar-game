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
        # Set rectangle dimensions and color
        warning_rect = pygame.Surface((self.width, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
        warning_rect.fill((255, 0, 0, self.opacity))

        # Draw rectangle
        game.base_surface.blit(warning_rect, (self.pos_x, 0))

        # Draw indicator 
        # Counter
        icon_pos_x = ((self.pos_x * 2) + self.width)/2 - 24
        icon_pos_y = settings.SCREEN_HEIGHT/2 - 54
        if self.loops > 0:
            counter = game.big_font.render(f"{self.loops}", True, settings.TEXT_COLOR)
            game.base_surface.blit(counter, (icon_pos_x, icon_pos_y))
        # Caution
        else:
            # Blend caution for correct opacity
            temp_caution = pygame.Surface(self.caution.get_size(), pygame.SRCALPHA)
            temp_caution.fill((255, 255, 255, min(self.opacity * 2, 255)))
            temp_caution.blit(self.caution, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

            game.base_surface.blit(temp_caution, (icon_pos_x - 75, icon_pos_y - 50))

        # Update opacity
        self.opacity -= self.speed * game.dt * 300
        
        # Blinking effect
        if self.opacity < 0:
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