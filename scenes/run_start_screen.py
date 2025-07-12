import pygame
from asset_loader import start_img

def run_start_screen(screen, clock):
    # scaling
    start_image_scaled = pygame.transform.scale(start_img, screen.get_size())

    # blit
    screen.blit(start_image_scaled, (0, 0))
    pygame.display.flip()

    # 2sec
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < 2000:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        clock.tick(60)
