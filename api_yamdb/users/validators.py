from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError


def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError('Использовать имя "me" запрещено.')
    UnicodeUsernameValidator()(value)
    return value
