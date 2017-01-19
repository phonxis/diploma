from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.db.models.signals import post_save
from django.dispatch import receiver
from slugify import slugify
from .fields import OrderField


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,
                            unique=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title


class Course(models.Model):
    # иструктор курса
    owner = models.ForeignKey(User,
                              related_name="courses_created")
    subject = models.ForeignKey(Subject,
                                related_name="courses")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,
                            unique=True)
    # описание курса
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(User,
                                      related_name="courses_joined",
                                      blank=True)

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
                               related_name="modules")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True,
                       for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return "{}. {}".format(self.order, self.title)


class Lecture(models.Model):
    module = models.ForeignKey(Module, related_name="lectures")
    title = models.CharField(max_length=100)
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


class Content(models.Model):
    lecture = models.ForeignKey(Lecture, related_name="contents")
    # связь с моделью contentType
    content_type = models.ForeignKey(ContentType,
                                     limit_choices_to={
                                         'model__in': ('file',
                                                       'image',
                                                       'text',
                                                       'video')
                                     })
    # сохранение PK связанного объекта
    object_id = models.PositiveIntegerField()
    # определение обобщенной связи
    content_object = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True,
                       for_fields=['lecture'])

    class Meta:
        ordering = ['order']


class BaseContent(models.Model):
    owner = models.ForeignKey(User,
                              related_name="%(class)s_related")
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def render(self):
        return render_to_string('courses/content/{}.html'.format(
                        self._meta.model_name), {'item': self})

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class File(BaseContent):
    #file = models.FileField(upload_to="files")
    data_field = models.FileField(upload_to="files")


class Image(BaseContent):
    #image = models.FileField(upload_to="images")
    data_field = models.FileField(upload_to="images")


class Text(BaseContent):
    #text = models.TextField()
    data_field = models.TextField()


class Video(BaseContent):
    #url = models.URLField()
    data_field = models.URLField()
