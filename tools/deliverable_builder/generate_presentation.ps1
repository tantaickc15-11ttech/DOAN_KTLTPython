param(
    [Parameter(Mandatory = $true)]
    [string]$OutputPath
)

function Get-Rgb([int]$red, [int]$green, [int]$blue) {
    return $red + ($green * 256) + ($blue * 65536)
}

$slidesData = @(
    @{ Title = 'ĐỒ ÁN LẬP TRÌNH PYTHON'; Lines = @('HỆ THỐNG PHÂN TÍCH CẢNH BÁO WAZUH VÀ GỬI CẢNH BÁO QUA TELEGRAM', 'Sinh viên: [HỌ VÀ TÊN] - MSSV: [MSSV]', 'Giảng viên: [TÊN GIẢNG VIÊN]') },
    @{ Title = '1. BÀI TOÁN'; Lines = @('Wazuh tạo nhiều cảnh báo dạng JSON', 'Khó quan sát nhanh bằng file log', 'Cần bảng, biểu đồ và thông báo Telegram') },
    @{ Title = '2. MỤC TIÊU'; Lines = @('Ứng dụng desktop dễ sử dụng', 'Nhập và lưu cảnh báo', 'Thống kê trực quan', 'Gửi cảnh báo mức cao') },
    @{ Title = '3. CÔNG NGHỆ'; Lines = @('Python và Tkinter', 'SQLite', 'Matplotlib', 'JSON và YAML', 'Telegram Bot API') },
    @{ Title = '4. KIẾN TRÚC'; Lines = @('JSON Wazuh', 'AlertReader → Alert', 'SQLite → AnalysisService', 'Dashboard và Telegram') },
    @{ Title = '5. CẤU TRÚC DỮ LIỆU'; Lines = @('Một bảng alerts', 'alert_id là khóa chính', 'rule_level phục vụ phân loại', 'telegram_sent lưu trạng thái', 'raw_json giữ dữ liệu gốc') },
    @{ Title = '6. CHỨC NĂNG CHÍNH'; Lines = @('Dashboard và ba biểu đồ', 'Danh sách cảnh báo', 'Tìm kiếm, lọc, xem chi tiết', 'Nhập JSON và chống trùng') },
    @{ Title = '7. QUY TẮC PHÂN TÍCH'; Lines = @('Thấp: 0-4', 'Trung bình: 5-7', 'Cao: 8-11', 'Nghiêm trọng: 12-15', 'Telegram: level lớn hơn hoặc bằng ngưỡng') },
    @{ Title = '8. DEMO VÀ KIỂM THỬ'; Lines = @('Dataset: 12 cảnh báo, 4 agent', '8/8 unit test đạt', 'GUI tải đủ dữ liệu', 'Demo được khi không có Internet') },
    @{ Title = '9. KẾT LUẬN'; Lines = @('Đạt mục tiêu đề tài', 'Bám sát kiến thức Python', 'Dễ cài đặt và trình bày', 'Hướng tới kết nối Wazuh trực tiếp', 'Cảm ơn thầy/cô!') }
)

$powerpoint = $null
$presentation = $null

try {
    $powerpoint = New-Object -ComObject PowerPoint.Application
    $presentation = $powerpoint.Presentations.Add()
    $presentation.PageSetup.SlideWidth = 960
    $presentation.PageSetup.SlideHeight = 540

    for ($index = 0; $index -lt $slidesData.Count; $index++) {
        $slide = $presentation.Slides.Add($index + 1, 12)

        $background = $slide.Shapes.AddShape(1, 0, 0, 960, 540)
        $background.Fill.ForeColor.RGB = Get-Rgb 242 246 250
        $background.Line.Visible = 0

        $header = $slide.Shapes.AddShape(1, 0, 0, 960, 95)
        $header.Fill.ForeColor.RGB = Get-Rgb 27 44 72
        $header.Line.Visible = 0

        $accent = $slide.Shapes.AddShape(1, 0, 92, 960, 5)
        $accent.Fill.ForeColor.RGB = Get-Rgb 0 156 190
        $accent.Line.Visible = 0

        $title = $slide.Shapes.AddTextbox(1, 45, 20, 870, 55)
        $title.TextFrame.TextRange.Text = $slidesData[$index].Title
        $title.TextFrame.TextRange.Font.Name = 'Segoe UI'
        $title.TextFrame.TextRange.Font.Size = 27
        $title.TextFrame.TextRange.Font.Bold = -1
        $title.TextFrame.TextRange.Font.Color.RGB = Get-Rgb 255 255 255

        $card = $slide.Shapes.AddShape(5, 55, 125, 850, 345)
        $card.Fill.ForeColor.RGB = Get-Rgb 255 255 255
        $card.Line.ForeColor.RGB = Get-Rgb 220 228 238

        $body = $slide.Shapes.AddTextbox(1, 95, 155, 770, 285)
        $body.TextFrame.TextRange.Text = ($slidesData[$index].Lines | ForEach-Object { "• $_" }) -join "`r`n"
        $body.TextFrame.TextRange.Font.Name = 'Segoe UI'
        $body.TextFrame.TextRange.Font.Size = 21
        $body.TextFrame.TextRange.Font.Color.RGB = Get-Rgb 45 58 78
        $body.TextFrame.TextRange.ParagraphFormat.SpaceAfter = 12

        $footer = $slide.Shapes.AddTextbox(1, 55, 495, 850, 25)
        $footer.TextFrame.TextRange.Text = "Đồ án Lập trình Python  |  $($index + 1)/10"
        $footer.TextFrame.TextRange.Font.Name = 'Segoe UI'
        $footer.TextFrame.TextRange.Font.Size = 10
        $footer.TextFrame.TextRange.Font.Color.RGB = Get-Rgb 95 112 136
    }

    $presentation.SaveAs($OutputPath, 24)
    Write-Output 'PowerPoint generated successfully.'
}
finally {
    if ($presentation) { $presentation.Close() }
    if ($powerpoint) { $powerpoint.Quit() }
}
