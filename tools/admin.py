from django.contrib import admin
from .models import Image, GeneralQuestion, TranslationQuestion

# Register your models here.
admin.site.register(Image)
admin.site.register(GeneralQuestion)
admin.site.register(TranslationQuestion)