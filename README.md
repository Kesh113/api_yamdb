# api_yamdb
# Проект Yamdb

```
Учебный проект по API- иммитация бэкэнда социальной сети по 
типу IMDB. Позьзовватели могут оставлять отзывы на произведения, 
а также писать комментарии к этим отзывам. Реализован при помощи JSON API.
```

# Стэк:
- Python 3.9
- Django Rest Framework 3.12.4
- SQlite


# Как запустить проект:

- Скопировать репозиторий -git clone:
```
git@github.com:SVKNL/api_final_yatube.git
```

- Cоздать и активировать виртуальное окружение:
```
python3 -m venv env
source env/bin/activate
```
- Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
- Выполнить миграции:
```
python3 manage.py migrate
```
- Заполнить БД из CSV:
```
"py manage.py load_csv static/data/category.csv"
1) load_csv - название команды
2) static/data/category.csv - путь до файла
```
- Запустить проект:
```
python3 manage.py runserver
```

# Документация
```
Для доступа к документации проекта необходимо
при запущенном проекте добавить к его адресу "/redok/".
Например, http://127.0.0.1:8000/redoc/. 
В документации указаны примеры запросов и ответов.
```

# Авторы
- Широкожухов Артем Андреевич 
- https://github.com/Kesh113
- 
- Герасимов Сергей Антонович
- https://github.com/crossmos
- 
- Степан Карпов
- https://github.com/SVKNL


