'''
250707 ジュンソ：

    game_sceneはクラスではなく関数で実装されていたため、
    result_scene.pyも同じく関数型に変更しました。

    また、main.pyでは
        game_scene -> result_scene -> 
            ・restartを選択したら再びgame_scene
            ・homeを選択したらstart_scene
    という流れになるように修正しています。

    +) 斉藤君へお願い：
        下記のように、game_scene.pyからスコアと判定数をreturnする形に修正をお願いします！
            final_score, perfect_nums, miss_nums = run_game_scene(screen, clock)
        （この形式で返せるようgame_scene側を調整してもらえると助かります）
'''

import pygame
import sys
import os
from scenes.start_scene import run_start_scene
from scenes.option_scene import run_option_scene
from scenes.game_scene import run_game_scene
from scenes.result_scene import run_result_scene


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

    while True:
        choice = run_start_scene(screen, clock)

        if choice == "start":
            while True:
                final_score, perfect_nums, miss_nums = run_game_scene(screen, clock)
                result_choice = run_result_scene(screen, clock, final_score, perfect_nums, miss_nums)

                if result_choice == "quit":
                    pygame.quit()
                    sys.exit()
                elif result_choice == "menu":
                    # メインメニューへ戻る
                    break
                elif result_choice == "start":
                    # もう一度ゲームを開始
                    continue

        elif choice == "option":
            run_option_scene(screen, clock)

        elif choice == "quit":
            break


        
    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()