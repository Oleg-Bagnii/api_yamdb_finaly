# Проект «YaMDb»

### Описание

_Проект YaMDb_ собирает отзывы пользователей на произведения. Cервис предполагает возможность зарегистрироваться, написать, отредактировать или удалить собственный отзыв, поставить оценку, читать и комментировать отзывы других пользователей.

_REST API_ для проекта YaMDb - это интерфейс, через который смогут работать мобильное приложение или чат-бот; данные через этот API можно передавать на фронтенд.

### Стек технологий:
- Python 3.9.10
- Django 3.2.16
- Django REST Framework
- Postman

###### Cпецификацию к API можно найти по адресу http://127.0.0.1:8000/redoc/ 

### Установка

##### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:
```sh
git clone git@github.com:Lililand91/api_yamdb.git
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:
```sh
python3 -m venv env
```
Если у вас Linux/macOS
```sh
source env/bin/activate
```
Если у вас windows
```sh
source env/scripts/activate
```
Установить зависимости из файла requirements.txt:
```sh
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
Выполнить миграции:
```sh
python3 manage.py migrate
```
Запустить проект:
```sh
python3 manage.py runserver
```

##### Как загрузить данные из csv-файлов в базу данных:

Установить библиотеку pandas:
```sh
pip install pandas
```
Перейти в директорию './api_yamdb' :
```sh
cd api_yamdb
```
Запустить файл 'load_data':
```sh
python static/data/load_data.py
```

###### Авторы проекта [Лилия Тазетдинова](https://github.com/Lililand91), [Олег Багний](https://github.com/Oleg-Bagnii), [Дмитрий Сырбу](https://github.com/ACkukoDC)
