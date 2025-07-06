# scenes/result_scene.py
import pygame
import os

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

# BaseSceneクラスを使用しないため、ResultSceneは必要なメソッドを直接実装します。
# GameManagerが呼び出す update, draw, handle_event メソッドを定義する必要があります。
class ResultScene: # BaseSceneを継承しません。
    def __init__(self, game_manager):
        # GameManagerインスタンスを保存し、シーン遷移などに使用します。
        self.game_manager = game_manager 
        self.final_score = 0
        self.judgment_counts = {}

        # フォントのロード (assets/fontsフォルダにyour_font.ttfファイルがあると仮定)
        try:
            # フォントファイルを正確に指定 (例: NotoSansJP-Regular.ttf)
            # プロジェクト構造に合わせて 'assets', 'fonts', 'your_font.ttf' のパスを確認してください。
            self.font_large = pygame.font.Font(os.path.join('assets', 'fonts', 'your_font.ttf'), 74)
            self.font_small = pygame.font.Font(os.path.join('assets', 'fonts', 'your_font.ttf'), 50)
        except Exception as e: # フォントファイルがないかロードに失敗した場合、デフォルトフォントを使用
            print(f"警告: カスタムフォントをロードできませんでした: {e}。デフォルトフォントを使用します。")
            self.font_large = pygame.font.Font(None, 74)
            self.font_small = pygame.font.Font(None, 50)

        # UI要素のテキストレンダリング
        self.restart_button_text = self.font_small.render("Restart", True, WHITE)
        self.restart_button_rect = self.restart_button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150))

        self.main_menu_button_text = self.font_small.render("Main Menu", True, WHITE)
        self.main_menu_button_rect = self.main_menu_button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))

        # --- 背景画像のロードとサイズ調整 ---
        # assets/images/result_test.png ファイルのパス
        background_image_path = os.path.join('assets', 'images', 'result_test.png')
        try:
            # 画像をロード
            original_background_image = pygame.image.load(background_image_path).convert() 
            
            # 画面サイズに合わせて画像のサイズを調整
            self.background_image = pygame.transform.scale(original_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            print(f"結果画面背景画像 '{background_image_path}'を {SCREEN_WIDTH}x{SCREEN_HEIGHT}に調整してロードしました。")
        except FileNotFoundError:
            print(f"エラー: 結果画面背景画像 '{background_image_path}'が見つかりません。")
            self.background_image = None 
        except pygame.error as e:
            print(f"エラー: 背景画像のロードまたはスケーリング中にエラーが発生しました: {e}")
            self.background_image = None
        # ------------------------------------

    # シーン遷移時に外部からデータを受け取るメソッド (GameManagerが呼び出す)
    def set_results(self, final_score, judgment_counts):
        self.final_score = final_score
        self.judgment_counts = judgment_counts

    # GameManagerが呼び出すイベント処理メソッド
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # リスタートボタンクリック処理
            if self.restart_button_rect.collidepoint(event.pos):
                self.game_manager.change_scene(GAME_STATE_PLAYING) # GameManagerを介してゲームシーンに遷移
            # メインメニューボタンクリック処理
            elif self.main_menu_button_rect.collidepoint(event.pos):
                self.game_manager.change_scene(GAME_STATE_START_SCREEN) # GameManagerを介してスタートシーンに遷移

    # GameManagerが呼び出す更新ロジックメソッド
    def update(self):
        # 結果画面では特に更新するゲームロジックはありません。
        pass

    # GameManagerが呼び出す描画ロジックメソッド
    def draw(self, screen):
        # --- 背景画像の描画 (他の要素より先に描画することで、その上に表示されます) ---
        if self.background_image:
            screen.blit(self.background_image, (0, 0)) 
        else:
            screen.fill(BLACK) # 画像がない場合、デフォルトの黒い背景で塗りつぶし
        # -----------------------------------------------------------------

        # テキストの色と位置を調整 (背景画像に合わせて読みやすく)
        # 例示画像の背景が明るいため、テキストの色を黒に変更することを検討できます。
        TEXT_COLOR = BLACK # 背景が明るいので黒いテキストの方がよく見えます。

        result_title = self.font_large.render("Game Over!", True, TEXT_COLOR)
        screen.blit(result_title, result_title.get_rect(center=(SCREEN_WIDTH // 2, 100)))

        final_score_text = self.font_small.render(f"Final Score: {self.final_score}", True, TEXT_COLOR)
        screen.blit(final_score_text, final_score_text.get_rect(center=(SCREEN_WIDTH // 2, 200)))

        y_offset = 280
        # Perfect, Miss の順に表示 (例示画像に「斬った悪霊」「逃げられた悪霊」があるので、それに合わせて文言を調整)
        # 「斬った悪霊」をPerfectに、「逃げられた悪霊」をMissに対応させてみましょう。
        display_judgments = {
            'Perfect': '斬った悪霊',
            'Miss': '逃げられた悪霊'
        }

        for judgment_key, display_text in display_judgments.items():
            count = self.judgment_counts.get(judgment_key, 0)
            count_text = self.font_small.render(f"{display_text}: {count}", True, TEXT_COLOR)
            screen.blit(count_text, count_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset)))
            y_offset += 40
        
        # 参考画像に「命中率」があるので、これも計算して表示できます。
        total_notes = self.judgment_counts.get('Perfect', 0) + self.judgment_counts.get('Miss', 0)
        accuracy = 0.0
        if total_notes > 0:
            accuracy = (self.judgment_counts.get('Perfect', 0) / total_notes) * 100

        accuracy_text = self.font_small.render(f"命中率: {accuracy:.1f}%", True, TEXT_COLOR)
        screen.blit(accuracy_text, accuracy_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset + 20)))


        # ボタンのテキストは背景画像とは独立してWHITEを維持するか、画像に合わせて変更してください。
        screen.blit(self.restart_button_text, self.restart_button_rect)
        screen.blit(self.main_menu_button_text, self.main_menu_button_rect)