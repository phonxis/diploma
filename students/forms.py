from django import forms
from django.contrib.auth.models import User
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
            attrs={'class': 'form-control form-group',
                   'placeholder': 'Username',
                   'required': 'True'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-group',
                   'placeholder': 'Password',
                   'required': 'True'}
        )
    )


class UsersCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email',)
        widgets = {
            'username': forms.TextInput(
                    attrs={'class': 'form-control form-group',
                           'placeholder': 'Username',
                           'required': 'True'}
            ),
            'email': forms.TextInput(
            attrs={'class': 'form-control form-group',
                   'placeholder': 'Email address',
                   'required': 'True'}
            )
        }

    '''username = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control form-group',
                   'placeholder': 'Username',
                   'required': 'True'}
        )
    )
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={'class': 'form-control form-group',
                   'placeholder': 'Email address',
                   'required': 'True'}
        )
    )'''
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-group',
                   'placeholder': 'Password',
                   'required': 'True'}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-group',
                   'placeholder': 'Confirm password',
                   'required': 'True'}
        )
    )
