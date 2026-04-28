from django.core.exceptions import ValidationError
from django.contrib.auth.validators import UnicodeUsernameValidator



def validate_username(value):
    if value.lower() == 'me':
        raise ValidationError('Использовать имя "me" запрещено.')
    UnicodeUsernameValidator()(value)
    return value