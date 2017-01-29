from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateResponseMixin, View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseRedirect, JsonResponse
from django.db import transaction
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from courses.models import Course, Module, Lecture, Content, StudentLectureComplete
from .models import Profile
from .forms import CourseEnrollForm, UsersLoginForm, UsersCreationForm, ProfileEditForm, UserEditForm


class StudentRegistrationView(CreateView):
    template_name = "students/student/registration.html"
    form_class = UsersCreationForm
    success_url = reverse_lazy('student_course_list')

    def form_valid(self, form):
        # после ввода корректных данных в signup форму юзер будет залогинен
        result = super(StudentRegistrationView, self).form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'], password=cd['password1'])
        login(self.request, user)

        # создание профиля для пользователя (для createsuperuser и social_auth не работает)
        #profile = Profile.objects.create(user=user)

        return result

    def get(self, request, *args, **kwargs):
        # если пользователь уже авторизован и пытается перейти на страницу
        # регистрации,то он будет перенаправлен на главную страницу
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        return super(StudentRegistrationView, self).get(request, *args, **kwargs)


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        # добавляем текущего пользователя к студентам курса
        self.course.students.add(self.request.user)
        # если форма валидна, пользователль будет перенаправлен
        # на URL из get_success_url
        return super(StudentEnrollCourseView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('student_course_detail', args=[self.course.id])


class StudentCourseListView(LoginRequiredMixin, ListView):
    """
    Список курсов на которые подписан студент
    """
    model = Course
    template_name = "students/course/list.html"
    queryset = Course.objects.prefetch_related('completed_course_lectures_by_student')

    def get_queryset(self):
        queryset = super(StudentCourseListView, self).get_queryset()
        return queryset.filter(students__in=[self.request.user])


'''
class ModuleDetail(JsonRequestResponseMixin, View):

    def get(self, request):
        module_id = request.GET['module_id']
        print(module_id)
        module = Module.objects.filter(id=module_id).values()#.values_list
        lectures = Lecture.objects.filter(module_id=module_id).values()
        print(module)
        print(lectures)
        resp = {'module': list(module), 'lectures': list(lectures)}
        return self.render_json_response(resp)
'''


'''
class LectureDetail(JsonRequestResponseMixin, View):

    def get(self, request):
        lecture_id = request.GET['lecture_id']
        print(lecture_id)
        lecture = Lecture.objects.filter(id=lecture_id).values()#.values_list
        content = Content.objects.filter(lecture_id=lecture_id).values()
        print(lecture)
        print(content)
        resp = {'lecture': list(lecture), 'content': list(content)}
        return self.render_json_response(resp)
'''


class StudentCourseDetailView(DetailView):
    """
    Отображение одного из курсов на которые подписан студент
    """
    model = Course
    template_name = "students/course/detail.html"

    def get_queryset(self):
        queryset = super(StudentCourseDetailView, self).get_queryset()
        # когда написано следующая строка
        # return queryset.filter(students__in=[self.request.user])
        # возникает ошибка in get_prep_value return(value) not be SimpleLazyObject
        return queryset.filter(students__in=[self.request.user.id])

    def get_context_data(self, **kwargs):
        context = super(StudentCourseDetailView,
                        self).get_context_data(**kwargs)
        course = self.get_object()

        #if 'module_id' in self.kwargs and not 'lecture_id' in self.kwargs:
        #    # если в параметрах вызова явно указан ид модуля
        #    # то возвращаем этот модуль
        #    context['module'] = course.modules.get(id=self.kwargs['module_id'])
        #    print(context['module'])

        if 'lecture_id' in self.kwargs and 'module_id' in self.kwargs:
            # если в URL указываются id лекции и модуля
            # то нужно вернуть указаную лекцию из указаного модуля
            context['lecture'] = Lecture.objects.get(id=self.kwargs['lecture_id'])

            context['module_id'] = self.kwargs['module_id']

            try:
                # пытаемся получить следующую (по order) лекцию этого же модуля
                context['next_lecture'] = Lecture.objects.filter(module__id=context['module_id'],
                                                                 order=context['lecture'].order+1).values('id')[0]
            except Exception:
                # если же получить лекцию невозможно
                # то переходим к следующему(по order) модулю этого же курса
                try:
                    # получаем объект модуля
                    module = Module.objects.get(id=self.kwargs['module_id'])
                    # получаем следующий модуль (order + 1)
                    next_module = Module.objects.get(course__id=course.id,
                                                     order=module.order+1)#.values('id')[0]
                    # получаем первую лекцию этого модуля (order = 0)
                    context['next_lecture'] = Lecture.objects.filter(module__id=next_module.id,
                                                                     order=0).values('id')[0]
                    # в контексте шаблона изменяем текущий модуль на следующий
                    context['module_id'] = next_module.id
                except Exception:
                    # исключение, если в этом курсе нет следующего модуля
                    # и нет следующей лекции
                    context['next_lecture'] = None
                    # указываем что курс был полностью пройден
                    context['complete_course'] = True
        else:
            # если id модуля и лекции не указаны
            # то будет отображатся содержание курса
            context['modules'] = course.modules.all()


            # иначе возвращаем первый модуль курса
            #try:
            #    context['module'] = course.modules.all()[0]
            #except IndexError:
            #    # ниодного модуля еще не было добавлено
            #    pass

        return context

    def get(self, request, *args, **kwargs):
        # получаем объект курса и его контекст для template
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        # получаем id лекции
        completed_lecture = request.GET.get('prev-lecture', None)
        prev_module = request.GET.get('prev-module', None)

        if 'lecture_id' in self.kwargs and 'module_id' in self.kwargs and completed_lecture and prev_module:
            # если указано id лекции и модуля и получено id пройденой лекции
            # то получаем следующие объекты из БД:
            student = User.objects.get(id=request.user.id)# студент
            lecture = Lecture.objects.get(id=int(completed_lecture))# пройденая лекция
            module = Module.objects.get(id=int(prev_module))# модуль последне пройденой лекции
            lecture_complete, created = StudentLectureComplete.objects.get_or_create(student=student,
                                                                                     course=self.object,
                                                                                     module=module,
                                                                                     lecture=lecture,
                                                                                     completed=True,
                                                                                     last=False)
            if created:
                # сохраняем пройденую лекцию
                lecture_complete.save()

        # получаем суммарное количество лекций курса
        course_lectures = Lecture.objects.filter(module__course__id=self.object.id).count()
        # получаемколичество лекций курса пройденого определенным студентом
        completed_lectures = StudentLectureComplete.objects.filter(student__id=request.user.id, course__id=self.object.id).count()

        # определяем процент пройденых лекций
        context['lectures_completed'] = (completed_lectures / course_lectures) * 100

        return self.render_to_response(context)


class CourseCompleted(View):
    def get(self, request, *args, **kwargs):
        # получаем id последней лекции курса
        last_lecture = request.GET.get('prev-lecture', None)
        # получаем id курса
        prev_course = request.GET.get('prev-course', None)
        # получаем id последнего модуля курса
        prev_module = request.GET.get('prev-module', None)

        if last_lecture and prev_course and prev_module:
            # если все id не равны None
            # то получаем следующие объекты:
            student = User.objects.get(id=request.user.id)# студент который прошел курс 
            lecture = Lecture.objects.get(id=int(last_lecture))# последняя лекция курса
            module = Module.objects.get(id=int(prev_module))# последний модуль курса
            course = Course.objects.get(id=prev_course)# курс, который был пройден
            # проверяем, был ли ранее пройден студентом этот курс
            lecture_complete, created = StudentLectureComplete.objects.get_or_create(student=student,
                                                                                     course=course,
                                                                                     module=module,
                                                                                     lecture=lecture,
                                                                                     completed=True,
                                                                                     last=True)

            if created:
                # сохраняем, если раньше студент не оканчивал этот курс
                lecture_complete.save()

            return render(request, 'students/course/completed_course.html', {
                'course': course
            })

        # если хотя бы одна id не была получена, то перенаправляем студента
        return redirect('student_course_list')


'''
class StudentModuleDetailView(DetailView):
    model = Module
    template_name = "students/course/lecture.html"

    #def get_queryset(self):
    #    queryset = super(StudentModuleDetailView, self).get_queryset()
    #    print(queryset)
    #    return queryset.filter(course__students__in=[self.request.user])

    def get_context_data(self, **kwargs):
        context = super(StudentModuleDetailView,
                        self).get_context_data(**kwargs)
        module = self.get_object()

        context['course'] = module.course.id

        if 'lecture_id' in self.kwargs:
            print(self.kwargs)
            # если в параметрах вызова явно указан ид модуля
            # то возвращаем этот модуль
            context['lecture'] = module.lectures.get(id=self.kwargs['lecture_id'])
            #print(context['lecture'].contents)
        else:
            # иначе возвращаем первый модуль курса
            try:
                context['lecture'] = module.lectures.all()[0]
            except IndexError:
                # ниодного модуля еще не было добавлено
                pass
        return context
'''


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        # формы с подтвержденными данными пользователя, отображаются после submit формы
        user_form = UserEditForm(data=request.POST, instance=request.user)
        profile_form = ProfileEditForm(data=request.POST,
                                       instance=request.user.profile,
                                       #files=request.FILES
                                       )

        if user_form.is_valid() and profile_form.is_valid():
            # если формы без ошибок, то сохраняем их
            user_form.save()
            profile_form.save()

            messages.success(request, 'Profile update successfully')
        else:
            messages.error(request, 'Correct errors')
    else:
        # отображение форм с данными из БД (которые были ранее сохранены)
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'students/student/edit_profile.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })