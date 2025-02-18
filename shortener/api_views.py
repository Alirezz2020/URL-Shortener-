from rest_framework import generics, permissions
from .models import ShortURL
from .serializers import ShortURLSerializer

class ShortURLListCreateAPIView(generics.ListCreateAPIView):
    queryset = ShortURL.objects.all()
    serializer_class = ShortURLSerializer
    permission_classes = [permissions.AllowAny]
