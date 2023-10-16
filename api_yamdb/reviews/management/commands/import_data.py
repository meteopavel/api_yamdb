from django.core.management.base import BaseCommand
import csv
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from datetime import datetime
import io

PATH_TO_CSV_USERS = 'static/data/users.csv'
PATH_TO_CSV_TITLE = 'static/data/titles.csv'
PATH_TO_CSV_CATEGORY = 'static/data/category.csv'
PATH_TO_CSV_GENRE = 'static/data/genre.csv'
PATH_TO_CSV_REVIEW = 'static/data/review.csv'
PATH_TO_CSV_COMMENT = 'static/data/comments.csv'
PATH_TO_CSV_GENRE_TITLE = 'static/data/genre_title.csv'


class Command(BaseCommand):
    help = 'Импортирует данные из CSV файлов в базу данных'

    def process_title(self, row):
        try:
            category_id = int(row['category'])
            category_instance = Category.objects.get(id=category_id)
            row['category'] = category_instance
        except Category.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    f'Категория с ID {category_id} не найдена.'
                )
            )
            return None
        except ValueError:
            self.stdout.write(
                self.style.ERROR(
                    f'Некорректный ID категории {row["category"]}.'
                )
            )
            return None
        return row

    def process_review(self, row):
        try:
            pub_date = datetime.fromisoformat(
                row['pub_date'].replace('Z', '+00:00')
            )
            row['pub_date'] = pub_date.date()
            author_id = int(row['author'])
            author_instance = User.objects.get(id=author_id)
            row['author'] = author_instance
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    f'Пользователь с ID {author_id} не найден.'
                )
            )
            return None
        except ValueError:
            self.stdout.write(
                self.style.ERROR(
                    f'Некорректный ID пользователя {row["author"]}.'
                )
            )
            return None
        return row

    def process_comment(self, row):
        try:
            author_id = int(row['author'])
            author_instance = User.objects.get(id=author_id)
            row['author'] = author_instance
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    f'Пользователь с ID {author_id} не найден.'
                )
            )
            return None
        except ValueError:
            self.stdout.write(
                self.style.ERROR(
                    f'Некорректный ID пользователя {row["author"]}.'
                )
            )
            return None
        return row

    def import_data_from_csv(self, model, filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            data = file.read()
            reader = csv.DictReader(io.StringIO(data))

            for row in reader:
                if model == Title:
                    row = self.process_title(row)
                elif model == Review:
                    row = self.process_review(row)
                elif model == Comment:
                    row = self.process_comment(row)

                if row is None:
                    continue

                instance = model(**row)
                try:
                    instance.save()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'{model.__name__} с ID {row["id"]}'
                            f'импортирован успешно.'
                        )
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Ошибка при импорте {model.__name__} '
                            f'с ID {row["id"]}: {str(e)}'
                        )
                    )

    def import_genre_title_relation(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    title = Title.objects.get(id=row['title_id'])
                    genre = Genre.objects.get(id=row['genre_id'])
                    title.genre.add(genre)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Жанр с ID {row["genre_id"]} успешно добавлен '
                            f'к произведению с ID {row["title_id"]}.'
                        )
                    )
                except Title.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Произведение с ID {row["title_id"]} не найдено.'
                        )
                    )
                except Genre.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Жанр с ID {row["genre_id"]} не найден.'
                        )
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f'Ошибка при обработке строки {e}'
                        )
                    )

    def handle(self, *args, **options):
        self.import_data_from_csv(User, PATH_TO_CSV_USERS)
        self.import_data_from_csv(Category, PATH_TO_CSV_CATEGORY)
        self.import_data_from_csv(Title, PATH_TO_CSV_TITLE)
        self.import_data_from_csv(Genre, PATH_TO_CSV_GENRE)
        self.import_data_from_csv(Review, PATH_TO_CSV_REVIEW)
        self.import_data_from_csv(Comment, PATH_TO_CSV_COMMENT)
        self.import_genre_title_relation(PATH_TO_CSV_GENRE_TITLE)
