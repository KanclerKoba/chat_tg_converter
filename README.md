# Telegram Export Converter

Мини-утилита, которая превращает выгрузку чата Telegram (JSON или HTML) в читаемый текстовый либо Markdown-файл. Интерфейс открывается прямо в браузере — нужен только Python и одна команда запуска.

## Что умеет
* Принимает **JSON** и **HTML**-экспорт Telegram.  
* Удаляет служебные подписи «(File not included …)», сжимает лишние пробелы.  
* По галочкам добавляет  
  • информацию, на какое сообщение был ответ;  
  • пометки о пересылках;  
  • счётчик реакций (❤×7, 🔥×2 …);  
  • анонимизацию: имя автора заменяется на `user[ID]`.  
* Фильтрует короткие реплики по заданной минимальной длине.  
* Переключает язык интерфейса **Русский / English**.  
* Показывает предварительный результат на странице и даёт скачать `output.txt`.

## Быстрый запуск (Windows 10/11)

```powershell
# Распакуйте проект в удобную папку, затем:
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Браузер откроет `http://localhost:8501`. Загрузите `result.json` или `messages.html`, отметьте опции, нажмите **Convert** и скачайте результат.  
> Совет: вместо команд можно запустить `start.bat` — он всё сделает сам.

## Быстрый запуск (macOS / Linux)

```bash
git clone https://github.com/<YOUR_LOGIN>/telegram_converter_app.git
cd telegram_converter_app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Состав проекта

| Файл               | Назначение                             |
| ------------------ | -------------------------------------- |
| `converter.py`     | Логика обработки JSON/HTML            |
| `streamlit_app.py` | Веб-интерфейс на Streamlit            |
| `requirements.txt` | Список Python-зависимостей            |
| `start.bat`        | Автозапуск под Windows (необязательно)|
| `README.md`        | Этот файл                             |

## Лицензия

MIT License © 2025 Кальмуцкий Владислав
