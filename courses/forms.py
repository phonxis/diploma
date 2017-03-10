from django import forms
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from .models import Course, Module, Lecture, Question, Answer

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
        #labels = {
        #  'title': ''
        #}


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('data_field',)
        widgets = {
            'data_field': forms.TextInput(
                attrs={
                    'class': 'form-control form-group',
                    'placeholder': 'additional data for question',
                    'required': 'True'
                }
            )
        }

AnswerForm = inlineformset_factory(Question,
                                   Answer,
                                   fields=['answer', 'correct'],
                                   extra=1,
                                   can_delete=True,
                                   widgets={'answer': forms.TextInput(
                                      attrs={
                                        'class': 'form-control form-group',
                                        'placeholder': 'Type answer',
                                        'required': 'True'
                                      }
                                    ),
                                   'correct': forms.CheckboxInput(
                                      attrs={'class': 'regular-checkbox'}
                                    )})
