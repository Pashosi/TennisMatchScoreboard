# проект "Табло теннисного матча"

Веб-приложение, реализующее табло счёта теннисного матча.
[Техническое задание проекта](https://zhukovsd.github.io/python-backend-learning-course/projects/tennis-scoreboard/)

Деплой ->http://195.133.26.31:8081/
## Основные функции

Работа с матчами:
- Создание нового матча
- Просмотр законченных матчей, поиск матчей по именам игроков
- Подсчёт очков в текущем матче

## Подсчёт очков в теннисном матче

Каждый матч играется по следующим правилам:

- Матч играется до двух сетов (best of 3)
- При счёте 6/6 в сете, играется тай-брейк до 7 очков

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Pashosi/TennisMatchScoreboard.git
cd TennisMatchScoreboard
```
2. Создание и активация виртуального окружения
```
python3 -m venv venv
venv\Scripts\activate
```
3. Установите зависимости:
```bash
pip install -r requirements.txt
```
4. Установите MySQL
5. Настройте переменные окружения для NAME и PASSWORD:
```bash
NAME=ваш_username_mysql
PASSWORD=ваш_password_mysql
```
6. Обновления базы данных до самой последней версии схемы
```
alembic upgrade head
```
8. Запуск приложения
```
python3 manage.py 
```

## Запуск тестов

Юнит тестами была покрыта логика подсчета очков в теннисном матче.
```
python -m unittest
```

## Стек технологий

- Python 3
- unittest
- Waitress
- Jinja2
- MySQL
- ORM SQLAlchemy
- Alembic
- HTML/CSS, JS

## Лицензия
---
Этот проект лицензируется под лицензией MIT - см. файл [LICENSE.md](LICENSE.md) для подробностей.
