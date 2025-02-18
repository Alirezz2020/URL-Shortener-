import string, random, io
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

def generate_short_code():
    length = 6
    characters = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choice(characters) for _ in range(length))
        if not ShortURL.objects.filter(short_code=code).exists():
            return code

class ShortURL(models.Model):
    long_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True, blank=True)
    custom_domain = models.CharField(
        max_length=255, blank=True, null=True,
        help_text="Optional custom domain for this shortened URL"
    )
    expiration_date = models.DateTimeField(
        blank=True, null=True,
        help_text="Optional expiration date for the URL"
    )
    password = models.CharField(
        max_length=128, blank=True,
        help_text="Optional password protection (will be hashed)"
    )
    branding = models.CharField(
        max_length=100, blank=True,
        help_text="Optional branding for the link (e.g., campaign name)"
    )
    click_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = generate_short_code()
        # Hash the password if provided and not already hashed
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        if not self.password:
            return True
        return check_password(raw_password, self.password)

    def is_expired(self):
        if self.expiration_date and timezone.now() > self.expiration_date:
            return True
        return False

    def __str__(self):
        return f"{self.short_code} -> {self.long_url}"

class ClickEvent(models.Model):
    short_url = models.ForeignKey(ShortURL, related_name='click_events', on_delete=models.CASCADE)
    clicked_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    referrer = models.URLField(blank=True, null=True)
    # In a real app you might add geo fields (country, city) using a geoip service

    def __str__(self):
        return f"Click on {self.short_url.short_code} at {self.clicked_at}"
