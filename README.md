# ONLINE CINEMA SERVICE (UGC)
## [Ссылка на репозиторий](https://github.com/SmirnovaT/ugc_sprint_2)

### Запуск приложения с docker compose
```
docker compose up --build
or
docker compose up --build -d
```

### Запуск приложения для локальной разработки
```
1. cp .env.prod.example .env
2. python3.12 -m venv venv
3. source venv/bin/activate
4. pip3 install poetry
5. poetry install (or python -m poetry install)
6. cd app
7. uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Инициализация mongodb кластера
```console
docker compose exec mongos1 bash /opt/init/mongo-init.sh
```

### Запуск тестов

Изменить в корне проекта в.env хост БД на test_mongodb
```
1. cd tests
2. docker-compose up --build

```

### Кибана

Перед просмотром логов в кибане нужно создать соответсвующие data views. Логи приложений, при наличии тегов, пишутся в раздельные индексы Elasticsearch (см. `./infra/filebeat.yml`) 


### Результаты тестирования DB

[Результаты тестирования MongoDB](research/mongo_db/result.md)

[Результаты тестирования Postgres](research/check_postgres/result.md)

