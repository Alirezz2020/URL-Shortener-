from django.urls import path
from .views import (
    ShortURLCreateView,
    ShortURLDetailView,
    ShortURLRedirectView,
    AnalyticsView
)

app_name = 'shortener'

urlpatterns = [
    path('', ShortURLCreateView.as_view(), name='create'),
    path('detail/<slug:short_code>/', ShortURLDetailView.as_view(), name='detail'),
    # Analytics view URL; you could put this under an admin namespace later if needed.
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
    # Catch-all for redirecting using the short code
    path('<slug:short_code>/', ShortURLRedirectView.as_view(), name='redirect'),
]
