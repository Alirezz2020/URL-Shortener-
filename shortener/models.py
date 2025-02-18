import string
import random
from django.db import models

def generate_short_code():
    length = 6
    characters = string.ascii_letters + string.digits
    # Keep generating until we find a unique code
    while True:
        code = ''.join(random.choice(characters) for _ in range(length))
        if not ShortURL.objects.filter(short_code=code).exists():
            return code

class ShortURL(models.Model):
    long_url = models.URLField()
    # Allow users to optionally specify a custom code; if left blank, one will be generated.
    short_code = models.CharField(max_length=10, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    click_count = models.PositiveIntegerField(default=0)  # For tracking clicks

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = generate_short_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.short_code} -> {self.long_url}"
