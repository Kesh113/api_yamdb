# api_yamdb
# Проект Yamdb

```
Учебный проект по API- иммитация бэкэнда социальной сети по 
типу IMDB. Позьзовватели могут оставлять отзывы на произведения, 
а также писать комментарии к этим отзывам. Реализован при помощи JSON API.
```

# Стэк:
- Python 
- Django Rest Framework 
- SQlite
- PyJWT 
- requests 

# Как запустить проект:

- Скопировать репозиторий:
```
git clone git@github.com:Kesh113/api_yamdb.git
```

- Перейти в нужную папку, cоздать и активировать виртуальное окружение:
```
cd api_yamdb
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
py manage.py load_csv --all
```
- Запустить проект:
```
python3 manage.py runserver
```

# Документация
```
Для доступа к документации проекта необходимо
при запущенном проекте добавить к его адресу "/redok/".
В документации указаны примеры запросов и ответов.
```
-[Redoc](http://127.0.0.1:8000/redoc/)

# Авторы
- Широкожухов Артем Андреевич 
- [GitHub](https://github.com/Kesh113)
- 
- Герасимов Сергей Антонович
- [GitHub](https://github.com/crossmos)
- 
- Степан Карпов
- [GitHub](https://github.com/SVKNL)


