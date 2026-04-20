# API YaMDb

REST API для сервиса YaMDb: произведения, категории, жанры, отзывы и комментарии. Регистрация пользователей, JWT-аутентификация, роли (пользователь, модератор, администратор).

Стек: Django, Django REST Framework, Simple JWT.

## Запуск

```bash
cd api_yamdb
python manage.py migrate
python manage.py runserver
```

Тесты из корня репозитория:

```bash
pytest
```
