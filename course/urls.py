from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib import admin
from . import views
from course import views as core_views

urlpatterns = [
    # template urls
    url(r'^$', views.homepage, name='homepage'),

    # authentification system urls
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),

    # admin page url
    url(r'^admin/', admin.site.urls),
    ]
