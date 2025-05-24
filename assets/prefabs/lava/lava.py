import pygame
import settings

class Lava:
    def __init__(self, pos, width, speed, sequence):
        ratio = settings.SCREEN_WIDTH / settings.GRID_SIZE
        self.loops = 3
        self.finished = False
        self.opacity = 127
        self.pos_x = pos * ratio
        self.width = width * ratio
        self.speed = speed
        self.sequence = sequence

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
        
        # Detection frames
        if self.loops == 0:
            if self.opacity > 200 and self.opacity < 255:
                self.detect_collision(game)

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
                self.finished = True
                self.sequence += 1
    

    def detect_collision(self, game):
        bound_left = self.pos_x 
        bound_right = self.pos_x + self.width

        player_pos = game.lidar_parse()

        if (player_pos >= bound_left and player_pos <= bound_right):
            game.change_states("restart")