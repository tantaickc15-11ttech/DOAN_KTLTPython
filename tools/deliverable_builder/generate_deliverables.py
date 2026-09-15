"""Generate DOCX and PPTX deliverables using only Python standard library."""

from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[2] / "deliverables"
REPORT_DIR = ROOT / "report"
SLIDES_DIR = ROOT / "slides"
DEMO_DIR = ROOT / "demo"
DOCS_DIR = ROOT / "docs"


PROJECT_TITLE = "HỆ THỐNG PHÂN TÍCH CẢNH BÁO WAZUH VÀ GỬI CẢNH BÁO QUA TELEGRAM"


REPORT_SECTIONS = [
    ("TRANG BÌA", [
        "TRƯỜNG: [BỔ SUNG TÊN TRƯỜNG]",
        "MÔN HỌC: LẬP TRÌNH PYTHON",
        PROJECT_TITLE,
        "Sinh viên: [HỌ VÀ TÊN]",
        "MSSV: [MÃ SỐ SINH VIÊN]    Lớp: [LỚP]",
        "Giảng viên: [TÊN GIẢNG VIÊN]",
        "Năm học 2026",
    ]),
    ("MỤC LỤC", [
        "1. Giới thiệu đề tài",
        "2. Mục tiêu và phạm vi",
        "3. Cơ sở lý thuyết",
        "4. Phân tích và thiết kế hệ thống",
        "5. Thiết kế dữ liệu",
        "6. Xây dựng chương trình",
        "7. Các chức năng chính",
        "8. Kiểm thử và kết quả",
        "9. Sử dụng AI trong đồ án",
        "10. Kết luận và hướng phát triển",
    ]),
    ("1. GIỚI THIỆU ĐỀ TÀI", [
        "Wazuh là nền tảng giám sát an ninh có khả năng thu thập và tạo cảnh báo từ nhiều máy trạm, máy chủ và thiết bị. Tuy nhiên, dữ liệu cảnh báo dạng JSON khó theo dõi nếu chỉ đọc trực tiếp từ file log.",
        "Đồ án xây dựng một ứng dụng desktop bằng Python để nhập cảnh báo Wazuh, lưu bằng SQLite, thống kê dữ liệu, hiển thị bảng và biểu đồ, đồng thời gửi cảnh báo mức cao qua Telegram.",
        "Ứng dụng tập trung vào kỹ thuật đã học: kiểu dữ liệu, điều kiện, vòng lặp, hàm, module, xử lý ngoại lệ, lập trình hướng đối tượng và GUI Tkinter.",
    ]),
    ("2. MỤC TIÊU VÀ PHẠM VI", [
        "Mục tiêu: xây dựng công cụ trực quan hóa cảnh báo dễ cài đặt, dễ sử dụng và dễ giải thích khi bảo vệ.",
        "Chức năng trong phạm vi: nhập JSON, chuẩn hóa cảnh báo, lưu SQLite, chống trùng, dashboard, biểu đồ, tìm kiếm, lọc, xem chi tiết và gửi Telegram theo ngưỡng.",
        "Ngoài phạm vi: Machine Learning, xử lý dữ liệu lớn thời gian thực, quản lý nhiều người dùng, tự động chặn IP và thay thế Wazuh Dashboard.",
        "Chương trình có chế độ demo offline để không phụ thuộc Wazuh hoặc Internet khi thuyết trình.",
    ]),
    ("3. CƠ SỞ LÝ THUYẾT", [
        "Python được sử dụng làm ngôn ngữ chính. Tkinter xây dựng cửa sổ, nút bấm và bảng Treeview. Matplotlib tạo biểu đồ. SQLite lưu dữ liệu trong một file và không cần máy chủ database riêng.",
        "JSON là định dạng đầu vào của cảnh báo Wazuh. PyYAML đọc cấu hình. Requests gọi Telegram Bot API.",
        "OOP được áp dụng qua lớp Alert và các lớp dịch vụ. try/except xử lý lỗi file, JSON, database và kết nối mạng.",
    ]),
    ("4. PHÂN TÍCH VÀ THIẾT KẾ HỆ THỐNG", [
        "Luồng tổng quát: JSON Wazuh → AlertReader → Alert → DatabaseService → AnalysisService → Tkinter/Matplotlib.",
        "Luồng Telegram: cảnh báo mới → kiểm tra level → định dạng message → Telegram Bot API → cập nhật trạng thái đã gửi.",
        "Cấu trúc source gồm models, services và ui. models biểu diễn dữ liệu; services thực hiện nghiệp vụ; ui tiếp nhận thao tác và hiển thị kết quả.",
        "main.py đọc cấu hình, khởi tạo database và mở cửa sổ chính.",
    ]),
    ("5. THIẾT KẾ DỮ LIỆU", [
        "Database data/alerts.db được tự tạo ở lần chạy đầu. Những lần sau ứng dụng sử dụng lại file đã có.",
        "Database có một bảng alerts. Mỗi dòng là một cảnh báo Wazuh. alert_id là khóa chính để chống trùng.",
        "Các cột chính: alert_id, timestamp, agent_id, agent_name, agent_ip, rule_id, rule_level, description, groups_json, location, telegram_sent và raw_json.",
        "File JSON chỉ là đầu vào. Sau khi nhập, GUI đọc dữ liệu từ SQLite để tạo bảng và biểu đồ.",
    ]),
    ("6. XÂY DỰNG CHƯƠNG TRÌNH", [
        "AlertReader.read_file() đọc JSON array, một JSON object, JSON Lines hoặc kết quả API có data.affected_items.",
        "Alert.from_wazuh_dict() lấy các trường cần thiết và chuyển rule_level thành số nguyên. Nếu thiếu ID, chương trình tạo ID ổn định.",
        "DatabaseService.save_alerts() dùng INSERT OR IGNORE. DatabaseService.get_alerts() đọc và lọc dữ liệu.",
        "AnalysisService phân loại level: thấp 0–4, trung bình 5–7, cao 8–11, nghiêm trọng 12–15.",
        "MainWindow điều phối thao tác người dùng và nhúng ba biểu đồ Matplotlib vào Tkinter.",
    ]),
    ("7. CÁC CHỨC NĂNG CHÍNH", [
        "Dashboard: tổng số cảnh báo, số cảnh báo cao, số agent và số cảnh báo đã gửi Telegram.",
        "Biểu đồ: số cảnh báo theo mức độ, theo ngày và Top agent.",
        "Danh sách: hiển thị thời gian, agent, IP, rule, level, mô tả và trạng thái Telegram.",
        "Tìm kiếm và lọc: theo từ khóa, nhóm mức độ và tên agent.",
        "Nhập JSON: kiểm tra dữ liệu, bỏ qua bản ghi lỗi, chống trùng và làm mới giao diện.",
        "Telegram: mặc định tắt; khi cấu hình hợp lệ chỉ gửi cảnh báo mới đạt ngưỡng.",
    ]),
    ("8. KIỂM THỬ VÀ KẾT QUẢ", [
        "Dataset mẫu gồm 12 cảnh báo, 4 agent và nhiều mức độ khác nhau.",
        "Tám unit test kiểm tra đọc JSON, phát hiện bản ghi lỗi, số liệu tổng quan, phân loại mức độ, Top agent, chống trùng SQLite và điều kiện Telegram.",
        "Kết quả: 8/8 kiểm thử đạt. GUI smoke test mở thành công và tải đủ 12 cảnh báo.",
        "Trường hợp lỗi đã xử lý: file rỗng, JSON sai, thiếu timestamp, level không phải số, mất mạng và cấu hình Telegram thiếu.",
    ]),
    ("9. SỬ DỤNG AI TRONG ĐỒ ÁN", [
        "AI được dùng để hỗ trợ phân tích yêu cầu, đề xuất cấu trúc thư mục, tạo bản nháp code, kiểm tra lỗi và soạn tài liệu.",
        "Sinh viên chịu trách nhiệm chạy thử, đọc hiểu, kiểm tra kết quả, thay đổi cấu hình và trình bày mã nguồn.",
        "Thông tin chi tiết về prompt, nội dung hỗ trợ và cách kiểm chứng được ghi trong docs/06_KHAI_BAO_SU_DUNG_AI.md.",
    ]),
    ("10. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN", [
        "Đồ án đã xây dựng được ứng dụng desktop trực quan hóa cảnh báo Wazuh, lưu trữ SQLite và gửi Telegram theo ngưỡng.",
        "Thiết kế đơn giản nhưng thể hiện đầy đủ các kiến thức Python chính trong môn học.",
        "Hướng phát triển: đọc alerts.json tự động, kết nối Wazuh API, bổ sung biểu đồ nhóm rule và cho phép xuất CSV. Các phần này chỉ thực hiện sau khi phiên bản cơ bản ổn định.",
    ]),
    ("TÀI LIỆU THAM KHẢO", [
        "[1] Slide môn Lập trình Python: kiểu dữ liệu, điều kiện, vòng lặp, hàm, module, exception, OOP và GUI.",
        "[2] Python Documentation — sqlite3, json, pathlib và tkinter.",
        "[3] Matplotlib Documentation.",
        "[4] Telegram Bot API Documentation.",
        "[5] Wazuh Documentation — Alert management.",
    ]),
]


SLIDES = [
    ("ĐỒ ÁN LẬP TRÌNH PYTHON", [PROJECT_TITLE, "Sinh viên: [HỌ VÀ TÊN] — MSSV: [MSSV]", "Giảng viên: [TÊN GIẢNG VIÊN]"]),
    ("1. Bài toán", ["Wazuh tạo nhiều cảnh báo dạng JSON", "Khó quan sát nhanh bằng file log", "Cần bảng, biểu đồ và thông báo Telegram"]),
    ("2. Mục tiêu", ["Ứng dụng desktop dễ sử dụng", "Nhập và lưu cảnh báo", "Thống kê trực quan", "Gửi cảnh báo mức cao"]),
    ("3. Công nghệ", ["Python + Tkinter", "SQLite", "Matplotlib", "JSON + YAML", "Telegram Bot API"]),
    ("4. Kiến trúc", ["JSON Wazuh", "↓ AlertReader → Alert", "↓ SQLite", "↓ AnalysisService", "Dashboard + Telegram"]),
    ("5. Cấu trúc dữ liệu", ["Một bảng alerts", "alert_id là khóa chính", "rule_level phục vụ phân loại", "telegram_sent lưu trạng thái", "raw_json giữ dữ liệu gốc"]),
    ("6. Chức năng chính", ["Dashboard và ba biểu đồ", "Danh sách cảnh báo", "Tìm kiếm, lọc, xem chi tiết", "Nhập JSON và chống trùng"]),
    ("7. Quy tắc phân tích", ["Thấp: 0–4", "Trung bình: 5–7", "Cao: 8–11", "Nghiêm trọng: 12–15", "Telegram: level ≥ ngưỡng cấu hình"]),
    ("8. Demo và kiểm thử", ["Dataset: 12 cảnh báo / 4 agent", "8/8 unit test đạt", "GUI tải đủ dữ liệu", "Demo được khi không có Internet"]),
    ("9. Kết luận", ["Đạt mục tiêu đề tài", "Bám sát kiến thức Python", "Dễ cài đặt và trình bày", "Hướng tới kết nối Wazuh trực tiếp", "Cảm ơn thầy/cô!"]),
]


def make_dirs():
    for directory in (REPORT_DIR, SLIDES_DIR, DEMO_DIR, DOCS_DIR):
        directory.mkdir(parents=True, exist_ok=True)


def w_paragraph(text, style=None, center=False, bold=False, size=24, page_break=False):
    p_pr = []
    if style:
        p_pr.append(f'<w:pStyle w:val="{style}"/>')
    if center:
        p_pr.append('<w:jc w:val="center"/>')
    if page_break:
        p_pr.append('<w:pageBreakBefore/>')
    ppr = f"<w:pPr>{''.join(p_pr)}</w:pPr>" if p_pr else ""
    rpr = f'<w:rPr>{"<w:b/>" if bold else ""}<w:sz w:val="{size}"/><w:szCs w:val="{size}"/></w:rPr>'
    return f'<w:p>{ppr}<w:r>{rpr}<w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>'


def create_docx(path):
    paragraphs = []
    for section_index, (title, lines) in enumerate(REPORT_SECTIONS):
        paragraphs.append(w_paragraph(title, style="Title" if section_index == 0 else "Heading1", center=section_index == 0, bold=True, size=34 if section_index == 0 else 28, page_break=section_index > 0))
        for line in lines:
            paragraphs.append(w_paragraph(line, center=section_index == 0, size=24))

    document_xml = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>
{''.join(paragraphs)}
<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1701"/></w:sectPr>
</w:body></w:document>'''
    styles_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="26"/></w:rPr><w:pPr><w:spacing w:after="120" w:line="360" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:qFormat/></w:style>
</w:styles>'''
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>'''
    root_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>'''
    doc_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>'''
    core = core_properties("Báo cáo đồ án Lập trình Python")
    app = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>Microsoft Office Word</Application></Properties>'''
    with ZipFile(path, "w", ZIP_DEFLATED) as archive:
        files = {"[Content_Types].xml": content_types, "_rels/.rels": root_rels, "word/document.xml": document_xml, "word/styles.xml": styles_xml, "word/_rels/document.xml.rels": doc_rels, "docProps/core.xml": core, "docProps/app.xml": app}
        for name, content in files.items():
            archive.writestr(name, content.encode("utf-8"))


def core_properties(title):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>{escape(title)}</dc:title><dc:creator>Sinh viên</dc:creator><cp:lastModifiedBy>Sinh viên</cp:lastModifiedBy><dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created><dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified></cp:coreProperties>'''


def shape(shape_id, name, text, x, y, cx, cy, font_size=2400, bold=False, color="FFFFFF", fill=None):
    fill_xml = f'<p:solidFill><a:srgbClr val="{fill}"/></p:solidFill>' if fill else '<p:noFill/>'
    paragraphs = []
    for line in text:
        paragraphs.append(f'''<a:p><a:r><a:rPr lang="vi-VN" sz="{font_size}" b="{1 if bold else 0}"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill></a:rPr><a:t>{escape(line)}</a:t></a:r><a:endParaRPr lang="vi-VN" sz="{font_size}"/></a:p>''')
    return f'''<p:sp><p:nvSpPr><p:cNvPr id="{shape_id}" name="{name}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="roundRect"><a:avLst/></a:prstGeom>{fill_xml}<a:ln><a:noFill/></a:ln></p:spPr><p:txBody><a:bodyPr wrap="square" anchor="mid" lIns="180000" rIns="180000" tIns="90000" bIns="90000"/><a:lstStyle/>{''.join(paragraphs)}</p:txBody></p:sp>'''


def slide_xml(index, title, bullets):
    accent = ["00B8D9", "6C63FF", "00A86B", "F59E0B", "E8590C", "D6336C", "7048E8", "1971C2", "2F9E44", "0B7285"][index - 1]
    items = [f"• {item}" for item in bullets]
    body = shape(2, "Title", [title], 650000, 450000, 10800000, 1000000, 3000, True, "FFFFFF", accent)
    body += shape(3, "Body", items, 1000000, 1800000, 9800000, 4300000, 2100, False, "24324A", "F5F7FB")
    body += shape(4, "Footer", [f"Đồ án Lập trình Python  |  {index}/10"], 700000, 6400000, 10500000, 350000, 1100, False, "607080", None)
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:cSld><p:bg><p:bgPr><a:solidFill><a:srgbClr val="E9EEF5"/></a:solidFill><a:effectLst/></p:bgPr></p:bg><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>{body}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'''


def create_pptx(path):
    slide_overrides = ''.join(f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>' for i in range(1, 11))
    content_types = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/><Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/><Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/><Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>{slide_overrides}<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/><Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/></Types>'''
    root_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/><Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/></Relationships>'''
    sld_ids = ''.join(f'<p:sldId id="{255+i}" r:id="rId{1+i}"/>' for i in range(1, 11))
    presentation = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst><p:sldIdLst>{sld_ids}</p:sldIdLst><p:sldSz cx="12192000" cy="6858000" type="screen16x9"/><p:notesSz cx="6858000" cy="9144000"/></p:presentation>'''
    rels = ['<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>']
    rels += [f'<Relationship Id="rId{1+i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>' for i in range(1, 11)]
    presentation_rels = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{''.join(rels)}</Relationships>'''
    master = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld><p:clrMap accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" bg1="lt1" bg2="lt2" folHlink="folHlink" hlink="hlink" tx1="dk1" tx2="dk2"/><p:sldLayoutIdLst><p:sldLayoutId id="1" r:id="rId1"/></p:sldLayoutIdLst><p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles></p:sldMaster>'''
    master_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/></Relationships>'''
    layout = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank"><p:cSld name="Blank"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>'''
    layout_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/></Relationships>'''
    theme = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Simple"><a:themeElements><a:clrScheme name="Simple"><a:dk1><a:srgbClr val="000000"/></a:dk1><a:lt1><a:srgbClr val="FFFFFF"/></a:lt1><a:dk2><a:srgbClr val="24324A"/></a:dk2><a:lt2><a:srgbClr val="E9EEF5"/></a:lt2><a:accent1><a:srgbClr val="00B8D9"/></a:accent1><a:accent2><a:srgbClr val="6C63FF"/></a:accent2><a:accent3><a:srgbClr val="00A86B"/></a:accent3><a:accent4><a:srgbClr val="F59E0B"/></a:accent4><a:accent5><a:srgbClr val="E8590C"/></a:accent5><a:accent6><a:srgbClr val="D6336C"/></a:accent6><a:hlink><a:srgbClr val="0000FF"/></a:hlink><a:folHlink><a:srgbClr val="800080"/></a:folHlink></a:clrScheme><a:fontScheme name="Simple"><a:majorFont><a:latin typeface="Segoe UI"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont><a:minorFont><a:latin typeface="Segoe UI"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont></a:fontScheme><a:fmtScheme name="Simple"><a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst><a:lnStyleLst><a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst><a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst><a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst></a:fmtScheme></a:themeElements></a:theme>'''
    app = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>Microsoft Office PowerPoint</Application><Slides>10</Slides></Properties>'''
    with ZipFile(path, "w", ZIP_DEFLATED) as archive:
        fixed = {"[Content_Types].xml": content_types, "_rels/.rels": root_rels, "ppt/presentation.xml": presentation, "ppt/_rels/presentation.xml.rels": presentation_rels, "ppt/slideMasters/slideMaster1.xml": master, "ppt/slideMasters/_rels/slideMaster1.xml.rels": master_rels, "ppt/slideLayouts/slideLayout1.xml": layout, "ppt/slideLayouts/_rels/slideLayout1.xml.rels": layout_rels, "ppt/theme/theme1.xml": theme, "docProps/core.xml": core_properties("Slide đồ án Lập trình Python"), "docProps/app.xml": app}
        for name, content in fixed.items():
            archive.writestr(name, content.encode("utf-8"))
        slide_rel = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/></Relationships>'''
        for index, (title, bullets) in enumerate(SLIDES, start=1):
            archive.writestr(f"ppt/slides/slide{index}.xml", slide_xml(index, title, bullets).encode("utf-8"))
            archive.writestr(f"ppt/slides/_rels/slide{index}.xml.rels", slide_rel.encode("utf-8"))


def write_supporting_docs():
    (DEMO_DIR / "KICH_BAN_DEMO.md").write_text('''# KỊCH BẢN DEMO (5–7 PHÚT)\n\n1. Giới thiệu mục tiêu: nhập JSON, phân tích và gửi Telegram.\n2. Chạy `python main.py`; giới thiệu bốn thẻ số liệu và ba biểu đồ.\n3. Mở tab Danh sách cảnh báo; tìm từ khóa `SSH`.\n4. Chọn mức độ `Cao`; chọn agent `WEB-SERVER`.\n5. Nhấp đúp một dòng để xem dữ liệu gốc.\n6. Bấm Nhập file JSON và chọn `data/sample_alerts.json`; giải thích dữ liệu trùng không được lưu lại.\n7. Giới thiệu `config.yml`; Telegram mặc định tắt để demo an toàn.\n8. Chạy `python -m unittest discover -s tests -v`; kết thúc với kết quả 8/8 test đạt.\n\n## Dự phòng\n\nNếu mất Internet, demo toàn bộ phần JSON, SQLite, bảng và biểu đồ. Không bật Telegram bằng token thật trong video công khai.\n''', encoding="utf-8")
    (DOCS_DIR / "06_KHAI_BAO_SU_DUNG_AI.md").write_text('''# KHAI BÁO SỬ DỤNG AI\n\n## Công cụ\n\nOpenAI Codex được sử dụng trong quá trình xây dựng đồ án.\n\n## Phạm vi hỗ trợ\n\n- Phân tích yêu cầu và đề xuất cấu trúc project.\n- Tạo bản nháp source code, dataset, test và tài liệu.\n- Phát hiện lỗi khóa SQLite và trường hợp gửi Telegram trùng.\n- Hỗ trợ soạn báo cáo, slide và kịch bản demo.\n\n## Prompt tiêu biểu\n\n1. “Xây dựng GUI desktop Python để phân tích dữ liệu cảnh báo Wazuh bằng biểu đồ và gửi Telegram.”\n2. “Ưu tiên code đơn giản, bám sát kiểu dữ liệu, điều kiện, vòng lặp, hàm, module, exception, OOP và GUI.”\n3. “Tạo tài liệu flow và đặc tả tính năng để source, báo cáo, slide và demo không lệch nhau.”\n4. “Giải thích các hàm và biến ảnh hưởng trực tiếp tới kết quả.”\n\n## Trách nhiệm của sinh viên\n\nSinh viên kiểm tra source, chạy unit test, đối chiếu kết quả với dataset, bảo vệ token, đọc hiểu từng hàm và chịu trách nhiệm về nội dung nộp bài. AI không thay thế việc kiểm chứng kết quả.\n\n## Skill/phương pháp\n\nPhương pháp sử dụng AI: chia bài toán thành các phần nhỏ; yêu cầu AI giải thích flow; kiểm thử sau mỗi thay đổi; ghi lại prompt và kiểm tra thủ công trước khi sử dụng. Không sử dụng skill bên ngoài chuyên biệt trong phần code cốt lõi.\n''', encoding="utf-8")
    (DOCS_DIR / "05_CAU_HOI_BAO_VE.md").write_text('''# CÂU HỎI BẢO VỆ VÀ TRẢ LỜI NGẮN\n\n1. **Vì sao dùng SQLite?** Vì SQLite là database dạng file, không cần server và phù hợp dữ liệu đồ án nhỏ.\n2. **JSON được dùng thế nào?** JSON là đầu vào; Python chuẩn hóa rồi lưu từng cảnh báo vào SQLite.\n3. **Vì sao cần alert_id?** Đây là khóa chính giúp nhận diện và chống lưu trùng cảnh báo.\n4. **Vì sao dùng OOP?** Lớp Alert gom dữ liệu và hành vi chuyển đổi của một cảnh báo.\n5. **Biểu đồ lấy dữ liệu ở đâu?** GUI đọc Alert từ SQLite rồi AnalysisService nhóm và đếm.\n6. **Telegram gửi khi nào?** Khi cấu hình sẵn sàng và rule_level lớn hơn hoặc bằng minimum_level.\n7. **Nếu mất Internet?** Phần phân tích vẫn chạy; Telegram trả lỗi được try/except xử lý.\n8. **Tại sao không commit config.yml?** Vì file này có thể chứa Bot Token và Chat ID thật.\n9. **Cảnh báo trùng được xử lý thế nào?** alert_id là khóa chính và INSERT OR IGNORE bỏ qua ID đã tồn tại.\n10. **Đóng chương trình có mất dữ liệu không?** Không, dữ liệu nằm trong data/alerts.db và được dùng lại ở lần chạy sau.\n''', encoding="utf-8")


def main():
    make_dirs()
    create_docx(REPORT_DIR / "BAO_CAO_DO_AN.docx")
    create_pptx(SLIDES_DIR / "SLIDE_THUYET_TRINH_10_TRANG.pptx")
    write_supporting_docs()
    print("Deliverables generated successfully.")


if __name__ == "__main__":
    main()
