import re

from django.core.exceptions import ValidationError


def validator(value):
    result = re.sub(r'^[\w.@+-]+\Z', '', value)
    if value == 'me':
        raise ValidationError('Имя пользователя "me" использовать нельзя!')
    if result:
        raise ValidationError(
            f'Имя пользователя не должно содержать {result}'
        )
    return value
