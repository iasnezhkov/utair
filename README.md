# UTAIR


### Как запустить сервис

#### Зависимости

* mongo server 3.6.5
* redis server 4.0.9
* python 3.7

#### Создание окружения

* создать виртуальное окружение: `python3 -m venv venv`
* активировать виртуальное окружение: `source venv/bin/activate`
* установить зависимости: `pip install -r requirements.txt`

#### Настройки

> настройки находятся в settings.py

* указать путь к базе данных mongo `MONGO_URI`
* указать путь к redis `CACHE_REDIS_URL`
* указать логин и пароль к гугл аккаунту для отправки писем `MAIL_USERNAME, MAIL_PASSWORD`
> возможно гугл будет блокировать отправку писем, для разблокировки нужно будет следовать указаниям в консоли сервиса

#### Запустить сервис
* активировать окружение: `source venv/bin/activate`
* экпортировать путь к приложению: `export FLASK_APP=backend/autoapp.py`
* запустить сервис: `flask run`
> сервис будет доступен на 127.0.0.1:5000

#### Заполнение базы
* активировать окружение: `source venv/bin/activate`
* экпортировать путь к приложению: `export FLASK_APP=autoapp.py`
* добавить пользователей: `flask populate_users`
* добавить транзакции: `flask populate_transactions --host http://127.0.0.1:5000 --count 100`

#### Запросы

* запрос кода для аутентификации
 
 `curl --request POST \
  --url http://127.0.0.1:5000/api/v1/auth/request-code \
  --header 'content-type: application/json' \
  --data '{"email": "iseption@gmail.com"}'`
* аутентификация по коду из письма 

`curl --request POST \
  --url http://127.0.0.1:5000/api/v1/auth/code-sign-in \
  --header 'content-type: application/json' \
  --data '{
	"code": "o2xomnkjkzj0ije"}'`
> в случае успеха будут возвращены токены `{
	"access_token": "test",
	"refresh_token": "tes2"
}`
* аутентификация по логину и паролю 

`curl --request POST \
  --url http://127.0.0.1:5000/api/v1/auth/sign-in \
  --header 'content-type: application/json' \
  --data '{
	"email": "iseption@gmail.com",
	"password": "test"
}'`
> в случае успеха будут возвращены токены `{
	"access_token": "test",
	"refresh_token": "tes2"
}`

* получение информации о пользователе

`curl --request GET \
  --url http://127.0.0.1:5000/api/v1/users/me \
  --header 'authorization: Bearer {access_token}'`
  
* получение транзакций

`curl --request GET \
  --url 'http://127.0.0.1:5000/api/v1/transactions?page=1&filter=%7B%22bonus_miles%22%3A%201221%7D' \
  --header 'authorization: Bearer {access_token}'`
  
* создание транзакции

`curl --request POST \
  --url http://127.0.0.1:5000/api/v1/transactions \
  --header 'content-type: application/json' \
  --data '{
	"user_card_number": 1221,
	"bonus_miles": 1221,
	"departure_location": "test",
	"arrival_location": "test2",
	"departure_date": "Tue, 02 Apr 2013 10:29:13 GMT"
}'`