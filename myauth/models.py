from django.contrib.auth.models import User
from django.db import models

# Create your models here.


def avatar_images_directory_path(instance: "Profile", filename: str):
    return "avatar/user_{pk}/images/{filename}".format(
        pk=instance.user.pk,
        filename=filename,
    )
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    agreement_accepted = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True, upload_to=avatar_images_directory_path)
