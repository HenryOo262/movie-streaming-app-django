from django import forms
from datetime import datetime
from .models import Series, SeriesResource
from movieStreamingApp.models import Genre, Country


class SeriesForm(forms.ModelForm):
    year_list = range(datetime.now().year, datetime.now().year-200, -1)

    class Meta:
        model = Series
        fields = ['title','poster','releaseDate','status','rating','description','genres','countries','productions','directors','casts']

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

    director = forms.CharField(
        label='Directors - optional',
        required=False,
        widget=forms.TextInput({'list':'director-list'})
    )

    codirector = forms.CharField(
        label='Co-Director - optional',
        required=False,
        widget=forms.TextInput({'list':'director-list'})
    )

    cast = forms.CharField(
        label='Casts - optional',
        required=False,
        widget=forms.TextInput({'list':'cast-list'})
    )

    cocast1 = forms.CharField(
        label='Co-Cast - optional',
        required=False,
        widget=forms.TextInput({'list':'cast-list'})
    )

    cocast2 = forms.CharField(
        label='Co-Cast - optional',
        required=False,
        widget=forms.TextInput({'list':'cast-list'})
    )

    production = forms.CharField(
        label='Production Companies - optional',
        required=False,
        widget=forms.TextInput({'list':'production-list'})
    )

    coproduction1 = forms.CharField(
        label='Co-Production Company - optional',
        required=False,
        widget=forms.TextInput({'list':'production-list'})
    )

    coproduction2 = forms.CharField(
        label='Co-Production Company - optional',
        required=False,
        widget=forms.TextInput({'list':'production-list'})
    )

    def clean_title(self):
        value = self.cleaned_data.get('title')
        return value.strip()

    def clean_poster(self):
        value = self.cleaned_data.get('poster')
        if value.content_type not in ['image/jpeg', 'image/jpg', 'image/jfif']:
            raise forms.ValidationError('Poster must be either JPEG or JPG')
        return value

    def clean_director(self):
        director = self.cleaned_data.get('director')
        return director.strip()

    def clean_codirector(self):
        codirector = self.cleaned_data.get('codirector')
        return codirector.strip()
    
    def clean_cast(self):
        cast = self.cleaned_data.get('cast')
        return cast.strip()
    
    def clean_cocast1(self):
        cocast1 = self.cleaned_data.get('cocast1')
        return cocast1.strip()
    
    def clean_cocast2(self):
        cocast2 = self.cleaned_data.get('cocast2')
        return cocast2.strip()

    def clean_production(self):
        production = self.cleaned_data.get('production')
        return production.strip()
    
    def clean_coproduction1(self):
        coproduction1 = self.cleaned_data.get('coproduction1')
        return coproduction1.strip()
    
    def clean_coproduction2(self):
        coproduction2 = self.cleaned_data.get('coproduction2')
        return coproduction2.strip()
    

class SeriesResourceForm(forms.Form):   # having problems with ModelForm, episode cannot be overidden
    series = forms.IntegerField(
        label="Series",
        widget=forms.NumberInput()
    )

    season = forms.IntegerField(
        label="Season",
        widget=forms.NumberInput()
    )

    episode = forms.IntegerField(
        label="Episode",
        widget=forms.NumberInput()
    )

    resolution = forms.ChoiceField(
        label="Resolution",
        choices=[('320p','320p'),('480p','480p'),('720p','720p'),('1080p','1080p')]
    )

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
        value = self.cleaned_data.get('source')
        if not value.content_type == 'video/mp4':
            raise forms.ValidationError('File must be MP4')
        return value
    
    def clean_season(self):
        value = self.cleaned_data.get('season')
        if value <= 0:
            raise forms.ValidationError('Invalid season number')
        return value
    
    def clean_episode(self):
        value = self.cleaned_data.get('episode')
        if value <= 0:
            raise forms.ValidationError('Invalid episode number')
        return value
        