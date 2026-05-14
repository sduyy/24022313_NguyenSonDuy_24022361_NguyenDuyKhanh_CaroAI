# Caro AI - Trò chơi Caro 9x9 kết hợp AI

Dự án này là một trò chơi Caro (Gomoku) kích thước 9x9 được phát triển bằng ngôn ngữ Python và thư viện Pygame. Trò chơi tích hợp các thuật toán tìm kiếm phổ biến trong AI như **Minimax** và **Alpha-Beta Pruning** để tạo ra một đối thủ máy thông minh.

## Nhóm Thực hiện
- **Nguyễn Sơn Duy** - MSV: 24022313
- **Nguyễn Duy Khánh** - MSV: 24022361

## Tính năng Nổi bật
- **Chế độ chơi đa dạng:**
  - Người vs Máy (Chọn thuật toán Minimax hoặc Alpha-Beta).
  - Người vs Người (Chơi trên cùng một máy tính).
- **Thuật toán AI:**
  - **Minimax:** Thuật toán tìm kiếm cơ bản.
  - **Alpha-Beta Pruning:** Cải tiến của Minimax giúp tối ưu hóa thời gian tính toán bằng cách cắt tỉa các nhánh không cần thiết.
  - **Move Ordering:** Sắp xếp nước đi ưu tiên để tăng hiệu quả cắt tỉa của Alpha-Beta.
- **Tùy chọn độ khó:** 3 mức độ (Dễ - Depth 2, Trung bình - Depth 3, Khó - Depth 4).
- **Giao diện người dùng (UI):**
  - Đồ họa phong cách gỗ truyền thống.
  - Hiệu ứng highlight nước đi cuối cùng.
  - Hiển thị đường kẻ chiến thắng khi kết thúc ván đấu.
  - Tính năng **Undo (Hoàn tác)** tối đa 2 lần.
  - Popup thông báo kết quả và tùy chọn chơi lại nhanh.

## 🛠 Yêu cầu Hệ thống
- **Ngôn ngữ:** Python 3.8 trở lên.
- **Thư viện:** `pygame-ce`.

## Hướng dẫn Cài đặt và Chạy

### 1. Tải dự án
Clone hoặc tải mã nguồn về máy tính.

### 2. Cài đặt thư viện cần thiết
Mở terminal/cmd tại thư mục gốc của dự án và chạy lệnh sau:
```bash
pip install -r requirements.txt
```

### 3. Chạy trò chơi
Chạy file chính trong thư mục `source_code`:
```bash
python source_code/caro_logic.py
```

### 4. Chạy Benchmark (Kiểm thử hiệu năng)
Để so sánh hiệu năng giữa thuật toán Minimax và Alpha-Beta, chạy file benchmark:
```bash
python source_code/benchmark.py
```

## Cấu trúc Thư mục
- `source_code/`: Chứa toàn bộ mã nguồn dự án.
  - `caro_logic.py`: Logic game, thuật toán AI và giao diện Pygame.
  - `benchmark.py`: Script kiểm thử tốc độ và số trạng thái đã duyệt của AI.
  - `background.png`: Hình nền cho trò chơi.
- `requirements.txt`: Danh sách các thư viện cần cài đặt.
- `README.md`: Hướng dẫn sử dụng dự án.

## Cách chơi
1. Tại Menu chính, chọn chế độ chơi (Minimax, Alpha-Beta hoặc 2 Người).
2. Nếu chọn đấu với Máy, hãy chọn độ khó.
3. Người chơi (X) đi trước. Click chuột vào các ô trống trên bàn cờ để đặt quân.
4. Đạt được 4 quân cờ liên tiếp theo hàng ngang, dọc hoặc chéo để giành chiến thắng.
5. Sử dụng nút **"Đi lại"** nếu muốn rút lại nước đi sai lầm.
