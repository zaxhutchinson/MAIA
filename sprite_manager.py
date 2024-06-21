from PIL import Image

SPRITE_PATH = ""


def init(ldr):
    global SPRITE_PATH
    SPRITE_PATH = ldr.get_main_config_data("sprite_path")


def load_image(filename):
    try:
        return Image.open(f"{SPRITE_PATH}/{filename}")
    except Exception:
        raise
