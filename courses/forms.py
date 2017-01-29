from django import forms
from django.forms.models import inlineformset_factory
from .models import Course, Module, Lecture

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
