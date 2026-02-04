## Quick Guide ##
## Запуск ##
На пк с установленным python в терминале выполнить:

1

    git clone https://github.com/smbd0x/rlt_tt

2

    cd rlt_tt

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
Промпт можно найти в файле [llm/parser](https://github.com/smbd0x/rlt_tt/blob/master/llm/parser.py)

LLM преобразует простые запросы в json формат по типу 

    {
      "action": "count_videos",
      "filters": {
          "creator_id": "uuid OPTIONAL",
          "created_from": "YYYY-MM-DD OPTIONAL",
          ...
      }
    }
или

    {
      "action": "count_snapshot_events",
      "metric": "views" | "likes" | "comments" | "reports",
      "date": "YYYY-MM-DD"
    }
    
и т.п. (все стандартные схемы подробно описаны в промпте)

Здесь строго задан тип действия, и параметры, которые в последствии строго и однозначно преобразуются в SQL в файле [db/queries](https://github.com/smbd0x/rlt_tt/blob/master/db/queries.py).

В случае сложных и нестандартных запросов LLM пишет "кастомный" запрос на SQL и отдает в виде:

    {
      "action": "custom_sql",
      "sql": "<SQL-запрос с параметрами :param>",
      "params": {"param1": "значение1", ...}
    }
