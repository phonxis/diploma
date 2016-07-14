from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', auth.login, name="login"),
    url(r'^accounts/logout/$', auth.logout, name="logout"),
    url(r'^course/', include('courses.urls')),
]
