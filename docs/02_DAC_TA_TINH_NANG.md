# ĐẶC TẢ TÍNH NĂNG HỆ THỐNG

## 1. Mục đích tài liệu

Tài liệu này xác định chính xác các tính năng sẽ được lập trình. Source code, báo cáo, slide và phần demo phải bám theo danh sách này. Phiên bản đầu ưu tiên đơn giản, dễ sử dụng và dễ giải thích bằng kiến thức Python đã học.

## 2. Vai trò sử dụng

Hệ thống chỉ có một vai trò trong phạm vi đồ án:

- **Người giám sát:** nhập dữ liệu, xem thống kê, lọc cảnh báo, xem chi tiết và kiểm tra việc gửi Telegram.

Không xây dựng đăng ký, đăng nhập hoặc phân quyền trong phiên bản này.

## 3. Danh sách tính năng

### F01 — Khởi động và kiểm tra dữ liệu

- **Mục đích:** Chuẩn bị ứng dụng để sử dụng.
- **Đầu vào:** File cấu hình và cơ sở dữ liệu hiện có.
- **Xử lý:** Đọc cấu hình, tạo SQLite nếu chưa tồn tại và tải dữ liệu.
- **Đầu ra:** Cửa sổ chính được hiển thị.
- **Ngoại lệ:** Cấu hình Telegram thiếu không được làm ứng dụng dừng.
- **Kỹ thuật Python:** Module, hàm, `if`, `try/except`, OOP và Tkinter.
- **Hoàn thành khi:** Chạy `python main.py` mở được ứng dụng.

### F02 — Nhập file cảnh báo Wazuh

- **Mục đích:** Đưa dữ liệu cảnh báo vào chương trình.
- **Đầu vào:** File JSON do người dùng chọn.
- **Xử lý:** Đọc JSON, kiểm tra trường bắt buộc, chuyển thành đối tượng `Alert` và loại bỏ bản ghi trùng.
- **Đầu ra:** Số bản ghi thành công, trùng và lỗi.
- **Ngoại lệ:** File không tồn tại, JSON sai định dạng hoặc thiếu dữ liệu.
- **Kỹ thuật Python:** File, dictionary, list, vòng lặp, điều kiện, hàm, exception và OOP.
- **Hoàn thành khi:** Có thể nhập dataset mẫu mà chương trình không báo lỗi.

### F03 — Lưu cảnh báo vào SQLite

- **Mục đích:** Giữ dữ liệu sau khi đóng chương trình.
- **Đầu vào:** Các đối tượng `Alert` hợp lệ.
- **Xử lý:** Tạo bảng, thêm bản ghi và kiểm tra khóa duy nhất.
- **Đầu ra:** Dữ liệu được lưu trong file database.
- **Ngoại lệ:** Lỗi kết nối hoặc câu lệnh SQLite.
- **Kỹ thuật Python:** Module `sqlite3`, hàm, class và exception.
- **Hoàn thành khi:** Mở lại ứng dụng vẫn xem được dữ liệu đã nhập.

### F04 — Dashboard tổng quan

- **Mục đích:** Cho biết nhanh tình trạng dữ liệu cảnh báo.
- **Thông tin hiển thị:**
  - Tổng số cảnh báo.
  - Số cảnh báo mức cao.
  - Số agent khác nhau.
  - Số cảnh báo đã gửi Telegram.
- **Đầu vào:** Dữ liệu SQLite.
- **Xử lý:** Đếm và tổng hợp dữ liệu.
- **Đầu ra:** Các thẻ số liệu trên GUI.
- **Kỹ thuật Python:** Biến, kiểu dữ liệu, hàm, vòng lặp và Tkinter.
- **Hoàn thành khi:** Các số liệu thay đổi đúng sau khi nhập file mới.

### F05 — Hiển thị danh sách cảnh báo

- **Mục đích:** Xem các cảnh báo dưới dạng bảng.
- **Cột chính:** Thời gian, agent, IP, rule ID, level, mô tả và trạng thái Telegram.
- **Đầu vào:** Danh sách cảnh báo từ SQLite.
- **Xử lý:** Duyệt dữ liệu và đưa từng dòng vào `ttk.Treeview`.
- **Đầu ra:** Bảng cảnh báo có thanh cuộn.
- **Kỹ thuật Python:** List, vòng lặp, hàm và Tkinter/ttk.
- **Hoàn thành khi:** Bảng hiển thị đúng số dòng và đúng giá trị dataset.

### F06 — Tìm kiếm và lọc

- **Mục đích:** Thu hẹp danh sách cần xem.
- **Đầu vào:** Từ khóa, mức độ hoặc agent.
- **Xử lý:** So sánh điều kiện và truy vấn dữ liệu phù hợp.
- **Đầu ra:** Bảng chỉ còn các cảnh báo thỏa điều kiện.
- **Ngoại lệ:** Không có kết quả thì hiển thị bảng rỗng, không gây lỗi.
- **Kỹ thuật Python:** Chuỗi, điều kiện, hàm và truy vấn SQLite.
- **Hoàn thành khi:** Các bộ lọc hoạt động độc lập và có thể kết hợp.

### F07 — Xem chi tiết cảnh báo

- **Mục đích:** Xem đầy đủ nội dung một cảnh báo.
- **Đầu vào:** Dòng đang được chọn trong bảng.
- **Xử lý:** Lấy ID và tìm bản ghi tương ứng.
- **Đầu ra:** Cửa sổ chi tiết.
- **Ngoại lệ:** Chưa chọn dòng thì hiển thị hướng dẫn.
- **Kỹ thuật Python:** Sự kiện GUI, điều kiện, hàm và OOP.
- **Hoàn thành khi:** Nhấp đúp hoặc bấm nút có thể mở đúng cảnh báo.

### F08 — Biểu đồ theo mức độ

- **Mục đích:** So sánh số lượng cảnh báo ở từng nhóm mức độ.
- **Quy ước ban đầu:** Thấp `0–4`, trung bình `5–7`, cao `8–11`, nghiêm trọng `12–15`.
- **Đầu vào:** Giá trị `rule_level`.
- **Xử lý:** Dùng điều kiện để phân nhóm và đếm.
- **Đầu ra:** Biểu đồ cột.
- **Kỹ thuật Python:** Dictionary, vòng lặp, điều kiện, hàm và Matplotlib.
- **Hoàn thành khi:** Tổng các cột bằng tổng số cảnh báo đang phân tích.

### F09 — Biểu đồ cảnh báo theo thời gian

- **Mục đích:** Quan sát sự thay đổi số cảnh báo.
- **Đầu vào:** Thời gian phát sinh cảnh báo.
- **Xử lý:** Chuyển đổi thời gian, nhóm theo ngày và đếm.
- **Đầu ra:** Biểu đồ đường.
- **Ngoại lệ:** Bản ghi có thời gian lỗi được bỏ qua và ghi nhận.
- **Kỹ thuật Python:** Chuỗi, `datetime`, dictionary, vòng lặp và Matplotlib.
- **Hoàn thành khi:** Các mốc ngày được sắp xếp đúng thứ tự.

### F10 — Thống kê agent và rule nổi bật

- **Mục đích:** Xác định nguồn phát sinh nhiều cảnh báo.
- **Đầu vào:** Agent và rule của các cảnh báo.
- **Xử lý:** Nhóm, đếm, sắp xếp và lấy các giá trị cao nhất.
- **Đầu ra:** Biểu đồ hoặc danh sách Top 5.
- **Kỹ thuật Python:** Dictionary, vòng lặp, hàm và sắp xếp.
- **Hoàn thành khi:** Kết quả Top 5 khớp với dataset kiểm thử.

### F11 — Gửi cảnh báo qua Telegram

- **Mục đích:** Thông báo cảnh báo nghiêm trọng.
- **Đầu vào:** Cảnh báo mới, ngưỡng level, Bot Token và Chat ID.
- **Xử lý:** Kiểm tra level, định dạng tin nhắn và gọi Telegram Bot API.
- **Đầu ra:** Tin nhắn Telegram và trạng thái gửi trong database.
- **Ngoại lệ:** Mất mạng, token sai, Chat ID sai hoặc Telegram trả lỗi.
- **Kỹ thuật Python:** Điều kiện, hàm, module, HTTP request và exception.
- **Hoàn thành khi:** Cảnh báo đủ ngưỡng được gửi; cảnh báo thấp hơn không gửi.

### F12 — Chế độ demo an toàn

- **Mục đích:** Bảo đảm có thể bảo vệ khi Wazuh hoặc Internet không hoạt động.
- **Đầu vào:** Dataset mẫu và tùy chọn bật/tắt Telegram.
- **Xử lý:** Sử dụng cùng luồng nhập và phân tích như dữ liệu thật.
- **Đầu ra:** Dashboard, bảng và biểu đồ đầy đủ mà không cần Wazuh.
- **Kỹ thuật Python:** File, cấu hình, điều kiện và module.
- **Hoàn thành khi:** Ngắt Internet vẫn demo được toàn bộ phần phân tích.

## 4. Các màn hình dự kiến

### M01 — Dashboard

- Các thẻ thống kê tổng quan.
- Biểu đồ theo mức độ.
- Biểu đồ theo thời gian.
- Top agent hoặc top rule.
- Nút nhập dữ liệu và làm mới.

### M02 — Danh sách cảnh báo

- Bảng `Treeview`.
- Ô tìm kiếm.
- Bộ lọc level và agent.
- Nút xem chi tiết.
- Trạng thái Telegram.

### M03 — Chi tiết cảnh báo

- Hiển thị đầy đủ các trường đã chuẩn hóa.
- Hiển thị nhóm sự kiện và vị trí nguồn log.
- Không cho phép sửa dữ liệu Wazuh trong phiên bản đầu.

### M04 — Cấu hình/Trạng thái

- Hiển thị có hay chưa có cấu hình Telegram.
- Hiển thị ngưỡng gửi cảnh báo.
- Cho phép bật/tắt gửi Telegram trong lúc demo.
- Không hiển thị đầy đủ Bot Token trên màn hình.

## 5. Cấu trúc source code dự kiến

```text
_DoAn/
|-- main.py
|-- README.md
|-- requirements.txt
|-- .gitignore
|-- config/
|   `-- config.example.yml
|-- data/
|   `-- sample_alerts.json
|-- src/
|   |-- models/
|   |   `-- alert.py
|   |-- services/
|   |   |-- alert_reader.py
|   |   |-- database_service.py
|   |   |-- analysis_service.py
|   |   `-- telegram_service.py
|   `-- ui/
|       |-- main_window.py
|       |-- dashboard_frame.py
|       `-- alerts_frame.py
|-- tests/
|   `-- test_core.py
`-- docs/
    |-- 01_KE_HOACH_VA_LUONG_HE_THONG.md
    `-- 02_DAC_TA_TINH_NANG.md
```

Cấu trúc này có thể rút gọn nếu code thực tế quá ít. Mục tiêu của việc chia file là minh họa module/package và tách trách nhiệm, không phải làm dự án phức tạp.

## 6. Liên hệ với nội dung môn học

| Nội dung đã học | Áp dụng trong đồ án |
|---|---|
| Kiểu dữ liệu | Chuỗi, số, list, tuple và dictionary của cảnh báo |
| Câu điều kiện | Phân loại level và quyết định gửi Telegram |
| Vòng lặp | Duyệt cảnh báo, tạo bảng và thống kê |
| Hàm | Chia nhỏ từng bước đọc, kiểm tra, phân tích và hiển thị |
| Module/package | Chia models, services và ui |
| Exception | Xử lý lỗi file, JSON, database và mạng |
| OOP | Lớp Alert và các lớp service/GUI cần thiết |
| GUI | Tkinter, ttk, sự kiện nút bấm và bảng dữ liệu |

Matplotlib, SQLite và HTTP request là thư viện hỗ trợ cho bài toán; phần sử dụng sẽ được giữ ở mức cơ bản và giải thích trong báo cáo.

## 7. Quy tắc dữ liệu và bảo mật

- Không commit file cấu hình thật chứa Bot Token hoặc Chat ID.
- Chỉ commit `config.example.yml` với giá trị giả.
- Database khi chạy thật được đưa vào `.gitignore`.
- Dataset nộp bài phải ẩn IP hoặc thông tin nhạy cảm nếu lấy từ hệ thống thật.
- Telegram mặc định tắt trong chế độ demo cho đến khi người dùng chủ động bật.

## 8. Tiêu chí hoàn thành chung

Hệ thống được xem là hoàn thành khi:

1. Cài đặt được từ hướng dẫn trong README.
2. Chạy được bằng một lệnh Python.
3. Nhập được dataset mẫu.
4. Hiển thị đúng bảng và các thống kê.
5. Các biểu đồ khớp với dữ liệu đầu vào.
6. Bộ lọc và màn hình chi tiết hoạt động.
7. Telegram hoạt động khi có cấu hình hợp lệ.
8. Lỗi thường gặp được xử lý bằng thông báo dễ hiểu.
9. Không có bí mật trong lịch sử Git.
10. Source, báo cáo, slide và demo thống nhất với hai tài liệu nền.

## 9. Các điểm cần xác nhận sau khi nhận code thật

- Cấu trúc file JSON của Wazuh.
- Cách file YAML hiện tại khai báo integration.
- Hàm gửi Telegram đang sử dụng.
- Quy tắc/ngưỡng level thực tế.
- Có đọc trực tiếp `alerts.json` hay nhập file thủ công khi demo.

