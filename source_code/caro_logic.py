import pygame
import random
import sys
import os
import math
import time

SIZE = 9
CELL_SIZE = 50
BOARD_SIZE = SIZE * CELL_SIZE
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 650

BOARD_X = (SCREEN_WIDTH - BOARD_SIZE) // 2
BOARD_Y = (SCREEN_HEIGHT - BOARD_SIZE) // 2 - 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_COLOR = (50, 50, 50)
X_COLOR = (200, 50, 50)
O_COLOR = (50, 50, 200)
BG_COLOR = (240, 240, 240)
BOARD_BG = (222, 184, 135)
BUTTON_COLOR = (139, 69, 19)
BUTTON_HOVER_COLOR = (160, 82, 45)
QUIT_BUTTON_COLOR = (178, 34, 34)
QUIT_BUTTON_HOVER_COLOR = (205, 92, 92)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Caro AI - 9x9")

try:
    font = pygame.font.SysFont('timesnewroman', 40, True)
    medium_font = pygame.font.SysFont('timesnewroman', 28, True)
    small_font = pygame.font.SysFont('timesnewroman', 24, True)
except Exception:
    font = pygame.font.Font(None, 40)
    medium_font = pygame.font.Font(None, 32)
    small_font = pygame.font.Font(None, 24)

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
    """Lớp quản lý trạng thái và logic trò chơi Caro."""
    
    def __init__(self):
        """Khởi tạo cấu hình và trạng thái mặc định của ván cờ."""
        self.board = []
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.game_mode = 1
        self.state = 'MENU'
        self.history = []
        self.undo_count = 0
        self.just_undid = False
        self.ai_type = 'Minimax'
        self.ai_depth = 3
        self.reset_game()

    def reset_game(self):
        """Làm sạch bàn cờ và thiết lập lại các biến vòng lặp."""
        self.board = [['.' for _ in range(SIZE)] for _ in range(SIZE)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.history = []
        self.undo_count = 0
        self.just_undid = False
        self.winning_line = None
        self.game_over_time = 0
        self.current_board_score = 0  # Điểm số cộng dồn của toàn bộ bàn cờ
        self.nodes_visited = 0        # Số trạng thái AI đã duyệt qua

    def make_move(self, r, c, player):
        """Kiểm tra và thực hiện đánh quân cờ vào tọa độ (r, c)."""
        if 0 <= r < SIZE and 0 <= c < SIZE and self.board[r][c] == '.':
            # Cập nhật điểm số cộng dồn trước khi đặt quân
            old_local = self.get_local_score(r, c)
            self.board[r][c] = player
            new_local = self.get_local_score(r, c)
            self.current_board_score += (new_local - old_local)
            
            self.history.append((r, c))
            self.just_undid = False
            return True
        return False

    def undo(self):
        """Xử lý logic lùi bước (hoãn cờ) dựa trên chế độ chơi."""
        if not self.history or self.undo_count >= 2 or getattr(self, 'just_undid', False):
            return False
            
        pops = 1
        if self.game_mode == 1:
            if self.winner == 'X' or len(self.history) == 1:
                pops = 1
            else:
                pops = 2
                
        for _ in range(pops):
            if self.history:
                r, c = self.history.pop()
                self.current_player = self.board[r][c]
                
                # Cập nhật điểm số cộng dồn khi hoàn tác
                old_local = self.get_local_score(r, c)
                self.board[r][c] = '.'
                new_local = self.get_local_score(r, c)
                self.current_board_score += (new_local - old_local)
            
        self.game_over = False
        self.winner = None
        self.undo_count += 1
        self.just_undid = True
        return True

    def check_win(self, r, c, player):
        """Kiểm tra nhanh điều kiện thắng tại vị trí vừa đánh (r, c)."""
        if r is None or c is None:
            return False
            
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            # Kiểm tra hướng dương
            for step in range(1, 4):
                nr, nc = r + dr * step, c + dc * step
                if 0 <= nr < SIZE and 0 <= nc < SIZE and self.board[nr][nc] == player:
                    count += 1
                else:
                    break
            # Kiểm tra hướng âm
            for step in range(1, 4):
                nr, nc = r - dr * step, c - dc * step
                if 0 <= nr < SIZE and 0 <= nc < SIZE and self.board[nr][nc] == player:
                    count += 1
                else:
                    break
            
            if count >= 4:
                return True
        return False

    def get_winning_line(self, player):
        """Trả về tọa độ bắt đầu và kết thúc của đường kẻ chiến thắng."""
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
                            return ((r, c), (r + dr * 3, c + dc * 3))
        return None

    def is_board_full(self):
        """Kiểm tra xem toàn bộ các ô trên bàn cờ đã được đánh hết chưa."""
        for r in range(SIZE):
            for c in range(SIZE):
                if self.board[r][c] == '.':
                    return False
        return True
    
    def evaluate_window_optimized(self, window):
        """Chấm điểm heuristic tối ưu cho một dải 4 ô liên tiếp."""
        bot_count = 0
        player_count = 0
        empty_count = 0
        for cell in window:
            if cell == 'O': bot_count += 1
            elif cell == 'X': player_count += 1
            else: empty_count += 1
        
        score = 0
        if bot_count == 4: score += 1000000
        elif bot_count == 3 and empty_count == 1: score += 5000
        elif bot_count == 2 and empty_count == 2: score += 100
        elif bot_count == 1 and empty_count == 3: score += 10

        if player_count == 4: score -= 1000000
        elif player_count == 3 and empty_count == 1: score -= 10000
        elif player_count == 2 and empty_count == 2: score -= 150
        elif player_count == 1 and empty_count == 3: score -= 15
        return score

    def get_local_score(self, r, c):
        """Tính điểm cục bộ xung quanh vị trí (r, c) để tối ưu hóa việc sắp xếp nước đi."""
        local_total = 0
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dr, dc in directions:
            for i in range(4):
                start_r = r - dr * i
                start_c = c - dc * i
                
                window = []
                valid_window = True
                for j in range(4):
                    nr, nc = start_r + dr * j, start_c + dc * j
                    if 0 <= nr < SIZE and 0 <= nc < SIZE:
                        window.append(self.board[nr][nc])
                    else:
                        valid_window = False
                        break
                
                if valid_window:
                    local_total += self.evaluate_window_optimized(window)
        return local_total

    def evaluate_board(self):
        """Tổng hợp điểm của tất cả các dải 4 ô trên bàn cờ."""
        total_score = 0
        
        for r in range(SIZE):
            for c in range(SIZE - 3):
                window = [self.board[r][c+i] for i in range(4)]
                total_score += self.evaluate_window_optimized(window)

        for c in range(SIZE):
            for r in range(SIZE - 3):
                window = [self.board[r+i][c] for i in range(4)]
                total_score += self.evaluate_window_optimized(window)

        for r in range(SIZE - 3):
            for c in range(SIZE - 3):
                window = [self.board[r+i][c+i] for i in range(4)]
                total_score += self.evaluate_window_optimized(window)

        for r in range(SIZE - 3):
            for c in range(SIZE):
                if c - 3 >= 0:
                    window = [self.board[r+i][c-i] for i in range(4)]
                    total_score += self.evaluate_window_optimized(window)

        return total_score
    
    def get_valid_moves(self):
        """Trả về danh sách các ô trống hợp lệ nằm kề với quân cờ đã có."""
        moves = []
        has_piece = False
        
        for r in range(SIZE):
            for c in range(SIZE):
                if self.board[r][c] != '.':
                    has_piece = True
                    break
            if has_piece: break
            
        if not has_piece:
            return [(SIZE // 2, SIZE // 2)]
            
        for r in range(SIZE):
            for c in range(SIZE):
                if self.board[r][c] == '.':
                    adjacent = False
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

    def get_ordered_moves(self, is_maximizing):
        """Sắp xếp danh sách nước đi theo điểm số để tối ưu cắt nhánh."""
        valid_moves = self.get_valid_moves()
        move_scores = []
        
        for r, c in valid_moves:
            player = 'O' if is_maximizing else 'X'
            self.board[r][c] = player
            score = self.get_local_score(r, c)
            self.board[r][c] = '.'
            move_scores.append((score, (r, c)))
            
        if is_maximizing:
            move_scores.sort(key=lambda x: x[0], reverse=True)
        else:
            move_scores.sort(key=lambda x: x[0])
            
        return [move for score, move in move_scores]

    def minimax(self, depth, is_maximizing, last_r=None, last_c=None):
        """Thuật toán Minimax tìm kiếm nước đi tối ưu với điểm số cộng dồn."""
        # Đồng bộ điểm số tại nút gốc (root)
        if self.nodes_visited == 0:
            self.current_board_score = self.evaluate_board()
        self.nodes_visited += 1

        # Kiểm tra thắng thua dựa trên nước đi cuối cùng
        if last_r is not None and last_c is not None:
            opponent = 'X' if is_maximizing else 'O'
            if self.check_win(last_r, last_c, opponent):
                return (10000000 + depth) if opponent == 'O' else (-10000000 - depth), None

        if self.is_board_full():
            return 0, None

        if depth == 0:
            return self.current_board_score, None

        valid_moves = self.get_ordered_moves(is_maximizing)
        best_move = None

        if is_maximizing:
            max_eval = -math.inf
            for (r, c) in valid_moves:
                # Cập nhật điểm số cộng dồn (Incremental Update)
                old_local = self.get_local_score(r, c)
                self.board[r][c] = 'O'
                new_local = self.get_local_score(r, c)
                diff = new_local - old_local
                self.current_board_score += diff
                
                eval_score, _ = self.minimax(depth - 1, False, r, c)
                
                # Hoàn tác (Backtrack)
                self.current_board_score -= diff
                self.board[r][c] = '.'
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = (r, c)
            return max_eval, best_move
            
        else:
            min_eval = math.inf
            for (r, c) in valid_moves:
                # Cập nhật điểm số cộng dồn (Incremental Update)
                old_local = self.get_local_score(r, c)
                self.board[r][c] = 'X'
                new_local = self.get_local_score(r, c)
                diff = new_local - old_local
                self.current_board_score += diff
                
                eval_score, _ = self.minimax(depth - 1, True, r, c)
                
                # Hoàn tác (Backtrack)
                self.current_board_score -= diff
                self.board[r][c] = '.'
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = (r, c)
            return min_eval, best_move
        
    def alphabeta(self, depth, alpha, beta, is_maximizing, last_r=None, last_c=None):
        """Thuật toán Alpha-Beta Pruning với điểm số cộng dồn."""
        # Đồng bộ điểm số tại nút gốc (root)
        if self.nodes_visited == 0:
            self.current_board_score = self.evaluate_board()
        self.nodes_visited += 1

        # Kiểm tra thắng thua dựa trên nước đi cuối cùng
        if last_r is not None and last_c is not None:
            opponent = 'X' if is_maximizing else 'O'
            if self.check_win(last_r, last_c, opponent):
                return (10000000 + depth) if opponent == 'O' else (-10000000 - depth), None

        if self.is_board_full():
            return 0, None
        if depth == 0:
            return self.current_board_score, None

        valid_moves = self.get_ordered_moves(is_maximizing)
        best_move = None

        if is_maximizing:
            max_eval = -math.inf
            for (r, c) in valid_moves:
                # Cập nhật điểm số cộng dồn (Incremental Update)
                old_local = self.get_local_score(r, c)
                self.board[r][c] = 'O'
                new_local = self.get_local_score(r, c)
                diff = new_local - old_local
                self.current_board_score += diff
                
                eval_score, _ = self.alphabeta(depth - 1, alpha, beta, False, r, c)
                
                # Hoàn tác (Backtrack)
                self.current_board_score -= diff
                self.board[r][c] = '.'
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = (r, c)
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break 
            return max_eval, best_move
            
        else:
            min_eval = math.inf
            for (r, c) in valid_moves:
                # Cập nhật điểm số cộng dồn (Incremental Update)
                old_local = self.get_local_score(r, c)
                self.board[r][c] = 'X'
                new_local = self.get_local_score(r, c)
                diff = new_local - old_local
                self.current_board_score += diff
                
                eval_score, _ = self.alphabeta(depth - 1, alpha, beta, True, r, c)
                
                # Hoàn tác (Backtrack)
                self.current_board_score -= diff
                self.board[r][c] = '.'
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = (r, c)
                
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break 
            return min_eval, best_move

    def bot_move(self):
        """Kích hoạt bot tính toán và in thời gian thực thi ra console."""
        DEPTH = self.ai_depth
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

def draw_board(game):
    """Vẽ nền, lưới bàn cờ và các quân cờ hiện tại."""
    if bg_image:
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill(BG_COLOR)
    
    pygame.draw.rect(screen, BOARD_BG, (BOARD_X, BOARD_Y, BOARD_SIZE, BOARD_SIZE))
    pygame.draw.rect(screen, BLACK, (BOARD_X, BOARD_Y, BOARD_SIZE, BOARD_SIZE), 3)

    for i in [-1, -2]:
        if len(game.history) >= abs(i):
            last_r, last_c = game.history[i]
            last_x = BOARD_X + last_c * CELL_SIZE
            last_y = BOARD_Y + last_r * CELL_SIZE
            color = (255, 235, 100) if i == -1 else (255, 245, 180)
            pygame.draw.rect(screen, color, (last_x, last_y, CELL_SIZE, CELL_SIZE))

    for x in range(0, BOARD_SIZE + 1, CELL_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (BOARD_X + x, BOARD_Y), (BOARD_X + x, BOARD_Y + BOARD_SIZE), 2)
    for y in range(0, BOARD_SIZE + 1, CELL_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (BOARD_X, BOARD_Y + y), (BOARD_X + BOARD_SIZE, BOARD_Y + y), 2)
        
    for r in range(SIZE):
        for c in range(SIZE):
            if game.board[r][c] == 'X':
                center_x = BOARD_X + c * CELL_SIZE + CELL_SIZE // 2
                center_y = BOARD_Y + r * CELL_SIZE + CELL_SIZE // 2
                offset = 15
                pygame.draw.line(screen, X_COLOR, (center_x - offset, center_y - offset), (center_x + offset, center_y + offset), 4)
                pygame.draw.line(screen, X_COLOR, (center_x + offset, center_y - offset), (center_x - offset, center_y + offset), 4)
            elif game.board[r][c] == 'O':
                center_x = BOARD_X + c * CELL_SIZE + CELL_SIZE // 2
                center_y = BOARD_Y + r * CELL_SIZE + CELL_SIZE // 2
                pygame.draw.circle(screen, O_COLOR, (center_x, center_y), 15, 4)

    if getattr(game, 'winning_line', None):
        (r1, c1), (r2, c2) = game.winning_line
        start_x = BOARD_X + c1 * CELL_SIZE + CELL_SIZE // 2
        start_y = BOARD_Y + r1 * CELL_SIZE + CELL_SIZE // 2
        end_x = BOARD_X + c2 * CELL_SIZE + CELL_SIZE // 2
        end_y = BOARD_Y + r2 * CELL_SIZE + CELL_SIZE // 2
        
        dr = int((r2 - r1) / 3)
        dc = int((c2 - c1) / 3)
        extend = 20
        start_x -= dc * extend
        start_y -= dr * extend
        end_x += dc * extend
        end_y += dr * extend
        
        pygame.draw.line(screen, (46, 204, 113), (start_x, start_y), (end_x, end_y), 5)

def draw_status(game, btn_undo, btn_menu, mouse_pos):
    """Vẽ thanh thông báo trạng thái và các nút chức năng phụ."""
    status_text = ""
    if not game.game_over:
        if game.current_player == 'X':
            status_text = "Lượt của X"
        else:
            if game.game_mode == 1:
                status_text = "Máy (O) đang nghĩ..."
            else:
                status_text = "Lượt của O"
            
    if status_text:
        text_surf = small_font.render(status_text, True, BLACK)
        status_y = BOARD_Y + BOARD_SIZE + 15
        text_bg = pygame.Surface((text_surf.get_width() + 30, text_surf.get_height() + 10))
        text_bg.fill((255, 255, 255))
        text_bg.set_alpha(180)
        screen.blit(text_bg, (SCREEN_WIDTH // 2 - text_bg.get_width() // 2, status_y - 5))
        screen.blit(text_surf, (SCREEN_WIDTH // 2 - text_surf.get_width() // 2, status_y))
    
    if len(game.history) > 0 and game.undo_count < 2 and not getattr(game, 'just_undid', False):
        color3 = BUTTON_HOVER_COLOR if btn_undo.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color3, btn_undo, border_radius=15)
        btn3_text = small_font.render(f"Đi lại ({2 - game.undo_count})", True, WHITE)
        screen.blit(btn3_text, (btn_undo.centerx - btn3_text.get_width() // 2, btn_undo.centery - btn3_text.get_height() // 2))

    color2 = QUIT_BUTTON_HOVER_COLOR if btn_menu.collidepoint(mouse_pos) else QUIT_BUTTON_COLOR
    pygame.draw.rect(screen, color2, btn_menu, border_radius=15)
    btn2_text = small_font.render("Thoát", True, WHITE)
    screen.blit(btn2_text, (btn_menu.centerx - btn2_text.get_width() // 2, btn_menu.centery - btn2_text.get_height() // 2))

def draw_game_over_popup(game, mouse_pos, btn_replay, btn_menu):
    """Vẽ bảng thông báo kết quả sau khi ván đấu kết thúc."""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.fill(BLACK)
    overlay.set_alpha(150)
    screen.blit(overlay, (0, 0))
    
    box_w, box_h = 400, 200
    box_rect = pygame.Rect(SCREEN_WIDTH // 2 - box_w // 2, SCREEN_HEIGHT // 2 - box_h // 2, box_w, box_h)
    pygame.draw.rect(screen, BG_COLOR, box_rect, border_radius=15)
    pygame.draw.rect(screen, LINE_COLOR, box_rect, width=3, border_radius=15)
    
    status_text = ""
    if game.winner == 'X':
        status_text = "BẠN ĐÃ THẮNG!" if game.game_mode == 1 else "Người chơi X Thắng!"
    elif game.winner == 'O':
        status_text = "BẠN ĐÃ THUA!" if game.game_mode == 1 else "Người chơi O Thắng!"
    else:
        status_text = "HÒA NHAU!"
        
    text = medium_font.render(status_text, True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
    
    c_yes = BUTTON_HOVER_COLOR if btn_replay.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, c_yes, btn_replay, border_radius=10)
    t_yes = small_font.render("Chơi lại", True, WHITE)
    screen.blit(t_yes, (btn_replay.centerx - t_yes.get_width() // 2, btn_replay.centery - t_yes.get_height() // 2))
    
    c_no = QUIT_BUTTON_HOVER_COLOR if btn_menu.collidepoint(mouse_pos) else QUIT_BUTTON_COLOR
    pygame.draw.rect(screen, c_no, btn_menu, border_radius=10)
    t_no = small_font.render("Về Menu", True, WHITE)
    screen.blit(t_no, (btn_menu.centerx - t_no.get_width() // 2, btn_menu.centery - t_no.get_height() // 2))

def draw_confirm_quit(mouse_pos, btn_yes, btn_no):
    """Vẽ bảng xác nhận khi người chơi nhấn nút thoát."""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.fill(BLACK)
    overlay.set_alpha(150)
    screen.blit(overlay, (0, 0))
    
    box_w, box_h = 400, 200
    box_rect = pygame.Rect(SCREEN_WIDTH // 2 - box_w // 2, SCREEN_HEIGHT // 2 - box_h // 2, box_w, box_h)
    pygame.draw.rect(screen, BG_COLOR, box_rect, border_radius=15)
    pygame.draw.rect(screen, LINE_COLOR, box_rect, width=3, border_radius=15)
    
    text = medium_font.render("Bạn có chắc chắn muốn thoát?", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
    
    c_yes = QUIT_BUTTON_HOVER_COLOR if btn_yes.collidepoint(mouse_pos) else QUIT_BUTTON_COLOR
    pygame.draw.rect(screen, c_yes, btn_yes, border_radius=10)
    t_yes = small_font.render("Xác nhận", True, WHITE)
    screen.blit(t_yes, (btn_yes.centerx - t_yes.get_width() // 2, btn_yes.centery - t_yes.get_height() // 2))
    
    c_no = BUTTON_HOVER_COLOR if btn_no.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, c_no, btn_no, border_radius=10)
    t_no = small_font.render("Hủy bỏ", True, WHITE)
    screen.blit(t_no, (btn_no.centerx - t_no.get_width() // 2, btn_no.centery - t_no.get_height() // 2))

def main():
    """Hàm chạy vòng lặp xử lý chính của trò chơi."""
    game = CaroGame()
    clock = pygame.time.Clock()

    btn_y = BOARD_Y + BOARD_SIZE + 60
    btn_undo   = pygame.Rect(SCREEN_WIDTH // 2 - 110, btn_y, 100, 40)
    btn_menu   = pygame.Rect(SCREEN_WIDTH // 2 + 10, btn_y, 100, 40)
    
    btn_yes = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 20, 100, 40)
    btn_no = pygame.Rect(SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 + 20, 100, 40)
    btn_replay_popup = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 20, 100, 40)
    btn_menu_popup = pygame.Rect(SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 + 20, 100, 40)

    btn_minimax = pygame.Rect(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 - 40, 250, 50)
    btn_alphabeta = pygame.Rect(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 + 30, 250, 50)
    btn_2p = pygame.Rect(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 + 100, 250, 50)

    btn_easy = pygame.Rect(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 - 50, 250, 45)
    btn_med = pygame.Rect(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 + 5, 250, 45)
    btn_hard = pygame.Rect(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 + 60, 250, 45)
    btn_back = pygame.Rect(SCREEN_WIDTH // 2 - 125, SCREEN_HEIGHT // 2 + 125, 250, 40)
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if game.state == 'MENU':
                        if btn_minimax.collidepoint(event.pos):
                            game.game_mode = 1
                            game.ai_type = 'Minimax'
                            game.state = 'DIFFICULTY'
                        elif btn_alphabeta.collidepoint(event.pos):
                            game.game_mode = 1
                            game.ai_type = 'Alpha-Beta'
                            game.state = 'DIFFICULTY'
                        elif btn_2p.collidepoint(event.pos):
                            game.game_mode = 2
                            game.reset_game()
                            game.state = 'PLAYING'
                            
                    elif game.state == 'DIFFICULTY':
                        if btn_easy.collidepoint(event.pos):
                            game.ai_depth = 2
                            game.reset_game()
                            game.state = 'PLAYING'
                        elif btn_med.collidepoint(event.pos):
                            game.ai_depth = 3
                            game.reset_game()
                            game.state = 'PLAYING'
                        elif btn_hard.collidepoint(event.pos):
                            game.ai_depth = 4
                            game.reset_game()
                            game.state = 'PLAYING'
                        elif btn_back.collidepoint(event.pos):
                            game.state = 'MENU'
                                    
                    elif game.state == 'PLAYING':
                        if btn_menu.collidepoint(event.pos):
                            game.state = 'CONFIRM_QUIT'
                        elif len(game.history) > 0 and game.undo_count < 2 and not getattr(game, 'just_undid', False) and btn_undo.collidepoint(event.pos):
                            game.undo()
                        elif game.game_over:
                            if pygame.time.get_ticks() - getattr(game, 'game_over_time', 0) > 1500:
                                if btn_replay_popup.collidepoint(event.pos):
                                    game.reset_game()
                                elif btn_menu_popup.collidepoint(event.pos):
                                    game.state = 'MENU'
                        else:
                            if game.game_mode == 2 or (game.game_mode == 1 and game.current_player == 'X'):
                                x, y = event.pos
                                if BOARD_X <= x < BOARD_X + BOARD_SIZE and BOARD_Y <= y < BOARD_Y + BOARD_SIZE:
                                    c = (x - BOARD_X) // CELL_SIZE
                                    r = (y - BOARD_Y) // CELL_SIZE
                                    if game.make_move(r, c, game.current_player):
                                        if game.check_win(r, c, game.current_player):
                                            game.game_over = True
                                            game.winner = game.current_player
                                            game.winning_line = game.get_winning_line(game.current_player)
                                            game.game_over_time = pygame.time.get_ticks()
                                        elif game.is_board_full():
                                            game.game_over = True
                                            game.winner = 'Draw'
                                            game.game_over_time = pygame.time.get_ticks()
                                        else:
                                            game.current_player = 'O' if game.current_player == 'X' else 'X'
                                            
                    elif game.state == 'CONFIRM_QUIT':
                        if btn_yes.collidepoint(event.pos):
                            game.state = 'MENU'
                        elif btn_no.collidepoint(event.pos):
                            game.state = 'PLAYING'
                                            
        if game.state == 'MENU':
            draw_menu(mouse_pos, btn_minimax, btn_alphabeta, btn_2p)
        elif game.state == 'DIFFICULTY':
            draw_difficulty_menu(mouse_pos, btn_easy, btn_med, btn_hard, btn_back)
        else:
            draw_board(game)
            draw_status(game, btn_undo, btn_menu, mouse_pos)
            
            if game.state == 'CONFIRM_QUIT':
                draw_confirm_quit(mouse_pos, btn_yes, btn_no)
                
            if game.game_over and game.state == 'PLAYING':
                if pygame.time.get_ticks() - getattr(game, 'game_over_time', 0) > 1500:
                    draw_game_over_popup(game, mouse_pos, btn_replay_popup, btn_menu_popup)
            
            if game.game_mode == 1 and not game.game_over and game.current_player == 'O' and game.state == 'PLAYING':
                pygame.display.flip()
                pygame.time.delay(500)
                move = game.bot_move()
                if move:
                    r, c = move
                    game.make_move(r, c, 'O')
                    if game.check_win(r, c, 'O'):
                        game.game_over = True
                        game.winner = 'O'
                        game.winning_line = game.get_winning_line('O')
                        game.game_over_time = pygame.time.get_ticks()
                    elif game.is_board_full():
                        game.game_over = True
                        game.winner = 'Draw'
                        game.game_over_time = pygame.time.get_ticks()
                    else:
                        game.current_player = 'X'
                        
        pygame.display.flip()
        clock.tick(30)
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
