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

    #url(r'^module/(?P<module_id>\d+)/content/(?P<model_name>\w+)/create/$',
    #    views.ContentCreateUpdateView.as_view(),
    #    name="create_module_content"),

    #url(r'^module/(?P<module_id>\d+)/content/(?P<model_name>\w+)/(?P<id>\d+)/$',
    #    views.ContentCreateUpdateView.as_view(),
    #    name="update_module_content"),


    # create lecture
    url(r'^module/(?P<module_id>\d+)/lecture/create/$',
        views.LectureCreateUpdateView.as_view(),
        name="create_lecture"),
    # update lecture
    url(r'module/(?P<module_id>\d+)/lecture/(?P<lecture_id>\d+)/$',
        views.LectureCreateUpdateView.as_view(),
        name="update_lecture"),
    # delete lecture
    url(r'lecture/(?P<lecture_id>\d+)/delete/$',
        views.LectureDeleteView.as_view(),
        name="delete_lecture"),
    # create lecture content
    url(r'^module/(?P<module_id>\d+)/lecture/(?P<lecture_id>\d+)/content/(?P<model_name>\w+)/create/$',
        views.ContentCreateUpdateView.as_view(),
        name="create_lecture_content"),
    # update lecture content
    url(r'^module/(?P<module_id>\d+)/lecture/(?P<lecture_id>\d+)/content/(?P<model_name>\w+)/(?P<id>\d+)/$',
        views.ContentCreateUpdateView.as_view(),
        name="update_lecture_content"),


    url(r'^content/(?P<id>\d+)/delete/$',
        views.ContentDeleteView.as_view(),
        name="delete_lecture_content"),
    url(r'^module/(?P<module_id>\d+)/$',
        views.ModuleLectureListView.as_view(),
        name="module_lecture_list"),
    url(r'^module/order/$',
        views.ModuleOrderView.as_view(),
        name="order_modules"),
    url(r'^content/order/$',
        views.ContentOrderView.as_view(),
        name="order_content"),

    url(r'^lecture/order/$',
        views.LectureOrderView.as_view(),
        name="order_lecture"),

    url(r'^subject/(?P<subject>[\w-]+)/$',
        views.CourseListView.as_view(),
        name="subject_course_list"),
    url(r'^(?P<slug>[\w-]+)/$',
        views.CourseDetailView.as_view(),
        name="course_detail"),


    #url(r'^module/(?P<module_id>\d+)/quiz/create/$',
    #    views.CreateQuizView.as_view(),
    #    name="create_quiz"),

    #url(r'^module/(?P<module_id>\d+)/quiz/(?P<pk>\d+)/$',
    #    views.UpdateQuizView.as_view(),
    #    name="update_quiz"),
]
