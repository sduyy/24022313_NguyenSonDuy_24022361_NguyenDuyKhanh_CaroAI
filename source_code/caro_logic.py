"""
caro_logic.py  (Entry Point — Backward Compatibility Shim)
────────────────────────────────────────────────────────────
File này giữ nguyên vai trò entry point cũ.
Toàn bộ logic đã được tách vào các module chuyên biệt:

    constants.py   — Hằng số (kích thước, màu sắc, ...)
    resources.py   — Khởi tạo pygame, font, ảnh nền
    game_logic.py  — Lớp CaroGame (bàn cờ, undo, check_win, heuristic)
    ai.py          — Thuật toán Minimax & Alpha-Beta Pruning
    renderer.py    — Các hàm vẽ giao diện
    main.py        — Vòng lặp game chính (game loop)

Chạy chương trình:
    python caro_logic.py
    hoặc: python main.py
"""

# Re-export để các module cũ (ví dụ benchmark.py) vẫn import được
from constants  import *          # noqa: F401, F403
from resources  import screen, font, medium_font, small_font, bg_image  # noqa: F401
from game_logic import CaroGame   # noqa: F401
import ai                         # noqa: F401  — gắn AI vào CaroGame
from renderer   import (          # noqa: F401
    draw_menu, draw_difficulty_menu,
    draw_board, draw_status,
    draw_game_over_popup, draw_confirm_quit,
)
from main import main             # noqa: F401


if __name__ == "__main__":
    main()
