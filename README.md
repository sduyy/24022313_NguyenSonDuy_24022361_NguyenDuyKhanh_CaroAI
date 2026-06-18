# 🎮 Caro AI — Trò chơi Caro 9×9 kết hợp AI

> Dự án môn **Cơ sở Trí tuệ Nhân tạo** — Trò chơi Caro (Gomoku) 9×9 xây dựng bằng Python + Pygame, tích hợp các thuật toán tìm kiếm **Minimax** và **Alpha-Beta Pruning** để tạo đối thủ máy thông minh.

---

## 👥 Nhóm Thực hiện

| Họ và tên | Mã sinh viên |
|---|---|
| Nguyễn Sơn Duy | 24022313 |
| Nguyễn Duy Khánh | 24022361 |

---

## ✨ Tính năng Nổi bật

### Chế độ chơi
- 🤖 **Người vs Máy** — Chọn thuật toán Minimax hoặc Alpha-Beta Pruning.
- 👥 **Người vs Người** — Chơi cùng nhau trên một máy tính.

### Thuật toán AI
| Thuật toán | Mô tả |
|---|---|
| **Minimax** | Tìm kiếm toàn bộ cây trạng thái, đảm bảo nước đi tối ưu |
| **Alpha-Beta Pruning** | Cải tiến Minimax, cắt tỉa nhánh không cần thiết giúp tăng tốc đáng kể |
| **Move Ordering** | Ưu tiên các nước đi có điểm heuristic cao để tối ưu hiệu quả cắt nhánh |
| **Incremental Scoring** | Cập nhật điểm bàn cờ tăng dần thay vì tính lại toàn bộ sau mỗi nước đi |

### Độ khó
| Mức | Độ sâu tìm kiếm (Depth) |
|---|---|
| Dễ | 2 |
| Trung bình | 3 |
| Khó | 4 |

### Giao diện
- 🎨 Đồ họa phong cách bàn cờ gỗ truyền thống.
- 💡 Highlight nước đi cuối cùng.
- 🏆 Hiển thị đường kẻ chiến thắng khi kết thúc ván đấu.
- ↩️ Tính năng **Undo (Hoàn tác)** tối đa 2 lần mỗi ván.
- 📣 Popup thông báo kết quả và tùy chọn chơi lại nhanh.

---

## 🛠 Yêu cầu Hệ thống

- **Python:** 3.8 trở lên
- **Thư viện:** `pygame-ce`

---

## 🚀 Hướng dẫn Cài đặt và Chạy

### 1. Tải dự án
```bash
git clone <repository-url>
cd 24022313_NguyenSonDuy_24022361_NguyenDuyKhanh_CaroAI
```

### 2. Cài đặt thư viện
```bash
pip install -r requirements.txt
```

### 3. Chạy trò chơi

**Cách 1** — Dùng file entry point mới (khuyến nghị):
```bash
python source_code/main.py
```

**Cách 2** — Dùng file gốc (vẫn hoạt động):
```bash
python source_code/caro_logic.py
```

### 4. Chạy Benchmark (Kiểm thử hiệu năng)
So sánh hiệu năng Minimax vs Alpha-Beta trên 5 trạng thái bàn cờ mẫu, với độ sâu từ 1 đến 4:
```bash
python source_code/benchmark.py
```

---

## 📁 Cấu trúc Thư mục

```
📦 24022313_NguyenSonDuy_24022361_NguyenDuyKhanh_CaroAI/
├── 📄 README.md              # Hướng dẫn sử dụng dự án
├── 📄 requirements.txt       # Danh sách thư viện cần cài đặt
├── 📄 reports.pdf            # Báo cáo đồ án
└── 📂 source_code/
    ├── 🐍 main.py            # Vòng lặp game chính (entry point)
    ├── 🐍 caro_logic.py      # Shim tương thích ngược, re-export toàn bộ module
    ├── 🐍 constants.py       # Hằng số: kích thước, màu sắc, vị trí bàn cờ
    ├── 🐍 resources.py       # Khởi tạo pygame, font chữ, ảnh nền
    ├── 🐍 game_logic.py      # Lớp CaroGame: bàn cờ, undo, kiểm tra thắng, heuristic
    ├── 🐍 ai.py              # Thuật toán Minimax & Alpha-Beta Pruning
    ├── 🐍 renderer.py        # Các hàm vẽ giao diện (menu, bàn cờ, popup)
    ├── 🐍 benchmark.py       # Script kiểm thử hiệu năng AI
    └── 🖼️  background.png    # Hình nền trò chơi
```

### Mô tả chi tiết từng module

| Module | Chức năng |
|---|---|
| `constants.py` | Định nghĩa tất cả hằng số dùng chung (SIZE, màu sắc, tọa độ) |
| `resources.py` | Khởi tạo pygame, tạo cửa sổ, load font chữ và ảnh nền |
| `game_logic.py` | Lớp `CaroGame`: quản lý bàn cờ, lịch sử, undo, check_win, hàm heuristic |
| `ai.py` | Thuật toán Minimax, Alpha-Beta Pruning và hàm `bot_move()` |
| `renderer.py` | Các hàm `draw_*`: vẽ menu, bàn cờ, quân cờ, popup kết quả |
| `main.py` | Vòng lặp game chính, xử lý sự kiện, điều phối giữa các trạng thái |
| `caro_logic.py` | File shim — re-export toàn bộ symbol để đảm bảo tương thích ngược |

---

## 🎯 Cách chơi

1. Tại **Menu chính**, chọn chế độ chơi:
   - **Đấu với Minimax** hoặc **Đấu với Alpha-Beta** để chơi với máy.
   - **2 Người chơi** để chơi cùng bạn bè.
2. Nếu chọn đấu với máy, chọn **độ khó** (Dễ / Trung bình / Khó).
3. Người chơi **X đi trước** — Click chuột vào ô trống trên bàn cờ để đặt quân.
4. Giành chiến thắng bằng cách tạo **4 quân cờ liên tiếp** theo hàng ngang, dọc hoặc chéo.
5. Dùng nút **「Đi lại」** để hoàn tác nước đi sai (tối đa 2 lần).
6. Khi ván kết thúc, chọn **Chơi lại** hoặc **Về Menu**.

---

## 📊 Kết quả Benchmark (Ví dụ)

Benchmark chạy Minimax và Alpha-Beta trên 5 trạng thái bàn cờ mẫu. Alpha-Beta thường duyệt **ít hơn 5–10 lần** số trạng thái so với Minimax thuần túy ở cùng độ sâu.

> Chạy `python source_code/benchmark.py` để xem kết quả chi tiết trên máy của bạn.
