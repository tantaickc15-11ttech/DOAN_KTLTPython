Add-Type -AssemblyName System.Drawing

$outputDir = Join-Path $PSScriptRoot '..\..\deliverables\demo'
$framesDir = Join-Path $outputDir 'frames'
New-Item -ItemType Directory -Path $framesDir -Force | Out-Null

$slides = @(
    @{ Title = 'WAZUH SECURITY MONITOR'; Lines = @('Đồ án môn Lập trình Python', 'Phân tích cảnh báo và gửi Telegram', 'Thời lượng demo: khoảng 2 phút') },
    @{ Title = '1. KHỞI ĐỘNG ỨNG DỤNG'; Lines = @('Chạy main.py bằng Python trong .venv', 'SQLite được tạo tự động khi chưa tồn tại', 'Dataset mẫu được tải khi database rỗng') },
    @{ Title = '2. DASHBOARD PHÂN TÍCH'; Lines = @('Tổng cảnh báo: 12', 'Cảnh báo mức cao trở lên: 6', 'Số agent: 4', 'Biểu đồ mức độ, thời gian và Top agent') },
    @{ Title = '3. NHẬP FILE JSON'; Lines = @('Chọn Nhập file JSON trên giao diện', 'AlertReader đọc và kiểm tra dữ liệu', 'DatabaseService lưu cảnh báo mới', 'ID trùng được tự động bỏ qua') },
    @{ Title = '4. TÌM KIẾM VÀ XEM CHI TIẾT'; Lines = @('Tìm theo mô tả, rule hoặc agent', 'Lọc theo mức độ và tên agent', 'Nhấp đúp để xem JSON gốc') },
    @{ Title = '5. CẢNH BÁO TELEGRAM'; Lines = @('Telegram mặc định tắt trong demo', 'Chỉ gửi khi level đạt ngưỡng cấu hình', 'Gửi thành công sẽ cập nhật trạng thái SQLite') },
    @{ Title = '6. KẾT QUẢ'; Lines = @('8/8 unit test đạt', 'GUI tải đúng 12 cảnh báo mẫu', 'Demo hoạt động khi không kết nối Wazuh', 'Cảm ơn thầy/cô!') }
)

$width = 1280
$height = 720
$background = [System.Drawing.Color]::FromArgb(242, 246, 250)
$navy = [System.Drawing.Color]::FromArgb(27, 44, 72)
$accent = [System.Drawing.Color]::FromArgb(0, 156, 190)
$dark = [System.Drawing.Color]::FromArgb(45, 58, 78)
$muted = [System.Drawing.Color]::FromArgb(95, 112, 136)

$titleFont = New-Object System.Drawing.Font('Segoe UI', 32, [System.Drawing.FontStyle]::Bold)
$bodyFont = New-Object System.Drawing.Font('Segoe UI', 22, [System.Drawing.FontStyle]::Regular)
$footerFont = New-Object System.Drawing.Font('Segoe UI', 13, [System.Drawing.FontStyle]::Regular)
$whiteBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)
$darkBrush = New-Object System.Drawing.SolidBrush($dark)
$mutedBrush = New-Object System.Drawing.SolidBrush($muted)
$navyBrush = New-Object System.Drawing.SolidBrush($navy)
$accentBrush = New-Object System.Drawing.SolidBrush($accent)

$concatLines = @()

for ($index = 0; $index -lt $slides.Count; $index++) {
    $bitmap = New-Object System.Drawing.Bitmap($width, $height)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $graphics.Clear($background)

    $graphics.FillRectangle($navyBrush, 0, 0, $width, 120)
    $graphics.FillRectangle($accentBrush, 0, 116, $width, 6)
    $graphics.DrawString($slides[$index].Title, $titleFont, $whiteBrush, 58, 34)

    $graphics.FillRectangle([System.Drawing.Brushes]::White, 70, 165, 1140, 450)
    $y = 215
    foreach ($line in $slides[$index].Lines) {
        $graphics.FillEllipse($accentBrush, 105, $y + 10, 13, 13)
        $graphics.DrawString($line, $bodyFont, $darkBrush, 145, $y)
        $y += 75
    }

    $footer = "Wazuh Security Monitor  |  $($index + 1)/$($slides.Count)"
    $graphics.DrawString($footer, $footerFont, $mutedBrush, 70, 660)

    $frameName = 'frame{0:D2}.png' -f ($index + 1)
    $framePath = Join-Path $framesDir $frameName
    $bitmap.Save($framePath, [System.Drawing.Imaging.ImageFormat]::Png)
    $graphics.Dispose()
    $bitmap.Dispose()

    $concatLines += "file '$($framePath.Replace('\', '/'))'"
    $concatLines += 'duration 4'
}

$lastFrame = Join-Path $framesDir ('frame{0:D2}.png' -f $slides.Count)
$concatLines += "file '$($lastFrame.Replace('\', '/'))'"
$concatPath = Join-Path $framesDir 'concat.txt'
[System.IO.File]::WriteAllLines($concatPath, $concatLines, [System.Text.UTF8Encoding]::new($false))

$titleFont.Dispose()
$bodyFont.Dispose()
$footerFont.Dispose()
$whiteBrush.Dispose()
$darkBrush.Dispose()
$mutedBrush.Dispose()
$navyBrush.Dispose()
$accentBrush.Dispose()

Write-Output $concatPath
