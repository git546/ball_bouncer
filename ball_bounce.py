import pygame
import sys
from pygame import gfxdraw
import sound_ctl
import time
# Initialize Pygame
pygame.init()

# Set up the display
width, height = 900, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Bouncing Ball Simulation')

# Define colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Ball settings
ball_pos = pygame.math.Vector2(width // 2, height // 3)
ball_speed = pygame.math.Vector2(1, 1)
ball_radius = 10
ball_growth = 1.1  # The factor by which the ball grows
energy_loss = 1.01  # The amount of energy lost on each bounce

# Border settings
border_center = pygame.math.Vector2(width // 2, height // 2)
border_radius = min(width, height) // 2
border_thickness = 1  # pixels

# Clock to control the frame rate
clock = pygame.time.Clock()
gravity = pygame.math.Vector2(0, 0.5)  # The gravitational acceleration

player = sound_ctl.StreamingMusicPlayer("./sample.mp3")
    
    
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

    if distance_from_center >= border_radius - ball_radius:
        # Calculate the normal at the point of contact
        normal = direction.normalize()

        # Reflect the ball's speed vector over the normal
        ball_speed.reflect_ip(normal)

        # Apply energy loss
        ball_speed *= energy_loss

        # Grow the ball
        ball_radius = int(ball_radius * ball_growth)

        # Correct the position so the ball is exactly on the border
        overlap = distance_from_center + ball_radius - border_radius
        ball_pos -= overlap * normal
        
        # 공이 경계에 충돌할 때마다 음악 재생
        player._play_segment(duration_ms=500)  # 예: 1초간 재생
        

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


