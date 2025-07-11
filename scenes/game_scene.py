import pygame
from asset_loader import (samurai_img, samurai_slash_img,blade_wave_img,
                          samurai_miss_img,miss_smoke_img,background_img,
                          slash_se,play_bgm,stop_bgm)
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
    start_ticks = pygame.time.get_ticks()
    bgm_started = False
    bgm_end_time = None  #BGM終了後のcurrent_timeを記録
    notes = []           # 生成済みノーツ
    smoke_effects = []
    font = pygame.font.Font(None, 48)
    feedbacks = []       # {'text': str, 'pos': (x,y), 'time': ms} の辞書を格納
    
    # サムライ画像位置設定
    _, img_h = samurai_img.get_size()
    margin_x, margin_y = 50, 30
    pos_x = margin_x
    pos_y = SCREEN_HEIGHT - img_h - margin_y

    # 譜面データ: time=ms, lane=0～NUM_LANES-1
    notes_data = [
        {"time": 1000, "lane": 0},
    {"time": 1000, "lane": 0},
    {"time": 1300, "lane": 1},
    {"time": 1600, "lane": 2},
    {"time": 1900, "lane": 0},
    {"time": 2200, "lane": 2},
    {"time": 2500, "lane": 3},
    {"time": 2800, "lane": 0},
    {"time": 3100, "lane": 3},
    {"time": 3400, "lane": 0},
    {"time": 3700, "lane": 1},
    {"time": 4000, "lane": 2},
    {"time": 4300, "lane": 3},
    {"time": 4600, "lane": 2},
    {"time": 4900, "lane": 0},
    {"time": 5200, "lane": 3},
    {"time": 5500, "lane": 3},
    {"time": 5800, "lane": 1},
    {"time": 6100, "lane": 0},
    {"time": 6400, "lane": 0},
    {"time": 6700, "lane": 2},
    {"time": 7000, "lane": 1},
    {"time": 7300, "lane": 0},
    {"time": 7600, "lane": 2},
    {"time": 7900, "lane": 1},
    {"time": 8200, "lane": 1},
    {"time": 8500, "lane": 0},
    {"time": 8800, "lane": 1},
    {"time": 9100, "lane": 3},
    {"time": 9400, "lane": 0},
    {"time": 9700, "lane": 0},
    {"time": 10000, "lane": 0},
    {"time": 10300, "lane": 2},
    {"time": 10600, "lane": 3},
    {"time": 10900, "lane": 0},
    {"time": 11200, "lane": 1},
    {"time": 11500, "lane": 1},
    {"time": 11800, "lane": 3},
    {"time": 12100, "lane": 3},
    {"time": 12400, "lane": 2},
    {"time": 12700, "lane": 0},
    {"time": 13000, "lane": 2},
    {"time": 13300, "lane": 0},
    {"time": 13600, "lane": 2},
    {"time": 13900, "lane": 1},
    {"time": 14200, "lane": 0},
    {"time": 14500, "lane": 0},
    {"time": 14800, "lane": 1},
    {"time": 15100, "lane": 1},
    {"time": 15400, "lane": 0},
    {"time": 15700, "lane": 2},
    {"time": 16000, "lane": 0},
    {"time": 16300, "lane": 0},
    {"time": 16600, "lane": 1},
    {"time": 16900, "lane": 3},
    {"time": 17200, "lane": 1},
    {"time": 17500, "lane": 1},
    {"time": 17800, "lane": 1},
    {"time": 18100, "lane": 0},
    {"time": 18400, "lane": 1},
    {"time": 18700, "lane": 2},
    {"time": 19000, "lane": 2},
    {"time": 19300, "lane": 0},
    {"time": 19600, "lane": 3},
    {"time": 19900, "lane": 0},
    {"time": 20200, "lane": 1},
    {"time": 20500, "lane": 0},
    {"time": 20800, "lane": 1},
    {"time": 21100, "lane": 1},
    {"time": 21400, "lane": 0},
    {"time": 21700, "lane": 2},
    {"time": 22000, "lane": 1},
    {"time": 22300, "lane": 2},
    {"time": 22600, "lane": 0},
    {"time": 22900, "lane": 2},
    {"time": 23200, "lane": 3},
    {"time": 23500, "lane": 0},
    {"time": 23800, "lane": 2},
    {"time": 24100, "lane": 1},
    {"time": 24400, "lane": 3},
    {"time": 24700, "lane": 0},
    {"time": 25000, "lane": 2},
    {"time": 25300, "lane": 1},
    {"time": 25600, "lane": 2},
    {"time": 25900, "lane": 1},
    {"time": 26200, "lane": 2},
    {"time": 26500, "lane": 0},
    {"time": 26800, "lane": 0},
    {"time": 27100, "lane": 2},
    {"time": 27400, "lane": 3},
    {"time": 27700, "lane": 3},
    {"time": 28000, "lane": 0},
    {"time": 28300, "lane": 0},
    {"time": 28600, "lane": 0},
    {"time": 28900, "lane": 3},
    {"time": 29200, "lane": 0},
    {"time": 29500, "lane": 0},
    {"time": 29800, "lane": 2},
    {"time": 30100, "lane": 3},
    {"time": 30400, "lane": 3},
    {"time": 30700, "lane": 0},
    {"time": 31000, "lane": 3},
    {"time": 31300, "lane": 1},
    {"time": 31600, "lane": 0},
    {"time": 31900, "lane": 1},
    {"time": 32200, "lane": 0},
    {"time": 32500, "lane": 2},
    {"time": 32800, "lane": 2},
    {"time": 33100, "lane": 0},
    {"time": 33400, "lane": 0},
    {"time": 33700, "lane": 0},
    {"time": 34000, "lane": 3},
    {"time": 34300, "lane": 2},
    {"time": 34600, "lane": 3},
    {"time": 34900, "lane": 2},
    {"time": 35200, "lane": 0},
    {"time": 35500, "lane": 0},
    {"time": 35800, "lane": 3},
    {"time": 36100, "lane": 1},
    {"time": 36400, "lane": 1},
    {"time": 36700, "lane": 3},
    {"time": 37000, "lane": 3},
    {"time": 37300, "lane": 2},
    {"time": 37600, "lane": 3},
    {"time": 37900, "lane": 2},
    {"time": 38200, "lane": 1},
    {"time": 38500, "lane": 1},
    {"time": 38800, "lane": 2},
    {"time": 39100, "lane": 3},
    {"time": 39400, "lane": 3},
    {"time": 39700, "lane": 3},
    {"time": 40000, "lane": 2},
    {"time": 40300, "lane": 0},
    {"time": 40600, "lane": 3},
    {"time": 40900, "lane": 0},
    {"time": 41200, "lane": 1},
    {"time": 41500, "lane": 0},
    {"time": 41800, "lane": 1},
    {"time": 42100, "lane": 1},
    {"time": 42400, "lane": 2},
    {"time": 42700, "lane": 3},
    {"time": 43000, "lane": 0},
    {"time": 43300, "lane": 0},
    {"time": 43600, "lane": 2},
    {"time": 43900, "lane": 2},
    {"time": 44200, "lane": 3},
    {"time": 44500, "lane": 2},
    {"time": 44800, "lane": 1},
    {"time": 45100, "lane": 3},
    {"time": 45400, "lane": 2},
    {"time": 45700, "lane": 0},
    {"time": 46000, "lane": 0},
    {"time": 46300, "lane": 2},
    {"time": 46600, "lane": 3},
    {"time": 46900, "lane": 1},
    {"time": 47200, "lane": 1},
    {"time": 47500, "lane": 1},
    {"time": 47800, "lane": 0},
    {"time": 48100, "lane": 2},
    {"time": 48400, "lane": 0},
    {"time": 48700, "lane": 0},
    {"time": 49000, "lane": 0},
    {"time": 49300, "lane": 0},
    {"time": 49600, "lane": 2},
    {"time": 49900, "lane": 2},
    {"time": 50200, "lane": 3},
    {"time": 50500, "lane": 3},
    {"time": 50800, "lane": 3},
    {"time": 51100, "lane": 1},
    {"time": 51400, "lane": 2},
    {"time": 51700, "lane": 2},
    {"time": 52000, "lane": 0},
    {"time": 52300, "lane": 1},
    {"time": 52600, "lane": 3},
    {"time": 52900, "lane": 2},
    {"time": 53200, "lane": 0},
    {"time": 53500, "lane": 2},
    {"time": 53800, "lane": 1},
    {"time": 54100, "lane": 0},
    {"time": 54400, "lane": 3},
    {"time": 54700, "lane": 1},
    {"time": 55000, "lane": 2},
    {"time": 55300, "lane": 1},
    {"time": 55600, "lane": 3},
    {"time": 55900, "lane": 3},
    {"time": 56200, "lane": 0},
    {"time": 56500, "lane": 2},
    {"time": 56800, "lane": 0},
    {"time": 57100, "lane": 1},
    {"time": 57400, "lane": 0},
    {"time": 57700, "lane": 2},
    {"time": 58000, "lane": 1},
    {"time": 58300, "lane": 3},
    {"time": 58600, "lane": 2},
    {"time": 58900, "lane": 1},
    {"time": 59200, "lane": 2},
    {"time": 59500, "lane": 0},
    {"time": 59800, "lane": 0},
    {"time": 60100, "lane": 0},
    {"time": 60400, "lane": 0},
    {"time": 60700, "lane": 0},
    {"time": 61000, "lane": 0},
    {"time": 61300, "lane": 1},
    {"time": 61600, "lane": 0},
    {"time": 61900, "lane": 3},
    {"time": 62200, "lane": 2},
    {"time": 62500, "lane": 1},
    {"time": 62800, "lane": 2},
    {"time": 63100, "lane": 0},
    {"time": 63400, "lane": 2},
    {"time": 63700, "lane": 3},
    {"time": 64000, "lane": 2},
    {"time": 64300, "lane": 1},
    {"time": 64600, "lane": 1},
    {"time": 64900, "lane": 1},
    {"time": 65200, "lane": 0},
    {"time": 65500, "lane": 2},
    {"time": 65800, "lane": 3},
    {"time": 66100, "lane": 0},
    {"time": 66400, "lane": 1},
    {"time": 66700, "lane": 0},
    {"time": 67000, "lane": 1},
    {"time": 67300, "lane": 1},
    {"time": 67600, "lane": 1},
    {"time": 67900, "lane": 3},
    {"time": 68200, "lane": 0},
    {"time": 68500, "lane": 1},
    {"time": 68800, "lane": 0},
    {"time": 69100, "lane": 1},
    {"time": 69400, "lane": 1},
    {"time": 69700, "lane": 1},
    {"time": 70000, "lane": 1},
    {"time": 70300, "lane": 3},
    {"time": 70600, "lane": 1},
    {"time": 70900, "lane": 1},
    {"time": 71200, "lane": 1},
    {"time": 71500, "lane": 2},
    {"time": 71800, "lane": 2},
    {"time": 72100, "lane": 0},
    {"time": 72400, "lane": 1},
    {"time": 72700, "lane": 3},
    {"time": 73000, "lane": 0},
    {"time": 73300, "lane": 3},
    {"time": 73600, "lane": 2},
    {"time": 73900, "lane": 1},
    {"time": 74200, "lane": 0},
    {"time": 74500, "lane": 3},
    {"time": 74800, "lane": 0},
    {"time": 75100, "lane": 2},
    {"time": 75400, "lane": 0},
    {"time": 75700, "lane": 0},
    {"time": 76000, "lane": 3},
    {"time": 76300, "lane": 3},
    {"time": 76600, "lane": 1},
    {"time": 76900, "lane": 2},
    {"time": 77200, "lane": 0},
    {"time": 77500, "lane": 3},
    {"time": 77800, "lane": 3},
    {"time": 78100, "lane": 2},
    {"time": 78400, "lane": 1},
    {"time": 78700, "lane": 0},
    {"time": 79000, "lane": 1},
    {"time": 79300, "lane": 0},
    {"time": 79600, "lane": 2},
    {"time": 79900, "lane": 1},
    {"time": 80200, "lane": 3},
    {"time": 80500, "lane": 3},
    {"time": 80800, "lane": 3},
    {"time": 81100, "lane": 3},
    {"time": 81400, "lane": 2},
    {"time": 81700, "lane": 3},
    {"time": 82000, "lane": 1},
    {"time": 82300, "lane": 3},
    {"time": 82600, "lane": 2},
    {"time": 82900, "lane": 0},
    {"time": 83200, "lane": 3},
    {"time": 83500, "lane": 2},
    {"time": 83800, "lane": 3},
    {"time": 84100, "lane": 2},
    {"time": 84400, "lane": 3},
    {"time": 84700, "lane": 2},
    {"time": 85000, "lane": 1},
    {"time": 85300, "lane": 1},
    {"time": 85600, "lane": 3},
    {"time": 85900, "lane": 0},
    {"time": 86200, "lane": 3},
    {"time": 86500, "lane": 1},
    {"time": 86800, "lane": 3},
    {"time": 87100, "lane": 1},
    {"time": 87400, "lane": 0},
    {"time": 87700, "lane": 3},
    {"time": 88000, "lane": 3},
    {"time": 88300, "lane": 1},
    {"time": 88600, "lane": 0},
    {"time": 88900, "lane": 3},
    {"time": 89200, "lane": 1},
    {"time": 89500, "lane": 1},
    {"time": 89800, "lane": 0},
    {"time": 90100, "lane": 2},
    {"time": 90400, "lane": 0},
    {"time": 90700, "lane": 1},
    {"time": 91000, "lane": 1},
    {"time": 91300, "lane": 1},
    {"time": 91600, "lane": 3},
    {"time": 91900, "lane": 0},
    {"time": 92200, "lane": 2},
    {"time": 92500, "lane": 0},
    {"time": 92800, "lane": 3},
    {"time": 93100, "lane": 3},
    {"time": 93400, "lane": 0},
    {"time": 93700, "lane": 3},
    {"time": 94000, "lane": 3},
    {"time": 94300, "lane": 3},
    {"time": 94600, "lane": 0},
    {"time": 94900, "lane": 1},
    {"time": 95200, "lane": 0},
    {"time": 95500, "lane": 0},
    {"time": 95800, "lane": 0},
    {"time": 96100, "lane": 2},
    {"time": 96400, "lane": 0},
    {"time": 96700, "lane": 1},
    {"time": 97000, "lane": 3},
    {"time": 97300, "lane": 3},
    {"time": 97600, "lane": 0},
    {"time": 97900, "lane": 1},
    {"time": 98200, "lane": 2},
    {"time": 98500, "lane": 0},
    {"time": 98800, "lane": 2},
    {"time": 99100, "lane": 1},
    {"time": 99400, "lane": 3},
    {"time": 99700, "lane": 2},
    {"time": 100000, "lane": 2},
    {"time": 100300, "lane": 2},
    {"time": 100600, "lane": 1},
    {"time": 100900, "lane": 3},
    {"time": 101200, "lane": 0},
    {"time": 101500, "lane": 0},
    {"time": 101800, "lane": 2},
    {"time": 102100, "lane": 1},
    {"time": 102400, "lane": 1},
    {"time": 102700, "lane": 2},
    {"time": 103000, "lane": 2},
    {"time": 103300, "lane": 2},
    {"time": 103600, "lane": 0},
    {"time": 103900, "lane": 2},
    {"time": 104200, "lane": 3},
    {"time": 104500, "lane": 0},
    {"time": 104800, "lane": 3},
    {"time": 105100, "lane": 2},
    {"time": 105400, "lane": 2},
    {"time": 105700, "lane": 1},
    {"time": 106000, "lane": 1},
    {"time": 106300, "lane": 1},
    {"time": 106600, "lane": 2},
    {"time": 106900, "lane": 0},
    {"time": 107200, "lane": 0},
    {"time": 107500, "lane": 1},
    {"time": 107800, "lane": 2},
    {"time": 108100, "lane": 3},
    {"time": 108400, "lane": 0},
    {"time": 108700, "lane": 0},
    {"time": 109000, "lane": 0},
    {"time": 109300, "lane": 2},
    {"time": 109600, "lane": 1},
    {"time": 109900, "lane": 2},
    {"time": 110200, "lane": 2},
    {"time": 110500, "lane": 1},
    {"time": 110800, "lane": 0},
    {"time": 111100, "lane": 1},
    {"time": 111400, "lane": 0},
    {"time": 111700, "lane": 0},
    {"time": 112000, "lane": 1},
    {"time": 112300, "lane": 3},
    {"time": 112600, "lane": 1},
    {"time": 112900, "lane": 3},
    {"time": 113200, "lane": 2},
    {"time": 113500, "lane": 1},
    {"time": 113800, "lane": 2},
    {"time": 114100, "lane": 2},
    {"time": 114400, "lane": 2},
    {"time": 114700, "lane": 0},
    {"time": 115000, "lane": 0},
    {"time": 115300, "lane": 3},
    {"time": 115600, "lane": 2},
    {"time": 115900, "lane": 0},
    {"time": 116200, "lane": 1},
    {"time": 116500, "lane": 0},
    {"time": 116800, "lane": 1},
    {"time": 117100, "lane": 1},
    {"time": 117400, "lane": 3},
    {"time": 117700, "lane": 1},
    {"time": 118000, "lane": 2},
    {"time": 118300, "lane": 2},
    {"time": 118600, "lane": 0},
    {"time": 118900, "lane": 2},
    {"time": 119200, "lane": 1},
    {"time": 119500, "lane": 1},
    {"time": 119800, "lane": 3},
    {"time": 120100, "lane": 3},
    {"time": 120400, "lane": 0},
    {"time": 120700, "lane": 1},
    {"time": 121000, "lane": 0},
    {"time": 121300, "lane": 0},
    {"time": 121600, "lane": 0},
    {"time": 121900, "lane": 2},
    {"time": 122200, "lane": 0},
    {"time": 122500, "lane": 1},
    {"time": 122800, "lane": 0},
    {"time": 123100, "lane": 1},
    {"time": 123400, "lane": 3},
    {"time": 123700, "lane": 2},
    {"time": 124000, "lane": 3},
    {"time": 124300, "lane": 3},
    {"time": 124600, "lane": 2},
    {"time": 124900, "lane": 2},
    {"time": 125200, "lane": 0},
    {"time": 125500, "lane": 2},
    {"time": 125800, "lane": 0},
    {"time": 126100, "lane": 2},
    {"time": 126400, "lane": 2},
    {"time": 126700, "lane": 0},
    {"time": 127000, "lane": 3},
    {"time": 127300, "lane": 1},
    {"time": 127600, "lane": 1},
    {"time": 127900, "lane": 1},
    {"time": 128200, "lane": 1},
    {"time": 128500, "lane": 3},
    {"time": 128800, "lane": 0},
    {"time": 129100, "lane": 3},
    {"time": 129400, "lane": 3},
    {"time": 129700, "lane": 0},
    {"time": 130000, "lane": 2},
    {"time": 130300, "lane": 3},
    {"time": 130600, "lane": 1},
    {"time": 130900, "lane": 0},
    {"time": 131200, "lane": 2},
    {"time": 131500, "lane": 2},
    {"time": 131800, "lane": 0},
    {"time": 132100, "lane": 1},
    {"time": 132400, "lane": 0},
    {"time": 132700, "lane": 2},
    {"time": 133000, "lane": 0},
    {"time": 133300, "lane": 1},
    {"time": 133600, "lane": 3},
    {"time": 133900, "lane": 2},
    {"time": 134200, "lane": 2},
    {"time": 134500, "lane": 2},
    {"time": 134800, "lane": 1},
    {"time": 135100, "lane": 2},
    {"time": 135400, "lane": 3},
    {"time": 135700, "lane": 2},
    {"time": 136000, "lane": 2},
    {"time": 136300, "lane": 0},
    {"time": 136600, "lane": 2},
    {"time": 136900, "lane": 0},
    {"time": 137200, "lane": 1},
    {"time": 137500, "lane": 3},
    {"time": 137800, "lane": 1},
    {"time": 138100, "lane": 3},
    {"time": 138400, "lane": 2},
    {"time": 138700, "lane": 0},
    {"time": 139000, "lane": 0},
    {"time": 139300, "lane": 1},
    {"time": 139600, "lane": 3},
    {"time": 139900, "lane": 0},
    {"time": 140200, "lane": 2},
    {"time": 140500, "lane": 2},
    {"time": 140800, "lane": 2},
    {"time": 141100, "lane": 3},
    {"time": 141400, "lane": 3},
    {"time": 141700, "lane": 0},
    {"time": 142000, "lane": 1},
    {"time": 142300, "lane": 2},
    {"time": 142600, "lane": 1},
    {"time": 142900, "lane": 1},
    {"time": 143200, "lane": 3},
    {"time": 143500, "lane": 3},
    {"time": 143800, "lane": 2},
    {"time": 144100, "lane": 2},
    {"time": 144400, "lane": 2},
    {"time": 144700, "lane": 1},
    {"time": 145000, "lane": 1},
    {"time": 145300, "lane": 0},
    {"time": 145600, "lane": 3},
    {"time": 145900, "lane": 3},
    {"time": 146200, "lane": 0},
    {"time": 146500, "lane": 0},
    {"time": 146800, "lane": 3},
    {"time": 147100, "lane": 2},
    {"time": 147400, "lane": 2},
    {"time": 147700, "lane": 3},
    {"time": 148000, "lane": 2},
    {"time": 148300, "lane": 2},
    {"time": 148600, "lane": 0},
    {"time": 148900, "lane": 1},
    {"time": 149200, "lane": 3},
    {"time": 149500, "lane": 1},
    {"time": 149800, "lane": 0},
    {"time": 150100, "lane": 1},
    {"time": 150400, "lane": 3},
    {"time": 150700, "lane": 2},
    {"time": 151000, "lane": 3},
    {"time": 151300, "lane": 3},
    {"time": 151600, "lane": 3},
    {"time": 151900, "lane": 1},
    {"time": 152200, "lane": 3},
    {"time": 152500, "lane": 0},
    {"time": 152800, "lane": 1},
    {"time": 153100, "lane": 2},
    {"time": 153400, "lane": 1},
    {"time": 153700, "lane": 2},
    {"time": 154000, "lane": 3},
    {"time": 154300, "lane": 0},
    {"time": 154600, "lane": 3},
    {"time": 154900, "lane": 3},
    {"time": 155200, "lane": 0},
    {"time": 155500, "lane": 3},
    {"time": 155800, "lane": 3},
    {"time": 156100, "lane": 3},
    {"time": 156400, "lane": 3},
    {"time": 156700, "lane": 1},
    {"time": 157000, "lane": 0},
    {"time": 157300, "lane": 0},
    {"time": 157600, "lane": 3},
    {"time": 157900, "lane": 1},
    {"time": 158200, "lane": 1},
    {"time": 158500, "lane": 0},
    {"time": 158800, "lane": 1},
    {"time": 159100, "lane": 2},
    {"time": 159400, "lane": 0},
    {"time": 159700, "lane": 1},
    {"time": 160000, "lane": 1},
    {"time": 160300, "lane": 1},
    {"time": 160600, "lane": 2},
    {"time": 160900, "lane": 0},
    {"time": 161200, "lane": 2},
    {"time": 161500, "lane": 2},
    {"time": 161800, "lane": 1},
    {"time": 162100, "lane": 3},
    {"time": 162400, "lane": 0},
    {"time": 162700, "lane": 0},
    {"time": 163000, "lane": 3},
    {"time": 163300, "lane": 0},
    {"time": 163600, "lane": 1},
    {"time": 163900, "lane": 0},
    {"time": 164200, "lane": 0},
    {"time": 164500, "lane": 1},
    {"time": 164800, "lane": 1},
    {"time": 165100, "lane": 2},
    {"time": 165400, "lane": 2},
    {"time": 165700, "lane": 0},
    {"time": 166000, "lane": 2},
    {"time": 166300, "lane": 0},
    {"time": 166600, "lane": 1},
    {"time": 166900, "lane": 2},
    {"time": 167200, "lane": 2},
    {"time": 167500, "lane": 3},
    {"time": 167800, "lane": 3},
    {"time": 168100, "lane": 2},
    {"time": 168400, "lane": 1},
    {"time": 168700, "lane": 2},
    {"time": 169000, "lane": 3},
    {"time": 169300, "lane": 1},
    {"time": 169600, "lane": 1},
    {"time": 169900, "lane": 2},
    {"time": 170200, "lane": 3},
    {"time": 170500, "lane": 0},
    {"time": 170800, "lane": 1},
    {"time": 171100, "lane": 0},
    {"time": 171400, "lane": 3},
    {"time": 171700, "lane": 3},
    {"time": 172000, "lane": 0},
    {"time": 172300, "lane": 0},
    {"time": 172600, "lane": 3},
    {"time": 172900, "lane": 0},
    {"time": 173200, "lane": 0},
    {"time": 173500, "lane": 3},
    {"time": 173800, "lane": 2},
    {"time": 174100, "lane": 0},
    {"time": 174400, "lane": 2},
    {"time": 174700, "lane": 0},
    {"time": 175000, "lane": 3},
    {"time": 175300, "lane": 3},
    {"time": 175600, "lane": 0},
    {"time": 175900, "lane": 2},
    {"time": 176200, "lane": 1},
    {"time": 176500, "lane": 0},
    {"time": 176800, "lane": 3},
    {"time": 177100, "lane": 0},
    {"time": 177400, "lane": 1},
    {"time": 177700, "lane": 1},
    {"time": 178000, "lane": 3},
    {"time": 178300, "lane": 2},
    {"time": 178600, "lane": 2},
    {"time": 178900, "lane": 3},
    {"time": 179200, "lane": 2},
    {"time": 179500, "lane": 2},
    {"time": 179800, "lane": 1}

    ]

    running = True
    score = combo = perfect_nums = miss_nums = 0
    miss_timer = -9999
    miss_samurai_duration = 300  #miss時侍画像切り替え時間
    miss_effect_duration = 300   #miss時エフェクト表示時間
    slash_timer = 0              #斬撃エフェクト表示中のタイマー
    slash_duration = 200         #斬撃エフェクト表示時間
    current_lane = None          #斬撃エフェクトを出すレーン
    key2lane = {pygame.K_a:0, pygame.K_s:1, pygame.K_d:2, pygame.K_f:3}
    
    while running:
        current_time = pygame.time.get_ticks() - start_ticks
        
        #7秒後にBGM再生開始
        if not bgm_started and current_time >= 7000:
            play_bgm("kiwami_bgm.mp3", loops=0, volume=1.0)
            bgm_started = True
        #BGM終了を検知したら時刻を記録し停止
        if bgm_started and not pygame.mixer.music.get_busy():
            stop_bgm()
            bgm_started = False
            bgm_end_time = current_time
        #BGMから3秒後にシーン終了
        if bgm_end_time is not None and current_time - bgm_end_time >= 3000:
            running = False

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
    
    if bgm_started:
        stop_bgm()
    
    return score, perfect_nums, miss_nums
