from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'sign_in/$', views.sign_in, name='sign_in'),
    url(r'login/$', views.sign_in, name='login'),
    url(r'sign_up/$', views.sign_up, name='sign_up'),
    url(r'sign_up_account/$', views.sign_up_account, name='register'),
    url(r'sign_out/$', views.sign_out, name='sign_out'),
    url(r'(?P<pk>\d+)/profile/$', views.profile, name='profile'),
    url(r'(?P<pk>\d+)/profile/bio/$', views.profile_bio, name='bio'),
    url(r'(?P<pk>\d+)/profile/edit/$', views.profile_edit, name='edit'),
    url(r'(?P<pk>\d+)/profile/change_password/$', views.pw_edit, name='pw_edit'),
    url(r'profile/list/$', views.profile_list, name='list'),
]
