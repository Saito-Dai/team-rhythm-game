import pygame
from asset_loader import background_img, YujiBoku_font, start_scene_samurai, YujiBoku_font_big, YujiBoku_font_little_big

def run_start_scene(screen, clock):
    """
    スタートシーンを実行します。
    ユーザーの選択に応じて "start", "option", "quit" のいずれかを返します。
    """
    background = background_img
    
    # ボタンの矩形領域を定義（Y座標を30上にシフト）
    start_button_rect = pygame.Rect(475, 303, 451, 93)
    option_button_rect = pygame.Rect(475, 400, 451, 93)
    quit_button_rect = pygame.Rect(475, 497, 451, 93)


    font = YujiBoku_font
    big_font = YujiBoku_font_big
    little_big_font = YujiBoku_font_little_big

    running = True
    while running:
        # 背景を描画
        screen.blit(background, (0, 0))
        screen.blit(start_scene_samurai, (-70, 50))
        #タイトル
        title_text = big_font.render("斬律", True, (0, 0, 0))
        subtitle_text = little_big_font.render("-ZANAITSU-", True, (0, 0, 0))

        # 整列
        title_rect = title_text.get_rect(center=(700, 130))
        subtitle_rect = subtitle_text.get_rect(center=(700, 210))

        screen.blit(title_text, title_rect)
        screen.blit(subtitle_text, subtitle_rect)
        # --- ボタンテキストを描画 ---
        start_text = font.render("いざ勝負", True, (0, 0, 0))
        option_text = font.render("設定", True, (0, 0, 0))
        quit_text = font.render("ゲーム終了", True, (0, 0, 0))

        # テキストをボタンの中央に配置
        start_text_rect = start_text.get_rect(center=start_button_rect.center)
        option_text_rect = option_text.get_rect(center=option_button_rect.center)
        quit_text_rect = quit_text.get_rect(center=quit_button_rect.center)

        screen.blit(start_text, start_text_rect)
        screen.blit(option_text, option_text_rect)
        screen.blit(quit_text, quit_text_rect)

        # 画面を更新
        pygame.display.update()

        # イベント処理ループ
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    return "start"
                elif option_button_rect.collidepoint(event.pos):
                    return "option"
                elif quit_button_rect.collidepoint(event.pos):
                    return "quit"

        # FPS制御
        clock.tick(60)