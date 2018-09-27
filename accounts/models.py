from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<id>/<filename>
    return 'accounts/{0}/{1}'.format(instance.pk, filename)


class Account(User):
    birth_date = models.DateField()
    bio = models.TextField()
    # Enforce bio minimum length in form?
    avatar = models.ImageField(blank=True, null=True,
                               upload_to=user_directory_path)
    country = models.CharField(default=None, max_length=250)
    website = models.URLField(default=None)
