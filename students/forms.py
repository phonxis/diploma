from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from courses.models import Course


class CourseEnrollForm(forms.Form):
    # при проверке формы заполняется одним
    # экземпляром объекта модели из queryset
    course = forms.ModelChoiceField(queryset=Course.objects.all(),
                                    widget=forms.HiddenInput)


class UsersLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Username'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Password'}
        )
    )


class UsersCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Username'}
        )
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Email address'}
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Password'}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Confirm password'}
        )
    )
