from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


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

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title


class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name="modules")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Content(models.Model):
    module = models.ForeignKey(Module, related_name="contents")
    # связь с моделью contentType
    content_type = models.ForeignKey(ContentType)
    # сохранение PK связанного объекта
    object_id = models.PositiveIntegerField()
    # определение обобщенной связи
    content_object = GenericForeignKey('content_type', 'object_id')

