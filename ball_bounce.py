import pygame
import sys
from pygame import gfxdraw
import sound_ctl
import time
# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1600, 1200
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Bouncing Ball Simulation')

# Define colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Ball settings
ball_pos = pygame.math.Vector2(width // 2, height // 3)
ball_speed = pygame.math.Vector2(2, 2)
ball_radius = 20
ball_growth = 1.1  # The factor by which the ball grows
energy_loss = 1.01  # The amount of energy lost on each bounce

# Border settings
border_center = pygame.math.Vector2(width // 2, height // 2)
border_radius = min(width, height) // 3
border_thickness = 10  # pixels

# Clock to control the frame rate
clock = pygame.time.Clock()
gravity = pygame.math.Vector2(0, 0.5)  # The gravitational acceleration

player = sound_ctl.StreamingMusicPlayer("./sample.mp3")  # 여러분의 오디오 파일 경로로 변경하세요.
    
    
def draw_antialiased_circle(surface, color, center, radius):
    gfxdraw.aacircle(surface, int(center.x), int(center.y), radius, color)
    gfxdraw.filled_circle(surface, int(center.x), int(center.y), radius, color)

def bounce_process():
    global ball_pos, ball_speed, ball_radius
    
    # Apply gravity to vertical speed
    ball_speed += gravity

    # Move the ball
    ball_pos += ball_speed

    # Collision detection and response
    direction = ball_pos - border_center
    distance_from_center = direction.length()

    if distance_from_center > border_radius - ball_radius:
        # Calculate the normal at the point of contact
        normal = direction.normalize()

        # Reflect the ball's speed vector over the normal
        ball_speed.reflect_ip(normal)

        # Apply energy loss
        ball_speed *= energy_loss

        # Grow the ball
        ball_radius = int(ball_radius * ball_growth)
        
        #play a song shortly
        player.play()
        player.pause()

        # Correct the position so the ball is exactly on the border
        overlap = distance_from_center + ball_radius - border_radius
        ball_pos -= overlap * normal

    # Clear the screen
    screen.fill(BLACK)

    # Draw the border with anti-aliasing
    draw_antialiased_circle(screen, WHITE, border_center, border_radius)
    # Draw the border outline
    pygame.draw.circle(screen, WHITE, border_center, border_radius, border_thickness)

    # Draw the ball with anti-aliasing
    draw_antialiased_circle(screen, RED, ball_pos, ball_radius)

    # Flip the display
    pygame.display.flip()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    bounce_process()
    clock.tick(60)  # The frame rate can be adjusted to your preference
    
    if ball_radius > border_radius * 3:
        running = False

# Quit Pygame
pygame.quit()
sys.exit()
