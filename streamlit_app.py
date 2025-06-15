import io
import os
import streamlit as st
from converter import convert_json_to_text, convert_html_to_text

# --- Конфигурация страницы ---
st.set_page_config(page_title="Telegram → Text", layout="centered")

# --- Выбор языка ---
lang = st.sidebar.radio(
    label="Язык / Language",
    options=["Русский", "English"],
    index=0
)

# --- Тексты интерфейса ---
if lang == "Русский":
    texts = {
        "title": "Конвертер Telegram-экспортов",
        "sidebar_header": "Дополнительная информация",
        "opt_replies": "Включать информацию об ответах",
        "opt_forwards": "Включать информацию о пересылках",
        "opt_reactions": "Включать информацию о реакциях (emoji×count)",
        "opt_anonymize": "Анонимизировать авторов (user[ID])",
        "upload_label": "Загрузите файл из Telegram-экспорта (JSON или HTML)",
        "min_len": "Минимальная длина сообщения (символов)",
        "format": "Формат вывода",
        "fmt_txt": "txt (обычный)",
        "fmt_md": "md (markdown)",
        "btn_convert": "Преобразовать",
        "preview_header": "📋 Предварительный результат",
        "download_label": "Скачать результат",
        "success": "Готово! Сообщений сохранено: {count}",
        "stop": "🛑 Завершить работу приложения",
        "stopped": "Приложение остановлено"
    }
else:
    texts = {
        "title": "Telegram Export Converter",
        "sidebar_header": "Additional Options",
        "opt_replies": "Include reply info",
        "opt_forwards": "Include forward info",
        "opt_reactions": "Include reactions (emoji×count)",
        "opt_anonymize": "Anonymize authors (user[ID])",
        "upload_label": "Upload Telegram export file (JSON or HTML)",
        "min_len": "Minimum message length (chars)",
        "format": "Output format",
        "fmt_txt": "txt (plain)",
        "fmt_md": "md (markdown)",
        "btn_convert": "Convert",
        "preview_header": "📋 Preview Output",
        "download_label": "Download result",
        "success": "Done! Messages saved: {count}",
        "stop": "🛑 Stop application",
        "stopped": "Application stopped"
    }

# --- Заголовок ---
st.title(texts["title"])

# --- Сайдбар: опции ---
st.sidebar.header(texts["sidebar_header"])
include_replies = st.sidebar.checkbox(texts["opt_replies"], value=False)
include_forwards = st.sidebar.checkbox(texts["opt_forwards"], value=False)
include_reactions = st.sidebar.checkbox(texts["opt_reactions"], value=False)
anonymize = st.sidebar.checkbox(texts["opt_anonymize"], value=False)
st.sidebar.markdown("---")

# --- Основной интерфейс ---
uploaded = st.file_uploader(
    texts["upload_label"],
    type=["json", "html"],
)

min_len = st.number_input(
    texts["min_len"],
    min_value=0,
    value=15,
    step=1,
)

output_fmt = st.radio(
    texts["format"],
    options=[texts["fmt_txt"], texts["fmt_md"]],
    horizontal=True,
)

if uploaded and st.button(texts["btn_convert"]):
    # Подготовка
    in_bytes = uploaded.read()
    in_mem = io.BytesIO(in_bytes)
    out_mem = io.StringIO()
    # Конвертация
    if uploaded.name.endswith(".json"):
        convert_json_to_text(
            io.TextIOWrapper(in_mem, encoding="utf-8"),
            out_mem,
            fmt="md" if output_fmt == texts["fmt_md"] else "txt",
            include_replies=include_replies,
            include_forwards=include_forwards,
            include_reactions=include_reactions,
            anonymize=anonymize,
        )
    else:
        html_text = in_bytes.decode("utf-8", errors="ignore")
        convert_html_to_text(html_text, out_mem)

    # Фильтрация
    raw = out_mem.getvalue().strip()
    blocks = [
        b for b in raw.split("\n\n")
        if len(b.splitlines()) >= 2 and len(b.splitlines()[1].strip()) >= min_len
    ]
    cleaned_text = "\n\n".join(blocks)

    # Предварительный просмотр
    st.subheader(texts["preview_header"])
    st.text_area(texts["download_label"], cleaned_text, height=300)

    # Скачивание
    st.success(texts["success"].format(count=len(blocks)))
    st.download_button(
        label=texts["download_label"],
        data=cleaned_text.encode("utf-8"),
        file_name="output.txt",
        mime="text/plain",
    )

# --- Кнопка остановки ---
if st.sidebar.button(texts["stop"]):
    st.warning(texts["stopped"])
    os._exit(0)
