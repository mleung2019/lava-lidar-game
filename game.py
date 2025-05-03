import pygame
import settings
from scenes.gameplay import Gameplay

class Game:
    def __init__(self):
        # Game management
        pygame.init()
        pygame.display.set_caption("Lava LIDAR Game")
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # Game states
        self.states = {
           "gameplay": Gameplay()   
        }
        self.current_state = self.states["gameplay"]

        # Game rendering
        self.base_surface = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

        # Global variables
        self.frame_counter = 0
        self.font = pygame.font.SysFont(None, 30)
        self.text_color = (255, 255, 255)


    def run(self):
        while self.running:
            self.clock.tick(settings.FPS)
            self.handle_events()

            # Draw game frame
            self.base_surface.fill((0, 0, 0))  # Clear with black
            self.current_state.draw(self)

            # Draw debug
            self.debug()

            # Resize frame output to window
            win_width, win_height = self.screen.get_size()
            scaled_surface = pygame.transform.scale(self.base_surface, (win_width, win_height))
            self.screen.blit(scaled_surface, (0, 0))

            pygame.display.flip()

            # Update frame_counter variable
            self.frame_counter = (self.frame_counter + 1) % 2

        pygame.quit()


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # Resize window if needed
            elif event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    
    def debug(self):
        fps = self.clock.get_fps()
        fps_text = self.font.render(f"FPS: {fps:.1f}", True, self.text_color)
        self.base_surface.blit(fps_text, (10, 10))