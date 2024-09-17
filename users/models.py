from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify

from PIL import Image
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    birth_date = models.DateField(blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    image = models.ImageField(blank=True, null=True, default='users/author.png', upload_to='users')
    slug = models.SlugField(editable=False, unique=True)

    def save(self, *args, **kwargs):
        self.slug   = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            new_size = (300, 300)
            img.thumbnail(new_size)
            img.save(self.image.path)

    def __str__(self):
        return self.user.username
    
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_profile, sender=settings.AUTH_USER_MODEL)