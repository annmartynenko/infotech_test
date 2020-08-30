from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
from PIL import Image

# Create your models here.
class Message(models.Model):
    text = models.TextField(validators=[MinLengthValidator(1, "Your message is empty.")])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    image = models.ImageField(blank=True, upload_to="files")
