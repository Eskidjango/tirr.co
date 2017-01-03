from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.views import View

from analytics.models import ClickEvent

from .forms import SubmitUrlForm
from .models import KirrURL

# Create your views here.

def home_view_fbv(request, *args, **kwargs):
    if request.method == 'POST':
        print(request.POST)

class HomeView(View):
    def get(self, request, *args, **kwargs):
        form = SubmitUrlForm()
        context = {
            'form': form,
            'title': 'Kirr.co',
        }
        return render(request, 'shortener/home.html', context)

    def post(self, request, *args, **kwargs):
        # print(request.POST)
        form = SubmitUrlForm(request.POST)
        context = {
            'form': form,
            'title': 'Kirr.co',
        }
        template = 'shortener/home.html'
        if form.is_valid():
            submitted_url = form.cleaned_data.get('url')
            print(submitted_url)
            obj, created = KirrURL.objects.get_or_create(url=submitted_url)
            context = {
                'object': obj,
                'created': created
            }
            if created:
                template = 'shortener/success.html'
            else:
                template = 'shortener/already-exists.html'

        return render(request, template, context)


class URLRedirectView(View): # class based view
    def get(self, request, shortcode=None, *args, **kwargs):
        qs = KirrURL.objects.filter(shortcode__iexact=shortcode)
        if qs.count() != 1 and not qs.exists():
            raise Http404
        obj = qs.first()
        print(ClickEvent.objects.create_event(obj))
        return HttpResponseRedirect(obj.url)















'''
# With comments
def kirr_redirect_view(request, shortcode, **kwargs): # function based view
    # print(request.user)
    # print(request.user.is_authenticated()) # useful to pay attention

    obj = get_object_or_404(KirrURL, shortcode=shortcode) # the best way to get our object

    # try: # not the best way to get our object
    #     obj = KirrURL.objects.get(shortcode=shortcode)
    # except:
    #     obj = KirrURL.objects.all().first()

    # obj_url = None # a bit better way but not the greatest
    # qs = KirrURL.objects.filter(shortcode__iexact=shortcode.upper())
    # if qs.exists() and qs.count() == 1:
    #     obj = qs.first()
    #     obj_url = obj.url
    return HttpResponse("hello from {sc}".format(sc=obj_url))
'''