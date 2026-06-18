import pygame
import os

from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    BG_COLOR,
)

# ─── Khởi tạo pygame & cửa sổ ────────────────────────────────────────────────
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Caro AI - 9x9")

# ─── Font chữ ─────────────────────────────────────────────────────────────────
try:
    font        = pygame.font.SysFont('timesnewroman', 40, True)
    medium_font = pygame.font.SysFont('timesnewroman', 28, True)
    small_font  = pygame.font.SysFont('timesnewroman', 24, True)
except Exception:
    font        = pygame.font.Font(None, 40)
    medium_font = pygame.font.Font(None, 32)
    small_font  = pygame.font.Font(None, 24)

# ─── Ảnh nền ──────────────────────────────────────────────────────────────────
bg_image = None
for ext in ["jpg", "png", "jpeg"]:
    for path_dir in [os.path.dirname(__file__), os.getcwd()]:
        full_path = os.path.join(path_dir, f"background.{ext}")
        if os.path.exists(full_path):
            try:
                img      = pygame.image.load(full_path)
                bg_image = pygame.transform.smoothscale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                break
            except Exception:
                pass
    if bg_image:
        break
