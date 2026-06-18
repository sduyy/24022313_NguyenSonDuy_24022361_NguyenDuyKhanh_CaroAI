"""
game_logic.py
Lớp CaroGame quản lý toàn bộ trạng thái và logic cơ bản của ván cờ:
  - Bàn cờ, lịch sử nước đi, lùi bước (undo)
  - Kiểm tra thắng / hòa
  - Hàm heuristic đánh giá cửa sổ và điểm toàn bàn
"""

import math
import time

from constants import SIZE


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

    # ──────────────────────────────────────────────────────────────────────────
    # Quản lý ván cờ
    # ──────────────────────────────────────────────────────────────────────────

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
        self.current_board_score = 0   # Điểm số cộng dồn của toàn bộ bàn cờ
        self.nodes_visited = 0         # Số trạng thái AI đã duyệt qua

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
        if self.game_over or not self.history or self.undo_count >= 2 or getattr(self, 'just_undid', False):
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

    # ──────────────────────────────────────────────────────────────────────────
    # Kiểm tra thắng / hòa
    # ──────────────────────────────────────────────────────────────────────────

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

    # ──────────────────────────────────────────────────────────────────────────
    # Hàm heuristic đánh giá
    # ──────────────────────────────────────────────────────────────────────────

    def evaluate_window_optimized(self, window):
        """Chấm điểm heuristic tối ưu cho một dải 4 ô liên tiếp."""
        bot_count    = 0
        player_count = 0
        empty_count  = 0
        for cell in window:
            if   cell == 'O': bot_count    += 1
            elif cell == 'X': player_count += 1
            else:             empty_count  += 1

        score = 0
        if   bot_count == 4:                          score += 1000000
        elif bot_count == 3 and empty_count == 1:     score +=    5000
        elif bot_count == 2 and empty_count == 2:     score +=     100
        elif bot_count == 1 and empty_count == 3:     score +=      10

        if   player_count == 4:                       score -= 1000000
        elif player_count == 3 and empty_count == 1:  score -=   10000
        elif player_count == 2 and empty_count == 2:  score -=     150
        elif player_count == 1 and empty_count == 3:  score -=      15
        return score

    def get_local_score(self, r, c):
        """Tính điểm cục bộ xung quanh vị trí (r, c) để tối ưu hóa việc sắp xếp nước đi."""
        local_total = 0
        directions  = [(0, 1), (1, 0), (1, 1), (1, -1)]

        for dr, dc in directions:
            for i in range(4):
                start_r = r - dr * i
                start_c = c - dc * i

                window       = []
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

        # Hàng ngang
        for r in range(SIZE):
            for c in range(SIZE - 3):
                window = [self.board[r][c + i] for i in range(4)]
                total_score += self.evaluate_window_optimized(window)

        # Hàng dọc
        for c in range(SIZE):
            for r in range(SIZE - 3):
                window = [self.board[r + i][c] for i in range(4)]
                total_score += self.evaluate_window_optimized(window)

        # Đường chéo xuôi
        for r in range(SIZE - 3):
            for c in range(SIZE - 3):
                window = [self.board[r + i][c + i] for i in range(4)]
                total_score += self.evaluate_window_optimized(window)

        # Đường chéo ngược
        for r in range(SIZE - 3):
            for c in range(SIZE):
                if c - 3 >= 0:
                    window = [self.board[r + i][c - i] for i in range(4)]
                    total_score += self.evaluate_window_optimized(window)

        return total_score

    # ──────────────────────────────────────────────────────────────────────────
    # Danh sách nước đi
    # ──────────────────────────────────────────────────────────────────────────

    def get_valid_moves(self):
        """Trả về danh sách các ô trống hợp lệ nằm kề với quân cờ đã có."""
        moves     = []
        has_piece = False

        for r in range(SIZE):
            for c in range(SIZE):
                if self.board[r][c] != '.':
                    has_piece = True
                    break
            if has_piece:
                break

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
        valid_moves  = self.get_valid_moves()
        move_scores  = []

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
