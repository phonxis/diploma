from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse_lazy, reverse
from django.forms.models import modelform_factory, inlineformset_factory
from django.apps import apps
from django.db.models import Count, Q
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth import REDIRECT_FIELD_NAME, login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect, JsonResponse
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from nested_formset import nestedformset_factory
from .models import Course, Module, Content, Subject, Lecture
from .forms import ModuleFormSet, LectureForm, QuestionForm, AnswerForm
from students.forms import CourseEnrollForm, UsersLoginForm, UsersCreationForm#, InstructorsCreationForm


class IndexView(TemplateView):
    template_name = "index.html"


class InstructorMixin(PermissionRequiredMixin):
    """
    Миксин для предотвращения возможности студентам зайти на страницы
    которые должны быть доступны только инструктору
    """
    permission_required = "courses.add_course"


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
    fields = ['subject', 'title', 'description']
    # указание, куда будет перенаправлен пользователь
    # после подтверждения формы.
    # manage_course_list это имя URL в url.py
    success_url = reverse_lazy('manage_course_list')
    template_name = "courses/manage/course/form.html"


class ManageCourseListView(InstructorMixin, OwnerCourseMixin, ListView):
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



class CourseModuleUpdateView(InstructorMixin, TemplateResponseMixin, View):
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


class LectureCreateUpdateView(InstructorMixin, TemplateResponseMixin, View):
    model = Lecture
    template_name = "courses/manage/lecture/form.html"
    module = None
    obj = None

    def dispatch(self, request, module_id, lecture_id=None):
        self.module = get_object_or_404(Module,
                                        id=module_id,
                                        course__owner=request.user)
        # если указан lecture_id то возвращаем объект
        if lecture_id:
            self.obj = get_object_or_404(self.model,
                                         id=lecture_id,
                                         module__course__owner=request.user)
        return super(LectureCreateUpdateView, self).dispatch(request,
                                                             module_id,
                                                             lecture_id)

    def get(self, request, module_id, lecture_id=None):
        form = LectureForm(instance=self.obj)

        # получаем контент текущей лекции
        contents = Lecture.objects.filter(id=self.obj.id).values('contents')[0]

        # стандартно будут отображаться все кнопки добавления контента
        allowed_text = True
        allowed_image = True
        allowed_video = True
        allowed_file = True
        allowed_question = True
        # для обозначения, что ни одна из кнопок не отображается
        allowed_nothing = False

        if contents['contents']:
            # получаем id контента
            type_content_id = Content.objects.filter(id=contents['contents']).values('content_type')[0]['content_type']
            # получаем тип контента: текст, видео, файл, вопрос для теста, изображение
            name_content = ContentType.objects.filter(id=type_content_id).values('model')[0]['model']

            if name_content == 'text':
                # лекция содержит текствые данные. нельзя добавить видео и вопрос для теста
                allowed_video = False
                allowed_question = False
            elif name_content == 'image':
                # лекция содержит изображение. нельзя добавить видео и вопрос для теста
                allowed_video = False
                allowed_question = False
            elif name_content == 'video':
                # лекция содержит видео. к этой лекции больше нельзя ничего добавить
                allowed_text = False
                allowed_image = False
                allowed_video = False
                allowed_file = False
                allowed_question = False
                # указываем, что больше нельзя ничего добавить
                allowed_nothing = True
            elif name_content == 'file':
                # лекция содержит файл. нельзя добавить видео и вопрос для теста
                allowed_video = False
                allowed_question = False
            elif name_content == 'question':
                # лекция содержит вопрос для теста. можно добавить только еще один вопрос
                allowed_text = False
                allowed_image = False
                allowed_video = False
                allowed_file = False

        else:
            # если контента в этой лекции еще нет, то будут выведены все кнопки для добавления контента
            print('No content')

        return self.render_to_response({
                'form': form,
                'module': module_id,
                'lecture': lecture_id,
                'object': self.obj,

                'allowed_text': allowed_text,
                'allowed_image': allowed_image,
                'allowed_video': allowed_video,
                'allowed_file': allowed_file,
                'allowed_question': allowed_question,
                'allowed_nothing': allowed_nothing
            })

    def post(self, request, module_id, lecture_id):
        form = LectureForm(instance=self.obj, data=request.POST)

        if form.is_valid():
            new_obj = form.save(commit=False)
            new_obj.module = self.module
            new_obj.save()
            return redirect('module_lecture_list', self.module.id)

        else:
            return self.render_to_response({'form': form})


class ContentCreateUpdateView(InstructorMixin, TemplateResponseMixin, View):
    lecture = None
    module = None
    model = None
    obj = None
    template_name = "courses/manage/content/form.html"

    def get_model(self, model_name):
        # если имя модели соответствует одному из имен моделей контента
        # вернуть модель для app_label и model_name
        if model_name in ['text', 'file', 'image', 'video', 'question']:
            return apps.get_model(app_label="courses", model_name=model_name)
        # если модель нам не подходит
        return None

    def get_form(self, model, *args, **kwargs):
        # возвращает ModelForm для указаной model
        # со всеми полями кроме тех что указаны в exclude
        # print(model._meta.model_name)
        if model._meta.model_name in ['text']:
            # форма с полем data_field
            Form = modelform_factory(model, exclude=['owner',
                                                     'created',
                                                     'updated',
                                                     'title',
                                                     'order'],
                                            labels={'data_field': 'Type text below'}) #widgets={'data_field': SummernoteWidget()})
        elif model._meta.model_name in ['video']:
            # форма с полем data_field
            Form = modelform_factory(model, exclude=['owner',
                                                     'created',
                                                     'updated',
                                                     'title',
                                                     'order'],
                                            labels={'data_field': 'URL video'})
        elif model._meta.model_name in ['question']:
            # форма с полем data_field и title
            Form = modelform_factory(model,
                                    exclude=['owner',
                                             #'title',
                                             'created',
                                             'updated',
                                             'order'],
                                    labels={'data_field': 'Additional info for question', 'title': 'Question'})
        else:
            # форма для загрузки файлов и изображений
            Form = modelform_factory(model, exclude=['owner',
                                                     'created',
                                                     'updated',
                                                     'title',
                                                     'order'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, lecture_id, model_name, id=None):
        self.module = get_object_or_404(Module,
                                        id=module_id,
                                        course__owner=request.user)

        self.lecture = get_object_or_404(Lecture,
                                        id=lecture_id)

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
                                                             lecture_id,
                                                             model_name,
                                                             id)

    def get(self, request, module_id, lecture_id, model_name, id=None):
        # возвращаем форму для изменения экземпляра контента при self.obj!=None.
        # при None, будт возвращена форма для создания экземпляра контента.
        answer_form = None
        if model_name in ['text', 'video',]:
            form = self.get_form(self.model, instance=self.obj)
        elif model_name in ['question']:
            lecture_obj = Lecture.objects.get(id=lecture_id)
            # inline форма для добавления ответов к вопросу
            answer_form = AnswerForm(instance=self.obj)
            # форма для добавдения вопроса
            form = self.get_form(self.model, instance=self.obj)
        else:
            # для загрузки файлов и изображений django форма не нужна
            form = None
        return self.render_to_response({
                                        'form': form,
                                        'lecture': lecture_id,
                                        'module':module_id,
                                        'answer_form': answer_form,
                                        'object': self.obj,
                                        'model_name': model_name})

    def post(self, request, module_id, lecture_id, model_name, id=None):
        # возвращаем форму с данными и файлами
        data = {'error': True, 'name': 'none'}
        form = self.get_form(self.model,
                             instance=self.obj,
                             data=request.POST,
                             files=request.FILES)
        print(form.errors)
        if form.is_valid():
            # задаем владельцем контента текущего пользователя
            obj = form.save(commit=False)
            obj.owner = request.user

            if model_name in ['question']:
                answer_form = AnswerForm(request.POST, instance=self.obj)
                if answer_form.is_valid():
                    # сохраняем объект question
                    obj.save()
                    # добавляем question как parent для объектов answer
                    answer_form.instance = obj
                    answer_form.save()
                else:
                    print(answer_form.errors)
                if not id:
                    # если id объекта не указан, создаем новый экземпляр question
                    Content.objects.create(lecture=self.lecture, content_object=obj)
                return redirect('update_lecture', self.module.id, self.lecture.id)

            elif model_name in ['text']:
                # задаем стандартный title
                obj.title = 'Text object'
                obj.save()
                if not id:
                    # если id объекта не указан, создаем новый экземпляр text
                    Content.objects.create(lecture=self.lecture, content_object=obj)
                #return redirect('module_content_list', self.module.id)
                return redirect('update_lecture', self.module.id, self.lecture.id)
            elif model_name in ['video']:
                # задаем сстандартный title
                obj.title = 'Video object'
                obj.save()
                if not id:
                    # если id объекта не указан, создаем новый экземпляр video
                    Content.objects.create(lecture=self.lecture, content_object=obj)
                return redirect('update_lecture', self.module.id, self.lecture.id)

            # указываем название для файла или изображения
            obj.title = "_".join(obj.data_field.name.split('/')[-1].split('.')[:-1])
            data = {'name': obj.title}
            obj.save()

            # создать message для отображения уведомления что файл сохранен

            if not id:
                # если id объекта не указан, создаем новый экземпляр file или image
                Content.objects.create(lecture=self.lecture, content_object=obj)
            
            #return redirect('module_content_list', self.module.id)
            return JsonResponse(data)
        #return self.render_to_response({'form': form, 'object': self.obj})
        #data = {'error': True}
        return JsonResponse(data)


class ContentDeleteView(InstructorMixin, View):
    def post(self, request, id):
        content = get_object_or_404(Content,
                                    id=id,
                                    lecture__module__course__owner=request.user)
        module = content.lecture.module
        content.content_object.delete()
        content.delete()
        # возвращаемся к списку контента лекции
        return redirect('update_lecture', module.id, content.lecture.id)
        #return redirect('module_lecture_list', module.id)
        #return JsonResponse({"data": "ok"})


class ModuleLectureListView(InstructorMixin, TemplateResponseMixin, View):
    template_name = "courses/manage/module/lecture_list.html"

    def get(self, request, module_id):
        module = get_object_or_404(Module,
                                   id=module_id,
                                   course__owner=request.user)
        return self.render_to_response({'module': module})


class ModuleOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    """
    CsrfExemptMixin освобождает запрос от csrf token'а.
    JsonRequestResponseMixin - помещает правильно отформатированый
    json запрос в request_json; также сериализирует response
    """
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id,
                                course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})


class LectureOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    def post(self, request):
        for id, order in self.request_json.items():
            Lecture.objects.filter(id=id, module__course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})


class ContentOrderView(CsrfExemptMixin, JsonRequestResponseMixin, View):
    """
    CsrfExemptMixin освобождает запрос от csrf token'а.
    JsonRequestResponseMixin - помещает правильно отформатированый
    json запрос в request_json; также сериализирует response
    """
    def post(self, request):
        for id, order in self.request_json.items():
            print('id', id, ' -- ', order)
        for id, order in self.request_json.items():
            Content.objects.filter(id=id,
                                   #lecture__module__course__owner=request.user).update(order=order)
                                   owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})


class CourseListView(TemplateResponseMixin, View):
    """
    Список всех курсов
    """
    model = Course
    template_name = "courses/course/list.html"

    def get(self, request, subject=None):
        # возвращаем все subjects с количеством курсов для subject
        # пытаемся получить из кеша
        subjects = cache.get('all_subjects')
        if not subjects:
            # если этого объекта нет в кеше, тогда заносим его туда
            subjects = Subject.objects.annotate(total_courses=Count('courses'))
            cache.set('all_subjects', subjects)

        # возвращаем все courses с количеством модулей для курса
        courses = Course.objects.annotate(total_modules=Count('modules'))

        if subject:
            # если указан subject, фильтруем по нему все курсы
            subject = get_object_or_404(Subject, slug=subject)
            # создаем ключ для кеша
            key = 'subject_{}_courses'.format(subject.id)
            subject_courses = cache.get(key)
            if not subject_courses:
                subject_courses = courses.filter(subject=subject)
                cache.set(key, subject_courses)
            return self.render_to_response({'subjects': subjects,
                                        'subject': subject,
                                        'courses': subject_courses})
        else:
            # возвращаем все курсы
            all_courses = cache.get('all_courses')
            if not all_courses:
                # если нет в кеше, тогда заносим туда
                cache.set('all_courses', courses)
            return self.render_to_response({'subjects': subjects,
                                        'subject': subject,
                                        'courses': courses})


class CourseDetailView(DetailView):
    """
    Отображает единственный объект по его slug.
    Этот объект присваивается к self.object
    """
    model = Course
    template_name = "courses/course/detail.html"

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        # добавляем в контекст форму подписки на текущий объект курса
        #context['enroll_form'] = CourseEnrollForm(initial={'course': self.object})
        user_enrolled_this_course = Course.objects.filter(id=self.object.id).filter(students__id__exact=self.request.user.id).exists()
        if user_enrolled_this_course:
            context['enroll_form'] = None
        else:
            context['enroll_form'] = CourseEnrollForm(initial={'course': self.object})
        #print(self.object.get(students__in=[self.request.user.id]).exists())
        #print(User.objects.get(courses_joined=self.object))
        context['lecture_count'] = Lecture.objects.filter(module__course__id=self.object.id).count()
        return context


class LoginView(FormView):
    # вьюха для авторизации пользователей
    form_class = UsersLoginForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = "registration/login.html"

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(LoginView, self).dispatch(*args, **kwargs)

    def form_valid(self, form, request):
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url(request))

    def get_success_url(self, request):
        if request.user.has_perm('courses.add_course'):
            # если пользователь имеет права на создания курса, значит это инструктор
            return reverse_lazy('manage_course_list')
        else:
            # иначе студент
            return reverse_lazy('student_course_list')

    def set_test_cookie(self):
        self.request.session.set_test_cookie()

    def check_and_delete_test_cookie(self):
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
            return True
        return False

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        self.set_test_cookie()
        return super(LoginView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            self.check_and_delete_test_cookie()
            return self.form_valid(form, request)
        else:
            self.set_test_cookie()
            return self.form_invalid(form)


class InstructorRegistrationView(CreateView):
    template_name = 'registration/registration.html'
    form_class = UsersCreationForm #InstructorsCreationForm
    #success_url = reverse_lazy('manage_course_list')

    def form_valid(self, form):

        # после ввода корректных данных в signup форму юзер будет залогинен
        result = super(InstructorRegistrationView, self).form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password1'])
        login(self.request, user)

        return result

    # каждого пользователя, который зарегистрировался по ссылке instructor_registration
    # добавляем в группу Instructor
    def get_success_url(self):
        # Получаем из БД группу преподавателей
        # При регистрации первого преподавателя, эта группа будет создана
        group, created = Group.objects.get_or_create(name='Instructor')
        if created:
            # сохраняем группу, если до этого она не была создана
            group.save()

            # отфильтровываем нужные для группы преподавателей разрешения
            # и добавляем их в эту группу (Group m2m relationship Permission)
            [group.permissions.add(perm) for perm in Permission.objects.filter(
                name__in=[
                    'Can add content', 'Can change content', 'Can delete content',
                    'Can add course', 'Can change course', 'Can delete course',
                    'Can add file', 'Can change file', 'Can delete file',
                    'Can add image', 'Can change image', 'Can delete image',
                    'Can add module', 'Can change module', 'Can delete module',
                    'Can add text', 'Can change text', 'Can delete text',
                    'Can add video', 'Can change video', 'Can delete video',
                ]
            )]
        # добавляем текущего пользователя в группу преподавателей
        group.user_set.add(self.object)

        return reverse('manage_course_list')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        return super(InstructorRegistrationView, self).get(request, *args, **kwargs)

