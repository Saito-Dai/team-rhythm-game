import pygame, os

BASE_DIR = os.path.dirname(__file__)
IMAGE_DIR = os.path.join(BASE_DIR, "assets", "image")

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
background_img = load_image("background.png",(1000, 600)) 
result_test_img = load_image("result_test.png")