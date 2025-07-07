import pygame

def show_start_screen(screen):
    background = pygame.image.load("assets/title.png")
    button_rect = pygame.Rect(511, 333, 451, 93)  # x, y, width, height

    running = True
    while running:
        screen.blit(background, (0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "quit"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    return "play"
