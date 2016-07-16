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
    url(r'^(?P<pk>\d+)/module/$',
        views.CourseModuleUpdateView.as_view(),
        name="update_course_module"),
    url(r'^module/(?P<module_id>\d+)/content/(?P<model_name>\w+)/create/$',
        views.ContentCreateUpdateView.as_view(),
        name="create_module_content"),
    url(r'^module/(?P<module_id>\d+)/content/(?P<model_name>\w+)/(?P<id>\d+)/$',
        views.ContentCreateUpdateView.as_view(),
        name="update_module_content"),
    url(r'^content/(?P<id>\d+)/delete/$',
        views.ContentDeleteView.as_view(),
        name="delete_module_content"),
    url(r'^module/(?P<module_id>\d+)/$',
        views.ModuleContentListView.as_view(),
        name="module_content_list")
]
