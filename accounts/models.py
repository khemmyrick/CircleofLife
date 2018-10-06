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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Use one-to-one field object?
    ## Is the following Django docs example linking MySpecialUser to two different models,
    ## Or is the user attribute supposed to represent the MySpecialUser instance itself?
    ## Also, does AUTH_USER_MODEL need to be added to settings?  How does that work?
    '''
    class MySpecialUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    supervisor = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='supervisor_of',
    )
    '''