import pygame
import sys

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RhythmGame")

clock = pygame.time.Clock()
FPS = 60

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((30,30,30))
        
        pygame.display.flip()
        
        clock.tick(FPS)
        
    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()