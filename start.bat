@echo off
REM — Перейти в папку скрипта (если вы запускаете из другого места)
cd /d "%~dp0"

REM — Активировать виртуальное окружение
call venv\Scripts\activate

REM — Установить зависимости (только если что-то новое добавили)
pip install -r requirements.txt

REM — Запустить Streamlit
streamlit run streamlit_app.py

REM — Остановить окружение после выхода
deactivate
pause
