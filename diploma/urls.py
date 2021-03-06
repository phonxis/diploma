from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from rest_framework import routers
from courses.views import CourseListView, IndexView, LoginView, InstructorRegistrationView
from students.views import add
from students.forms import UsersLoginForm
from courses.viewsets import QuestionViewSet, LectureViewSet, ContentViewSet, QuestionList


router = routers.DefaultRouter()
router.register(r'questions', QuestionViewSet)
router.register(r'lectures', LectureViewSet)
router.register(r'contents', ContentViewSet)


urlpatterns = i18n_patterns(
    url(r'^admin/', admin.site.urls),
    url(r'accounts/login/$', LoginView.as_view(), name="login"),
    #url(r'^accounts/login/$', auth.login, {'authentication_form': UsersLoginForm}, name="login"),
    url(r'^accounts/logout/$', auth.logout, {'next_page': '/'}, name="logout"),
    url(r'^course/', include('courses.urls')),
    url(r'^courses/$', CourseListView.as_view(), name="course_list"),
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^students/', include('students.urls')),

    # регистрация преподавателей
    url(r'^accounts/registration/$',
        InstructorRegistrationView.as_view(),
        name='instructor_registration'),

    # social auth
    url(r'^social/', include('social_django.urls', namespace='social')),
    # for nested_admin app
    url(r'^nested_admin/', include('nested_admin.urls')),
    # api urls
    url(r'api/', include(router.urls)),
    url(r'api1/(?P<ids>.+)/$', QuestionList.as_view()),

    # avatar
    url(r'^avatar/', include('avatar.urls')),
    # update avatar
    url(r'^avatar/add-or-update/$', add, name='add_update_avatar'),

    # for internationalization with rosetta
    url(r'^rosetta/', include('rosetta.urls')),
)

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)
