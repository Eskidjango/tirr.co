from django import forms

from .validators import validate_url, validate_dot_com

class SubmitUrlForm(forms.Form):
    url = forms.CharField(
        label='',
        validators=[validate_url],
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Long URL',
                'class': 'form-control',
            }
        ),
        )
    def clean_url(self):
        url = self.cleaned_data['url']
        if not url.startswith('https://'):
            url = 'http://' + url
        return url