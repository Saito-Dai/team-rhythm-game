import pygame
import json
import os
from asset_loader import background_img, YujiBoku_font, YujiBoku_font_small

# 機能：ゲームの設定画面を表示し、ノーツ速度とBGM音量をマウスで調整
# 主なクラス：
# 　Slider：スライダーUIを管理
# 　SettingsScene：設定画面のロジックと描画
# 設定の保存先：config.json

# ─────── 定数定義 ───────
WIDTH, HEIGHT = 1000, 600
SLIDER_WIDTH, SLIDER_HEIGHT = 400, 20
SLIDER_X = (WIDTH - SLIDER_WIDTH) // 2
NOTE_Y = HEIGHT // 4
BGM_Y = HEIGHT // 2
SE_Y = (HEIGHT * 3) // 4
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config.json')


# ─────── Slider クラス ───────
class Slider:
    """
    スライダーUIを管理するクラス。
    """
    def __init__(self, x, y, width, height, min_val, max_val, current):
        self.rect = pygame.Rect(x, y, width, height)
        self.min = min_val
        self.max = max_val
        self.value = current
        self.handle_rect = pygame.Rect(0, 0, 10, height + 4)
        self.update_handle()

    def update_handle(self):
        """
        現在の値に基づいてハンドル位置を更新
        """
        ratio = (self.value - self.min) / (self.max - self.min)
        self.handle_rect.centerx = self.rect.x + ratio * self.rect.width
        self.handle_rect.centery = self.rect.centery

    def draw(self, screen):
        """
        スライダー本体を描画
        """
        pygame.draw.rect(screen, (150, 150, 150), self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.handle_rect)


# ─────── SettingsScene クラス ───────
class SettingsScene:
    """
    設定画面を管理するクラス
    - マウス操作でスライダーを調整
    - 設定を保存
    """
    def __init__(self, screen):
        BUTTON_WIDTH = 80
        BUTTON_HEIGHT = 30
        BUTTON_X_OFFSET = SLIDER_WIDTH + 20  # スライダーの右側

        self.note_reset_rect = pygame.Rect(SLIDER_X + BUTTON_X_OFFSET, NOTE_Y - 15, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.bgm_reset_rect = pygame.Rect(SLIDER_X + BUTTON_X_OFFSET, BGM_Y - 15, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.se_reset_rect = pygame.Rect(SLIDER_X + BUTTON_X_OFFSET, SE_Y - 15, BUTTON_WIDTH, BUTTON_HEIGHT)

        self.screen = screen
        self.config = self.load_config()

        self.note_slider = Slider(
            SLIDER_X, NOTE_Y, SLIDER_WIDTH, SLIDER_HEIGHT,
            0.5, 3.0, self.config.get('note_speed', 1.0)
        )

        self.bgm_slider = Slider(
            SLIDER_X, BGM_Y, SLIDER_WIDTH, SLIDER_HEIGHT,
            0.0, 1.0, self.config.get('bgm_volume', 0.5)
        )

        self.se_slider = Slider(
            SLIDER_X, SE_Y, SLIDER_WIDTH, SLIDER_HEIGHT,
            0.0, 1.0, self.config.get('se_volume', 0.5)
        )

        self.background = background_img
        self.quit_button_rect = pygame.Rect((WIDTH - 200)//2, HEIGHT - 100, 200, 50)
        self.dragging_slider = None

    def load_config(self):
        """
        config.json から設定を読み込む
        """
        try:
            with open(CONFIG_PATH, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_config(self):
        """
        設定をconfig.jsonに保存
        """
        self.config['note_speed'] = self.note_slider.value
        self.config['bgm_volume'] = self.bgm_slider.value
        self.config['se_volume'] = self.se_slider.value

        with open(CONFIG_PATH, 'w') as f:
            json.dump(self.config, f, indent=2)

    def update_slider_value_from_pos(self, pos):
        """
        マウス座標に基づいてスライダー値を更新
        """
        slider = self.dragging_slider
        if not slider:
            return
        rel_x = pos[0] - slider.rect.x
        ratio = max(0, min(1, rel_x / slider.rect.width))
        slider.value = slider.min + ratio * (slider.max - slider.min)
        slider.update_handle()

    def run(self):
        """
        メインループ：イベント処理と描画
        """
        clock = pygame.time.Clock()
        running = True

        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False

                elif e.type == pygame.MOUSEBUTTONDOWN:
                    if self.quit_button_rect.collidepoint(e.pos):
                        self.save_config()
                        running = False
                    elif self.note_slider.rect.collidepoint(e.pos):
                        self.dragging_slider = self.note_slider
                        self.update_slider_value_from_pos(e.pos)
                    elif self.bgm_slider.rect.collidepoint(e.pos):
                        self.dragging_slider = self.bgm_slider
                        self.update_slider_value_from_pos(e.pos)
                    elif self.se_slider.rect.collidepoint(e.pos):
                        self.dragging_slider = self.se_slider
                        self.update_slider_value_from_pos(e.pos)
                    elif self.note_reset_rect.collidepoint(e.pos):
                        self.note_slider.value = 1.0
                        self.note_slider.update_handle()
                    elif self.bgm_reset_rect.collidepoint(e.pos):
                        self.bgm_slider.value = 0.5
                        self.bgm_slider.update_handle()
                    elif self.se_reset_rect.collidepoint(e.pos):
                        self.se_slider.value = 0.5
                        self.se_slider.update_handle()

                elif e.type == pygame.MOUSEBUTTONUP:
                    self.dragging_slider = None

                elif e.type == pygame.MOUSEMOTION:
                    if self.dragging_slider:
                        self.update_slider_value_from_pos(e.pos)

            # ── 描画処理 ──
            self.screen.blit(self.background, (0, 0))

            # フォント設定
            big_font = YujiBoku_font
            small_font = YujiBoku_font_small


            # EXIT文字のみ（背景なし）
            quit_text = big_font.render("戻る", True, (0, 0, 0))
            text_rect = quit_text.get_rect(center=self.quit_button_rect.center)
            self.screen.blit(quit_text, text_rect)


            # スライダーラベル（小さいフォント）
            note_txt = small_font.render(
                f"速さ: {self.note_slider.value:.1f}x", True, (0, 0, 0)
            )
            bgm_txt = small_font.render(
                f"音量: {int(self.bgm_slider.value * 100)}%", True, (0, 0, 0)
            )
            se_txt = small_font.render(
                f"効果音: {int(self.se_slider.value * 100)}%", True, (0, 0, 0)
            )
            # --- 初期化 ボタンを描画 ---
            button_color = (200, 200, 200)
            text_color = (0, 0, 0)

            reset_text = small_font.render("初期化", True, text_color)

            self.screen.blit(
                reset_text,
                reset_text.get_rect(center=self.note_reset_rect.center)
            )
            self.screen.blit(
                reset_text,
                reset_text.get_rect(center=self.bgm_reset_rect.center)
            )
            self.screen.blit(
                reset_text,
                reset_text.get_rect(center=self.se_reset_rect.center)
            )

            
            
            self.screen.blit(se_txt, (SLIDER_X, SE_Y - 60))
            self.screen.blit(note_txt, (SLIDER_X, NOTE_Y - 60))
            self.screen.blit(bgm_txt, (SLIDER_X, BGM_Y - 60))

            # スライダー本体を描画
            self.note_slider.draw(self.screen)
            self.bgm_slider.draw(self.screen)
            self.se_slider.draw(self.screen)



            # ガイドテキスト（大きいフォント）
            guide_text = big_font.render("スライダーをマウスで調整してください", True, (0, 0, 0))
            self.screen.blit(guide_text, (50, 20))

            pygame.display.flip()
            clock.tick(60)

def run_option_scene(screen, clock):
    """
    main.py から呼び出すための関数
    """
    scene = SettingsScene(screen)
    scene.run()
