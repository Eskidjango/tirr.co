from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

def validate_url(value):
    url_validator = URLValidator()
    if value.startswith('http://'):
        new_value = value
    else:
        new_value = 'http://' + value
    try:
        url_validator(new_value)
    except:
        raise ValidationError('Invalid URL for this field')
    return new_value


def validate_dot_com(value):
    if not 'com' in value:
        raise ValidationError('This field is not valid because of no .com')
    return value
