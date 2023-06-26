from django.contrib import admin
from .models import SocialPost, Image, SocialComment

# Register your models here.

admin.site.register(SocialPost)
admin.site.register(SocialComment)
admin.site.register(Image)