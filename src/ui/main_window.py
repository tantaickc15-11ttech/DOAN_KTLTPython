"""Cửa sổ chính, bảng cảnh báo và các biểu đồ phân tích."""

import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from src.services.alert_reader import AlertReader
from src.services.analysis_service import AnalysisService
from src.services.telegram_service import TelegramService


class MainWindow(tk.Tk):
    """Giao diện chính của chương trình."""

    def __init__(self, database, config, sample_file):
        super().__init__()
        self.database = database
        self.config_data = config
        self.sample_file = sample_file
        self.telegram = TelegramService(config.get("telegram", {}))
        self.current_alerts = []

        app_config = config.get("app", {})
        self.title(app_config.get("title", "Wazuh Security Monitor"))
        self.geometry("1200x760")
        self.minsize(1000, 650)

        self._configure_style()
        self._create_toolbar()
        self._create_notebook()
        self._create_status_bar()
        self._auto_load_sample(app_config)
        self.refresh_data()

    def _configure_style(self):
        style = ttk.Style(self)
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"))
        style.configure("CardTitle.TLabel", font=("Segoe UI", 10))
        style.configure("CardValue.TLabel", font=("Segoe UI", 22, "bold"))
        style.configure("Treeview", rowheight=28)

    def _create_toolbar(self):
        toolbar = ttk.Frame(self, padding=(12, 10))
        toolbar.pack(fill="x")
        ttk.Label(toolbar, text="Wazuh Security Monitor", style="Title.TLabel").pack(
            side="left"
        )
        ttk.Button(toolbar, text="Nhập file JSON", command=self.import_json).pack(
            side="right", padx=4
        )
        ttk.Button(toolbar, text="Làm mới", command=self.refresh_data).pack(
            side="right", padx=4
        )

    def _create_notebook(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=(0, 8))

        self.dashboard_tab = ttk.Frame(self.notebook, padding=10)
        self.alerts_tab = ttk.Frame(self.notebook, padding=10)
        self.settings_tab = ttk.Frame(self.notebook, padding=10)

        self.notebook.add(self.dashboard_tab, text="Tổng quan")
        self.notebook.add(self.alerts_tab, text="Danh sách cảnh báo")
        self.notebook.add(self.settings_tab, text="Trạng thái hệ thống")

        self._create_dashboard()
        self._create_alert_table()
        self._create_settings()

    def _create_dashboard(self):
        cards = ttk.Frame(self.dashboard_tab)
        cards.pack(fill="x", pady=(0, 10))
        self.card_values = {}

        items = [
            ("total", "Tổng cảnh báo"),
            ("high", "Mức cao trở lên"),
            ("agents", "Số agent"),
            ("sent", "Đã gửi Telegram"),
        ]
        for index, (key, title) in enumerate(items):
            card = ttk.LabelFrame(cards, padding=12)
            card.grid(row=0, column=index, padx=5, sticky="nsew")
            cards.columnconfigure(index, weight=1)
            ttk.Label(card, text=title, style="CardTitle.TLabel").pack()
            label = ttk.Label(card, text="0", style="CardValue.TLabel")
            label.pack(pady=(5, 0))
            self.card_values[key] = label

        self.figure = Figure(figsize=(10, 5), dpi=100)
        self.chart_canvas = FigureCanvasTkAgg(self.figure, master=self.dashboard_tab)
        self.chart_canvas.get_tk_widget().pack(fill="both", expand=True)

    def _create_alert_table(self):
        filters = ttk.Frame(self.alerts_tab)
        filters.pack(fill="x", pady=(0, 8))

        ttk.Label(filters, text="Tìm kiếm:").pack(side="left")
        self.keyword_var = tk.StringVar()
        ttk.Entry(filters, textvariable=self.keyword_var, width=28).pack(
            side="left", padx=(5, 12)
        )

        ttk.Label(filters, text="Mức độ:").pack(side="left")
        self.severity_var = tk.StringVar(value="Tất cả")
        self.severity_box = ttk.Combobox(
            filters,
            textvariable=self.severity_var,
            values=["Tất cả", "Thấp", "Trung bình", "Cao", "Nghiêm trọng"],
            state="readonly",
            width=14,
        )
        self.severity_box.pack(side="left", padx=(5, 12))

        ttk.Label(filters, text="Agent:").pack(side="left")
        self.agent_var = tk.StringVar(value="Tất cả")
        self.agent_box = ttk.Combobox(
            filters, textvariable=self.agent_var, state="readonly", width=18
        )
        self.agent_box.pack(side="left", padx=(5, 12))
        ttk.Button(filters, text="Lọc", command=self.apply_filters).pack(side="left")
        ttk.Button(filters, text="Xóa lọc", command=self.clear_filters).pack(
            side="left", padx=5
        )
        ttk.Button(filters, text="Xem chi tiết", command=self.show_detail).pack(
            side="right"
        )

        table_frame = ttk.Frame(self.alerts_tab)
        table_frame.pack(fill="both", expand=True)
        columns = (
            "timestamp",
            "agent",
            "ip",
            "rule",
            "level",
            "description",
            "telegram",
        )
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        headings = {
            "timestamp": "Thời gian",
            "agent": "Agent",
            "ip": "IP",
            "rule": "Rule ID",
            "level": "Level",
            "description": "Mô tả",
            "telegram": "Telegram",
        }
        widths = {
            "timestamp": 165,
            "agent": 130,
            "ip": 110,
            "rule": 80,
            "level": 60,
            "description": 390,
            "telegram": 90,
        }
        for column in columns:
            self.tree.heading(column, text=headings[column])
            self.tree.column(column, width=widths[column], anchor="w")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.tree.bind("<Double-1>", lambda _event: self.show_detail())

    def _create_settings(self):
        ttk.Label(
            self.settings_tab, text="Trạng thái cấu hình", style="Title.TLabel"
        ).pack(anchor="w", pady=(0, 12))
        app_config = self.config_data.get("app", {})
        telegram_config = self.config_data.get("telegram", {})
        status_items = [
            ("Chế độ demo", "Bật" if app_config.get("demo_mode", True) else "Tắt"),
            ("Gửi Telegram", "Sẵn sàng" if self.telegram.is_ready() else "Đang tắt"),
            ("Ngưỡng Telegram", str(telegram_config.get("minimum_level", 8))),
            ("Cơ sở dữ liệu", str(self.database.database_path)),
        ]
        for title, value in status_items:
            row = ttk.Frame(self.settings_tab, padding=8)
            row.pack(fill="x")
            ttk.Label(row, text=f"{title}:", width=22).pack(side="left")
            ttk.Label(row, text=value).pack(side="left")

        note = (
            "Để cấu hình Telegram, sao chép config/config.example.yml thành "
            "config/config.yml, điền thông tin thật và bật enabled. "
            "File config.yml không được đưa lên GitHub."
        )
        ttk.Label(self.settings_tab, text=note, wraplength=800).pack(
            anchor="w", pady=16
        )

    def _create_status_bar(self):
        self.status_var = tk.StringVar(value="Sẵn sàng")
        ttk.Label(self, textvariable=self.status_var, relief="sunken", anchor="w").pack(
            fill="x", side="bottom"
        )

    def _auto_load_sample(self, app_config):
        if not app_config.get("auto_load_sample", True):
            return
        if self.database.get_alerts() or not self.sample_file.exists():
            return
        try:
            alerts, _errors = AlertReader.read_file(self.sample_file)
            self.database.save_alerts(alerts)
        except (OSError, ValueError) as error:
            self.status_var.set(f"Không tải được dữ liệu mẫu: {error}")

    def import_json(self):
        file_path = filedialog.askopenfilename(
            title="Chọn file cảnh báo Wazuh",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if not file_path:
            return

        try:
            alerts, errors = AlertReader.read_file(file_path)
            known_ids = {
                alert.alert_id for alert in self.database.get_alerts()
            }
            new_alerts = []
            for alert in alerts:
                if alert.alert_id not in known_ids:
                    new_alerts.append(alert)
                    known_ids.add(alert.alert_id)

            inserted, duplicated = self.database.save_alerts(alerts)
            sent = self._send_new_alerts(new_alerts)
            self.refresh_data()
            messagebox.showinfo(
                "Kết quả nhập dữ liệu",
                f"Thêm mới: {inserted}\nTrùng: {duplicated}\n"
                f"Bản ghi lỗi: {len(errors)}\nĐã gửi Telegram: {sent}",
            )
        except (OSError, ValueError) as error:
            messagebox.showerror("Lỗi nhập dữ liệu", str(error))

    def _send_new_alerts(self, alerts):
        sent = 0
        for alert in alerts:
            if not self.telegram.should_send(alert):
                continue
            success, _message = self.telegram.send_alert(alert)
            if success:
                self.database.mark_telegram_sent(alert.alert_id)
                sent += 1
        return sent

    def refresh_data(self):
        self.current_alerts = self.database.get_alerts()
        self._update_agent_filter()
        self._update_cards(self.current_alerts)
        self._update_charts(self.current_alerts)
        self._update_table(self.current_alerts)
        self.status_var.set(f"Đang hiển thị {len(self.current_alerts)} cảnh báo")

    def apply_filters(self):
        alerts = self.database.get_alerts(
            keyword=self.keyword_var.get(),
            severity=self.severity_var.get(),
            agent=self.agent_var.get(),
        )
        self.current_alerts = alerts
        self._update_table(alerts)
        self.status_var.set(f"Tìm thấy {len(alerts)} cảnh báo")

    def clear_filters(self):
        self.keyword_var.set("")
        self.severity_var.set("Tất cả")
        self.agent_var.set("Tất cả")
        self.refresh_data()

    def _update_agent_filter(self):
        values = ["Tất cả"] + self.database.get_agent_names()
        self.agent_box.configure(values=values)
        if self.agent_var.get() not in values:
            self.agent_var.set("Tất cả")

    def _update_cards(self, alerts):
        overview = AnalysisService.overview(alerts)
        for key, label in self.card_values.items():
            label.configure(text=str(overview[key]))

    def _update_table(self, alerts):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for alert in alerts:
            self.tree.insert(
                "",
                "end",
                iid=alert.alert_id,
                values=(
                    alert.timestamp,
                    alert.agent_name,
                    alert.agent_ip,
                    alert.rule_id,
                    alert.rule_level,
                    alert.description,
                    "Đã gửi" if alert.telegram_sent else "Chưa gửi",
                ),
            )

    def _update_charts(self, alerts):
        self.figure.clear()
        severity = AnalysisService.count_by_severity(alerts)
        dates = AnalysisService.count_by_date(alerts)
        agents = AnalysisService.top_agents(alerts)

        chart1 = self.figure.add_subplot(131)
        chart1.bar(severity.keys(), severity.values(), color=["#4caf50", "#ffb300", "#fb8c00", "#e53935"])
        chart1.set_title("Cảnh báo theo mức độ")
        chart1.tick_params(axis="x", rotation=25)

        chart2 = self.figure.add_subplot(132)
        chart2.plot(list(dates.keys()), list(dates.values()), marker="o", color="#1976d2")
        chart2.set_title("Cảnh báo theo ngày")
        chart2.tick_params(axis="x", rotation=35)

        chart3 = self.figure.add_subplot(133)
        chart3.barh(list(agents.keys()), list(agents.values()), color="#7e57c2")
        chart3.set_title("Top agent")
        chart3.invert_yaxis()

        self.figure.tight_layout()
        self.chart_canvas.draw()

    def show_detail(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một cảnh báo.")
            return

        alert_id = selected[0]
        alert = next(
            (item for item in self.current_alerts if item.alert_id == alert_id), None
        )
        if alert is None:
            messagebox.showerror("Không tìm thấy", "Không tìm thấy cảnh báo đã chọn.")
            return

        window = tk.Toplevel(self)
        window.title(f"Chi tiết cảnh báo {alert.alert_id}")
        window.geometry("720x520")

        text = tk.Text(window, wrap="word", padx=12, pady=12)
        text.pack(fill="both", expand=True)
        detail = {
            "Mã cảnh báo": alert.alert_id,
            "Thời gian": alert.timestamp,
            "Agent ID": alert.agent_id,
            "Tên agent": alert.agent_name,
            "IP": alert.agent_ip,
            "Rule ID": alert.rule_id,
            "Level": alert.rule_level,
            "Mô tả": alert.description,
            "Nhóm": ", ".join(alert.groups),
            "Nguồn log": alert.location,
            "Đã gửi Telegram": "Có" if alert.telegram_sent else "Không",
        }
        for key, value in detail.items():
            text.insert("end", f"{key}: {value}\n")
        text.insert(
            "end",
            "\nDữ liệu gốc:\n" + json.dumps(alert.raw_data, ensure_ascii=False, indent=2),
        )
        text.configure(state="disabled")
