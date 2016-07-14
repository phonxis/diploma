from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^list/$',
        views.ManageCourseListView.as_view(),
        name="manage_course_list"),
    url(r'^create/$',
        views.CourseCreateView.as_view(),
        name="create_course"),
    url(r'^(?P<pk>\d+)/edit/$',
        views.CourseUpdateView.as_view(),
        name="edit_course"),
    url(r'^(?P<pk>\d+)/delete/$',
        views.CourseDeleteView.as_view(),
        name="delete_course"),
]
