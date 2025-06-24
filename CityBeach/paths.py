# paths.py
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SRC_DIR = os.path.join(BASE_DIR, "src")
IMG_DIR = os.path.join(SRC_DIR, "img")
FONTS_DIR = os.path.join(SRC_DIR, "fonts")

def image_path(filename: str) -> str:
    return os.path.join(IMG_DIR, filename)

def font_path(filename: str) -> str:
    return os.path.join(FONTS_DIR, filename)
