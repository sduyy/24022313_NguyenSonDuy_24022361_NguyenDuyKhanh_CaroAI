import pygame
import random
import sys
import os
import math
import time



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
        self.ai_type = 'Minimax' # Mặc định ban đầu
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
    
    # --- Phần AI
    # Hàm đánh giá
    def evaluate_window(self, window):
        """Chấm điểm cho 1 cụm 4 ô liên tiếp"""
        score = 0
        bot = 'O'
        player = 'X'

        bot_count = window.count(bot)
        player_count = window.count(player)
        empty_count = window.count('.')

        # Ưu tiên tấn công (cộng điểm)
        if bot_count == 4:
            score += 100000
        elif bot_count == 3 and empty_count == 1:
            score += 1000
        elif bot_count == 2 and empty_count == 2:
            score += 100
        elif bot_count == 1 and empty_count == 3:
            score += 10

        # Ưu tiên phòng thủ (trừ điểm nếu người chơi có lợi thế)
        if player_count == 4:
            score -= 100000
        elif player_count == 3 and empty_count == 1:
            score -= 1500  # Trừ nặng hơn mức cộng tương ứng để ưu tiên chặn
        elif player_count == 2 and empty_count == 2:
            score -= 150
        elif player_count == 1 and empty_count == 3:
            score -= 15

        return score

    def evaluate_board(self):
        """Quét toàn bộ bàn cờ để tính tổng điểm"""
        total_score = 0
        
        # 1. Chấm điểm theo hàng ngang
        for r in range(SIZE):
            for c in range(SIZE - 3):
                window = [self.board[r][c+i] for i in range(4)]
                total_score += self.evaluate_window(window)

        # 2. Chấm điểm theo hàng dọc
        for c in range(SIZE):
            for r in range(SIZE - 3):
                window = [self.board[r+i][c] for i in range(4)]
                total_score += self.evaluate_window(window)

        # 3. Chấm điểm theo đường chéo chính (\)
        for r in range(SIZE - 3):
            for c in range(SIZE - 3):
                window = [self.board[r+i][c+i] for i in range(4)]
                total_score += self.evaluate_window(window)

        # 4. Chấm điểm theo đường chéo phụ (/)
        for r in range(SIZE - 3):
            for c in range(SIZE):
                if c - 3 >= 0:
                    window = [self.board[r+i][c-i] for i in range(4)]
                    total_score += self.evaluate_window(window)

        return total_score
    
    def get_valid_moves(self):
        """Giới hạn không gian tìm kiếm: Chỉ lấy các ô trống nằm lân cận quân cờ đã có"""
        moves = []
        has_piece = False
        
        # Kiểm tra xem bàn cờ đã có quân nào chưa
        for r in range(SIZE):
            for c in range(SIZE):
                if self.board[r][c] != '.':
                    has_piece = True
                    break
            if has_piece: break
            
        # Nếu bàn cờ trống (nước đi đầu tiên), AI đánh thẳng vào giữa bàn cờ
        if not has_piece:
            return [(SIZE // 2, SIZE // 2)]
            
        # Nếu đã có quân, chỉ quét các ô kề (bán kính 1 ô)
        for r in range(SIZE):
            for c in range(SIZE):
                if self.board[r][c] == '.':
                    adjacent = False
                    # Quét 8 ô xung quanh
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < SIZE and 0 <= nc < SIZE and self.board[nr][nc] != '.':
                                adjacent = True
                                break
                        if adjacent:
                            break
                    if adjacent:
                        moves.append((r, c))
        return moves

    # Minimax
    def minimax(self, depth, is_maximizing):
        self.nodes_visited += 1 # Tăng biến đếm số trạng thái đã xét

        # 1. Kiểm tra trạng thái kết thúc (Base cases)
        if self.check_win('O'):
            return 10000000, None  # Trọng số vô cực cho trạng thái thắng
        if self.check_win('X'):
            return -10000000, None # Trọng số âm vô cực cho trạng thái thua
        if self.is_board_full():
            return 0, None         # Hòa

        # 2. Kiểm tra giới hạn độ sâu
        if depth == 0:
            return self.evaluate_board(), None

        valid_moves = self.get_valid_moves()
        best_move = None

        # 3. Lượt của Máy (Player 'O' - MAX)
        if is_maximizing:
            max_eval = -math.inf
            for (r, c) in valid_moves:
                self.board[r][c] = 'O' # Đánh thử
                eval_score, _ = self.minimax(depth - 1, False)
                self.board[r][c] = '.' # Hoàn tác
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = (r, c)
            return max_eval, best_move
            
        # 4. Lượt của Người (Player 'X' - MIN)
        else:
            min_eval = math.inf
            for (r, c) in valid_moves:
                self.board[r][c] = 'X' # Đánh thử
                eval_score, _ = self.minimax(depth - 1, True)
                self.board[r][c] = '.' # Hoàn tác
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = (r, c)
            return min_eval, best_move
        
    # Alpha-Beta    
    def alphabeta(self, depth, alpha, beta, is_maximizing):
        self.nodes_visited += 1

        # 1. Base cases (Giống hệt Minimax)
        if self.check_win('O'):
            return 10000000, None
        if self.check_win('X'):
            return -10000000, None
        if self.is_board_full():
            return 0, None
        if depth == 0:
            return self.evaluate_board(), None

        valid_moves = self.get_valid_moves()
        best_move = None

        # 2. Lượt của Máy (Player 'O' - MAX)
        if is_maximizing:
            max_eval = -math.inf
            for (r, c) in valid_moves:
                self.board[r][c] = 'O'
                eval_score, _ = self.alphabeta(depth - 1, alpha, beta, False)
                self.board[r][c] = '.'
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = (r, c)
                
                # Cập nhật alpha là giá trị tốt nhất hiện tại của MAX [cite: 105]
                alpha = max(alpha, eval_score)
                # Cắt nhánh nếu beta <= alpha [cite: 107]
                if beta <= alpha:
                    break 
            return max_eval, best_move
            
        # 3. Lượt của Người (Player 'X' - MIN)
        else:
            min_eval = math.inf
            for (r, c) in valid_moves:
                self.board[r][c] = 'X'
                eval_score, _ = self.alphabeta(depth - 1, alpha, beta, True)
                self.board[r][c] = '.'
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = (r, c)
                
                # Cập nhật beta là giá trị tốt nhất hiện tại của MIN [cite: 106]
                beta = min(beta, eval_score)
                # Cắt nhánh nếu beta <= alpha [cite: 107]
                if beta <= alpha:
                    break 
            return min_eval, best_move

    def bot_move(self):
        """Hàm chọn thuật toán dựa trên cấu hình người dùng chọn"""
        DEPTH = 3 # Bạn có thể để Depth 3 để thấy sự khác biệt tốc độ
        self.nodes_visited = 0
        start_time = time.time()
        
        if self.ai_type == 'Alpha-Beta':
            print(f"\n--- AI ĐANG CHẠY: ALPHA-BETA (Depth {DEPTH}) ---")
            best_score, move = self.alphabeta(DEPTH, -math.inf, math.inf, True)
        else:
            print(f"\n--- AI ĐANG CHẠY: MINIMAX (Depth {DEPTH}) ---")
            best_score, move = self.minimax(DEPTH, True)
            
        elapsed_time = time.time() - start_time
        print(f"Nước đi chọn: {move}")
        print(f"Số trạng thái đã duyệt: {self.nodes_visited}")
        print(f"Thời gian thực thi: {elapsed_time:.4f}s")
        
        return move



def draw_menu(mouse_pos, btn_minimax, btn_alphabeta, btn_2p):
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill(BG_COLOR)
        
    title = font.render("CARO AI - CHỌN CHẾ ĐỘ", True, BLACK)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 4))
    
    # Nút AI Minimax
    c1 = BUTTON_HOVER_COLOR if btn_minimax.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, c1, btn_minimax, border_radius=15)
    t1 = small_font.render("Đấu với Minimax", True, WHITE)
    screen.blit(t1, (btn_minimax.centerx - t1.get_width() // 2, btn_minimax.centery - t1.get_height() // 2))
    
    # Nút AI Alpha-Beta
    c2 = BUTTON_HOVER_COLOR if btn_alphabeta.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, c2, btn_alphabeta, border_radius=15)
    t2 = small_font.render("Đấu với Alpha-Beta", True, WHITE)
    screen.blit(t2, (btn_alphabeta.centerx - t2.get_width() // 2, btn_alphabeta.centery - t2.get_height() // 2))
    
    # Nút 2 Người
    c3 = BUTTON_HOVER_COLOR if btn_2p.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, c3, btn_2p, border_radius=15)
    t3 = small_font.render("2 Người chơi", True, WHITE)
    screen.blit(t3, (btn_2p.centerx - t3.get_width() // 2, btn_2p.centery - t3.get_height() // 2))



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

    # Kích thước và vị trí nút bấm CHƠI LẠI, UNDO, MENU
    btn_y = BOARD_Y + BOARD_SIZE + 60
    btn_undo   = pygame.Rect(SCREEN_WIDTH // 2 - 160, btn_y, 100, 40)
    btn_replay = pygame.Rect(SCREEN_WIDTH // 2 - 50, btn_y, 100, 40)
    btn_menu   = pygame.Rect(SCREEN_WIDTH // 2 + 60, btn_y, 100, 40)
    
    # Kích thước nút xác nhận thoát
    btn_yes = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 20, 100, 40)
    btn_no = pygame.Rect(SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 + 20, 100, 40)

    # Nút chọn chế độ chơi
    btn_minimax = pygame.Rect(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 - 40, 250, 50)
    btn_alphabeta = pygame.Rect(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 + 30, 250, 50)
    btn_2p = pygame.Rect(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 + 100, 250, 50)
    
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
                        if btn_minimax.collidepoint(event.pos):
                            game.game_mode = 1
                            game.ai_type = 'Minimax'
                            game.reset_game()
                            game.state = 'PLAYING'
                        elif btn_alphabeta.collidepoint(event.pos):
                            game.game_mode = 1
                            game.ai_type = 'Alpha-Beta'
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
            draw_menu(mouse_pos, btn_minimax, btn_alphabeta, btn_2p)
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
