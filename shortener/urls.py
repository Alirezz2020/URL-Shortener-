from django.urls import path
from .views import ShortURLCreateView, ShortURLDetailView, ShortURLRedirectView

app_name = 'shortener'

urlpatterns = [
    # Form to create a new short URL
    path('', ShortURLCreateView.as_view(), name='create'),
    # Detail view to show the generated short URL
    path('detail/<slug:short_code>/', ShortURLDetailView.as_view(), name='detail'),
    # Catch-all for redirecting using the short code
    path('<slug:short_code>/', ShortURLRedirectView.as_view(), name='redirect'),
]
