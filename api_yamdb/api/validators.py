import re

from django.core.exceptions import ValidationError


def validator(value):
    pattern = r'^[\w.@+-]+\Z'
    result = re.match(pattern, value)
    if value == 'me':
        raise ValidationError('Имя пользователя "me" нельзя использовать.')
    elif not result:
        raise ValidationError(
                f'Имя пользователя не должно содержать {result}'
            )
    return value
