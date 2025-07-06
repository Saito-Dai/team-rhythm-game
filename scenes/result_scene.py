# scenes/result_scene.py
import pygame
import os

# --- 이 파일 내에서 직접 상수를 정의합니다 ---
# 화면 설정 (main.py의 SCREEN_WIDTH, SCREEN_HEIGHT와 일치해야 합니다)
SCREEN_WIDTH = 1000  # main.py에서 정의된 값과 동일하게 설정
SCREEN_HEIGHT = 600  # main.py에서 정의된 값과 동일하게 설정

# 색상 정의 (RGB 형식)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# 필요하다면 다른 색상도 여기에 정의할 수 있습니다.

# 게임 상태 (main.py의 GameManager와 일치해야 합니다)
# 이 상수는 GameManager에서 씬 전환 시 사용되므로, GameManager와 동일하게 유지해야 합니다.
GAME_STATE_PLAYING = 1
GAME_STATE_START_SCREEN = 0
GAME_STATE_RESULT_SCREEN = 3 # 이 씬 자체의 상태

# ----------------------------------------

# BaseScene 클래스를 사용하지 않으므로, ResultScene은 직접 필요한 메서드를 구현합니다.
# GameManager가 호출할 update, draw, handle_event 메서드를 정의해야 합니다.
class ResultScene: # BaseScene을 상속받지 않습니다.
    def __init__(self, game_manager):
        # GameManager 인스턴스를 저장하여 씬 전환 등에 사용합니다.
        self.game_manager = game_manager 
        self.final_score = 0
        self.judgment_counts = {}

        # 폰트 로드 (assets/fonts 폴더에 your_font.ttf 파일이 있다고 가정)
        try:
            # 폰트 파일을 정확히 지정 (예: NotoSansJP-Regular.ttf)
            # 프로젝트 구조에 따라 'assets', 'fonts', 'your_font.ttf' 경로를 확인하세요.
            self.font_large = pygame.font.Font(os.path.join('assets', 'fonts', 'your_font.ttf'), 74)
            self.font_small = pygame.font.Font(os.path.join('assets', 'fonts', 'your_font.ttf'), 50)
        except Exception as e: # 폰트 파일이 없거나 로드 실패 시 기본 폰트 사용
            print(f"警告: カスタムフォントをロードできませんでした: {e}。デフォルトフォントを使用します。")
            self.font_large = pygame.font.Font(None, 74)
            self.font_small = pygame.font.Font(None, 50)

        # UI 요소 텍스트 렌더링
        self.restart_button_text = self.font_small.render("Restart", True, WHITE)
        self.restart_button_rect = self.restart_button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150))

        self.main_menu_button_text = self.font_small.render("Main Menu", True, WHITE)
        self.main_menu_button_rect = self.main_menu_button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))

        # --- 배경 이미지 로드 및 크기 조절 ---
        # assets/images/result.png 파일 경로
        background_image_path = os.path.join('assets', 'images', 'result_test.png')
        try:
            # 이미지 로드
            original_background_image = pygame.image.load(background_image_path).convert() 
            
            # 화면 크기에 맞춰 이미지 크기 조절
            self.background_image = pygame.transform.scale(original_background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            print(f"結果画面背景画像 '{background_image_path}'を {SCREEN_WIDTH}x{SCREEN_HEIGHT}に調整してロードしました。")
        except FileNotFoundError:
            print(f"エラー: 結果画面背景画像 '{background_image_path}'が見つかりません。")
            self.background_image = None 
        except pygame.error as e:
            print(f"エラー: 背景画像のロードまたはスケーリング中にエラーが発生しました: {e}")
            self.background_image = None
        # ------------------------------------

    # 씬 전환 시 외부에서 데이터를 받아올 메서드 (GameManager가 호출)
    def set_results(self, final_score, judgment_counts):
        self.final_score = final_score
        self.judgment_counts = judgment_counts

    # GameManager가 호출할 이벤트 처리 메서드
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 재시작 버튼 클릭 처리
            if self.restart_button_rect.collidepoint(event.pos):
                self.game_manager.change_scene(GAME_STATE_PLAYING) # GameManager를 통해 게임 씬으로 전환
            # 메인 메뉴 버튼 클릭 처리
            elif self.main_menu_button_rect.collidepoint(event.pos):
                self.game_manager.change_scene(GAME_STATE_START_SCREEN) # GameManager를 통해 시작 씬으로 전환

    # GameManager가 호출할 업데이트 로직 메서드
    def update(self):
        # 결과 화면에서는 특별히 업데이트할 게임 로직이 없습니다.
        pass

    # GameManager가 호출할 그리기 로직 메서드
    def draw(self, screen):
        # --- 배경 이미지 그리기 (가장 먼저 그려야 다른 요소가 그 위에 보임) ---
        if self.background_image:
            screen.blit(self.background_image, (0, 0)) 
        else:
            screen.fill(BLACK) # 이미지가 없으면 기본 검은색 배경으로 채우기
        # -----------------------------------------------------------------

        # 텍스트 색상 및 위치 조정 (배경 이미지에 맞춰 가독성 좋게)
        # 예시 이미지의 배경이 밝으므로, 텍스트 색상을 검은색으로 변경하는 것을 고려할 수 있습니다.
        TEXT_COLOR = BLACK # 배경이 밝으니 검정색 텍스트가 더 잘 보일 수 있습니다.

        result_title = self.font_large.render("Game Over!", True, TEXT_COLOR)
        screen.blit(result_title, result_title.get_rect(center=(SCREEN_WIDTH // 2, 100)))

        final_score_text = self.font_small.render(f"Final Score: {self.final_score}", True, TEXT_COLOR)
        screen.blit(final_score_text, final_score_text.get_rect(center=(SCREEN_WIDTH // 2, 200)))

        y_offset = 280
        # Perfect, Miss 순서로 표시 (예시 이미지에 '斬った悪霊', '逃げられた悪霊'이 있으니, 그에 맞춰 문구 조정)
        # '斬った悪霊' (벤 악령)을 Perfect에, '逃げられた悪霊' (놓친 악령)을 Miss에 대응시켜 봅시다.
        display_judgments = {
            'Perfect': '斬った悪霊',
            'Miss': '逃げられた悪霊'
        }

        for judgment_key, display_text in display_judgments.items():
            count = self.judgment_counts.get(judgment_key, 0)
            count_text = self.font_small.render(f"{display_text}: {count}", True, TEXT_COLOR)
            screen.blit(count_text, count_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset)))
            y_offset += 40
        
        # 참고 이미지에 '命中率' (명중률)이 있으므로, 이것도 계산하여 표시할 수 있습니다.
        total_notes = self.judgment_counts.get('Perfect', 0) + self.judgment_counts.get('Miss', 0)
        accuracy = 0.0
        if total_notes > 0:
            accuracy = (self.judgment_counts.get('Perfect', 0) / total_notes) * 100

        accuracy_text = self.font_small.render(f"命中率: {accuracy:.1f}%", True, TEXT_COLOR)
        screen.blit(accuracy_text, accuracy_text.get_rect(center=(SCREEN_WIDTH // 2, y_offset + 20)))


        # 버튼 텍스트는 배경 이미지와 독립적으로 WHITE로 유지하거나, 이미지에 맞춰 변경
        screen.blit(self.restart_button_text, self.restart_button_rect)
        screen.blit(self.main_menu_button_text, self.main_menu_button_rect)