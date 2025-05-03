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
        self.dt = 0
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
        self.medium_font = pygame.font.SysFont("bitstreamverasans", 90)


    def run(self):
        while self.running:
            self.dt = self.clock.tick(settings.FPS) / 1000
            self.handle_events()

            # Draw game frame
            self.base_surface.fill((0, 0, 0))  # Clear with black
            self.current_state.execute(self)

            # Draw debug
            self.debug()

            # Resize frame output to window
            win_width, win_height = self.screen.get_size()
            scaled_surface = pygame.transform.scale(self.base_surface, (win_width, win_height))
            self.screen.blit(scaled_surface, (0, 0))

            pygame.display.flip()

            # Update frame_counter variable
            self.frame_counter += 1

        pygame.quit()


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # Resize window if needed
            elif event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            # Handle events from other states
            else:
                self.current_state.handle_events(self, event)


    
    def debug(self):
        fps = self.clock.get_fps()
        fps_text = self.medium_font.render(f"FPS: {fps:.1f}", True, settings.TEXT_COLOR)
        self.base_surface.blit(fps_text, (10, 10))