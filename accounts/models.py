from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    return 'accounts/{0}/{1}'.format(instance.pk, filename)


class Account(models.Model):
    dob = models.DateField()
    bio = models.TextField()
    ava = models.ImageField(blank=True, null=True,
                            upload_to=user_directory_path)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='classic_user',
    )
    
    def __str__(self):
        '''Display account objects as usernames in admin.'''
        return self.user.username
