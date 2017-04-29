from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.db.models.signals import post_save
from django.dispatch import receiver
from slugify import slugify
from .fields import OrderField


class Subject(models.Model):
    title = models.CharField(verbose_name=_("Subject's title"), max_length=200)
    slug = models.SlugField(verbose_name=_("Subject's slug"), max_length=200,
                            unique=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class Course(models.Model):
    # иструктор курса
    owner = models.ForeignKey(User,
                              verbose_name=_("Course owner"),
                              related_name="courses_created")
    subject = models.ForeignKey(Subject,
                                verbose_name=_("Course subject"),
                                related_name="courses")
    title = models.CharField(verbose_name=_("Course title"), max_length=200)
    slug = models.SlugField(max_length=200,
                            verbose_name=_("Course slug"),
                            unique=True)
    # описание курса
    description = models.TextField(verbose_name=_("Course description"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Course created datetime"))
    students = models.ManyToManyField(User,
                                      related_name="courses_joined",
                                      verbose_name=_("Course students"),
                                      blank=True)

    def get_completed(self):
        if self.completed_course_lectures_by_student:
            c = self.completed_course_lectures_by_student.first()
            print(c, c.date_completed)
            return "{}".format(c.date_completed)

    class Meta:
        ordering = ('-created',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course,
                                verbose_name=_("Module course"),
                               related_name="modules")
    title = models.CharField(max_length=200, verbose_name=_("Module title"))
    description = models.TextField(blank=True, verbose_name=_("Module description"))
    order = OrderField(blank=True,
                       for_fields=['course'],
                       verbose_name=_("Module order"))

    class Meta:
        ordering = ['order']

    def __str__(self):
        return "{}. {}".format(self.order, self.title)


class Lecture(models.Model):
    module = models.ForeignKey(Module, related_name="lectures", verbose_name=_("Lecture module"))
    title = models.CharField(max_length=100, verbose_name=_("Lecture title"))
    order = OrderField(blank=True, for_fields=['module'], verbose_name=_("Lecture order"))

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Content(models.Model):
    lecture = models.ForeignKey(Lecture, related_name="contents", verbose_name=_("Content lecture"))
    # связь с моделью contentType
    content_type = models.ForeignKey(ContentType,
                                     limit_choices_to={
                                         'model__in': ('file',
                                                       'image',
                                                       'text',
                                                       'video',
                                                       'question')
                                     })
    # сохранение PK связанного объекта
    object_id = models.PositiveIntegerField()
    # определение обобщенной связи
    content_object = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True,
                       for_fields=['lecture'],
                       verbose_name=_("Content order"))

    class Meta:
        ordering = ['order']


class BaseContent(models.Model):
    owner = models.ForeignKey(User,
                              related_name="%(class)s_related",
                              verbose_name=_("Content owner"))
    title = models.CharField(max_length=250, default='', verbose_name=_("Content title"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Content created datetime"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Content updated datetime"))

    def render(self):
        return render_to_string('courses/content/{}.html'.format(
                        self._meta.model_name), {'item': self})

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class File(BaseContent):
    #file = models.FileField(upload_to="files")
    data_field = models.FileField(upload_to="files", verbose_name=_("File"))


class Image(BaseContent):
    #image = models.FileField(upload_to="images")
    data_field = models.FileField(upload_to="images", verbose_name=_("Image"))


class Text(BaseContent):
    #text = models.TextField()
    data_field = models.TextField(verbose_name=_("Text"))


class Video(BaseContent):
    #url = models.URLField()
    data_field = models.URLField(verbose_name=_("Video"))


class StudentLectureComplete(models.Model):
    student = models.ForeignKey(User, related_name="completed_course_lectures", verbose_name=_("Comleted lecture student"))
    course = models.ForeignKey(Course, related_name="completed_course_lectures_by_student", verbose_name=_("Completed lecture course"))
    # в модель добавлен модуль для формирования ссылки на последнюю пройденую лекцию в шаблоне списка курсов студента
    module = models.ForeignKey(Module, related_name="completed_module_lectures", verbose_name=_("Completed lecture module"))
    lecture = models.ForeignKey(Lecture, related_name="student_completed_lecture", verbose_name=_("Completed lecture"))
    #next_lecture = models.ForeignKey(Lecture, related_name="student_next_lecture")
    completed = models.BooleanField(default=False, verbose_name=_("Completed?"))
    # добавлено last field для обозначения была ли эта лекция последней в пройденом курсе
    last = models.BooleanField(default=False, verbose_name=_("Lecture is last?"))
    date_completed = models.DateTimeField(auto_now_add=True, verbose_name=_("Completed lecture datetime"))

    class Meta:
        ordering = ('-date_completed',)
        # указываем по какому полю будет будет определятся последняя запись
        get_latest_by = "date_completed"

    def __str__(self):
        return "user:{} course:{} lecture:{} date:{}".format(self.student.email,
                                                             self.course.id,
                                                             self.lecture.id,
                                                             self.date_completed)


class Question(BaseContent):
    data_field = models.TextField(blank=True, null=True, verbose_name="")


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name="answers", verbose_name=_("Question"))
    answer = models.CharField(max_length=100, verbose_name=_("Answer"))
    correct = models.BooleanField(default=False, verbose_name=_("Correct?"))

    def __str__(self):
        return self.answer
