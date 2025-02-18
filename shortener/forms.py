from django import forms
from django.utils import timezone
from .models import ShortURL

class ShortURLForm(forms.ModelForm):
    class Meta:
        model = ShortURL
        fields = ['long_url', 'short_code', 'custom_domain', 'expiration_date', 'password', 'branding']
        widgets = {
            'expiration_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_short_code(self):
        code = self.cleaned_data.get('short_code')
        if code:
            if not code.isalnum():
                raise forms.ValidationError("Custom short code must be alphanumeric.")
            if ShortURL.objects.filter(short_code=code).exists():
                raise forms.ValidationError("This short code is already in use. Please choose another.")
        return code

    def clean_expiration_date(self):
        exp_date = self.cleaned_data.get('expiration_date')
        if exp_date and exp_date < timezone.now():
            raise forms.ValidationError("Expiration date must be in the future.")
        return exp_date

class BulkShortURLForm(forms.Form):
    long_urls = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 10}),
        help_text="Enter one URL per line."
    )
