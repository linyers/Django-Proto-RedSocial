from django import forms
from .models import SocialPost, SocialComment

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.ImageField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={
                'class': 'relative dark:text-dark-txt dark:bg-dark-second cursor-pointer bg-white rounded-md font-medium text-blue-600 hover:text-blue-500 focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-blue-500',
                }))
        
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class SocialPostForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={
            'class': 'shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-dark-third dark:border-dark-third dark:text-dark-txt max-w-full sm:text-sm border-gray-300 rounded-md',
            'rows': '3',
            'placeholder': 'Say Something...'
            }),
        required=True)

    images = MultipleFileField(required=False)

    class Meta:
        model=SocialPost
        fields=['body']

class SocialCommentForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={
            'class': 'shadow-sm focus:ring-blue-500 focus:border-blue-500 dark:bg-dark-third dark:border-dark-third dark:text-dark-txt max-w-full sm:text-sm border-gray-300 rounded-md',
            'rows': '1',
            'placeholder': 'Comment Something...'
            }),
        required=True)
    
    class Meta:
        model = SocialComment
        fields = ['comment']