from .models import Profile
from django import forms

from django.contrib.auth import get_user_model
User = get_user_model()

class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        required=False,
        widget = forms.TextInput(attrs={
            'class': 'max-w-lg shadow-sm focus:ring-blue-500 dark:bg-dark-third dark:text-dark-txt block w-full sm:text-sm border-gray-300 rounded-md',

            })
    )

    last_name = forms.CharField(
        required=False,
        widget = forms.TextInput(attrs={
            'class': 'max-w-lg shadow-sm focus:ring-blue-500 dark:bg-dark-third dark:text-dark-txt block w-full sm:text-sm border-gray-300 rounded-md',

            })
    )

    picture = forms.ImageField(label='Profile Picture', required=False, widget=forms.FileInput)
    
    banner = forms.ImageField(label='Banner Picture', required=False, widget=forms.FileInput)
    location = forms.CharField(
        required=False,
        widget = forms.TextInput(attrs={
            'class': 'max-w-lg shadow-sm focus:ring-blue-500 dark:bg-dark-third dark:text-dark-txt block w-full sm:text-sm border-gray-300 rounded-md',

            })
    )
    url = forms.URLField(
        label='Website URL',
        required=False,
        widget = forms.TextInput(attrs={
            'class': 'max-w-lg shadow-sm focus:ring-blue-500 dark:bg-dark-third dark:text-dark-txt block w-full sm:text-sm border-gray-300 rounded-md',

            })
    )
    bio = forms.CharField(
        required=False,
        widget = forms.TextInput(attrs={
            'class': 'max-w-lg shadow-sm focus:ring-blue-500 dark:bg-dark-third dark:text-dark-txt block w-full sm:text-sm border-gray-300 rounded-md',

            })
    )
    birthday = forms.DateField(
        required=False,
        widget = forms.DateInput(attrs={
            'class': 'max-w-lg shadow-sm focus:ring-blue-500 dark:bg-dark-third dark:text-dark-txt block w-full sm:text-sm border-gray-300 rounded-md',

            })
    )

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'picture', 'banner', 'location', 'url', 'bio', 'birthday')