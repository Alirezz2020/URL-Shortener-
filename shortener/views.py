from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.base import RedirectView, View
from django.views.generic import ListView
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse
from django.utils import timezone

from .models import ShortURL, ClickEvent
from .forms import ShortURLForm, BulkShortURLForm

# Import ratelimit decorator (pip install django-ratelimit)
from ratelimit.decorators import ratelimit

# Single URL creation with rate limiting and session tracking
class ShortURLCreateView(CreateView):
    model = ShortURL
    form_class = ShortURLForm
    template_name = 'shortener/shorturl_form.html'




    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        # Save the created URL ID in session for dashboard tracking
        urls = self.request.session.get('created_urls', [])
        urls.append(self.object.id)
        self.request.session['created_urls'] = urls
        return response

    def get_success_url(self):
        return reverse_lazy('shortener:detail', kwargs={'short_code': self.object.short_code})

# Bulk URL shortening view
class BulkShortURLView(FormView):
    template_name = 'shortener/bulk_shorturl_form.html'
    form_class = BulkShortURLForm


    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        urls_text = form.cleaned_data['long_urls']
        url_list = urls_text.splitlines()
        created_urls = []
        for url in url_list:
            url = url.strip()
            if url:
                short_url = ShortURL.objects.create(long_url=url)
                created_urls.append(short_url)
                # Track in session for dashboard
                dashboard_urls = self.request.session.get('created_urls', [])
                dashboard_urls.append(short_url.id)
                self.request.session['created_urls'] = dashboard_urls
        return render(self.request, 'shortener/bulk_success.html', {'created_urls': created_urls})

# Detail view to display a single URL's info
class ShortURLDetailView(DetailView):
    model = ShortURL
    template_name = 'shortener/shorturl_detail.html'
    context_object_name = 'shorturl'
    slug_field = 'short_code'
    slug_url_kwarg = 'short_code'

# Redirect view with click logging and expiration check
class ShortURLRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        short_code = kwargs.get('short_code')
        short_url_obj = get_object_or_404(ShortURL, short_code=short_code)
        if short_url_obj.is_expired():
            raise Http404("This URL has expired.")
        # Here you could also require password verification if needed
        # Log the click event
        ClickEvent.objects.create(
            short_url=short_url_obj,
            ip_address=self.request.META.get('REMOTE_ADDR'),
            user_agent=self.request.META.get('HTTP_USER_AGENT', ''),
            referrer=self.request.META.get('HTTP_REFERER', '')
        )
        short_url_obj.click_count += 1
        short_url_obj.save(update_fields=['click_count'])
        return short_url_obj.long_url

# Detailed analytics view listing all URLs
class AnalyticsView(ListView):
    model = ShortURL
    template_name = 'shortener/analytics.html'
    context_object_name = 'shorturls'
    ordering = ['-created_at']

# Dashboard view: session-based view of URLs you’ve created
class DashboardView(ListView):
    template_name = 'shortener/dashboard.html'
    context_object_name = 'shorturls'

    def get_queryset(self):
        url_ids = self.request.session.get('created_urls', [])
        return ShortURL.objects.filter(id__in=url_ids)

# QR Code generation view using the "qrcode" library (pip install qrcode[pil])
import qrcode
class QRCodeView(View):
    def get(self, request, short_code):
        short_url_obj = get_object_or_404(ShortURL, short_code=short_code)
        # Build the full URL for the QR code (using the short URL, not the long one)
        full_url = request.build_absolute_uri(
            reverse_lazy('shortener:redirect', kwargs={'short_code': short_url_obj.short_code})
        )
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(full_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        return HttpResponse(buf.getvalue(), content_type='image/png')
