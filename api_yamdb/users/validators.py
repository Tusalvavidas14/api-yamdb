from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


username_regex_validator = RegexValidator(
    regex=r"^[\w.@+-]+\Z",
    message="Недопустимые символы в username.",
)


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError('Использовать имя "me" запрещено.')
    username_regex_validator(value)
    return value
