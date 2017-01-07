from django.conf.urls import url
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = [
    url(r'^register/$',
        views.StudentRegistrationView.as_view(),
        name="student_registration"),
    url(r'^enroll/$',
        views.StudentEnrollCourseView.as_view(),
        name="student_enroll_course"),
    url(r'^courses/$',
        cache_page(60 * 30)(views.StudentCourseListView.as_view()),
        name="student_course_list"),
    url(r'^course/(?P<pk>\d+)/$',
        cache_page(60 * 30)(views.StudentCourseDetailView.as_view()),
        name="student_course_detail"),
    url(r'^course/(?P<pk>\d+)/(?P<module_id>\d+)/$',
        cache_page(60 * 30)(views.StudentCourseDetailView.as_view()),
        name="student_course_detail_module"),

    # изменения данны профиля студентов
    url(r'^profile/$',
        views.update_profile,
        name="update_profile"),
]
