from django.db import models

# Create your models here.
# The first value is for the choice value, the second value is used for displaying in the form
LANGUAGE_CHOICES = (
    ('English', 'English'),
    ('Korean', 'Korean'),
)

class Image(models.Model):
    prompt = models.CharField(max_length=1024)
    ai_image = models.ImageField(upload_to='images')
    created = models.DateField(auto_now=True, null=True)

    def __str__(self):
        return str(self.prompt)

class GeneralQuestion(models.Model):
    prompt = models.CharField(max_length=512)
    ai_response = models.TextField(max_length=1024, blank=True, null=True)
    created = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.prompt)
    
class TranslationQuestion(models.Model):
    prompt = models.CharField(max_length=512)
    to_language = models.CharField(max_length=12, choices=LANGUAGE_CHOICES, blank=True, null=True)
    to_other_language = models.CharField(max_length=24, blank=True, null=True)
    ai_response = models.TextField(max_length=1024, blank=True, null=True)
    created = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.prompt)

