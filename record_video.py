import cv2
import pygame
import sys
import threading
import subprocess
from pygame.math import Vector2
from ball_bounce import Game
import numpy as np

# 비디오 녹화 설정
def record_video(game, output_filename='video.mp4', width=1920, height=1080, fps=60):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Bouncing Ball Simulation with Video Recording')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        game.update()  # Update game logic
        game.draw(screen)  # Render the game

        pygame.display.flip()

        # Capture frame for video
        frame = pygame.surfarray.array3d(pygame.display.get_surface())
        frame = cv2.transpose(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        video.write(frame)
    
    video.release()
    pygame.quit()

def main():
    game = Game()
    # Start video recording in a thread
    video_thread = threading.Thread(target=record_video, args=(game,))
    video_thread.start()
    
    # Wait for video recording to finish
    video_thread.join()

    # Improve video quality
    improve_video_quality('video.mp4', 'enhanced_video.mp4')

    # Merge enhanced video with the recorded audio
    command = ['ffmpeg', '-i', 'enhanced_video.mp4', '-i', 'audio.wav', '-c:v', 'copy', '-c:a', 'aac', 'final_output.mp4']
    subprocess.run(command)

if __name__ == "__main__":
    main()
