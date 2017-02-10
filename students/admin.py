from django.contrib import admin
from django.contrib.auth.models import User
from nested_admin import NestedModelAdmin, NestedTabularInline
from .models import Profile
from courses.models import Quiz, Question, Answer


admin.site.unregister(User)

class ProfileInline(admin.TabularInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    inlines = [ProfileInline,]

admin.site.register(User, UserAdmin)


class AnswerInline(NestedTabularInline):
    model = Answer

class QuestionInline(NestedTabularInline):
    model = Question
    inlines = [AnswerInline]

class QuizInline(NestedModelAdmin):
    model = Quiz
    inlines = [QuestionInline]

admin.site.register(Quiz, QuizInline)
