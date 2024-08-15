from django import forms
from datetime import datetime
from movieStreamingApp.models import Genre, Country
from .models import Movie, MovieResource

class MovieForm(forms.ModelForm):
    year_list = range(datetime.now().year, datetime.now().year-200, -1)

    class Meta:
        model = Movie
        fields = ['title','poster','releaseDate','description','genres','countries']

    releaseDate = forms.DateField(
        label='Release Date',
        widget=forms.SelectDateWidget(
            years=year_list
        )
    )

    poster = forms.FileField(
        label='Poster',
        widget=forms.FileInput({
            'accept':'image/jpeg,image/jpg,image/jfif'
        })
    )

    genre = forms.ModelMultipleChoiceField(
        label='Genres',
        queryset = Genre.objects.filter().order_by('name'),
        widget=forms.CheckboxSelectMultiple()
    )

    country = forms.ModelMultipleChoiceField(
        label='Countries',
        queryset = Country.objects.filter().order_by('name'),
        widget=forms.CheckboxSelectMultiple()
    )

    def clean_poster(self):
        value = self.cleaned_data['poster']
        if value.content_type not in ['image/jpeg', 'image/jpg', 'image/jfif']:
            raise forms.ValidationError('Poster must be either JPEG or JPG')
        return value


#######################################################################


class MovieResourceForm(forms.ModelForm):
    class Meta:
        model = MovieResource
        fields = ['movie', 'resolution','source']

    source = forms.FileField(
        label='Video File',
        widget=forms.FileInput({
            'accept':'video/mp4'
        })
    )

    sourceFileName = forms.CharField(
        widget=forms.TextInput({
            'style':'display:none;',
            'readonly':'readonly'
        })
    )

    def clean_source(self):
        value = self.cleaned_data['source']
        if not value.content_type == 'video/mp4':
            raise forms.ValidationError('File must be MP4')
        return value
        