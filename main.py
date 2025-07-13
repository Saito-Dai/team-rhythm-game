import pygame
import sys
import os

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RhythmGame")

clock = pygame.time.Clock()
FPS = 60

from scenes.start_scene import run_start_scene
from scenes.option_scene import run_option_scene
from scenes.game_scene import run_game_scene
from scenes.result_scene import run_result_scene
from scenes.run_start_screen import run_start_screen


def main():
    run_start_screen(screen, clock)
    while True:
        choice = run_start_scene(screen, clock)

        if choice == "start":
            while True:
                final_score, perfect_nums, good_nums, miss_nums = run_game_scene(screen, clock)
                result_choice = run_result_scene(screen, clock, final_score, perfect_nums, good_nums, miss_nums)

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
            import asset_loader
            import importlib
            importlib.reload(asset_loader)

        elif choice == "quit":
            break

    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()