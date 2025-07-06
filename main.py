import pygame
import sys

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RhythmGame")

clock = pygame.time.Clock()
FPS = 60

#レーンの描画
LANE_HEIGHT = 80
LANE_GAP = 20
NUM_LANES = 4
LANE_Y = [100 + i*(LANE_HEIGHT + LANE_GAP) for i in range(NUM_LANES)]
HIT_LINE_X = 150
LANE_END_X = SCREEN_WIDTH -200

def draw_lanes():
    for y in LANE_Y:
        pygame.draw.rect(screen,(50,50,50),(HIT_LINE_X, y, LANE_END_X - HIT_LINE_X, LANE_HEIGHT))
    pygame.draw.line(screen, (255,255,255), (HIT_LINE_X, 0), (HIT_LINE_X,SCREEN_HEIGHT), 2)

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((0,0,0))
        draw_lanes()
        
        pygame.display.flip()
        
        clock.tick(FPS)
        
    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()