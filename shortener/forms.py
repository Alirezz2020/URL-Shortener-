from django import forms
from .models import ShortURL

class ShortURLForm(forms.ModelForm):
    # Make the custom short code optional.
    short_code = forms.CharField(
        max_length=10,
        required=False,
        help_text="Optional: Enter a custom short code (letters and numbers only)."
    )

    class Meta:
        model = ShortURL
        fields = ['long_url', 'short_code']

    def clean_short_code(self):
        code = self.cleaned_data.get('short_code')
        if code:
            # Optional: Add extra validations (e.g., alphanumeric check)
            if not code.isalnum():
                raise forms.ValidationError("Custom short code must be alphanumeric.")
            # Check for uniqueness
            if ShortURL.objects.filter(short_code=code).exists():
                raise forms.ValidationError("This short code is already in use. Please choose another.")
        return code
