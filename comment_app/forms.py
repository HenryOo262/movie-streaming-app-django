from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['commentText']

    commentText = forms.CharField(
        widget=forms.Textarea(attrs={
            'class':'commentText',
            'placeholder':'Join the discussion . . .',
        })
    )

    def clean_commentText(self):
        value = self.cleaned_data['commentText']
        if len(value) > 280:
            raise forms.ValidationError('Comment must be no more than 280 characters')
        return value
    

class EditForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['commentText']

    commentText = forms.CharField(
        widget=forms.Textarea(attrs={
            'class':'editText',
            'placeholder':'Edit your comment . . .',
            'id': 'id_editText',
        })
    )

    commentId = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'readonly':'readonly',
            'class':'hidden',
        })
    )

    def clean_commentText(self):
        value = self.cleaned_data['commentText']
        if len(value) > 280:
            raise forms.ValidationError('Comment must be no more than 280 characters')
        return value