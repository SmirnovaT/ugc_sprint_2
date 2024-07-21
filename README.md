### ONLINE CINEMA SERVICE (UGC)
___
#### [Ссылка на репозиторий](https://github.com/SmirnovaT/ugc_sprint_2)
___

Запуск приложения с docker compose
```
docker-compose up --build
or
docker-compose up --build -d
```

Запуск приложения для локальной разработки
```
1. cp .env_example .env
2. python3.12 -m venv venv
3. source venv/bin/activate
4. pip3 install poetry
5. poetry install (or python -m poetry install)
6. cd app
7. uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

