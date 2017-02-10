from django.conf.urls import url
from django.views.decorators.cache import cache_page
from . import views

urlpatterns = [
    #регистрация студентов
    url(r'^registration/$',
        views.StudentRegistrationView.as_view(),
        name="student_registration"),

    # подписка студента на курс
    url(r'^enroll/$',
        views.StudentEnrollCourseView.as_view(),
        name="student_enroll_course"),

    # список курсов на которые подписан студент
    url(r'^courses/$',
        #cache_page(60 * 30)(views.StudentCourseListView.as_view()),
        views.StudentCourseListView.as_view(),
        name="student_course_list"),

    # содержание курса
    url(r'^courses/(?P<pk>\d+)/$',
        #cache_page(60 * 30)(views.StudentCourseDetailView.as_view()),
        views.StudentCourseDetailView.as_view(),
        name="student_course_detail"),

    #
    #url(r'courses/(?P<pk>\d+)/curriculum/$',
    #    views.course_curriculum,
    #    name="student_course_curriculum"),

    # about курса
    url(r'courses/(?P<pk>\d+)/about/$',
        views.course_about,
        name="student_course_about"),

    # отображение модуля курса
    url(r'^courses/(?P<pk>\d+)/modules/(?P<module_id>\d+)/$',
        #cache_page(60 * 30)(views.StudentCourseDetailView.as_view()),
        views.StudentCourseDetailView.as_view(),
        name="student_course_detail_module"),

    # лекция курса
    url(r'^courses/(?P<pk>\d+)/modules/(?P<module_id>\d+)/lectures/(?P<lecture_id>\d+)/$',
        #cache_page(60 * 30)(views.StudentCourseDetailView.as_view()),
        views.StudentCourseDetailView.as_view(),
        name="student_course_detail_module_lecture"),

    # изменения данных профиля студентов/преподавателей
    url(r'^profile/$',
        views.update_profile,
        name="update_profile"),

    # отображение контента лекций
    #url(r'^course/(?P<course_id>\d+)/(?P<pk>\d+)/(?P<lecture_id>\d+)/$',
    #    views.StudentModuleDetailView.as_view(),
    #    name="lecture_detail"),

    #url(r'module-detail/$',
    #    views.ModuleDetail.as_view(),
    #    name="detailed_module"),

    #url(r'lecture-detail/$',
    #    views.LectureDetail.as_view(),
    #    name="detailed_lecture"),

    # страница оповещающая об окончании курса
    url(r'course/completed/$',
        views.CourseCompleted.as_view(),
        name="course_completed"),
]
