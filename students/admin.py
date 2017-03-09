from django.contrib import admin
from django.contrib.auth.models import User
from nested_admin import NestedModelAdmin, NestedTabularInline
from .models import Profile
from courses.models import Question, Answer


admin.site.unregister(User)

class ProfileInline(admin.TabularInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    inlines = [ProfileInline,]

admin.site.register(User, UserAdmin)


class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionInline(admin.ModelAdmin):
    model = Question
    inlines = [AnswerInline]


admin.site.register(Question, QuestionInline)
