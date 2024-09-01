
from django import forms

from .models import Cast

class CastForm(forms.Form):
    class Meta:
        model = Cast
        fields = ['name', 'bio', 'image']

    name = forms.CharField(
        label='Name',
        widget=forms.TextInput()
    )

    bio = forms.CharField(
        label='Mini Bio*',
        required=False,
        widget=forms.Textarea()
    )

    image = forms.FileField(
        label='Image*',
        required=False,
        widget=forms.FileInput({'accept':'image/jpeg,image/jpg,image/jfif'})
    )

    imdb = forms.CharField(
        label='IMDB Link*',
        required=False,
        widget=forms.TextInput()
    )

    def clean_name(self):
        value = self.cleaned_data.get('name')
        return value.strip()
    
    def clean_imdb(self):
        value = self.cleaned_data.get('imdb')
        return value.strip()
    
    def clean_bio(self):
        value = self.cleaned_data.get('bio')
        return value.strip()
    
    def clean_image(self):
        value = self.cleaned_data.get('image')
        if value is not None and value.content_type not in ['image/jpeg', 'image/jpg', 'image/jfif']:
            raise forms.ValidationError('Image must be either JPEG or JPG')
        return value