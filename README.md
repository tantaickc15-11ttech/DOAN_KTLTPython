# DOAN_KTLTPython

## Hệ thống phân tích cảnh báo Wazuh và gửi cảnh báo qua Telegram

Đây là đồ án môn Lập trình Python. Chương trình đọc cảnh báo Wazuh từ JSON, lưu vào SQLite, hiển thị bảng và biểu đồ trên giao diện Tkinter, đồng thời có khả năng gửi cảnh báo mức cao qua Telegram.

## Chức năng phiên bản đầu

- Tự tải dataset mẫu khi chạy lần đầu.
- Nhập file JSON hoặc JSON Lines của Wazuh.
- Chuẩn hóa và chống lưu trùng cảnh báo.
- Lưu dữ liệu bằng SQLite.
- Dashboard hiển thị số liệu tổng quan.
- Biểu đồ theo mức độ, theo ngày và Top agent.
- Bảng cảnh báo, tìm kiếm và lọc.
- Cửa sổ xem chi tiết cảnh báo.
- Gửi Telegram theo ngưỡng cấu hình; mặc định đang tắt.

Phạm vi và flow chi tiết nằm trong thư mục [`docs`](docs/).

## Công nghệ

- Python 3
- Tkinter và ttk
- SQLite
- Matplotlib
- PyYAML
- Requests

## Cài đặt

Mở PowerShell tại thư mục project và chạy:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Nếu PowerShell không cho phép kích hoạt môi trường, có thể gọi Python trong môi trường trực tiếp:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Chạy chương trình

```powershell
python main.py
```

Hoặc khi chưa kích hoạt môi trường:

```powershell
.\.venv\Scripts\python.exe main.py
```

Lần chạy đầu, chương trình tự nhập 12 cảnh báo trong `data/sample_alerts.json` vào `data/alerts.db`.

## Cấu hình Telegram

Sao chép file cấu hình mẫu:

```powershell
Copy-Item .\config\config.example.yml .\config\config.yml
```

Sau đó sửa `config/config.yml`:

```yaml
telegram:
  enabled: true
  bot_token: "TOKEN_THAT_CUA_BAN"
  chat_id: "CHAT_ID_THAT_CUA_BAN"
  minimum_level: 8
  timeout_seconds: 10
```

`config/config.yml` đã được đưa vào `.gitignore`; không được dùng lệnh ép Git thêm file này.

## Chạy kiểm thử

```powershell
python -m unittest discover -s tests -v
```

## Cấu trúc chính

```text
main.py                         Điểm bắt đầu chương trình
config/config.example.yml      Cấu hình mẫu an toàn
data/sample_alerts.json        Dataset phục vụ demo
src/models/alert.py            Lớp Alert
src/services/alert_reader.py   Đọc và kiểm tra JSON
src/services/database_service.py  Lưu và truy vấn SQLite
src/services/analysis_service.py  Thống kê dữ liệu
src/services/telegram_service.py  Gửi Telegram
src/ui/main_window.py          Giao diện và biểu đồ
tests/test_core.py             Kiểm thử chức năng chính
docs/                          Kế hoạch, flow và tài liệu bảo vệ
```

## Lưu ý bảo mật

- Không đưa Bot Token, Chat ID, mật khẩu hoặc API key lên GitHub.
- Không sử dụng nguyên dữ liệu nhạy cảm của hệ thống thật làm dataset nộp bài.
- Chỉ commit `config.example.yml` chứa giá trị giả.
