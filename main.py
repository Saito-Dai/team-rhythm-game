import pygame
import sys
import os

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RhythmGame")

clock = pygame.time.Clock()
FPS = 60

BASE_DIR = os.path.dirname(__file__)
def load_image(name):
    path = os.path.join(BASE_DIR,"assets","image",name)
    return pygame.image.load(path).convert_alpha()
# 侍の画像は一時的にmain.pyに組み込みます。
# もう一枚画像を作る際にロードフォルダを作って呼び出せるように修正します。
samurai_img = load_image("Samurai.png")
samurai_img = pygame.transform.smoothscale(samurai_img, (200, 300))

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 侍を左下に描画
        img_w, img_h = samurai_img.get_size()
        margin_x, margin_y = 50, 30
        pos_x = margin_x
        pos_y = SCREEN_HEIGHT - img_h - margin_y
        screen.blit(samurai_img, (pos_x, pos_y))
        
        pygame.display.flip()
        clock.tick(FPS)
        
    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()