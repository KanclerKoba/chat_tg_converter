import json
from bs4 import BeautifulSoup
from datetime import datetime
import re

def clean_text(text: str) -> str:
    """Удаляет служебные подписи и лишние пробелы."""
    if not isinstance(text, str):
        return ""
    patterns = [
        r"\(File not included\. Change data exporting settings to download\.\)",
        r"\(Voice message not included\. Change data exporting settings to download\.\)",
        r"\(Sticker not included\. Change data exporting settings to download\.\)",
        r"\(Video not included\. Change data exporting settings to download\.\)",
        r"\(Audio file not included\. Change data exporting settings to download\.\)",
    ]
    for p in patterns:
        text = re.sub(p, "", text)
    return re.sub(r"\s+", " ", text).strip()

def convert_html_to_text(file_like, file_out):
    """Конвертирует HTML-экспорт Telegram в текст."""
    soup = BeautifulSoup(file_like, "html.parser")
    messages = soup.find_all("div", class_="message")

    for msg in messages:
        if "service" in msg.get("class", []):
            continue
        try:
            from_name = msg.find("div", class_="from_name").text.strip()
            date = msg.find("div", class_="date").text.strip()
            text_tag = msg.find("div", class_="text")
            text = text_tag.text.strip() if text_tag else ""
            text = clean_text(text)
            if text:
                file_out.write(f"{date} | {from_name}:\n{text}\n\n")
        except AttributeError:
            continue

def convert_json_to_text(
    file_like,
    file_out,
    fmt="txt",
    include_replies=False,
    include_forwards=False,
    include_reactions=False,
    anonymize=False,
):
    """Конвертирует JSON-экспорт Telegram в текст/Markdown.
    Параметр anonymize заменяет имя автора на 'user[ID]'."""
    data = json.load(file_like)

    for message in data.get("messages", []):
        if message.get("type") == "service":
            continue

        # --- автор и дата ---
        date = datetime.fromisoformat(message["date"]).strftime("%Y-%m-%d %H:%M:%S")
        if anonymize:
            author_label = f"user[{message.get('id', '?')}]"
        else:
            author_label = message.get("from", "Unknown")

        # --- заголовок (ID в заголовке, если включены ответы) ---
        if include_replies:
            msg_id = message.get("id", "?")
            header = f"{msg_id} | {date} | {author_label}:\n"
        else:
            header = f"{date} | {author_label}:\n"

        # --- ответы на сообщения ---
        reply_info = ""
        if include_replies and message.get("reply_to_message_id"):
            reply_to = message["reply_to_message_id"]
            reply_info = f"(ответ на сообщение #{reply_to})\n"

        # --- пересылки ---
        forward_info = ""
        if include_forwards and message.get("forward_from"):
            ffrom = message["forward_from"]
            fdate = message.get("forward_date", "")
            forward_info = f"[Переслано от {ffrom}"
            if fdate:
                try:
                    fdate_fmt = datetime.fromisoformat(fdate).strftime("%Y-%m-%d %H:%M:%S")
                except Exception:
                    fdate_fmt = str(fdate)
                forward_info += f", {fdate_fmt}"
            forward_info += "]\n"

        # --- текст сообщения ---
        text = message.get("text", "")
        if isinstance(text, list):
            parts = []
            for t in text:
                if isinstance(t, str):
                    parts.append(t)
                elif isinstance(t, dict) and "text" in t:
                    parts.append(t["text"])
            text = " ".join(parts)
        text = clean_text(text)
        if not text:
            continue

        # --- реакции ---
        reactions_info = ""
        reacts = message.get("reactions", [])
        if include_reactions and reacts:
            pairs = []
            for r in reacts:
                emoji = r.get("emoji")
                count = r.get("count")
                if emoji is None or count is None:
                    continue
                pairs.append(f"{emoji}×{count}")
            if pairs:
                reactions_info = "[Реакции: " + ", ".join(pairs) + "]\n"

        # --- сборка и запись ---
        body = reply_info + forward_info + text + "\n" + reactions_info + "\n"
        if fmt == "md":
            file_out.write(f"**{header}{body}**")
        else:
            file_out.write(header + body)
