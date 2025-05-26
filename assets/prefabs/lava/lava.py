import pygame
import settings

class Lava:
    def __init__(self, pos, width, speed, movement=0):
        ratio = settings.SCREEN_WIDTH / settings.GRID_SIZE
        self.loops = 3
        self.finished = False
        self.opacity = 127

        # For non-homing lava
        if pos != -1:
            self.pos_x = pos * ratio
        # For homing lava
        else:
            self.pos_x = -1

        self.width = width * ratio
        self.speed = speed
        self.movement = movement

        # Caution indicator
        self.caution = pygame.image.load("./assets/images/caution.png").convert_alpha()
        self.caution = pygame.transform.scale(self.caution, (170, 170))
    

    def execute(self, game):
        # For homing lava
        if self.pos_x == -1:
            self.pos_x = game.lidar_parse() - (self.width / 2)

        self.draw_lava_anim(game)
        
        
    def draw_lava_anim(self, game):
        self.prune_lava()

        # Set rectangle dimensions and color
        warning_rect = pygame.Surface((self.width, settings.SCREEN_HEIGHT), pygame.SRCALPHA)
        warning_rect.fill((255, 0, 0, self.opacity))

        # Draw rectangle
        game.base_surface.blit(warning_rect, (self.pos_x, 0))

        # Draw indicator 
        icon_pos_x = ((self.pos_x * 2) + self.width) / 2
        icon_pos_y = settings.SCREEN_HEIGHT / 2
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
        
        # Movement frames
        if self.loops > 0:
            if self.movement:
                self.pos_x += self.speed * game.dt * self.movement * 600

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
                self.speed = max(2, self.speed * 2)
            # Despawn
            else:
                self.finished = True
    

    def detect_collision(self, game):
        bound_left = self.pos_x 
        bound_right = self.pos_x + self.width

        player_pos = game.lidar_parse()

        if (player_pos >= bound_left and player_pos <= bound_right):
            game.change_states("restart")


    def prune_lava(self):
        # Only prune lava if it's static
        if not self.movement:
            # Prune the lava on the left side of the screen
            if self.pos_x < 0:
                self.width += self.pos_x
                self.pos_x = 0
            
            # Prune the lava on the right side of the screen
            if self.pos_x + self.width > settings.SCREEN_WIDTH:
                self.width -= self.pos_x + self.width - settings.SCREEN_WIDTH
        else:
            # Wraparound
            if self.movement > 0:
                if self.pos_x > settings.SCREEN_WIDTH:
                    self.pos_x = 0
            else:
                if self.pos_x + self.width < 0:
                    self.pos_x = settings.SCREEN_WIDTH