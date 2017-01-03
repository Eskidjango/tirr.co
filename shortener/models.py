from django.conf import settings
from django.db import models


from django_hosts.resolvers import reverse
from .utils import code_generator, create_shortcode
from .validators import validate_url, validate_dot_com

#finding the attribute 'SHORTCODE_MAX' in settings. If the attribute hasn't been found, return 15.
SHORTCODE_MAX = getattr(settings, 'SHORTCODE_MAX', 16)


class KirrURLManager(models.Manager):
    def all(self, *args, **kwargs):
        # calling the default 'all' method of manager
        qs_main = super(KirrURLManager, self).all(*args, **kwargs)
        qs = qs_main.filter(active=True)
        return qs

    def refresh_shortcodes(self, items=None):
        qs = KirrURL.objects.filter(id__gte=1)
        if items is not None and isinstance(items, int): # isinstance's checking if the items is int
            qs = qs.order_by('-id')[:items]
        new_codes = 0
        for q in qs:
            q.shortcode = create_shortcode(q)
            print(q.id)
            q.save()
            new_codes += 1
        return "New codes made: {i}".format(i=new_codes)



class KirrURL(models.Model):
    url        = models.CharField(max_length=220, validators=[validate_url])
    shortcode  = models.CharField(max_length=SHORTCODE_MAX, unique=True, blank=True)
    timestamp  = models.DateTimeField(auto_now=True) #everytime the model is saved
    updated    = models.DateTimeField(auto_now_add=True) #when model was created
    active     = models.BooleanField(default=True)
    objects = KirrURLManager()
    some_random = KirrURLManager()

    def save(self, *args, **kwargs):
        if self.shortcode is None or self.shortcode == '':
            self.shortcode = create_shortcode(self)
        if not self.url.startswith('http://'):
            self.url = 'http://' + self.url
        super(KirrURL, self).save(*args, **kwargs)

    def __unicode__(self):
        return str(self.url)

    def get_short_url(self):
        url_path = reverse("scode", kwargs={'shortcode': self.shortcode}, host='www', scheme='http')
        return url_path


    def __str__(self):
        return str(self.url)