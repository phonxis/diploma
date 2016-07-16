from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.forms.models import modelform_factory
from django.apps import apps
from django.views.generic.list import ListView
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import Course, Module, Content
from .forms import ModuleFormSet


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


class CourseModuleUpdateView(TemplateResponseMixin, View):
    """
    Класс используется для добавления, обновления и удаления модулей
    определенного курса.
    --------------------
    TemplateResponseMixin используется для отображения templates, для него
    обязательно нужно указывать template_name или реализовать
    метод get_template_names; имеет метод render_to_response
    для отображения context в template
    --------------------
    View реализует метод dispatch, который анализирует response на метод запроса
    и в зависимости от его типа отправляет его нужному методу (get(), post()...)
    """
    template_name = "courses/manage/module/formset.html"
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        # ищем определенный курс текущего пользователя
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super(CourseModuleUpdateView, self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        # создаем пустой formset
        formset = self.get_formset()
        return self.render_to_response({'course': self.course,
                                        'formset': formset})

    def post(self, request, *args, **kwargs):
        # создаем formset с данными
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course': self.course,
                                        'formset': formset})


class CourseModuleUpdateView(TemplateResponseMixin, View):
    """
    Класс используется для добавления, обновления и удаления модулей
    определенного курса.
    --------------------
    TemplateResponseMixin используется для отображения templates, для него
    обязательно нужно указывать template_name или реализовать
    метод get_template_names; имеет метод render_to_response
    для отображения context в template
    --------------------
    View реализует метод dispatch, который анализирует response на метод запроса
    и в зависимости от его типа отправляет его нужному методу (get(), post()...)
    """
    template_name = "courses/manage/module/formset.html"
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)

    def dispatch(self, request, pk):
        # ищем определенный курс текущего пользователя
        self.course = get_object_or_404(Course, id=pk, owner=request.user)
        return super(CourseModuleUpdateView, self).dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        # создаем пустой formset
        formset = self.get_formset()
        return self.render_to_response({'course': self.course,
                                        'formset': formset})

    def post(self, request, *args, **kwargs):
        # создаем formset с данными
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course': self.course,
                                        'formset': formset})


class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = "courses/manage/content/form.html"

    def get_model(self, model_name):
        # если имя модели соответствует одному из имен моделей контента
        # вернуть модель для app_label и model_name
        if model_name in ['text', 'file', 'image', 'video']:
            return apps.get_model(app_label="courses", model_name=model_name)
        # если модель нам не подходит
        return None

    def get_form(self, model, *args, **kwargs):
        # возвращает ModelForm для указаной model
        # со всеми полями кроме тех что указаны в exclude
        Form = modelform_factory(model, exclude=['owner'
                                                'created',
                                                'updated',
                                                'order', 'owner'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        # получаем модуль с которым будет асоциирован объект
        self.module = get_object_or_404(Module,
                                        id=module_id,
                                        course__owner=request.user)
        # получаем модель которая будет соответсвотать типу контента
        self.model = self.get_model(model_name)
        # если не None, то объект будет обновлен, иначе будет создан новый
        if id:
            self.obj = get_object_or_404(self.model,
                                        id=id,
                                        owner=request.user)
        # вызываем метод родителя
        return super(ContentCreateUpdateView, self).dispatch(request,
                                                            module_id,
                                                            model_name,
                                                            id)

    def get(self, request, module_id, model_name, id=None):
        # возвращаем форму для изменения экземпляра контента при self.obj!=None.
        # при None, будт возвращена форма для создания экземпляра контента.
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form,
                                        'object': self.obj})

    def post(self, request, module_id, model_name, id=None):
        # возвращаем форму с данными и файлами
        form = self.get_form(self.model,
                            instance=self.obj,
                            data=request.POST,
                            files=request.FILES)
        if form.is_valid():
            # задаем владельцем контента текущего пользователя
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                # если id объекта не указан, создаем новый экземпляр
                Content.objects.create(module=self.module, content_object=obj)
            return redirect('module_content_list', self.module.id)
        return self.render_to_response({'form': form, 'object': self.obj})


class ContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(Content,
                                    id=id,
                                    module__course__owner=request.user)
        module = content.module
        content.content_object.delete()
        content.delete()
        # возвращаемся к списку контента модуля
        return redirect('module_content_list', module.id)


class ModuleContentListView(TemplateResponseMixin, View):
    template_name = "courses/manage/module/content_list.html"

    def get(self, request, module_id):
        module = get_object_or_404(Module,
                                    id=module_id,
                                    course__owner=request.user)
        return self.render_to_response({'module': module})