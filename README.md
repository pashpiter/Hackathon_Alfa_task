# **MVP индивидуального плана развития для сотрудников Альфа-Банка**
![Development](https://github.com/pashpiter/Hackathon_Alfa_task/actions/workflows/dev_workflows.yml/badge.svg)

![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![image](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![image](https://img.shields.io/badge/sql%20alchemy-grey?style=for-the-badge&logo=alchemy)
![image](https://img.shields.io/badge/alembic-7FFFD4?style=for-the-badge)
![image](https://img.shields.io/badge/pydantic-FF1493?style=for-the-badge&logo=pydantic)
![image](https://img.shields.io/badge/poetry-4169E1?style=for-the-badge&logo=poetry)
![image](https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
![image](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)

Репозиторий с исходным кодом: https://github.com/pashpiter/Hackathon_Alfa_task/  
Проект запущен по адресу: http://51.250.6.208/

___
## **Спецификация проекта**:
- для построения REST API используется фреймворк FastAPI
- в качестве хранилища данных проекта используется СУБД PostgreSQL
- раздачей статики и проксированием http-запросов занимается web-сервер nginx
- в качестве упрощённого механизма авторизации используется проверка Bearer-токенов. 
Токены статически хранятся в БД, выдача токенов не предусмотрена

___
## **Энодпоинты API**:

![](docs/endpoints.png)


___
## **Как запустить проект локально**:

- Склонируйте репозитарий:
```
git clone git@github.com:pashpiter/Hackathon_Alfa_task.git
```

- Установите Docker согласно инструкции с официального сайта: _https://docs.docker.com/_
- В папке infra создайте папку env с файлами переменных окружения (в качестве 
примера можно взять папку env.example):

```
# env/general

# Server
SERVER_HOST=127.0.0.1
SERVER_PORT=80

# Versions
POSTGRES_VERSION=15
NGINX_VERSION=1.23.3

# Hosts
POSTGRES_HOST=postgres
NGINX_HOST=nginx
FASTAPI_HOST=fastapi

# Ports
POSTGRES_PORT=5432
FASTAPI_PORT=8001
```
```
# env/postgres

POSTGRES_DB=database
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_SCHEMA=plans
```
```
# env/fastapi

APP_NAME="ИПР для сотрудников Альфа-Банка"
DEBUG=False
```

Список команд для управления работой сервиса:
```
make up             - запуск сервиса
make down           - остановка сервиса
make down-volumes   - остановка сервиса с удалением всех данных
```

Openapi документация доступна по адресам:
- Swagger: _http://<ip адрес сервера>/api/v1/openapi_
- ReDoc: _http://<ip адрес сервера>/api/v1/redoc_

## **Разработчики**:
[Павел Дровнин](https://github.com/pashpiter) - Тимлид

[Александр Бондаренко](https://github.com/dcomrad) - Разработчик

[Денис Заборовский](https://github.com/danlaryushin) - Разработчик

[Иван Павлов](https://github.com/GUSICATC) - Разработчик
