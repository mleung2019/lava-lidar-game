import pygame
import settings
from assets.scenes.gameplay import Gameplay
from assets.scenes.calibration import Calibration
from assets.scenes.restart import Restart

class Game:
    def __init__(self):
        # Game management
        pygame.init()
        pygame.display.set_caption("Lava LIDAR Game")
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.running = True

        # Initial game state
        self.change_states("calibration")

        # Game rendering
        self.base_surface = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)).convert_alpha()
        self.last_frame = None

        # Global variables
        self.frame_counter = 0
        self.time = 0
        self.best_time = 0
        # First element is the LIDAR measurement on the left side, second element
        # is the LIDAR measurement on the right side
        self.calibration = [0, 0]
        # Font(s)
        self.small_font = pygame.font.SysFont("bitstreamverasans", 45)
        self.medium_font = pygame.font.SysFont("bitstreamverasans", 60)
        self.big_font = pygame.font.SysFont("bitstreamverasans", 90)


    def change_states(self, state):
        if state == "gameplay":
            self.time = 0
            self.current_state = Gameplay()
        elif state == "calibration":
            self.current_state = Calibration()
        elif state == "restart":
            self.best_time = max(self.time, self.best_time)
            self.current_state = Restart()


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


    def execute(self):
        while self.running:
            self.dt = self.clock.tick(settings.FPS) / 1000
            self.handle_events()

            # Draw game frame
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

    
    def debug(self):
        fps = self.clock.get_fps()
        fps_text = self.small_font.render(f"FPS: {fps:.1f}", True, settings.TEXT_COLOR)
        self.base_surface.blit(fps_text, (1065, 10))