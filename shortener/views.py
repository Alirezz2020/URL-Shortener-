from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.base import RedirectView
from django.http import Http404

from .models import ShortURL
from .forms import ShortURLForm

# View to create a new ShortURL entry
class ShortURLCreateView(CreateView):
    model = ShortURL
    form_class = ShortURLForm
    template_name = 'shortener/shorturl_form.html'

    def get_success_url(self):
        # Redirect to a detail view that shows the generated short URL
        return reverse_lazy('shortener:detail', kwargs={'short_code': self.object.short_code})

# Detail view to display the short URL info
class ShortURLDetailView(DetailView):
    model = ShortURL
    template_name = 'shortener/shorturl_detail.html'
    context_object_name = 'shorturl'
    slug_field = 'short_code'
    slug_url_kwarg = 'short_code'

# Redirect view to forward short URLs to their long destination
class ShortURLRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        short_code = kwargs.get('short_code')
        try:
            short_url_obj = ShortURL.objects.get(short_code=short_code)
            return short_url_obj.long_url
        except ShortURL.DoesNotExist:
            raise Http404("Short URL not found.")
