from django.db import models
from django.contrib.auth.models import User
from PIL import Image

from staffing.models import Restaurant, Location


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # the restaurant field will be set only for restaurant admins
    restaurant = models.ForeignKey(Restaurant, blank=True, null=True, on_delete=models.CASCADE)
    # the location field will be set only for hiring managers
    location = models.ForeignKey(Location, blank=True, null=True, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    # Scale photo size down
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)





