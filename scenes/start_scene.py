import pygame
from asset_loader import background_img

def run_start_scene(screen, clock): # main.py から clock 引数が渡されるため、追加します。
    """
    スタートシーンを実行します。
    ユーザーの選択に応じて "start", "option", "quit" のいずれかを返します。
    """
    background = background_img
    
    # "ゲーム開始" ボタンの矩形領域を定義します。
    start_button_rect = pygame.Rect(511, 333, 451, 93) 
    
    # "オプション" ボタンの矩形領域を定義します。
    option_button_rect = pygame.Rect(511, 430, 451, 93) 

    # "QUIT" ボタンの矩形領域を定義します。
    quit_button_rect = pygame.Rect(511, 527, 451, 93)
    
    running = True
    while running:
        # 背景を描画
        screen.blit(background, (0, 0))
        
        # デバッグ用にボタンの領域を四角で表示したい場合、コメントを外してください。
        pygame.draw.rect(screen, (255,0,0), start_button_rect, 2) 
        pygame.draw.rect(screen, (0,255,0), option_button_rect, 2) 
        pygame.draw.rect(screen, (0,0,255), quit_button_rect, 2)

        
        # 画面を更新
        pygame.display.update()

        # イベント処理ループ
        for event in pygame.event.get():
            # ウィンドウの閉じるボタンが押された場合
            if event.type == pygame.QUIT:
                running = False
                return "quit" # main.py に "quit" を返して終了を指示

            # マウスボタンが押された場合
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # "ゲーム開始" ボタンがクリックされたかチェック
                if start_button_rect.collidepoint(event.pos):
                    return "start" # main.py に "start" (ゲームシーンへ) を指示
                # "オプション" ボタンがクリックされたかチェック
                elif option_button_rect.collidepoint(event.pos):
                    return "option" # main.py に "option" (オプションシーンへ) を指示
                # "QUIT" ボタンがクリックされたかチェック
                elif quit_button_rect.collidepoint(event.pos):
                    return "quit"
        
        # ゲームのフレームレートを制限 (main.py の FPS と一致させる)
        clock.tick(60)