"""Gửi cảnh báo đủ mức độ tới Telegram Bot API."""

import html

import requests


class TelegramService:
    """Đóng gói cấu hình và thao tác gửi Telegram."""

    def __init__(self, config):
        self.enabled = bool(config.get("enabled", False))
        self.bot_token = str(config.get("bot_token", ""))
        self.chat_id = str(config.get("chat_id", ""))
        self.minimum_level = int(config.get("minimum_level", 8))
        self.timeout_seconds = int(config.get("timeout_seconds", 10))

    def is_ready(self):
        invalid_tokens = {"", "YOUR_BOT_TOKEN"}
        invalid_chats = {"", "YOUR_CHAT_ID"}
        return (
            self.enabled
            and self.bot_token not in invalid_tokens
            and self.chat_id not in invalid_chats
        )

    def should_send(self, alert):
        return self.is_ready() and alert.rule_level >= self.minimum_level

    def send_alert(self, alert):
        if not self.should_send(alert):
            return False, "Telegram đang tắt hoặc cảnh báo chưa đủ ngưỡng."

        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "parse_mode": "HTML",
            "text": self._format_message(alert),
        }

        try:
            response = requests.post(url, data=payload, timeout=self.timeout_seconds)
            response.raise_for_status()
            result = response.json()
            if result.get("ok"):
                return True, "Đã gửi Telegram."
            return False, result.get("description", "Telegram từ chối yêu cầu.")
        except (requests.RequestException, ValueError) as error:
            return False, f"Không gửi được Telegram: {error}"

    @staticmethod
    def _format_message(alert):
        return (
            "<b>WAZUH SECURITY ALERT</b>\n"
            f"Thời gian: {html.escape(alert.timestamp)}\n"
            f"Agent: {html.escape(alert.agent_name)}\n"
            f"IP: {html.escape(alert.agent_ip or 'N/A')}\n"
            f"Rule: {html.escape(alert.rule_id)}\n"
            f"Level: <b>{alert.rule_level}</b>\n"
            f"Mô tả: {html.escape(alert.description)}"
        )

