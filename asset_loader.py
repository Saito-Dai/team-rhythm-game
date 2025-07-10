import pygame, os

#サウンドシステム初期化
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

BASE_DIR = os.path.dirname(__file__)
IMAGE_DIR = os.path.join(BASE_DIR, "assets", "image")
SOUND_DIR = os.path.join(BASE_DIR, "assets", "sound")

def load_image(name, size=None):
    """
    assets/imageから画像を読み込み、必要に応じてリサイズして返す
    :param name: 画像ファイル名
    :param size: (width, height)のタプル。Noneの場合はリサイズしない。
    """
    path = os.path.join(IMAGE_DIR, name)
    try:
        img = pygame.image.load(path).convert_alpha()
    except FileNotFoundError:
        print(f"[Error]画像が見つかりません:{path}")
        raise
    return pygame.transform.smoothscale(img, size) if size else img

samurai_img = load_image("samurai.png",(200, 300)) 
samurai_slash_img = load_image("samurai_slash.png",(200,300))
blade_wave_img = load_image("blade_wave.png")
miss_smoke_img = load_image("miss_effect.png")
background_img = load_image("background.png",(1000, 600)) 
result_test_img = load_image("result_test.png")

def load_sound(name: str, volume: float = 1.0) -> pygame.mixer.Sound:
    """
    効果音を読み込み、指定ボリュームで返す
    :param name: ファイル名
    ;param volume: 0.0 ~ 1.0
    """
    path = os.path.join(SOUND_DIR, name)
    try:
        sound = pygame.mixer.Sound(path)
    except pygame.error as e:
        print(f"[Error] サウンドが見つかりません: {path}")
        raise e
    sound.set_volume(volume)
    return sound

slash_se = load_sound("slash_se.mp3")

def play_bgm(file: str, loops: int = -1, volume: float = 0.5):
    """
    BGMを再生する
    :param file: ファイル名
    :param loops: ループ回数(-1で無限)
    :param volume: 0.0 ~ 1.0
    """
    path = os.path.join(SOUND_DIR, file)
    try:
        pygame.mixer.music.load(path)
    except pygame.error as e:
        print(f"[Error] BGMが見つかりません: {path}")
        raise e
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(loops)
    
def stop_bgm():
    pygame.mixer.music.stop()