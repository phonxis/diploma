from django import forms
from courses.models import Course


class CourseEnrollForm(forms.Form):
    # при проверке формы заполняется одним 
    # экземпляром объекта модели из queryset
    course = forms.ModelChoiceField(queryset=Course.objects.all(),
                                    widget=forms.HiddenInput)
