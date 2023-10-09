import csv
import os

import django
import tablib

from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
)
from reviews.resources import (
    CategoryResource,
    CommentResource,
    GenreResource,
    ReviewResource,
    TitleResource,
    UserResource,
)
from users.models import MyUser

# Указываем Django где находятся настройки
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api_yamdb.settings")

# Для инициализации Django
django.setup()

PATH_TO_CSV_USERS = 'static/data/users.csv'
PATH_TO_CSV_TITLE = 'static/data/titles.csv'
PATH_TO_CSV_CATEGORY = 'static/data/category.csv'
PATH_TO_CSV_GENRE = 'static/data/genre.csv'
PATH_TO_CSV_REVIEW = 'static/data/review.csv'
PATH_TO_CSV_COMMENT = 'static/data/comments.csv'
PATH_TO_CSV_GENRE_TITLE = 'static/data/genre_title.csv'


def import_data(model, resource, filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        dataset = tablib.Dataset().load(file.read(), format='csv')
        result = resource().import_data(dataset, dry_run=False)
        if not result.has_errors():
            print(f'Данные из модели {model.__name__} ипортированы успешно!')
        else:
            print(f'Ошибка ипорта данных из модели {model.__name__}:')
            for line, errors in result.row_errors():
                for error in errors:
                    print(f'Строка {line} - {error.error}')


def import_genre_title_relation(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                title = Title.objects.get(id=row['title_id'])
                genre = Genre.objects.get(id=row['genre_id'])
                title.genre.add(genre)
                print(
                    f'Жанр с ID {row["genre_id"]} успешно добавлен к'
                    f'произведению с ID {row["title_id"]}.'
                )

            except Title.DoesNotExist:
                print(f'Произведение с ID {row["title_id"]} не найдено.')

            except Genre.DoesNotExist:
                print(f'Жанр с ID {row["genre_id"]} не найден.')


import_data(MyUser, UserResource, PATH_TO_CSV_USERS)
import_data(Category, CategoryResource, PATH_TO_CSV_CATEGORY)
import_data(Title, TitleResource, PATH_TO_CSV_TITLE)
import_data(Genre, GenreResource, PATH_TO_CSV_GENRE)
import_data(Review, ReviewResource, PATH_TO_CSV_REVIEW)
import_data(Comment, CommentResource, PATH_TO_CSV_COMMENT)

import_genre_title_relation(PATH_TO_CSV_GENRE_TITLE)
