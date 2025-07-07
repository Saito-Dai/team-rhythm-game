import pygame
from asset_loader import samurai_img, background_img
from game_objects.note import Note, NOTE_HEIGHT, NOTE_WIDTH, WHITE

# 定数
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
LANE_HEIGHT = 50
LANE_GAP = 10
NUM_LANES = 4
LANE_WIDTH = 600
HIT_LINE_X = SCREEN_WIDTH - LANE_WIDTH
NOTE_SPEED = NOTE_WIDTH  # 調整不要、Note内部で設定

# レーンY座標計算
_total_lanes_height = NUM_LANES * LANE_HEIGHT + (NUM_LANES - 1) * LANE_GAP
_start_y = (SCREEN_HEIGHT - _total_lanes_height) // 2
LANE_Y = [_start_y + i * (LANE_HEIGHT + LANE_GAP) for i in range(NUM_LANES)]


def draw_lanes(screen):
    """レーンと判定ラインを描画する"""
    for y in LANE_Y:
        pygame.draw.rect(
            screen,
            (50, 50, 50),
            (HIT_LINE_X, y, LANE_WIDTH, LANE_HEIGHT)
        )
    # 判定ライン
    pygame.draw.line(
        screen,
        (255, 255, 255),
        (HIT_LINE_X, 0),
        (HIT_LINE_X, SCREEN_HEIGHT),
        2
    )


def run_game_scene(screen, clock):
    """
    プレイ中のシーンを実行する。
    戻り値: (final_score, perfect_nums, miss_nums)
    """
    # --- 初期化 ---
    # サムライ画像位置設定
    _, img_h = samurai_img.get_size()
    margin_x, margin_y = 50, 30
    pos_x = margin_x
    pos_y = SCREEN_HEIGHT - img_h - margin_y

    # 譜面データ: time=ms, lane=0～NUM_LANES-1
    notes_data = [
        {"time": 1000, "lane": 0},
        # 追加譜面はここに足す
    ]
    notes = []  # 生成済みノーツ
    start_ticks = pygame.time.get_ticks()

    running = True
    score = 0
    combo = 0
    perfect_nums = 0
    miss_nums = 0

    while running:
        current_time = pygame.time.get_ticks() - start_ticks

        # ノーツ生成
        for nd in notes_data[:]:
            if current_time >= nd["time"]:
                x0 = SCREEN_WIDTH
                y0 = LANE_Y[nd["lane"]] + (LANE_HEIGHT - NOTE_HEIGHT) // 2
                notes.append(Note(x0, y0, color=WHITE, target_hit_time=nd["time"]))
                notes_data.remove(nd)

        # イベント処理
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            if e.type == pygame.KEYDOWN:
                # キー→レーン対応
                key2lane = {
                    pygame.K_a: 0,
                    pygame.K_s: 1,
                    pygame.K_d: 2,
                    pygame.K_f: 3,
                }
                if e.key in key2lane:
                    lane = key2lane[e.key]
                    # 同レーンかつ未判定のノーツ抽出
                    candidates = [n for n in notes if not n.judged and n.rect.y // (LANE_HEIGHT + LANE_GAP) == lane]
                    if candidates:
                        # 最も近いタイミングのノーツを判定
                        n = min(candidates, key=lambda n: abs(current_time - n.target_hit_time))
                        delta = abs(current_time - n.target_hit_time)
                        # 判定幅 ±150ms
                        if delta <= 150:
                            n.judged = True
                            score += 100
                            combo += 1
                            perfect_nums += 1
                        else:
                            combo = 0
                            miss_nums += 1
        # ESCキーでシーン終了
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            running = False

        # 更新
        for n in notes:
            n.update()

        # 描画
        screen.blit(background_img, (0, 0))
        screen.blit(samurai_img, (pos_x, pos_y))
        draw_lanes(screen)
        for n in notes:
            n.draw(screen)

        # 画面更新
        pygame.display.flip()
        clock.tick(60)

        # ノーツ削除: 判定済 or 画面外
        for n in notes:
            if n.is_offscreen() and not n.judged:
                miss_nums += 1
        notes = [n for n in notes if not (n.judged or n.is_offscreen())]

    return score, perfect_nums, miss_nums
