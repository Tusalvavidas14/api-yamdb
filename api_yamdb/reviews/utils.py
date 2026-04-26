from datetime import date


def _current_year() -> int:
    """ Делаем валидатор "живым":
    чтобы при старте в новом году не требовалась правка миграций. """
    return date.today().year
