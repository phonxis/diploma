from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from .models import Course, Module, Lecture, Quiz

ModuleFormSet = inlineformset_factory(Course,
                                      Module,
                                      fields=['title',
                                              'description'],
                                      extra=1,
                                      can_delete=True)

class LectureForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = ('title',)
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control form-group',
                    'placeholder': 'Title of lecture',
                    'required': 'True'
                }
            )
        }


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('title',)
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control form-group',
                    'placeholder': 'Title of quiz',
                    'required': 'True'
                }
            )
        }
