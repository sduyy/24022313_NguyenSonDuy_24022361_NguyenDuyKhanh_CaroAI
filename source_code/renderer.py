import pygame

from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    BOARD_X, BOARD_Y, BOARD_SIZE, CELL_SIZE, SIZE,
    WHITE, BLACK, LINE_COLOR,
    X_COLOR, O_COLOR,
    BG_COLOR, BOARD_BG,
    BUTTON_COLOR, BUTTON_HOVER_COLOR,
    QUIT_BUTTON_COLOR, QUIT_BUTTON_HOVER_COLOR,
)
from resources import screen, bg_image, font, medium_font, small_font


# ──────────────────────────────────────────────────────────────────────────────
# Menu chính
# ──────────────────────────────────────────────────────────────────────────────

def draw_menu(mouse_pos, btn_minimax, btn_alphabeta, btn_2p):
    """Vẽ giao diện hiển thị Menu chính."""
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill(BG_COLOR)

    title = font.render("CARO AI - CHỌN CHẾ ĐỘ", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 4))

    c1 = BUTTON_HOVER_COLOR if btn_minimax.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, c1, btn_minimax, border_radius=15)
    t1 = small_font.render("Đấu với Minimax", True, WHITE)
    screen.blit(t1, (btn_minimax.centerx - t1.get_width() // 2, btn_minimax.centery - t1.get_height() // 2))

    c2 = BUTTON_HOVER_COLOR if btn_alphabeta.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, c2, btn_alphabeta, border_radius=15)
    t2 = small_font.render("Đấu với Alpha-Beta", True, WHITE)
    screen.blit(t2, (btn_alphabeta.centerx - t2.get_width() // 2, btn_alphabeta.centery - t2.get_height() // 2))

    c3 = BUTTON_HOVER_COLOR if btn_2p.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, c3, btn_2p, border_radius=15)
    t3 = small_font.render("2 Người chơi", True, WHITE)
    screen.blit(t3, (btn_2p.centerx - t3.get_width() // 2, btn_2p.centery - t3.get_height() // 2))


# ──────────────────────────────────────────────────────────────────────────────
# Menu chọn độ khó
# ──────────────────────────────────────────────────────────────────────────────

def draw_difficulty_menu(mouse_pos, btn_easy, btn_med, btn_hard, btn_back):
    """Vẽ giao diện hiển thị bảng chọn độ khó cho AI."""
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill(BG_COLOR)

    title = font.render("CHỌN ĐỘ KHÓ", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 4 - 30))

    c1 = BUTTON_HOVER_COLOR if btn_easy.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, c1, btn_easy, border_radius=15)
    t1 = small_font.render("Dễ (Mức 2)", True, WHITE)
    screen.blit(t1, (btn_easy.centerx - t1.get_width() // 2, btn_easy.centery - t1.get_height() // 2))

    c2 = BUTTON_HOVER_COLOR if btn_med.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, c2, btn_med, border_radius=15)
    t2 = small_font.render("Trung Bình (Mức 3)", True, WHITE)
    screen.blit(t2, (btn_med.centerx - t2.get_width() // 2, btn_med.centery - t2.get_height() // 2))

    c3 = BUTTON_HOVER_COLOR if btn_hard.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, c3, btn_hard, border_radius=15)
    t3 = small_font.render("Khó (Mức 4)", True, WHITE)
    screen.blit(t3, (btn_hard.centerx - t3.get_width() // 2, btn_hard.centery - t3.get_height() // 2))

    c4 = QUIT_BUTTON_HOVER_COLOR if btn_back.collidepoint(mouse_pos) else QUIT_BUTTON_COLOR
    pygame.draw.rect(screen, c4, btn_back, border_radius=15)
    t4 = small_font.render("Quay lại", True, WHITE)
    screen.blit(t4, (btn_back.centerx - t4.get_width() // 2, btn_back.centery - t4.get_height() // 2))


# ──────────────────────────────────────────────────────────────────────────────
# Bàn cờ
# ──────────────────────────────────────────────────────────────────────────────

def draw_board(game):
    """Vẽ nền, lưới bàn cờ và các quân cờ hiện tại."""
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill(BG_COLOR)

    pygame.draw.rect(screen, BOARD_BG,  (BOARD_X, BOARD_Y, BOARD_SIZE, BOARD_SIZE))
    pygame.draw.rect(screen, BLACK,     (BOARD_X, BOARD_Y, BOARD_SIZE, BOARD_SIZE), 3)

    # Tô nền cho 2 nước đi gần nhất
    for i in [-1, -2]:
        if len(game.history) >= abs(i):
            last_r, last_c = game.history[i]
            last_x = BOARD_X + last_c * CELL_SIZE
            last_y = BOARD_Y + last_r * CELL_SIZE
            color  = (255, 235, 100) if i == -1 else (255, 245, 180)
            pygame.draw.rect(screen, color, (last_x, last_y, CELL_SIZE, CELL_SIZE))

    # Lưới
    for x in range(0, BOARD_SIZE + 1, CELL_SIZE):
        pygame.draw.line(screen, LINE_COLOR,
                         (BOARD_X + x, BOARD_Y),
                         (BOARD_X + x, BOARD_Y + BOARD_SIZE), 2)
    for y in range(0, BOARD_SIZE + 1, CELL_SIZE):
        pygame.draw.line(screen, LINE_COLOR,
                         (BOARD_X, BOARD_Y + y),
                         (BOARD_X + BOARD_SIZE, BOARD_Y + y), 2)

    # Quân cờ
    for r in range(SIZE):
        for c in range(SIZE):
            if game.board[r][c] == 'X':
                cx = BOARD_X + c * CELL_SIZE + CELL_SIZE // 2
                cy = BOARD_Y + r * CELL_SIZE + CELL_SIZE // 2
                offset = 15
                pygame.draw.line(screen, X_COLOR,
                                 (cx - offset, cy - offset), (cx + offset, cy + offset), 4)
                pygame.draw.line(screen, X_COLOR,
                                 (cx + offset, cy - offset), (cx - offset, cy + offset), 4)
            elif game.board[r][c] == 'O':
                cx = BOARD_X + c * CELL_SIZE + CELL_SIZE // 2
                cy = BOARD_Y + r * CELL_SIZE + CELL_SIZE // 2
                pygame.draw.circle(screen, O_COLOR, (cx, cy), 15, 4)

    # Đường kẻ chiến thắng
    if getattr(game, 'winning_line', None):
        (r1, c1), (r2, c2) = game.winning_line
        start_x = BOARD_X + c1 * CELL_SIZE + CELL_SIZE // 2
        start_y = BOARD_Y + r1 * CELL_SIZE + CELL_SIZE // 2
        end_x   = BOARD_X + c2 * CELL_SIZE + CELL_SIZE // 2
        end_y   = BOARD_Y + r2 * CELL_SIZE + CELL_SIZE // 2

        dr     = int((r2 - r1) / 3)
        dc     = int((c2 - c1) / 3)
        extend = 20
        start_x -= dc * extend
        start_y -= dr * extend
        end_x   += dc * extend
        end_y   += dr * extend

        pygame.draw.line(screen, (46, 204, 113), (start_x, start_y), (end_x, end_y), 5)


# ──────────────────────────────────────────────────────────────────────────────
# Thanh trạng thái & nút phụ
# ──────────────────────────────────────────────────────────────────────────────

def draw_status(game, btn_undo, btn_menu, mouse_pos):
    """Vẽ thanh thông báo trạng thái và các nút chức năng phụ."""
    status_text = ""
    if not game.game_over:
        if game.current_player == 'X':
            status_text = "Lượt của X"
        else:
            status_text = "Máy (O) đang nghĩ..." if game.game_mode == 1 else "Lượt của O"

    if status_text:
        text_surf = small_font.render(status_text, True, BLACK)
        status_y  = BOARD_Y + BOARD_SIZE + 15
        text_bg   = pygame.Surface((text_surf.get_width() + 30, text_surf.get_height() + 10))
        text_bg.fill((255, 255, 255))
        text_bg.set_alpha(180)
        screen.blit(text_bg,   (SCREEN_WIDTH // 2 - text_bg.get_width()   // 2, status_y - 5))
        screen.blit(text_surf, (SCREEN_WIDTH // 2 - text_surf.get_width() // 2, status_y))

    if (not game.game_over
            and len(game.history) > 0
            and game.undo_count < 2
            and not getattr(game, 'just_undid', False)):
        color3    = BUTTON_HOVER_COLOR if btn_undo.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color3, btn_undo, border_radius=15)
        btn3_text = small_font.render(f"Đi lại ({2 - game.undo_count})", True, WHITE)
        screen.blit(btn3_text, (btn_undo.centerx - btn3_text.get_width() // 2,
                                btn_undo.centery - btn3_text.get_height() // 2))

    color2   = QUIT_BUTTON_HOVER_COLOR if btn_menu.collidepoint(mouse_pos) else QUIT_BUTTON_COLOR
    pygame.draw.rect(screen, color2, btn_menu, border_radius=15)
    btn2_text = small_font.render("Thoát", True, WHITE)
    screen.blit(btn2_text, (btn_menu.centerx - btn2_text.get_width() // 2,
                            btn_menu.centery - btn2_text.get_height() // 2))


# ──────────────────────────────────────────────────────────────────────────────
# Popup kết quả
# ──────────────────────────────────────────────────────────────────────────────

def draw_game_over_popup(game, mouse_pos, btn_replay, btn_menu):
    """Vẽ bảng thông báo kết quả sau khi ván đấu kết thúc."""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.fill(BLACK)
    overlay.set_alpha(150)
    screen.blit(overlay, (0, 0))

    box_w, box_h = 400, 200
    box_rect = pygame.Rect(SCREEN_WIDTH // 2 - box_w // 2, SCREEN_HEIGHT // 2 - box_h // 2, box_w, box_h)
    pygame.draw.rect(screen, BG_COLOR,   box_rect, border_radius=15)
    pygame.draw.rect(screen, LINE_COLOR, box_rect, width=3, border_radius=15)

    if game.winner == 'X':
        status_text = "BẠN ĐÃ THẮNG!" if game.game_mode == 1 else "Người chơi X Thắng!"
    elif game.winner == 'O':
        status_text = "BẠN ĐÃ THUA!"  if game.game_mode == 1 else "Người chơi O Thắng!"
    else:
        status_text = "HÒA NHAU!"

    text = medium_font.render(status_text, True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))

    c_yes = BUTTON_HOVER_COLOR if btn_replay.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, c_yes, btn_replay, border_radius=10)
    t_yes = small_font.render("Chơi lại", True, WHITE)
    screen.blit(t_yes, (btn_replay.centerx - t_yes.get_width() // 2,
                        btn_replay.centery - t_yes.get_height() // 2))

    c_no = QUIT_BUTTON_HOVER_COLOR if btn_menu.collidepoint(mouse_pos) else QUIT_BUTTON_COLOR
    pygame.draw.rect(screen, c_no, btn_menu, border_radius=10)
    t_no = small_font.render("Về Menu", True, WHITE)
    screen.blit(t_no, (btn_menu.centerx - t_no.get_width() // 2,
                       btn_menu.centery - t_no.get_height() // 2))


# ──────────────────────────────────────────────────────────────────────────────
# Popup xác nhận thoát
# ──────────────────────────────────────────────────────────────────────────────

def draw_confirm_quit(mouse_pos, btn_yes, btn_no):
    """Vẽ bảng xác nhận khi người chơi nhấn nút thoát."""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.fill(BLACK)
    overlay.set_alpha(150)
    screen.blit(overlay, (0, 0))

    box_w, box_h = 400, 200
    box_rect = pygame.Rect(SCREEN_WIDTH // 2 - box_w // 2, SCREEN_HEIGHT // 2 - box_h // 2, box_w, box_h)
    pygame.draw.rect(screen, BG_COLOR,   box_rect, border_radius=15)
    pygame.draw.rect(screen, LINE_COLOR, box_rect, width=3, border_radius=15)

    text = medium_font.render("Bạn có chắc chắn muốn thoát?", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))

    c_yes = QUIT_BUTTON_HOVER_COLOR if btn_yes.collidepoint(mouse_pos) else QUIT_BUTTON_COLOR
    pygame.draw.rect(screen, c_yes, btn_yes, border_radius=10)
    t_yes = small_font.render("Xác nhận", True, WHITE)
    screen.blit(t_yes, (btn_yes.centerx - t_yes.get_width() // 2,
                        btn_yes.centery - t_yes.get_height() // 2))

    c_no = BUTTON_HOVER_COLOR if btn_no.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, c_no, btn_no, border_radius=10)
    t_no = small_font.render("Hủy bỏ", True, WHITE)
    screen.blit(t_no, (btn_no.centerx - t_no.get_width() // 2,
                       btn_no.centery - t_no.get_height() // 2))
