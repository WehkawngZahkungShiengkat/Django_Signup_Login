from django.db import models
from django.contrib.auth.models import User

#########
#username - ahhkawng
#password - 12345
#########

# Create your models here.

class UserProfileInfo(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)

    portfolio_site = models.URLField(blank=True)

    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        return self.user.username

    def picreturn(self):
        return self.profile_pic
