# KẾ HOẠCH THỰC HIỆN VÀ LUỒNG HOẠT ĐỘNG HỆ THỐNG

## 1. Thông tin đề tài

- **Tên đề tài:** Hệ thống phân tích cảnh báo an ninh từ Wazuh và gửi cảnh báo qua Telegram.
- **Loại ứng dụng:** Ứng dụng desktop viết bằng Python.
- **Giao diện:** Tkinter.
- **Biểu đồ:** Matplotlib nhúng trong Tkinter.
- **Nguồn dữ liệu:** File cảnh báo JSON của Wazuh hoặc dataset JSON mẫu.
- **Lưu trữ:** SQLite.
- **Kênh cảnh báo:** Telegram Bot API.

## 2. Mục tiêu

Xây dựng một chương trình Python có khả năng nhập dữ liệu cảnh báo Wazuh, lưu dữ liệu, thống kê các thông tin quan trọng, trình bày kết quả bằng bảng và biểu đồ, đồng thời gửi những cảnh báo có mức độ cao tới Telegram.

Đồ án ưu tiên:

- Bám sát kiến thức môn Lập trình Python.
- Code rõ ràng, dễ đọc và dễ giải thích.
- Chạy được khi demo không có kết nối tới Wazuh.
- Không sử dụng Machine Learning hoặc kiến trúc phức tạp.
- Không lưu token Telegram và thông tin bí mật lên GitHub.

## 3. Phạm vi

### 3.1. Trong phạm vi

- Chọn và nhập file JSON chứa cảnh báo.
- Kiểm tra, chuẩn hóa và lưu cảnh báo vào SQLite.
- Hiển thị danh sách cảnh báo trên GUI.
- Tìm kiếm và lọc cảnh báo.
- Thống kê cảnh báo theo mức độ, thời gian và agent.
- Hiển thị các thống kê bằng biểu đồ.
- Xem nội dung chi tiết của một cảnh báo.
- Gửi cảnh báo mức cao qua Telegram.
- Ghi nhận trạng thái gửi Telegram.
- Cung cấp dataset mẫu để demo offline.

### 3.2. Ngoài phạm vi phiên bản đồ án

- Machine Learning và dự đoán tấn công.
- Xử lý dữ liệu thời gian thực ở quy mô lớn.
- Thay thế chức năng quản trị của Wazuh Dashboard.
- Quản lý nhiều người dùng và phân quyền phức tạp.
- Can thiệp hoặc thay đổi rule của Wazuh.
- Tự động phản ứng như khóa tài khoản hoặc chặn IP.

## 4. Kiến trúc tổng quát

```text
Nguồn cảnh báo Wazuh / Dataset mẫu
                 |
                 v
       Module đọc dữ liệu JSON
                 |
                 v
       Kiểm tra và chuẩn hóa dữ liệu
                 |
                 v
            Cơ sở dữ liệu SQLite
              /              \
             v                v
   GUI Tkinter + biểu đồ    Kiểm tra level
                                |
                                v
                         Telegram Bot API
```

## 5. Các luồng hoạt động

### Flow 1: Khởi động chương trình

```text
Người dùng chạy main.py
        |
        v
Đọc cấu hình chương trình
        |
        v
Khởi tạo/kiểm tra SQLite
        |
        v
Tải dữ liệu đã có
        |
        v
Hiển thị cửa sổ Dashboard
```

Nếu chưa có cơ sở dữ liệu, chương trình tự tạo file và bảng cần thiết. Nếu cấu hình Telegram chưa có, các chức năng xem và phân tích dữ liệu vẫn hoạt động.

### Flow 2: Nhập dữ liệu cảnh báo

```text
Nhấn "Nhập dữ liệu"
        |
        v
Chọn file JSON
        |
        v
Đọc file bằng Python
        |
        v
File hợp lệ? -- Không --> Hiển thị thông báo lỗi
        |
       Có
        |
        v
Chuẩn hóa các trường cần thiết
        |
        v
Kiểm tra cảnh báo trùng
        |
        v
Lưu cảnh báo mới vào SQLite
        |
        v
Cập nhật bảng và biểu đồ
```

### Flow 3: Xem và lọc cảnh báo

```text
Nhập từ khóa/chọn mức độ/chọn agent
        |
        v
Nhấn "Lọc"
        |
        v
Truy vấn danh sách phù hợp
        |
        v
Hiển thị kết quả trong bảng
        |
        v
Chọn một dòng --> Xem chi tiết cảnh báo
```

### Flow 4: Phân tích và vẽ biểu đồ

```text
Dữ liệu trong SQLite
        |
        v
Nhóm và đếm bằng các hàm Python
        |
        +--> Theo mức độ
        +--> Theo ngày/giờ
        +--> Theo agent
        +--> Theo rule
        |
        v
Chuyển kết quả sang Matplotlib
        |
        v
Hiển thị biểu đồ trong Tkinter
```

### Flow 5: Gửi cảnh báo Telegram

```text
Cảnh báo mới được nhập
        |
        v
So sánh level với ngưỡng cấu hình
        |
  Không đủ ngưỡng --> Không gửi
        |
       Đủ ngưỡng
        |
        v
Tạo nội dung tin nhắn
        |
        v
Gọi Telegram Bot API
        |
        +--> Thành công: lưu trạng thái "Đã gửi"
        +--> Thất bại: lưu lỗi và hiển thị thông báo
```

Khi chạy bằng dataset demo, có thể tắt gửi Telegram để tránh gửi tin nhắn ngoài ý muốn.

## 6. Dữ liệu chính

Mỗi cảnh báo dự kiến có các trường:

| Trường | Ý nghĩa |
|---|---|
| `alert_id` | Mã duy nhất của cảnh báo |
| `timestamp` | Thời gian phát sinh |
| `agent_id` | Mã agent Wazuh |
| `agent_name` | Tên máy/agent |
| `agent_ip` | Địa chỉ IP của agent |
| `rule_id` | Mã rule Wazuh |
| `rule_level` | Mức độ cảnh báo |
| `description` | Mô tả cảnh báo |
| `groups` | Nhóm sự kiện |
| `location` | Nguồn log |
| `telegram_sent` | Trạng thái gửi Telegram |

Cấu trúc chính xác sẽ được đối chiếu lại khi nhận file cảnh báo Wazuh thật.

## 7. Kế hoạch thực hiện và lịch sử commit

| Giai đoạn | Công việc | Commit dự kiến |
|---|---|---|
| 1 | Chốt phạm vi, flow và tính năng | `docs: add project plan and feature specification` |
| 2 | Tạo cấu trúc thư mục và cửa sổ Tkinter | `feat: create initial tkinter application` |
| 3 | Xây dựng lớp Alert và đọc JSON | `feat: import and validate wazuh alerts` |
| 4 | Tạo SQLite và lưu dữ liệu | `feat: persist alerts in sqlite database` |
| 5 | Hiển thị bảng, tìm kiếm và bộ lọc | `feat: add alert table and filters` |
| 6 | Thêm các biểu đồ phân tích | `feat: add alert analysis charts` |
| 7 | Tích hợp gửi Telegram | `feat: add telegram alert notification` |
| 8 | Bổ sung exception và kiểm thử | `test: add core feature tests` |
| 9 | Hoàn thiện hướng dẫn và khai báo AI | `docs: complete usage and ai disclosure` |
| 10 | Hoàn thiện báo cáo, slide và demo | `docs: add final report and presentation` |

## 8. Hồ sơ phải nộp

- Source code Python và file `requirements.txt`.
- Input/dataset JSON mẫu.
- Báo cáo DOCX dưới 20 trang.
- File khai báo sử dụng AI, prompt và skill/phương pháp sử dụng.
- Slide thuyết trình đúng 10 trang.
- Kịch bản demo trực tiếp và video dự phòng nếu cần.
- Repository GitHub có lịch sử commit rõ ràng.
- Bộ câu hỏi và trả lời chuẩn bị bảo vệ.

## 9. Nguyên tắc chống lệch phạm vi

- Mỗi chức năng code mới phải tồn tại trong tài liệu đặc tả tính năng.
- Nếu thay đổi chức năng, cập nhật hai tài liệu nền trước khi sửa code.
- Tên chức năng trong source, báo cáo, slide và kịch bản demo phải thống nhất.
- Không thêm kỹ thuật phức tạp chỉ để làm chương trình trông lớn hơn.
- Token, Chat ID và dữ liệu nhạy cảm chỉ đặt trong file cấu hình cá nhân đã được Git bỏ qua.

## 10. Thông tin còn cần bổ sung

- Script Python integration Telegram hiện tại.
- File YAML đang sử dụng.
- Mẫu `alerts.json` đã ẩn thông tin nhạy cảm.
- Ngưỡng level cần gửi Telegram.
- Thông tin sinh viên, lớp, giảng viên và mẫu báo cáo.

