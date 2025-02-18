from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.base import RedirectView, TemplateView
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from .models import ShortURL
from .forms import ShortURLForm

class ShortURLCreateView(CreateView):
    model = ShortURL
    form_class = ShortURLForm
    template_name = 'shortener/shorturl_form.html'

    def get_success_url(self):
        return reverse_lazy('shortener:detail', kwargs={'short_code': self.object.short_code})

class ShortURLDetailView(DetailView):
    model = ShortURL
    template_name = 'shortener/shorturl_detail.html'
    context_object_name = 'shorturl'
    slug_field = 'short_code'
    slug_url_kwarg = 'short_code'

class ShortURLRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        short_code = kwargs.get('short_code')
        short_url_obj = get_object_or_404(ShortURL, short_code=short_code)
        # Increment the click counter and save
        short_url_obj.click_count += 1
        short_url_obj.save(update_fields=['click_count'])
        return short_url_obj.long_url





class AnalyticsView(ListView):
    model = ShortURL
    template_name = 'shortener/analytics.html'
    context_object_name = 'shorturls'
    ordering = ['-created_at']  # Show newest first
