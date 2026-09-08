# SỔ TAY CÁC HÀM, BIẾN VÀ ĐOẠN CODE QUAN TRỌNG

## 1. Cách sử dụng tài liệu

Tài liệu này dùng để ôn phần bảo vệ đồ án. Mỗi mục trả lời bốn câu hỏi:

1. Tính năng nằm ở file nào?
2. Hàm nào thực hiện tính năng?
3. Biến hoặc điều kiện nào ảnh hưởng trực tiếp đến kết quả?
4. Đầu vào thay đổi thì đầu ra thay đổi như thế nào?

Tài liệu phải được cập nhật khi tên hàm, quy tắc hoặc cấu trúc source code thay đổi.

## 2. Điểm bắt đầu chương trình

### File `main.py`

#### Hàm `main()`

- **Nhiệm vụ:** Khởi tạo toàn bộ ứng dụng.
- **Các biến quan trọng:**
  - `BASE_DIR`: Thư mục gốc, giúp chương trình tìm đúng config và database dù chạy từ vị trí khác.
  - `config`: Dictionary chứa cấu hình ứng dụng và Telegram.
  - `database`: Đối tượng thao tác SQLite.
  - `app`: Đối tượng cửa sổ Tkinter.
- **Luồng:** Đọc config → tạo bảng SQLite → tạo cửa sổ → gọi `mainloop()`.
- **Câu hỏi có thể gặp:** Vì sao dùng `if __name__ == "__main__"`?
- **Trả lời:** Để `main()` chỉ tự chạy khi chạy trực tiếp file này, không tự chạy khi file được import như một module.

## 3. Đọc cấu hình

### File `src/config_loader.py`

#### Biến `DEFAULT_CONFIG`

- Là dictionary chứa cấu hình mặc định an toàn.
- `demo_mode=True`: Chương trình ưu tiên chạy bằng dữ liệu mẫu.
- `auto_load_sample=True`: Tự nhập dataset mẫu nếu database chưa có dữ liệu.
- `telegram.enabled=False`: Không tự gửi Telegram khi mới tải project.
- `telegram.minimum_level=8`: Chỉ cảnh báo từ level 8 mới đủ điều kiện gửi.

#### Hàm `load_config(file_path)`

- Nếu không có `config/config.yml`, hàm trả về `DEFAULT_CONFIG`.
- Nếu file tồn tại, hàm cập nhật các giá trị do người dùng khai báo.
- `try/except` giúp lỗi YAML không làm chương trình dừng.
- **Biến ảnh hưởng kết quả:** `file_path`, `user_config`, `section` và `values`.

## 4. Chuẩn hóa một cảnh báo

### File `src/models/alert.py`

#### Lớp `Alert`

- Đại diện cho một cảnh báo sau khi chuẩn hóa.
- Giúp GUI và database không phải hiểu toàn bộ cấu trúc JSON phức tạp của Wazuh.

#### Hàm `Alert.from_wazuh_dict(data)`

- **Đầu vào:** Một dictionary từ JSON.
- **Đầu ra:** Một đối tượng `Alert`.
- **Biến ảnh hưởng trực tiếp:**
  - `timestamp`: Bắt buộc; thiếu trường này thì bản ghi bị báo lỗi.
  - `agent`: Dictionary con chứa ID, tên và IP agent.
  - `rule`: Dictionary con chứa ID, level, mô tả và groups.
  - `rule_level`: Được ép sang `int`; đây là giá trị dùng để phân loại mức độ và gửi Telegram.
  - `alert_id`: Dùng để phát hiện cảnh báo trùng.
- Nếu dữ liệu không có ID, chương trình tạo ID ổn định từ thời gian, agent, rule và mô tả bằng SHA-256.

#### Hàm `to_database_tuple()`

- Chuyển thuộc tính của đối tượng thành tuple đúng thứ tự các cột SQLite.
- `groups` và `raw_data` được chuyển thành chuỗi JSON trước khi lưu.

#### Hàm `from_database_row(row)`

- Chuyển một dòng SQLite trở lại thành đối tượng `Alert`.
- Chỉ số như `row[6]`, `row[8]` phụ thuộc trực tiếp vào thứ tự cột trong câu `SELECT *`.

## 5. Nhập file JSON

### File `src/services/alert_reader.py`

#### Hàm `read_file(file_path)`

- **Đầu vào:** Đường dẫn file JSON.
- **Đầu ra:** Tuple `(alerts, errors)`.
- `alerts`: Danh sách bản ghi hợp lệ.
- `errors`: Danh sách lỗi của từng bản ghi không hợp lệ.
- Vòng lặp `for` giúp một bản ghi lỗi không làm mất toàn bộ file.

#### Hàm `_parse_records(text)`

- Thử đọc toàn bộ nội dung bằng `json.loads(text)`.
- Nếu không phải JSON hoàn chỉnh, hàm thử đọc từng dòng theo định dạng JSON Lines.
- Hỗ trợ ba dạng dữ liệu:
  - Danh sách JSON.
  - Một object JSON.
  - Kết quả API có `data.affected_items`.
- **Biến ảnh hưởng kết quả:** `text`, `data`, `records`, `line_number`.

## 6. Lưu và truy vấn SQLite

### File `src/services/database_service.py`

#### Hàm `initialize()`

- Tạo bảng `alerts` nếu chưa tồn tại.
- `alert_id` là `PRIMARY KEY`, vì vậy một ID không thể được lưu hai lần.

#### Hàm `save_alerts(alerts)`

- Duyệt danh sách và chạy `INSERT OR IGNORE`.
- `inserted`: Số cảnh báo mới được thêm.
- `duplicated`: Số cảnh báo đã tồn tại.
- `cursor.rowcount` quyết định tăng biến nào.
- **Kết quả:** Trả về tuple `(inserted, duplicated)`.

#### Hàm `get_alerts(keyword, severity, agent)`

- Xây dựng câu truy vấn dựa trên các bộ lọc.
- `keyword` tác động tới mô tả, rule ID và tên agent.
- `severity` tác động tới khoảng `rule_level`.
- `agent` yêu cầu tên agent trùng chính xác.
- Dictionary `ranges` quy định:
  - Thấp: 0–4.
  - Trung bình: 5–7.
  - Cao: 8–11.
  - Nghiêm trọng: 12–15.

#### Hàm `mark_telegram_sent(alert_id)`

- Đổi `telegram_sent` thành 1 cho đúng cảnh báo.
- Biến `alert_id` quyết định dòng nào được cập nhật.

## 7. Phân tích dữ liệu

### File `src/services/analysis_service.py`

#### Hàm `severity_name(level)`

- Đây là hàm quan trọng nhất của biểu đồ mức độ.
- Kết quả phụ thuộc trực tiếp vào `level` và các mốc 4, 7, 11.
- Nếu thay đổi các mốc này, bộ lọc SQLite cũng phải thay đổi theo.

#### Hàm `overview(alerts)`

- `len(alerts)`: Tổng cảnh báo.
- `high_count`: Tăng khi `rule_level >= 8`.
- `sent_count`: Tăng khi `telegram_sent=True`.
- `agents`: Dùng `set` để tên agent trùng chỉ được đếm một lần.

#### Hàm `count_by_severity(alerts)`

- Gọi `severity_name()` cho từng cảnh báo.
- Dictionary `result` là dữ liệu trực tiếp đưa vào biểu đồ cột.

#### Hàm `count_by_date(alerts)`

- Gọi `_get_date()` để lấy ngày từ timestamp.
- Dùng `Counter` để đếm và `sorted` để sắp xếp ngày.
- Kết quả trực tiếp tạo biểu đồ đường.

#### Hàm `top_agents(alerts, limit=5)`

- `limit` quyết định số agent tối đa được hiển thị.
- `Counter.most_common(limit)` trả về các agent có nhiều cảnh báo nhất.

## 8. Điều kiện gửi Telegram

### File `src/services/telegram_service.py`

#### Hàm `is_ready()`

Trả về `True` chỉ khi đồng thời thỏa mãn:

- `enabled=True`.
- `bot_token` không rỗng và không phải giá trị mẫu.
- `chat_id` không rỗng và không phải giá trị mẫu.

#### Hàm `should_send(alert)`

Điều kiện trực tiếp:

```python
self.is_ready() and alert.rule_level >= self.minimum_level
```

Nếu `minimum_level` tăng, số cảnh báo được gửi sẽ giảm.

#### Hàm `send_alert(alert)`

- Tạo URL từ `bot_token`.
- Tạo `payload` gồm `chat_id`, `parse_mode` và `text`.
- `timeout_seconds` quyết định thời gian chờ tối đa.
- Trả về `(True, message)` khi thành công hoặc `(False, error)` khi thất bại.
- `try/except` xử lý mất mạng, timeout hoặc phản hồi không hợp lệ.

## 9. Giao diện và biểu đồ

### File `src/ui/main_window.py`

#### Hàm `_auto_load_sample(app_config)`

- Chỉ tải dataset mẫu khi:
  - `auto_load_sample=True`.
  - Database chưa có cảnh báo.
  - File mẫu tồn tại.

#### Hàm `import_json()`

- Mở hộp thoại chọn file.
- Gọi `AlertReader.read_file()`.
- `known_ids` chứa ID đã có trong database.
- `new_alerts` chỉ chứa ID chưa tồn tại; danh sách này giúp tránh gửi lại Telegram khi nhập trùng file.
- Gọi `database.save_alerts()`.
- Gọi `_send_new_alerts(new_alerts)`.
- Cuối cùng gọi `refresh_data()` để cập nhật GUI.
- Các biến `inserted`, `duplicated`, `errors`, `sent` được hiển thị cho người dùng.

#### Hàm `refresh_data()`

- Lấy toàn bộ cảnh báo từ database.
- Cập nhật danh sách agent, các thẻ số liệu, biểu đồ và bảng.
- `self.current_alerts` giữ danh sách đang dùng trên GUI.

#### Hàm `apply_filters()`

- Lấy giá trị từ ba biến Tkinter:
  - `keyword_var`.
  - `severity_var`.
  - `agent_var`.
- Kết quả từ database được đưa vào bảng.

#### Hàm `_update_charts(alerts)`

- `severity`: Dữ liệu cho biểu đồ cột mức độ.
- `dates`: Dữ liệu cho biểu đồ đường theo ngày.
- `agents`: Dữ liệu cho biểu đồ ngang Top agent.
- Nếu danh sách `alerts` thay đổi, ba biểu đồ thay đổi theo.

#### Hàm `show_detail()`

- `selected`: ID dòng được chọn trong `Treeview`.
- Dùng ID để tìm đúng đối tượng trong `self.current_alerts`.
- Nếu chưa chọn dòng, chương trình hiển thị cảnh báo thay vì phát sinh lỗi.

## 10. Các quy tắc phải đồng bộ khi chỉnh sửa

| Quy tắc | Các vị trí cần sửa cùng nhau |
|---|---|
| Khoảng phân loại level | `AnalysisService.severity_name()` và `DatabaseService.get_alerts()` |
| Ngưỡng gửi Telegram | `config.yml` và phần giải thích/demo |
| Tên trường cảnh báo | `Alert`, cấu trúc bảng SQLite và cột GUI |
| Số lượng Top agent | Tham số `limit` và tiêu đề slide/báo cáo |
| Chế độ demo | `config.yml`, README và kịch bản demo |

## 11. Điểm sẽ cập nhật sau khi có integration thật

- Mapping chính xác giữa JSON Wazuh thực tế và lớp `Alert`.
- Cách script hiện tại nhận tham số từ Wazuh.
- Nội dung tin nhắn Telegram đang dùng.
- Tên và ý nghĩa các biến trong file YAML thực tế.
- Quy tắc chống gửi lại cùng một cảnh báo.
