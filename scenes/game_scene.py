import pygame
from asset_loader import samurai_img, samurai_slash_img,blade_wave_img,samurai_miss_img,miss_smoke_img,background_img,slash_se
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
    notes = []           # 生成済みノーツ
    smoke_effects = []
    start_ticks = pygame.time.get_ticks()
    font = pygame.font.Font(None, 48)
    feedbacks = []       # {'text': str, 'pos': (x,y), 'time': ms} の辞書を格納

    running = True
    score = 0
    combo = 0
    perfect_nums = 0
    miss_nums = 0
    miss_timer = -9999
    miss_samurai_duration = 300  #miss時侍画像切り替え時間
    miss_effect_duration = 300   #miss時エフェクト表示時間
    slash_timer = 0              #斬撃エフェクト表示中のタイマー
    slash_duration = 200         #斬撃エフェクト表示時間
    current_lane = None          #斬撃エフェクトを出すレーン
    key2lane = {pygame.K_a:0, pygame.K_s:1, pygame.K_d:2, pygame.K_f:3}
    
    while running:
        current_time = pygame.time.get_ticks() - start_ticks

        # ノーツ生成
        for nd in notes_data[:]:
            if current_time >= nd["time"]:
                x0 = SCREEN_WIDTH
                y0 = LANE_Y[nd["lane"]] + (LANE_HEIGHT - NOTE_HEIGHT) // 2
                n = Note(x0, y0, color=WHITE, target_hit_time=nd["time"])
                n.lane = nd["lane"]
                notes.append(n)
                notes_data.remove(nd)

        # イベント処理
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            elif e.type == pygame.KEYDOWN and e.key in key2lane:
                lane = key2lane[e.key]
                current_lane = lane
                slash_timer = current_time
                # 同レーンかつ未判定のノーツ抽出
                candidates = [n for n in notes if not n.judged and n.lane == lane]
                if candidates:
                    # 最も近いタイミングのノーツを判定
                    n = min(candidates, key=lambda n: abs(current_time - n.target_hit_time))
                    delta = abs(current_time - n.target_hit_time)
                    # 判定幅 150ms以内→"良",150ms超~200ms以内→"可"を表示
                    if delta <= 150:
                        n.judged = True
                        score += 100
                        combo += 1
                        perfect_nums += 1
                        slash_se.play()
                        feedbacks.append({
                            'text' : '良',
                            'pos'  : (n.rect.centerx, n.rect.y - 20),
                            'time' : current_time
                        })
                    elif delta <= 200:
                        n.judged = True
                        combo += 1
                        miss_nums += 1
                        slash_se.play()
                        feedbacks.append({
                            'text' : '可',
                            'pos'  : (n.rect.centerx, n.rect.y - 20),
                            'time' : current_time
                        })
                    else:
                        n.judged = True
                        n.miss_time = current_time
                        smoke_effects.append({
                            'pos'  : (n.rect.x, n.rect.y),
                            'time' : current_time,
                            'note' : n
                        })
                        combo = 0
                        miss_nums += 1
                        miss_timer = current_time
                            
        # ESCキーでシーン終了
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            running = False

        # 更新
        for n in notes:
            n.update()
            
        screen.blit(background_img, (0, 0))    
        
        # 侍の描画
        if current_time - miss_timer < miss_samurai_duration:
            img = samurai_miss_img
        elif current_lane is not None and current_time - slash_timer < slash_duration:
            img = samurai_slash_img
        else:
            img = samurai_img
        screen.blit(img, (pos_x, pos_y))

        #レーン・ノーツの描画
        draw_lanes(screen)
        for n in notes:
            if not n.judged:
                n.draw(screen)

        #miss時の煙エフェクト
        for se in smoke_effects[:]:
            elapsed = current_time - se['time']
            if elapsed <= miss_effect_duration:
                screen.blit(miss_smoke_img, se['pos'])
            else:
                if se['note'] in notes:
                    notes.remove(se['note'])
                smoke_effects.remove(se)
                            
        # 斬撃エフェクトを表示
        if current_lane is not None and current_time - slash_timer < slash_duration:
            #レーンの判定ラインX座標
            fx = HIT_LINE_X
            #Y座標は押されたレーンの中央当たりか固定の高さ
            fy = LANE_Y[current_lane] + LANE_HEIGHT // 2
            screen.blit(blade_wave_img,
                        (fx - blade_wave_img.get_width(),
                         fy - blade_wave_img.get_height() // 2))
        
        # 判定フィードバックを短時間ノーツ上に表示
        for fb in feedbacks[:]:
            if current_time - fb['time'] < 500:
                surf = font.render(fb['text'], True, WHITE)
                screen.blit(surf, fb['pos'])
            else:
                feedbacks.remove(fb)
                
        # スコア表示(画面右上)
        score_surf = font.render(f"得点：{score}", True, WHITE)
        screen.blit(
            score_surf,
            (SCREEN_WIDTH - score_surf.get_width() - 20, 20)
        )
        
        # コンボ表示(侍頭上)
        if combo > 1:
            combo_surf = font.render(f"{combo}連", True, WHITE)
            screen.blit(
                combo_surf,
                (pos_x, pos_y - combo_surf.get_height() - 10)
            )

        # 画面更新
        pygame.display.flip()
        clock.tick(60)

        # ノーツ削除: 判定済 or 画面外
        for n in notes[:]:
            if n.is_offscreen() and not n.judged:
                n.judged = True
                n.miss_time = current_time
                smoke_effects.append({
                    'pos'  : (n.rect.x, n.rect.y),
                    'time' : current_time,
                    'note' : n
                })
                miss_nums += 1
                miss_timer = current_time
                
        notes = [
            n for n in notes
            if (not n.judged)
            or (hasattr (n, 'miss_time') and current_time - n.miss_time <= miss_effect_duration)]

    return score, perfect_nums, miss_nums
