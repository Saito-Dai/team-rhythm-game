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
        →修正完了しました。画像や音楽を一元管理するasset_loaderファイルを新規作成しました。
        各ファイルで同じ読み込みコードを書かずに済ませる。ゲームロジックに集中させる目的で実装しました。
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

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
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