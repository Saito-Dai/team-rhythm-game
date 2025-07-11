'''
250707ジュンソ : game_sceneがクラスではなく、関数として実装されていたので、result_scene.pyも関数系に変更
'''
# scenes/result_scene.py
import pygame

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from asset_loader import background_img, YujiBoku_font


# --- このファイル内で直接定数を定義します ---
# 画面設定 (main.pyのSCREEN_WIDTH, SCREEN_HEIGHTと一致する必要があります)
SCREEN_WIDTH = 1000  # main.pyで定義された値と同じに設定
SCREEN_HEIGHT = 600  # main.pyで定義された値と同じに設定

# 色の定義 (RGB形式)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 必要であれば他の色もここに定義できます。

# ゲーム状態 (main.pyのGameManagerと一致する必要があります)
# これらの定数はGameManagerでシーン遷移時に使用されるため、GameManagerと同じに保つ必要があります。
GAME_STATE_PLAYING = 1
GAME_STATE_START_SCREEN = 0
GAME_STATE_RESULT_SCREEN = 3 # このシーン自身の状態

# ----------------------------------------
def run_result_scene(screen, clock, final_score, perfect_nums, miss_nums):
    pygame.font.init()
    font_small = YujiBoku_font

    # 画像のロードとサイズ調整
    background_image = background_img

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                # リスタートボタンのクリック判定
                if restart_button_rect.collidepoint((x, y)):
                    return "start"
                # メインメニューボタンのクリック判定
                elif main_menu_button_rect.collidepoint((x, y)):
                    return "menu"

        # 背景描画
        if background_image:
            screen.blit(background_image, (0, 0))
        else:
            screen.fill((0, 0, 0))

        # タイトル
        result_title = YujiBoku_font.render("Game Over!", True, BLACK)
        screen.blit(result_title, (350, 50))

        # スコア表示
        final_score_text = font_small.render(f"Score: {final_score}", True, BLACK)
        screen.blit(final_score_text, (150, 140))

        # PerfectとMissの表示
        perfect_text = font_small.render(f"斬った悪霊 (Perfect): {perfect_nums}", True, BLACK)
        screen.blit(perfect_text, (150, 220))

        miss_text = font_small.render(f"逃げられた悪霊 (Miss): {miss_nums}", True, BLACK)
        screen.blit(miss_text, (150, 300))

        # 命中率計算と表示
        total_notes = perfect_nums + miss_nums
        accuracy = 0.0
        if total_notes > 0:
            accuracy = (perfect_nums / total_notes) * 100

        accuracy_text = font_small.render(f"命中率: {accuracy:.1f}%", True, BLACK)
        screen.blit(accuracy_text, (300, 380))

        # ボタンの描画
        restart_button_text = font_small.render("Restart", True, BLACK)
        restart_button_rect = restart_button_text.get_rect(center=(500, 470))
        screen.blit(restart_button_text, restart_button_rect)

        main_menu_button_text = font_small.render("Main Menu", True, BLACK)
        main_menu_button_rect = main_menu_button_text.get_rect(center=(500, 520))
        screen.blit(main_menu_button_text, main_menu_button_rect)

        pygame.display.flip()
        clock.tick(60)

    return "menu"
