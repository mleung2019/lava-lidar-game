import cv2
import pygame
import sys

# Use first webcam
cap = cv2.VideoCapture(0)

# Start game
pygame.init()

# Dimensions
webcam_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
webcam_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

frame_width = 1280
frame_height = 720

screen = pygame.display.set_mode((frame_width, frame_height))
pygame.display.set_caption("Lava LIDAR Game")

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read frame from webcam
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Flip camera horizontally
    # Convert BGR (OpenCV) to RGB (Pygame)
    # Resize frame
    # Transpose to a surface
    frame = cv2.flip(frame, 1)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (frame_width, frame_height))
    frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1)) 

    # Display on screen
    screen.blit(frame, (0, 0))
    pygame.display.flip()

# Cleanup
cap.release()
pygame.quit()
sys.exit()
