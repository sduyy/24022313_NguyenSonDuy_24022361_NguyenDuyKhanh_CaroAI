import pygame
import random
import sys

# Hằng số
SIZE = 9
CELL_SIZE = 50
WIDTH = SIZE * CELL_SIZE
HEIGHT = WIDTH + 100 # Thêm không gian bên dưới để hiển thị thông báo và nút bấm

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_COLOR = (50, 50, 50)
X_COLOR = (200, 50, 50)
O_COLOR = (50, 50, 200)
BG_COLOR = (240, 240, 240)
BUTTON_COLOR = (100, 200, 100)
BUTTON_HOVER_COLOR = (120, 220, 120)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Caro AI - 9x9")

# Font chữ (sử dụng font hệ thống hỗ trợ tiếng Việt)
try:
    font = pygame.font.SysFont('arial', 40, True)
    small_font = pygame.font.SysFont('arial', 24, True)
except Exception:
    font = pygame.font.Font(None, 40)
    small_font = pygame.font.Font(None, 24)

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
        self.reset_game()

    def reset_game(self):
        self.board = [['.' for _ in range(SIZE)] for _ in range(SIZE)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None
        self.history = []
        self.undo_count = 0

    def make_move(self, r, c, player):
        if 0 <= r < SIZE and 0 <= c < SIZE and self.board[r][c] == '.':
            self.board[r][c] = player
            self.history.append((r, c)) # Lưu lại nước đi vào lịch sử
            return True
        return False

    def undo(self):
        """Hàm xử lý lùi bước (hoãn cờ)"""
        if not self.history or self.undo_count >= 2:
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
    screen.fill(BG_COLOR)
    title = font.render("CHON CHE DO CHOI", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 3))
    
    # Nút 1 Người (vs Máy)
    c1 = BUTTON_HOVER_COLOR if btn_1p.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, c1, btn_1p)
    t1 = small_font.render("1 Nguoi (vs May)", True, WHITE)
    screen.blit(t1, (btn_1p.centerx - t1.get_width() // 2, btn_1p.centery - t1.get_height() // 2))
    
    # Nút 2 Người
    c2 = BUTTON_HOVER_COLOR if btn_2p.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, c2, btn_2p)
    t2 = small_font.render("2 Nguoi", True, WHITE)
    screen.blit(t2, (btn_2p.centerx - t2.get_width() // 2, btn_2p.centery - t2.get_height() // 2))

def draw_board(game):
    screen.fill(BG_COLOR)
    
    # Vẽ lưới
    for x in range(0, WIDTH + 1, CELL_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (x, 0), (x, WIDTH), 2)
    for y in range(0, WIDTH + 1, CELL_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0, y), (WIDTH, y), 2)
        
    # Vẽ quân X và O
    for r in range(SIZE):
        for c in range(SIZE):
            if game.board[r][c] == 'X':
                # Vẽ X
                center_x = c * CELL_SIZE + CELL_SIZE // 2
                center_y = r * CELL_SIZE + CELL_SIZE // 2
                offset = 15
                pygame.draw.line(screen, X_COLOR, (center_x - offset, center_y - offset), (center_x + offset, center_y + offset), 4)
                pygame.draw.line(screen, X_COLOR, (center_x + offset, center_y - offset), (center_x - offset, center_y + offset), 4)
            elif game.board[r][c] == 'O':
                # Vẽ O
                center_x = c * CELL_SIZE + CELL_SIZE // 2
                center_y = r * CELL_SIZE + CELL_SIZE // 2
                pygame.draw.circle(screen, O_COLOR, (center_x, center_y), 15, 4)

def draw_status(game, btn_replay, btn_undo, btn_menu, mouse_pos):
    # Vẽ thông báo trạng thái
    status_text = ""
    if game.game_over:
        if game.winner == 'X':
            status_text = "Nguoi choi X Thang!"
        elif game.winner == 'O':
            if game.game_mode == 1:
                status_text = "May (O) Thang!"
            else:
                status_text = "Nguoi choi O Thang!"
        else:
            status_text = "Hoa!"
    else:
        if game.current_player == 'X':
            status_text = "Luot cua X"
        else:
            if game.game_mode == 1:
                status_text = "May (O) dang nghi..."
            else:
                status_text = "Luot cua O"
            
    text_surf = small_font.render(status_text, True, BLACK)
    screen.blit(text_surf, (WIDTH // 2 - text_surf.get_width() // 2, WIDTH + 10))
    
    # Nút Undo hiện khi có lịch sử nước đi và còn lượt Undo
    if len(game.history) > 0 and game.undo_count < 2:
        color3 = BUTTON_HOVER_COLOR if btn_undo.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color3, btn_undo)
        btn3_text = small_font.render(f"Undo ({2 - game.undo_count})", True, WHITE)
        screen.blit(btn3_text, (btn_undo.centerx - btn3_text.get_width() // 2, btn_undo.centery - btn3_text.get_height() // 2))

    # Nút Chơi Lại và Menu khi game kết thúc
    if game.game_over:
        color1 = BUTTON_HOVER_COLOR if btn_replay.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color1, btn_replay)
        btn_text = small_font.render("Choi Lai", True, WHITE)
        screen.blit(btn_text, (btn_replay.centerx - btn_text.get_width() // 2, btn_replay.centery - btn_text.get_height() // 2))

        color2 = BUTTON_HOVER_COLOR if btn_menu.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(screen, color2, btn_menu)
        btn2_text = small_font.render("Menu", True, WHITE)
        screen.blit(btn2_text, (btn_menu.centerx - btn2_text.get_width() // 2, btn_menu.centery - btn2_text.get_height() // 2))

def main():
    game = CaroGame()
    clock = pygame.time.Clock()
    
    # Kích thước và vị trí nút bấm MENU
    btn_1p = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    btn_2p = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 70, 200, 50)
    
    # Kích thước và vị trí nút bấm CHƠI LẠI, UNDO, MENU
    btn_replay = pygame.Rect(WIDTH // 2 - 160, WIDTH + 45, 100, 40)
    btn_undo   = pygame.Rect(WIDTH // 2 - 50, WIDTH + 45, 100, 40)
    btn_menu   = pygame.Rect(WIDTH // 2 + 60, WIDTH + 45, 100, 40)
    
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
                        # Ưu tiên xử lý nút Undo (có thể bấm bất cứ lúc nào có history)
                        if len(game.history) > 0 and game.undo_count < 2 and btn_undo.collidepoint(event.pos):
                            game.undo()
                        # Xử lý các nút khi Game Over
                        elif game.game_over:
                            if btn_replay.collidepoint(event.pos):
                                game.reset_game()
                            elif btn_menu.collidepoint(event.pos):
                                game.state = 'MENU'
                        else:
                            # Nếu chế độ 2 Người, hoặc (chế độ 1 Người và đang là lượt của X)
                            if game.game_mode == 2 or (game.game_mode == 1 and game.current_player == 'X'):
                                x, y = event.pos
                                if y < WIDTH:
                                    c = x // CELL_SIZE
                                    r = y // CELL_SIZE
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
                                            
        if game.state == 'MENU':
            draw_menu(mouse_pos, btn_1p, btn_2p)
        else:
            draw_board(game)
            draw_status(game, btn_replay, btn_undo, btn_menu, mouse_pos)
            
            # Lượt của Máy (Bot)
            if game.game_mode == 1 and not game.game_over and game.current_player == 'O':
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