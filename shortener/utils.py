from django.conf import settings
import random
import string

# 'from shortener.models import KirrURL'
# The import up there isn't gonna work because code_generator has already been imported to models

#finding the attribute 'SHORTCODE_MAX' in settings. If the attribute hasn't been found, return 6.
SHORTCODE_MIN = getattr(settings, 'SHORTCODE_MIN', 6)

def code_generator(size=SHORTCODE_MIN, chars=string.ascii_lowercase + string.digits):
    # new_code = ''
    # for _ in range(size):
    #     new_code += random.choice(chars)
    # return new_code
    # The block above is the same as the string below
    return ''.join(random.choice(chars) for _ in range(size))

def create_shortcode(instance, size=SHORTCODE_MIN):
    new_code = code_generator(size=size)
    # print(instance) # output the instance of KirrURL (for example "shibata"
    # print(instance.__class__) # output the <class 'shortener.models.KirrURL'>
    # print(instance.__class__.__name__) # output the 'KirrURL'
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(shortcode=new_code).exists()
    if qs_exists:
        return create_shortcode(size=size)
    return new_code