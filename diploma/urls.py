from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth
from django.conf import settings
from django.conf.urls.static import static
from courses.views import CourseListView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', auth.login, name="login"),
    url(r'^accounts/logout/$', auth.logout, name="logout"),
    url(r'^course/', include('courses.urls')),
    url(r'^$', CourseListView.as_view(), name="course_list"),
    url(r'^students/', include('students.urls')),
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
