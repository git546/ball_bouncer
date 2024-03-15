import cv2
import pygame
import sys
from pygame.math import Vector2
import ball_bounce.py
# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Bouncing Ball Simulation with Video Recording')

# Initialize video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Define the codec
fps = 60  # Define the FPS of the output video
video = cv2.VideoWriter('simulation.mp4', fourcc, fps, (width, height))

# Main animation loop...
# After drawing everything on the screen, capture the screen and write it to the video
running = True
while running:
    # Your game logic and drawing code here
    ball_bounce.bounce_process()
    # Capture the screen
    pygame.display.flip()
    frame = pygame.surfarray.array3d(pygame.display.get_surface())
    frame = cv2.transpose(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    # Write the frame
    video.write(frame)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Release the video writer and quit Pygame
video.release()
pygame.quit()
sys.exit()
