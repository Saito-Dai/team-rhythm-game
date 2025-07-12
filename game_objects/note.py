# note.py
import pygame 
from asset_loader import get_note_speed


NOTE_WIDTH = 10
NOTE_HEIGHT = 50

def get_current_note_speed():
    return 5 * get_note_speed()


# 色の定義 (RGB形式)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0) # 必要であれば追加

# デフォルトのノーツの色
DEFAULT_NOTE_COLOR = WHITE 

class Note:
    """
    リズムゲームのノーツを表すクラス。
    右から左へ移動し、特定の時間に判定ラインに到達する必要があります。
    """
    def __init__(self, x, y, color = DEFAULT_NOTE_COLOR, target_hit_time=20):
        """
        Noteオブジェクトを初期化します。

        Args:
            x (int): ノーツの初期X座標 (通常は画面の最も右側)。
            y (int): ノーツが移動するレーンのY座標。
            color (tuple): ノーツの色 (RGBタプル例: (255, 0, 0))。
            target_hit_time (int): このノーツが判定ラインに正確に到達すべきゲーム内の時間 (ミリ秒)。
                                   (GameSceneで計算して渡されます)。
        """
        # PygameのRectオブジェクトを使用して、ノーツの位置とサイズを管理します。
        # Rect(left, top, width, height)
        self.rect = pygame.Rect(x, y, NOTE_WIDTH, NOTE_HEIGHT)
        
        self.speed = get_current_note_speed()  # ノーツの移動速度 (ピクセル/フレーム)。
        self.color = color       # ノーツの色。
        self.target_hit_time = target_hit_time  # 判定の正確さのための目標時間。
        self.judged = False      # このノーツが既に判定済み (PerfectまたはMiss) かどうかを示すフラグ。
                                 # 重複判定を防ぎ、判定後にノーツを削除するために使用されます。

    def update(self):
        """
        ノーツの状態を更新します (主に位置の移動)。
        毎フレーム呼び出され、ノーツを右から左へ移動させます。
        """
        # X座標を速度分だけ減算し、左へ移動させます。
        self.rect.x -= self.speed

    def draw(self, screen):
        """
        現在のノーツの位置にノーツを描画します。

        Args:
            screen (pygame.Surface): ノーツが描画されるPygameの画面オブジェクト。
        """
        # screenオブジェクトにself.colotrの色でself.rectのサイズの四角形を描画します。
        pygame.draw.rect(screen, self.color, self.rect)

        # もし画像を使用するノーツであれば、次のように描画します。
        # screen.blit(self.image, self.rect)

    def is_offscreen(self):
        """
        ノーツが画面の左外へ完全に移動したかどうかを確認します。

        Returns:
            bool: ノーツが画面外へ移動していればTrue、そうでなければFalse。
        """
        # ノーツの右端 (self.rect.right) が0より小さければ、画面の左外へ移動したことになります。
        return self.rect.right < 0