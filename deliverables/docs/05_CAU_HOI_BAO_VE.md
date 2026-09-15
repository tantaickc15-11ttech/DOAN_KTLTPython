# CÂU HỎI BẢO VỆ VÀ TRẢ LỜI NGẮN

1. **Vì sao dùng SQLite?** Vì SQLite là database dạng file, không cần server và phù hợp dữ liệu đồ án nhỏ.
2. **JSON được dùng thế nào?** JSON là đầu vào; Python chuẩn hóa rồi lưu từng cảnh báo vào SQLite.
3. **Vì sao cần alert_id?** Đây là khóa chính giúp nhận diện và chống lưu trùng cảnh báo.
4. **Vì sao dùng OOP?** Lớp Alert gom dữ liệu và hành vi chuyển đổi của một cảnh báo.
5. **Biểu đồ lấy dữ liệu ở đâu?** GUI đọc Alert từ SQLite rồi AnalysisService nhóm và đếm.
6. **Telegram gửi khi nào?** Khi cấu hình sẵn sàng và rule_level lớn hơn hoặc bằng minimum_level.
7. **Nếu mất Internet?** Phần phân tích vẫn chạy; Telegram trả lỗi được try/except xử lý.
8. **Tại sao không commit config.yml?** Vì file này có thể chứa Bot Token và Chat ID thật.
9. **Cảnh báo trùng được xử lý thế nào?** alert_id là khóa chính và INSERT OR IGNORE bỏ qua ID đã tồn tại.
10. **Đóng chương trình có mất dữ liệu không?** Không, dữ liệu nằm trong data/alerts.db và được dùng lại ở lần chạy sau.
