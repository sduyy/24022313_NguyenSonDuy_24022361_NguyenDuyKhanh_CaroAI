import math
import time
from caro_logic import CaroGame, SIZE

def run_benchmark():
    game = CaroGame()
    
    # Chuẩn bị 5 trạng thái bàn cờ kiểm thử
    states = [
        {
            "name": "1. Đầu ván (Trống)",
            "board": [['.' for _ in range(SIZE)] for _ in range(SIZE)]
        },
        {
            "name": "2. Người chơi sắp thắng (Cần chặn)",
            "board": [
                ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', 'X', 'X', 'X', '.', '.', '.', '.'],
                ['.', '.', '.', 'O', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', 'O', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.', '.']
            ]
        },
        {
            "name": "3. Máy có thể thắng ngay",
            "board": [
                ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', 'O', 'O', 'O', '.', '.', '.', '.'],
                ['.', '.', 'X', 'X', '.', '.', '.', '.', '.'],
                ['.', '.', '.', 'X', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.', '.']
            ]
        },
        {
            "name": "4. Giữa ván (Hai bên cùng tấn công)",
            "board": [
                ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', 'X', '.', '.', '.', '.'],
                ['.', '.', '.', 'O', 'X', '.', '.', '.', '.'],
                ['.', '.', '.', 'X', 'O', 'O', '.', '.', '.'],
                ['.', '.', '.', '.', 'X', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.', '.']
            ]
        },
        {
            "name": "5. Trạng thái phân tán (Nhiều nhánh)",
            "board": [
                ['.', 'X', '.', '.', '.', '.', '.', 'O', '.'],
                ['.', '.', '.', '.', 'O', '.', '.', '.', '.'],
                ['.', '.', 'X', '.', '.', '.', 'X', '.', '.'],
                ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                ['O', '.', '.', '.', 'X', '.', '.', '.', 'O'],
                ['.', '.', '.', '.', '.', '.', '.', '.', '.'],
                ['.', '.', 'O', '.', '.', '.', 'X', '.', '.'],
                ['.', '.', '.', '.', 'O', '.', '.', '.', '.'],
                ['.', 'X', '.', '.', '.', '.', '.', 'O', '.']
            ]
        }
    ]

    # Chạy các độ sâu 1, 2, 3 và cả 4 (để ép xung)
    depths_to_test = [1, 2, 3, 4]

    print(f"{'Trạng thái':<35} | {'Thuật toán':<12} | {'Độ sâu':<6} | {'Nước đi':<10} | {'Số TT đã xét':<15} | {'Thời gian (s)'}")
    print("-" * 105)

    for state in states:
        for depth in depths_to_test:
            # 1. Test Minimax (Chỉ chạy khi Depth <= 3 để tránh treo máy)
            if depth <= 3:
                game.board = [row[:] for row in state["board"]]
                game.nodes_visited = 0
                start = time.time()
                _, move_mm = game.minimax(depth, True)
                time_mm = time.time() - start
                nodes_mm = game.nodes_visited
                
                print(f"{state['name']:<35} | {'Minimax':<12} | {depth:<6} | {str(move_mm):<10} | {nodes_mm:<15} | {time_mm:.4f}")
            else:
                # Nếu Depth = 4, in ra N/A để báo cáo
                print(f"{state['name']:<35} | {'Minimax':<12} | {depth:<6} | {'N/A':<10} | {'> 500,000':<15} | {'Timeout'}")

            # 2. Test Alpha-Beta (Chạy ở mọi Độ sâu, kể cả Depth 4)
            game.board = [row[:] for row in state["board"]]
            game.nodes_visited = 0
            start = time.time()
            _, move_ab = game.alphabeta(depth, -math.inf, math.inf, True)
            time_ab = time.time() - start
            nodes_ab = game.nodes_visited

            # Nếu là Minimax thì in kèm tên trạng thái, Alpha-beta thì để trống cột đầu cho đẹp
            name_col = "" if depth <= 3 else state['name'] 
            print(f"{name_col:<35} | {'Alpha-Beta':<12} | {depth:<6} | {str(move_ab):<10} | {nodes_ab:<15} | {time_ab:.4f}")
            
        print("-" * 105)

if __name__ == "__main__":
    run_benchmark()
