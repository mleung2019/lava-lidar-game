import pygame
import settings
import cv2

# Parent class for all the scenes
class Scene:
    def __init__(self):
        # Webcam capture feed
        self.capture = cv2.VideoCapture(0)
        # NOTE: We assume that the webcam runs at 30FPS. Our game runs at 60FPS,
        # meaning that we reuse every webcam frame once
        self.last_capture = None


    def draw_webcam(self, game):
        # Grab webcam frame every 2 frames
        if game.frame_counter % 2 == 0:
            ret, frame = self.capture.read()
            if not ret:
                print("Failed to grab frame")

            # Process webcam frame
            frame = cv2.flip(frame, 1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            self.last_capture = frame_surface

        # Draw everything to base surface
        if self.last_capture:
            game.base_surface.blit(self.last_capture, (0, 0))
