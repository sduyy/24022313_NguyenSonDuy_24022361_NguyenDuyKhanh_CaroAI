import pygame
import random
import sys
import os

# Hằng số kích thước
SIZE = 9
CELL_SIZE = 50
BOARD_SIZE = SIZE * CELL_SIZE
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 650

# Căn giữa bàn cờ
BOARD_X = (SCREEN_WIDTH - BOARD_SIZE) // 2
BOARD_Y = (SCREEN_HEIGHT - BOARD_SIZE) // 2 - 30

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_COLOR = (50, 50, 50)
X_COLOR = (200, 50, 50)
O_COLOR = (50, 50, 200)
BG_COLOR = (240, 240, 240)
BOARD_BG = (222, 184, 135) # Màu nền gỗ cho khu vực bàn cờ
BUTTON_COLOR = (139, 69, 19) # Màu gỗ sồi sẫm
BUTTON_HOVER_COLOR = (160, 82, 45) # Màu gỗ sồi sáng hơn
QUIT_BUTTON_COLOR = (178, 34, 34) # Đỏ bã trầu (tone trầm)
QUIT_BUTTON_HOVER_COLOR = (205, 92, 92) # Đỏ sáng

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Caro AI - 9x9")

# Font chữ (sử dụng font hệ thống hỗ trợ tiếng Việt)
try:
    font = pygame.font.SysFont('timesnewroman', 40, True)
    medium_font = pygame.font.SysFont('timesnewroman', 28, True)

    small_font = pygame.font.SysFont('timesnewroman', 24, True)
except Exception:
    font = pygame.font.Font(None, 40)
    medium_font = pygame.font.Font(None, 32)
    small_font = pygame.font.Font(None, 24)

# Tải hình nền tự động
bg_image = None
for ext in ["jpg", "png", "jpeg"]:
    for path_dir in [os.path.dirname(__file__), os.getcwd()]:
        full_path = os.path.join(path_dir, f"background.{ext}")
        if os.path.exists(full_path):
            try:
                img = pygame.image.load(full_path)
                bg_image = pygame.transform.smoothscale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
                break
            except Exception:
                pass
    if bg_image:
        break

class CaroGame:
    def __init__(self):
        self.board = []
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.game_mode = 1 # 1: Người vs Máy, 2: Người vs Người
        self.state = 'MENU' # Trạng thái hiện tại: 'MENU' hoặc 'PLAYING'
        self.history = []
        self.undo_count = 0
        self.just_undid = False
        self.reset_game()

    def reset_game(self):
        self.board = [['.' for _ in range(SIZE)] for _ in range(SIZE)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.history = []
        self.undo_count = 0
        self.just_undid = False

    def make_move(self, r, c, player):
        if 0 <= r < SIZE and 0 <= c < SIZE and self.board[r][c] == '.':
            self.board[r][c] = player
            self.history.append((r, c)) # Lưu lại nước đi vào lịch sử
            self.just_undid = False # Xóa cờ khóa undo khi có nước đi mới
            return True
        return False

    def undo(self):
        """Hàm xử lý lùi bước (hoãn cờ)"""
        if not self.history or self.undo_count >= 2 or getattr(self, 'just_undid', False):
            return False
            
        pops = 1
        if self.game_mode == 1:
            # Nếu người thắng, hoặc chỉ mới có 1 nước đi, ta chỉ lùi 1 bước.
            # Nếu không, phải lùi 2 bước (xóa cả nước của máy và của người để đến lượt người)
            if self.winner == 'X' or len(self.history) == 1:
                pops = 1
            else:
                pops = 2
                
        for _ in range(pops):
            if self.history:
                r, c = self.history.pop()
                self.current_player = self.board[r][c] # Trả lại lượt cho người vừa đi
                self.board[r][c] = '.'
            
        self.game_over = False
        self.winner = None
        self.undo_count += 1
        self.just_undid = True
        return True

    def check_win(self, player):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for r in range(SIZE):
            for c in range(SIZE):
                if self.board[r][c] == player:
                    for dr, dc in directions:
                        count = 1
                        for step in range(1, 4):
                            nr, nc = r + dr * step, c + dc * step
                            if 0 <= nr < SIZE and 0 <= nc < SIZE and self.board[nr][nc] == player:
                                count += 1
                            else:
                                break
                        if count == 4:
                            return True
        return False

    def is_board_full(self):
        for r in range(SIZE):
            for c in range(SIZE):
                if self.board[r][c] == '.':
                    return False
        return True

    def bot_move(self):
        empty_cells = [(r, c) for r in range(SIZE) for c in range(SIZE) if self.board[r][c] == '.']
        if empty_cells:
            return random.choice(empty_cells)
        return None

def draw_menu(mouse_pos, btn_1p, btn_2p):
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill(BG_COLOR)
        
    title = font.render("CHỌN CHẾ ĐỘ CHƠI", True, BLACK)
    
    # Hiển thị trực tiếp tiêu đề, không cần nền trắng
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 3))
    
    # Nút 1 Người (vs Máy)
    c1 = BUTTON_HOVER_COLOR if btn_1p.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, c1, btn_1p, border_radius=15)
    t1 = small_font.render("1 Người (vs Máy)", True, WHITE)
    screen.blit(t1, (btn_1p.centerx - t1.get_width() // 2, btn_1p.centery - t1.get_height() // 2))
    
    # Nút 2 Người
    c2 = BUTTON_HOVER_COLOR if btn_2p.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, c2, btn_2p, border_radius=15)
    t2 = small_font.render("2 Người", True, WHITE)
    screen.blit(t2, (btn_2p.centerx - t2.get_width() // 2, btn_2p.centery - t2.get_height() // 2))

def draw_board(game):
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill(BG_COLOR)
    
    # Vẽ nền bàn cờ (màu gỗ) để đè lên hình nền nếu có (tạo hiệu ứng bàn cờ thật)
    pygame.draw.rect(screen, BOARD_BG, (BOARD_X, BOARD_Y, BOARD_SIZE, BOARD_SIZE))
    # Viền bàn cờ
    pygame.draw.rect(screen, BLACK, (BOARD_X, BOARD_Y, BOARD_SIZE, BOARD_SIZE), 3)

    # Vẽ lưới
    for x in range(0, BOARD_SIZE + 1, CELL_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (BOARD_X + x, BOARD_Y), (BOARD_X + x, BOARD_Y + BOARD_SIZE), 2)
    for y in range(0, BOARD_SIZE + 1, CELL_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (BOARD_X, BOARD_Y + y), (BOARD_X + BOARD_SIZE, BOARD_Y + y), 2)
        
    # Vẽ quân X và O
    for r in range(SIZE):
        for c in range(SIZE):
            if game.board[r][c] == 'X':
                # Vẽ X
                center_x = BOARD_X + c * CELL_SIZE + CELL_SIZE // 2
                center_y = BOARD_Y + r * CELL_SIZE + CELL_SIZE // 2
                offset = 15
                pygame.draw.line(screen, X_COLOR, (center_x - offset, center_y - offset), (center_x + offset, center_y + offset), 4)
                pygame.draw.line(screen, X_COLOR, (center_x + offset, center_y - offset), (center_x - offset, center_y + offset), 4)
            elif game.board[r][c] == 'O':
                # Vẽ O
                center_x = BOARD_X + c * CELL_SIZE + CELL_SIZE // 2
                center_y = BOARD_Y + r * CELL_SIZE + CELL_SIZE // 2
                pygame.draw.circle(screen, O_COLOR, (center_x, center_y), 15, 4)

def draw_status(game, btn_replay, btn_undo, btn_menu, mouse_pos):
    # Vẽ thông báo trạng thái
    status_text = ""
    if game.game_over:
        if game.winner == 'X':
            status_text = "Người chơi X Thắng!"
        elif game.winner == 'O':
            if game.game_mode == 1:
                status_text = "Máy (O) Thắng!"
            else:
                status_text = "Người chơi O Thắng!"
        else:
            status_text = "Hòa!"
    else:
        if game.current_player == 'X':
            status_text = "Lượt của X"
        else:
            if game.game_mode == 1:
                status_text = "Máy (O) đang nghĩ..."
            else:
                status_text = "Lượt của O"
            
    text_surf = small_font.render(status_text, True, BLACK)
    
    # Tạo nền mờ cho text trạng thái dễ đọc
    status_y = BOARD_Y + BOARD_SIZE + 15
    text_bg = pygame.Surface((text_surf.get_width() + 30, text_surf.get_height() + 10))
    text_bg.fill((255, 255, 255))
    text_bg.set_alpha(180)
    screen.blit(text_bg, (SCREEN_WIDTH // 2 - text_bg.get_width() // 2, status_y - 5))
    screen.blit(text_surf, (SCREEN_WIDTH // 2 - text_surf.get_width() // 2, status_y))
    
    # Nút Undo hiện khi có lịch sử nước đi và còn lượt Undo, đồng thời chưa bị khóa (không undo 2 lần liên tiếp)
    if len(game.history) > 0 and game.undo_count < 2 and not getattr(game, 'just_undid', False):
        color3 = BUTTON_HOVER_COLOR if btn_undo.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color3, btn_undo, border_radius=15)
        btn3_text = small_font.render(f"Đi lại ({2 - game.undo_count})", True, WHITE)
        screen.blit(btn3_text, (btn_undo.centerx - btn3_text.get_width() // 2, btn_undo.centery - btn3_text.get_height() // 2))

    # Nút Thoát (Menu) luôn hiển thị để có thể thoát ván ngang chừng
    color2 = QUIT_BUTTON_HOVER_COLOR if btn_menu.collidepoint(mouse_pos) else QUIT_BUTTON_COLOR
    pygame.draw.rect(screen, color2, btn_menu, border_radius=15)
    btn2_text = small_font.render("Thoát", True, WHITE)
    screen.blit(btn2_text, (btn_menu.centerx - btn2_text.get_width() // 2, btn_menu.centery - btn2_text.get_height() // 2))

    # Nút Chơi Lại chỉ hiện khi game kết thúc
    if game.game_over:
        color1 = BUTTON_HOVER_COLOR if btn_replay.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color1, btn_replay, border_radius=15)
        btn_text = small_font.render("Chơi Lại", True, WHITE)
        screen.blit(btn_text, (btn_replay.centerx - btn_text.get_width() // 2, btn_replay.centery - btn_text.get_height() // 2))

def draw_confirm_quit(mouse_pos, btn_yes, btn_no):
    # Lớp phủ mờ
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.fill(BLACK)
    overlay.set_alpha(150)
    screen.blit(overlay, (0, 0))
    
    # Hộp thoại
    box_w, box_h = 400, 200
    box_rect = pygame.Rect(SCREEN_WIDTH // 2 - box_w // 2, SCREEN_HEIGHT // 2 - box_h // 2, box_w, box_h)
    pygame.draw.rect(screen, BG_COLOR, box_rect, border_radius=15)
    pygame.draw.rect(screen, LINE_COLOR, box_rect, width=3, border_radius=15)
    
    text = medium_font.render("Bạn có chắc chắn muốn thoát?", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
    
    # Nút Xác nhận
    c_yes = QUIT_BUTTON_HOVER_COLOR if btn_yes.collidepoint(mouse_pos) else QUIT_BUTTON_COLOR
    pygame.draw.rect(screen, c_yes, btn_yes, border_radius=10)
    t_yes = small_font.render("Xác nhận", True, WHITE)
    screen.blit(t_yes, (btn_yes.centerx - t_yes.get_width() // 2, btn_yes.centery - t_yes.get_height() // 2))
    
    # Nút Hủy
    c_no = BUTTON_HOVER_COLOR if btn_no.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, c_no, btn_no, border_radius=10)
    t_no = small_font.render("Hủy bỏ", True, WHITE)
    screen.blit(t_no, (btn_no.centerx - t_no.get_width() // 2, btn_no.centery - t_no.get_height() // 2))

def main():
    game = CaroGame()
    clock = pygame.time.Clock()
    
    # Kích thước và vị trí nút bấm MENU
    btn_1p = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50)
    btn_2p = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 70, 200, 50)
    
    # Kích thước và vị trí nút bấm CHƠI LẠI, UNDO, MENU
    btn_y = BOARD_Y + BOARD_SIZE + 60
    btn_undo   = pygame.Rect(SCREEN_WIDTH // 2 - 160, btn_y, 100, 40)
    btn_replay = pygame.Rect(SCREEN_WIDTH // 2 - 50, btn_y, 100, 40)
    btn_menu   = pygame.Rect(SCREEN_WIDTH // 2 + 60, btn_y, 100, 40)
    
    # Kích thước nút xác nhận thoát
    btn_yes = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 20, 100, 40)
    btn_no = pygame.Rect(SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 + 20, 100, 40)
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Đang ở Menu
                    if game.state == 'MENU':
                        if btn_1p.collidepoint(event.pos):
                            game.game_mode = 1
                            game.reset_game()
                            game.state = 'PLAYING'
                        elif btn_2p.collidepoint(event.pos):
                            game.game_mode = 2
                            game.reset_game()
                            game.state = 'PLAYING'
                    
                    # Đang chơi game
                    elif game.state == 'PLAYING':
                        # Luôn xử lý nút Thoát (Menu) bất kể game over hay chưa
                        if btn_menu.collidepoint(event.pos):
                            game.state = 'CONFIRM_QUIT'
                        # Ưu tiên xử lý nút Undo
                        elif len(game.history) > 0 and game.undo_count < 2 and not getattr(game, 'just_undid', False) and btn_undo.collidepoint(event.pos):
                            game.undo()
                        # Xử lý nút chơi lại khi Game Over
                        elif game.game_over:
                            if btn_replay.collidepoint(event.pos):
                                game.reset_game()
                        else:
                            # Nếu chế độ 2 Người, hoặc (chế độ 1 Người và đang là lượt của X)
                            if game.game_mode == 2 or (game.game_mode == 1 and game.current_player == 'X'):
                                x, y = event.pos
                                # Kiểm tra xem click có nằm trong bàn cờ không
                                if BOARD_X <= x < BOARD_X + BOARD_SIZE and BOARD_Y <= y < BOARD_Y + BOARD_SIZE:
                                    c = (x - BOARD_X) // CELL_SIZE
                                    r = (y - BOARD_Y) // CELL_SIZE
                                    if game.make_move(r, c, game.current_player):
                                        if game.check_win(game.current_player):
                                            game.game_over = True
                                            game.winner = game.current_player
                                        elif game.is_board_full():
                                            game.game_over = True
                                            game.winner = 'Draw'
                                        else:
                                            # Đổi lượt
                                            game.current_player = 'O' if game.current_player == 'X' else 'X'
                                            
                    # Đang hiển thị hộp thoại xác nhận thoát
                    elif game.state == 'CONFIRM_QUIT':
                        if btn_yes.collidepoint(event.pos):
                            game.state = 'MENU'
                        elif btn_no.collidepoint(event.pos):
                            game.state = 'PLAYING'
                                            
        if game.state == 'MENU':
            draw_menu(mouse_pos, btn_1p, btn_2p)
        else:
            draw_board(game)
            draw_status(game, btn_replay, btn_undo, btn_menu, mouse_pos)
            
            if game.state == 'CONFIRM_QUIT':
                draw_confirm_quit(mouse_pos, btn_yes, btn_no)
            
            # Lượt của Máy (Bot) chỉ chạy khi đang PLAYING
            if game.game_mode == 1 and not game.game_over and game.current_player == 'O' and game.state == 'PLAYING':
                pygame.display.flip() # Cập nhật màn hình để hiện chữ "Máy đang nghĩ..."
                pygame.time.delay(500) # Đợi 0.5s 
                move = game.bot_move()
                if move:
                    r, c = move
                    game.make_move(r, c, 'O')
                    if game.check_win('O'):
                        game.game_over = True
                        game.winner = 'O'
                    elif game.is_board_full():
                        game.game_over = True
                        game.winner = 'Draw'
                    else:
                        game.current_player = 'X'
                        
        pygame.display.flip()
        clock.tick(30)
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()