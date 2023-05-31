import re

from django.core.exceptions import ValidationError


def validate_username(value):
    if value == 'me':
        raise ValidationError('Имя пользователя не может быть <me>.')

    if not re.match(r"[\w.@+-]+\Z", value):
        raise ValidationError(
            (f'Не допустимые символы <{value}> в имени пользователя.'),
        )
