# scenes/game_scene.py
import pygame, os

def load_image(name, base_dir):
    return pygame.image.load(
        os.path.join(base_dir, "assets", "image", name)
    ).convert_alpha()

def run_game_scene(screen, clock, base_dir):
    """プレイ中のシーン処理を行い、終了したら戻る"""
    # 初期化
    samurai_img = load_image("samurai.png", base_dir)
    samurai_img = pygame.transform.smoothscale(samurai_img, (200, 300))
    img_w, img_h = samurai_img.get_size()
    margin_x, margin_y = 50, 30
    pos_x = margin_x
    pos_y = screen.get_height() - img_h - margin_y

    # メインループ
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False   # アプリ終了サイン
            
            # ここでキー操作や判定処理を追加

        screen.fill((0,0,0))
        screen.blit(samurai_img, (pos_x, pos_y))
        # lanes やノーツの描画・更新もここに追加する予定

        pygame.display.flip()
        clock.tick(60)

        # ESCキーで一時的にシーンを終了する
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

    return True  # シーン終了サイン
