import csv
import os

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class Command(BaseCommand):
    help = 'Импорт данных из CSV файлов'

    def handle(self, *args, **options):
        data_dir = os.path.join(settings.BASE_DIR, 'static', 'data')
        self.stdout.write('Начинаю импорт данных...')

        with transaction.atomic():
            self.import_users(data_dir)
            self.import_categories(data_dir)
            self.import_genres(data_dir)
            self.import_titles(data_dir)
            self.import_genre_title(data_dir)
            self.import_reviews(data_dir)
            self.import_comments(data_dir)

        self.stdout.write(self.style.SUCCESS('Импорт завершен!'))

    def import_users(self, data_dir):
        """Импорт пользователей из users.csv."""
        file_path = os.path.join(data_dir, 'users.csv')

        if not os.path.exists(file_path):
            self.stdout.write(
                self.style.WARNING(f'Файл {file_path} не найден, пропускаем')
            )
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0

            for row in reader:
                User.objects.update_or_create(
                    id=row['id'],
                    defaults={
                        'username': row['username'],
                        'email': row['email'],
                        'role': row.get('role') or User.USER,
                        'bio': row.get('bio') or '',
                        'first_name': row.get('first_name') or '',
                        'last_name': row.get('last_name') or '',
                    },
                )
                count += 1

            self.stdout.write(f' Импортировано пользователей: {count}')

    def import_categories(self, data_dir):
        """Импорт категорий из category.csv"""
        file_path = os.path.join(data_dir, 'category.csv')

        if not os.path.exists(file_path):
            self.stdout.write(
                self.style.WARNING(f'Файл {file_path} не найден, пропускаем')
            )
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0

            for row in reader:
                Category.objects.get_or_create(
                    id=row['id'],
                    defaults={'name': row['name'], 'slug': row['slug']},
                )
                count += 1

            self.stdout.write(f' Импортировано категорий: {count}')

    def import_genres(self, data_dir):
        """Импорт жанров из genre.csv"""
        file_path = os.path.join(data_dir, 'genre.csv')

        if not os.path.exists(file_path):
            self.stdout.write(
                self.style.WARNING(f'Файл {file_path} не найден, пропускаем')
            )
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0

            for row in reader:
                Genre.objects.get_or_create(
                    id=row['id'],
                    defaults={'name': row['name'], 'slug': row['slug']},
                )
                count += 1

            self.stdout.write(f' Импортировано жанров: {count}')

    def import_titles(self, data_dir):
        """Импорт произведений из titles.csv"""
        file_path = os.path.join(data_dir, 'titles.csv')

        if not os.path.exists(file_path):
            self.stdout.write(
                self.style.WARNING(f'Файл {file_path} не найден, пропускаем')
            )
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0

            for row in reader:
                try:
                    category = Category.objects.get(id=row['category'])
                except Category.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        'Категория id='
                        f'{row["category"]} не найдена для {row["name"]}'
                    ))
                    continue

                Title.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'name': row['name'],
                        'year': int(row['year']),
                        'description': row.get('description') or '',
                        'category': category,
                    },
                )
                count += 1

            self.stdout.write(f' Импортировано произведений: {count}')

    def import_genre_title(self, data_dir):
        """Импорт связей из genre_title.csv"""
        file_path = os.path.join(data_dir, 'genre_title.csv')

        if not os.path.exists(file_path):
            self.stdout.write(
                self.style.WARNING(f'Файл {file_path} не найден, пропускаем')
            )
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0

            for row in reader:
                try:
                    title = Title.objects.get(id=row['title_id'])
                    genre = Genre.objects.get(id=row['genre_id'])
                    title.genre.add(genre)
                    count += 1
                except Title.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        f'Произведение id={row["title_id"]} не найдено'
                    ))
                except Genre.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        f'Жанр id={row["genre_id"]} не найден'
                    ))

            self.stdout.write(f' Добавлено связей: {count}')

    def import_reviews(self, data_dir):
        """Импорт отзывов из review.csv."""
        file_path = os.path.join(data_dir, 'review.csv')

        if not os.path.exists(file_path):
            self.stdout.write(
                self.style.WARNING(f'Файл {file_path} не найден, пропускаем')
            )
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0

            for row in reader:
                try:
                    title = Title.objects.get(id=row['title_id'])
                    author = User.objects.get(id=row['author'])
                except Title.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        f'Произведение id={row["title_id"]} не найдено'
                    ))
                    continue
                except User.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        f'Пользователь id={row["author"]} не найден'
                    ))
                    continue

                Review.objects.update_or_create(
                    id=row['id'],
                    defaults={
                        'title': title,
                        'text': row['text'],
                        'author': author,
                        'score': int(row['score']),
                        'pub_date': row['pub_date'],
                    },
                )
                count += 1

            self.stdout.write(f' Импортировано отзывов: {count}')

    def import_comments(self, data_dir):
        """Импорт комментариев из comments.csv."""
        file_path = os.path.join(data_dir, 'comments.csv')

        if not os.path.exists(file_path):
            self.stdout.write(
                self.style.WARNING(f'Файл {file_path} не найден, пропускаем')
            )
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0

            for row in reader:
                try:
                    review = Review.objects.get(id=row['review_id'])
                    author = User.objects.get(id=row['author'])
                except Review.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        f'Отзыв id={row["review_id"]} не найден'
                    ))
                    continue
                except User.DoesNotExist:
                    self.stdout.write(self.style.WARNING(
                        f'Пользователь id={row["author"]} не найден'
                    ))
                    continue

                Comment.objects.update_or_create(
                    id=row['id'],
                    defaults={
                        'review': review,
                        'text': row['text'],
                        'author': author,
                        'pub_date': row['pub_date'],
                    },
                )
                count += 1

            self.stdout.write(f' Импортировано комментариев: {count}')
