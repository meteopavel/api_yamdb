# API для YaMDb

## Проект YaMDb

Проект YaMDb собирает **отзывы** пользователей на **произведения**. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на **категории**, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен.

Произведению может быть присвоен **жанр** из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).

Добавлять произведения, категории и жанры может только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые **отзывы** и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — **рейтинг** (целое число). На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять **комментарии** к отзывам.

Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи. 

## Пользовательские роли и права доступа
* **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
* **Аутентифицированный пользователь (user)** — может читать всё, как и **Аноним**, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
* **Модератор** — те же права, что и у **Аутентифицированного пользователя**, плюс право удалять и редактировать **любые** отзывы и комментарии.
* **Администратор (admin)** — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:
```bash
git clone git@github.com:meteopavel/api_yamdb.git
cd yatube_api
```
Cоздать и активировать виртуальное окружение:
```bash
python3 -m venv venv
linux: source env/bin/activate
windows: source venv/Scripts/activate
```
Установить зависимости из файла requirements.txt:
```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
Выполнить миграции:
```bash
python3 manage.py migrate
```
Загрузить коллекцию предустановленных данных в базу данных:
```bash
python manage.py csv_to_db
```
После успешного импорта данных из csv-файла в консоли должно появиться сообщение:
```bash
$ Данные объекта _название_модели_ успешно загружены.
```
Запустить проект:
```bash
python manage.py runserver
```

## Документация

Для доступа к документации в формате ReDoc пройти по эндпоинту /redoc/

## API-токен

Для регистрации отправить POST-запрос по эндпоинту /api/v1/auth/signup/
В запросе указать следующее:
```json
{
    "email": "user@example.com",
    "username": "string"
}
```

Код получения токена будет выслан на указанный e-mail. Для получения токена отправить POST-запрос на эндпоинт /api/v1/auth/token/
В запросе указать следующее:
```json
{
  "username": "string",
  "confirmation_code": "string"
}
```

## Примеры запросов

### Получение списка всех произведений

>**GET** http://127.0.0.1:8000/api/v1/titles/

***Пример ответа:***
```json
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "string"
        }
      ],
      "category": {
        "name": "string",
        "slug": "string"
      }
    }
  ]
}
```

### Добавление произведения

>**POST** http://127.0.0.1:8000/api/v1/titles/
```json
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```
***Пример ответа:***
```json
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```

### Добавление жанра. Права доступа: *Администратор*

>**POST** http://127.0.0.1:8000/api/v1/genres/
```json
{
  "name": "string",
  "slug": "string"
}
```
***Пример ответа:***
```json
{
  "name": "string",
  "slug": "string"
}
```

## Основные используемые инструменты

* Python 3.9.10
* Django 3.2.16
* djangorestframework 3.12.4
* pytest 6.2.4
* PyJWT 2.1.0


## Авторы

[Альбина Лифанова](https://github.com/lifaalbina)

Разработала всю часть, касающуюся управления пользователями:
* систему регистрации и аутентификации,
* права доступа,
* работу с токеном,
* систему подтверждения через e-mail.


[Адель Хакимов](https://github.com/AdelKhakimov)

Описал модели, view и эндпоинты для:
* произведений,
* категорий,
* жанров.

А также реализовал импорт данных из csv-файла.

[Павел Найденов](https://github.com/meteopavel)

Описал модели, view и эндпоинты для:
* отзывов,
* комментариев,
* рейтинга произведений.
