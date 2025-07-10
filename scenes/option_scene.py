import pygame
import json
import os
from asset_loader import background_img

# 機能：ゲームの設定画面を表示し、ノーツ速度とBGM音量の調整を行う
# 主なクラス：
# 　Slider：スライダーUIを管理
# 　SettingsScene：設定画面のロジックと描画
# 設定永続化：config.json に保存・読み込み

# ─────── 定数定義 ───────
WIDTH, HEIGHT = 1000, 600
SLIDER_WIDTH, SLIDER_HEIGHT = 400, 20
SLIDER_X = (WIDTH - SLIDER_WIDTH) // 2
NOTE_Y, BGM_Y = HEIGHT // 3, HEIGHT // 2
# config.json のパス。プロジェクトルート直下に配置想定
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config.json')


# ─────── Slider クラス ───────
class Slider:
    """
    スライダーUIを管理するクラス。
    - rect: スライダー背景の矩形
    - handle_rect: 現在値を示すハンドルの矩形
    - min, max: 値の最小・最大
    - value: 現在のスライダー値
    """
    def __init__(self, x, y, width, height, min_val, max_val, current):
        
        self.rect = pygame.Rect(x, y, width, height)
        self.min, self.max = min_val, max_val
        self.value = current
        # ハンドルサイズを決定（縦横微調整）
        self.handle_rect = pygame.Rect(0, 0, 10, height + 4)
        self.update_handle()

    def update_handle(self):
        """
        現在値に応じてハンドル位置を更新する。
        値の比率に合わせて背景上を移動。
        """
        ratio = (self.value - self.min) / (self.max - self.min)
        self.handle_rect.centerx = self.rect.x + ratio * self.rect.width
        self.handle_rect.centery = self.rect.centery

    def draw(self, screen):
        """
        スライダー背景とハンドルを描画する。
        """
        pygame.draw.rect(screen, (150, 150, 150), self.rect)      # 背景
        pygame.draw.rect(screen, (255, 255, 255), self.handle_rect)  # ハンドル

    def adjust(self, delta):
        """
        値を増減し、更新後にハンドル位置も再計算する。
        :param delta: 加算する値（正または負）
        """
        self.value = max(self.min, min(self.max, self.value + delta))
        self.update_handle()


# ─────── SettingsScene クラス ───────
class SettingsScene:
    """
    設定画面のロジックを担当。
    - load_config: 設定ファイルを読み込み
    - save_config: スライダーの値をファイルに保存
    - run: メインループ（イベント処理、描画）
    """
    def __init__(self, screen):
        self.screen = screen
        # 設定ファイルから初期値を取得
        self.config = self.load_config()
        # ノーツ速度用スライダー（0.5〜3.0倍）
        self.note_slider = Slider(
            SLIDER_X, NOTE_Y, SLIDER_WIDTH, SLIDER_HEIGHT,
            0.5, 3.0, self.config.get('note_speed', 1.0)
        )

        # BGM音量用スライダー（0〜100%）
        self.bgm_slider = Slider(
            SLIDER_X, BGM_Y, SLIDER_WIDTH, SLIDER_HEIGHT,
            0.0, 1.0, self.config.get('bgm_volume', 0.5)
        )
        # 選択中のスライダー：0=ノーツ, 1=BGM
        self.selected = 0
        self.background = background_img
        #Quitボタンの領域
        self.quit_button_rect = pygame.Rect((WIDTH - 200)//2, HEIGHT - 100, 200, 50)

    def load_config(self):
        """
        config.json から設定を読み込む。
        ファイルがなければ空の dict を返す。
        """
        try:
            with open(CONFIG_PATH, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_config(self):
        """
        現在のスライダー値を config.json に上書き保存する。
        """
        self.config['note_speed'] = self.note_slider.value
        self.config['bgm_volume'] = self.bgm_slider.value
        with open(CONFIG_PATH, 'w') as f:
            json.dump(self.config, f, indent=2)

    def run(self):
        """
        設定画面のメインループ。
        - イベント処理：キー操作でスライダー選択・調整、決定・キャンセル
        - 描画処理：背景・ラベル・スライダー
        """
        clock = pygame.time.Clock()
        running = True

        while running:
            for e in pygame.event.get():
                # 閉じるボタンで終了
                if e.type == pygame.QUIT:
                    running = False
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    if self.quit_button_rect.collidepoint(e.pos):
                        running = False

                # キー入力処理
                elif e.type == pygame.KEYDOWN:
                    # 上下キーで選択切り替え
                    if e.key in (pygame.K_UP, pygame.K_DOWN):
                        self.selected = 1 - self.selected

                    # 左右キーで値を調整
                    elif e.key in (pygame.K_LEFT, pygame.K_RIGHT):
                        delta = -0.1 if e.key == pygame.K_LEFT else 0.1
                        if self.selected == 0:
                            self.note_slider.adjust(delta)
                        else:
                            self.bgm_slider.adjust(delta)

                    # Enterで保存＆画面閉じる
                    elif e.key == pygame.K_RETURN:
                        self.save_config()
                        running = False

                    # Escで保存せずに閉じる
                    elif e.key == pygame.K_ESCAPE:
                        running = False

            # ── 描画 ──
            # 背景を描画
            self.screen.blit(self.background, (0, 0))

            # フォント
            font = pygame.font.SysFont(None, 36)

            # Quitボタン
            pygame.draw.rect(self.screen, (100, 100, 100), self.quit_button_rect)
            quit_font = pygame.font.SysFont(None, 32)
            quit_text = quit_font.render("QUIT", True, (255, 255, 255))
            text_rect = quit_text.get_rect(center=self.quit_button_rect.center)
            self.screen.blit(quit_text, text_rect)

            # ラベル表示：現在値をテキスト化
            note_txt = font.render(
                f"Note Speed: {self.note_slider.value:.1f}x", True, (255, 255, 255)
            )
            bgm_txt = font.render(
                f"BGM Volume: {int(self.bgm_slider.value * 100)}%", True, (255, 255, 255)
            )
            self.screen.blit(note_txt, (SLIDER_X, NOTE_Y - 40))
            self.screen.blit(bgm_txt, (SLIDER_X, BGM_Y - 40))

            # スライダー本体を描画
            self.note_slider.draw(self.screen)
            self.bgm_slider.draw(self.screen)


            pygame.display.flip()
            clock.tick(60)

def run_option_scene(screen, clock):
    """
    main.pyから呼び出すための関数型ラッパー。
    SettingsSceneを作ってその.run()を呼ぶだけ。
    """
    scene = SettingsScene(screen)
    scene.run()
