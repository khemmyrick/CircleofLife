from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    return 'accounts/{0}/{1}'.format(instance.pk, filename)


class Account(models.Model):
    birth_date = models.DateField()
    bio = models.TextField()
    avatar = models.ImageField(blank=True, null=True,
                               upload_to=user_directory_path)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Does the Django docs example link MySpecialUser to two different models,
    # Or is the user attribute supposed to represent the MySpecialUser instance itself?
    # AUTH_USER_MODEL is for replacing User model. Shouldn't need it here.
    account = models.OneToOneField(
        on_delete=models.CASCADE,
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='classic_user',
    )
