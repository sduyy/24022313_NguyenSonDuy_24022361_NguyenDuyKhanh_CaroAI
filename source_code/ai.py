import math
import time

from game_logic import CaroGame


# ──────────────────────────────────────────────────────────────────────────────
# Minimax
# ──────────────────────────────────────────────────────────────────────────────

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
    best_move   = None

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
                max_eval  = eval_score
                best_move = (r, c)
        return max_eval, best_move

    else:
        min_eval = math.inf
        for (r, c) in valid_moves:
            old_local = self.get_local_score(r, c)
            self.board[r][c] = 'X'
            new_local = self.get_local_score(r, c)
            diff = new_local - old_local
            self.current_board_score += diff

            eval_score, _ = self.minimax(depth - 1, True, r, c)

            self.current_board_score -= diff
            self.board[r][c] = '.'

            if eval_score < min_eval:
                min_eval  = eval_score
                best_move = (r, c)
        return min_eval, best_move


# ──────────────────────────────────────────────────────────────────────────────
# Alpha-Beta Pruning
# ──────────────────────────────────────────────────────────────────────────────

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
    best_move   = None

    if is_maximizing:
        max_eval = -math.inf
        for (r, c) in valid_moves:
            old_local = self.get_local_score(r, c)
            self.board[r][c] = 'O'
            new_local = self.get_local_score(r, c)
            diff = new_local - old_local
            self.current_board_score += diff

            eval_score, _ = self.alphabeta(depth - 1, alpha, beta, False, r, c)

            self.current_board_score -= diff
            self.board[r][c] = '.'

            if eval_score > max_eval:
                max_eval  = eval_score
                best_move = (r, c)

            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break   # Cắt nhánh Beta
        return max_eval, best_move

    else:
        min_eval = math.inf
        for (r, c) in valid_moves:
            old_local = self.get_local_score(r, c)
            self.board[r][c] = 'X'
            new_local = self.get_local_score(r, c)
            diff = new_local - old_local
            self.current_board_score += diff

            eval_score, _ = self.alphabeta(depth - 1, alpha, beta, True, r, c)

            self.current_board_score -= diff
            self.board[r][c] = '.'

            if eval_score < min_eval:
                min_eval  = eval_score
                best_move = (r, c)

            beta = min(beta, eval_score)
            if beta <= alpha:
                break   # Cắt nhánh Alpha
        return min_eval, best_move


# ──────────────────────────────────────────────────────────────────────────────
# Giao diện gọi bot
# ──────────────────────────────────────────────────────────────────────────────

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


# ──────────────────────────────────────────────────────────────────────────────
# Gắn các phương thức AI vào CaroGame
# ──────────────────────────────────────────────────────────────────────────────
CaroGame.minimax   = minimax
CaroGame.alphabeta = alphabeta
CaroGame.bot_move  = bot_move
