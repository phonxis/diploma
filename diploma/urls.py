from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth
from django.conf import settings
from django.conf.urls.static import static
from courses.views import CourseListView, IndexView, LoginView
from students.forms import UsersLoginForm


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'accounts/login/$', LoginView.as_view(), name="login"),
    #url(r'^accounts/login/$', auth.login, {'authentication_form': UsersLoginForm}, name="login"),
    url(r'^accounts/logout/$', auth.logout, {'next_page': '/'}, name="logout"),
    url(r'^course/', include('courses.urls')),
    url(r'^courses/$', CourseListView.as_view(), name="course_list"),
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^students/', include('students.urls')),

    # social auth
    url(r'^social/', include('social_django.urls', namespace='social'))
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
