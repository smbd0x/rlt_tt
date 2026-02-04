## Quick Guide ##
## Запуск ##
На пк с установленным python в терминале выполнить:

1

    git clone https://github.com/smbd0x/luna_tt

2

    cd luna_tt

3 Создать .env файл, пример (OPENAI_API_KEY берется с сайта https://proxyapi.ru/):

    OPENAI_API_KEY=...
    BOT_TOKEN=...
    DATABASE_URL=postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}


4 Создать виртуальное окружение с помощью команды:

    python3 -m venv venv

5 Активировать виртуалльно окружение (для linux):

    source venv/bin/activate

  Для windows:

    venv\Scripts\activate.bat

6 Установить зависимости

    pip install requirements.txt

7 Для заполнения таблиц данными из json выполнить:

    python3 import_json.py

8 Для запуска бота выполнить:

    python3 bot.py


## О боте ##
Промпт можно найти в файле [llm/parser](llm/parser)
