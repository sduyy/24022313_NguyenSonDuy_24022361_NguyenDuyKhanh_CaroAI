"""
constants.py
Định nghĩa tất cả hằng số dùng chung trong toàn bộ dự án Caro AI.
"""

# ─── Kích thước bàn cờ ────────────────────────────────────────────────────────
SIZE = 9
CELL_SIZE = 50
BOARD_SIZE = SIZE * CELL_SIZE

# ─── Kích thước cửa sổ ────────────────────────────────────────────────────────
SCREEN_WIDTH  = 900
SCREEN_HEIGHT = 650

# ─── Vị trí bàn cờ trên màn hình ─────────────────────────────────────────────
BOARD_X = (SCREEN_WIDTH  - BOARD_SIZE) // 2
BOARD_Y = (SCREEN_HEIGHT - BOARD_SIZE) // 2 - 30

# ─── Bảng màu ─────────────────────────────────────────────────────────────────
WHITE                   = (255, 255, 255)
BLACK                   = (0,   0,   0)
LINE_COLOR              = (50,  50,  50)
X_COLOR                 = (200, 50,  50)
O_COLOR                 = (50,  50,  200)
BG_COLOR                = (240, 240, 240)
BOARD_BG                = (222, 184, 135)
BUTTON_COLOR            = (139, 69,  19)
BUTTON_HOVER_COLOR      = (160, 82,  45)
QUIT_BUTTON_COLOR       = (178, 34,  34)
QUIT_BUTTON_HOVER_COLOR = (205, 92,  92)
