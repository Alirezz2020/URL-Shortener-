from django.urls import path, reverse_lazy
from .views import (
    ShortURLCreateView,
    ShortURLDetailView,
    ShortURLRedirectView,
    AnalyticsView,
    BulkShortURLView,
    DashboardView,
    QRCodeView
)
from .api_views import ShortURLListCreateAPIView

app_name = 'shortener'

urlpatterns = [
    # Single URL creation
    path('', ShortURLCreateView.as_view(), name='create'),
    # Detail view
    path('detail/<slug:short_code>/', ShortURLDetailView.as_view(), name='detail'),
    # Bulk URL shortening
    path('bulk/', BulkShortURLView.as_view(), name='bulk'),
    # Dashboard view (session-based)
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # Analytics view
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
    # QR Code generation
    path('qrcode/<slug:short_code>/', QRCodeView.as_view(), name='qrcode'),
    # API endpoint
    path('api/shorturls/', ShortURLListCreateAPIView.as_view(), name='api_shorturls'),
    # Catch-all: redirect view (should be last)
    path('<slug:short_code>/', ShortURLRedirectView.as_view(), name='redirect'),
]
