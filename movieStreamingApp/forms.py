from typing import Any
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['commentText']

    commentText = forms.CharField(
        widget=forms.Textarea({
            'class':'commentText',
            'placeholder':'Join the discussion . . .'
        })
    )

    def clean_commentText(self):
        value = self.cleaned_data['commentText']
        if len(value) > 280:
            raise forms.ValidationError('Comment must be no more than 280 characters')
        return value