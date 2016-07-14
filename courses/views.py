from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Course


class OwnerMixin(object):
    """
    Миксин переопределяющий метод get_queryset
    во всех дочерних классах.
    Может взаимодействовать со всеми моделями
    у которых есть атрибут owner.
    """

    def get_queryset(self):
        """
        вернуть объекты созданные только текущим пользователем
        """
        queryset = super(OwnerMixin, self).get_queryset()
        return queryset.filter(owner=self.request.user)


class OwnerEditMixin(object):
    """
    Миксин переопределяющий метод form_valid
    во всех дочерних классах.
    """

    def form_valid(self, form):
        """
        С помощью этого метода при создании объекта(подтверждение формы)
        задается владелец этого объекта.
        """
        form.instance.owner = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)


class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin):
    """
    Указание модели для queryset во всех дочерних классах
    """
    model = Course


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    """
    Миксин который должен использоватся в классах изменяющиюх
    или создающих объекты модели Course
    """

    # указание полей для форм дочерних классов
    fields = ['subject', 'title', 'slug', 'description']
    # указание, куда будет перенаправлен пользователь
    # после подтверждения формы.
    # manage_course_list это имя URL в url.py
    success_url = reverse_lazy('manage_course_list')
    template_name = "courses/manage/course/form.html"


class ManageCourseListView(OwnerCourseMixin, ListView):
    """
    Используя наследование от OwnerCourseMixin, ListView
    этот класс также будет содержать все поля и методы из
    OwnerCourseMixin, ListView, OwnerMixin
    """
    template_name = "courses/manage/course/list.html"


class CourseCreateView(PermissionRequiredMixin, OwnerCourseEditMixin, CreateView):
    """
    Используется для создания нового Course
    """

    # PermissionRequiredMixin проверяет если у пользователя указанный
    # permission_required
    permission_required = "courses.add_course"


class CourseUpdateView(PermissionRequiredMixin, OwnerCourseEditMixin, UpdateView):
    """
    Используется для изменения Course
    """

    # PermissionRequiredMixin проверяет если у пользователя указанный
    # permission_required
    permission_required = "courses.change_course"


class CourseDeleteView(PermissionRequiredMixin, OwnerCourseMixin, DeleteView):
    """
    Используется для удаления Course
    """

    # PermissionRequiredMixin проверяет если у пользователя указанный
    # permission_required
    permission_required = "courses.delete_course"
    # указание, куда будет перенаправлен пользователь
    # после подтверждения формы.
    # manage_course_list это имя URL в url.py
    success_url = reverse_lazy('manage_course_list')
    template_name = "courses/manage/course/delete.html"
