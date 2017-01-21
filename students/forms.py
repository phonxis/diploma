from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from courses.models import Course
from .models import Profile


class CourseEnrollForm(forms.Form):
    # при проверке формы заполняется одним
    # экземпляром объекта модели из queryset
    course = forms.ModelChoiceField(queryset=Course.objects.all(),
                                    widget=forms.HiddenInput)


class UsersLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={'class': 'form-control form-group',
                   'placeholder': 'Username or E-mail address',
                   'required': 'True'}
        )
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-group',
                   'placeholder': 'Password',
                   'required': 'True'}
        )
    )


class UsersCreationForm(UserCreationForm):
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
        label='Password',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-group',
                   'placeholder': 'Password',
                   'required': 'True'}
        )
    )
    password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-group',
                   'placeholder': 'Confirm password',
                   'required': 'True'}
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email',)
        widgets = {
            'username': forms.TextInput(
                    attrs={'class': 'form-control form-group',
                           'placeholder': 'Username',
                           'required': 'True'}
            ),
            'email': forms.EmailInput(
            attrs={'class': 'form-control form-group',
                   'placeholder': 'Email address',
                   'required': 'True'}
            )
        }


# форма для изменения некоторых данных из User модели
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
          'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control form-group',
                    'placeholder': 'First name',
                }
            ),
          'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control form-group',
                    'placeholder': 'Last name'
                }
            ),
          'email': forms.EmailInput(
                attrs={
                    'class': 'form-control form-group',
                    'placeholder': 'Email',
                    'required': 'True'
                }
            )
        }

# форма для изменения некоторых данных из Profile модели
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth',)
        widgets = {
            'date_of_birth': forms.DateInput(
                attrs={
                    'class': 'form-control form-group',
                    'placeholder': 'Birthday date'
                }
            )
        }
        labels = {
            'date_of_birth': "Birthday date"
        }

# не используется----------------------------------------------------------
class InstructorsCreationForm(UserCreationForm):
    password1 = forms.CharField(
        #label='Password',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-group',
                   'placeholder': 'Password',
                   'required': 'True'}
        )
    )
    password2 = forms.CharField(
        #label='Confirm password',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control form-group',
                   'placeholder': 'Confirm password',
                   'required': 'True'}
        )
    )
    '''group = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control form-group',
                   'placeholder': '',
                   'required': 'True',
                   'value': 'Instructor'}
        )
    )'''

    class Meta:
        model = User
        fields = ('username', 'email',)
        widgets = {
            'username': forms.TextInput(
                    attrs={'class': 'form-control form-group',
                           'placeholder': 'Username',
                           'required': 'True'}
            ),
            'email': forms.EmailInput(
            attrs={'class': 'form-control form-group',
                   'placeholder': 'Email address',
                   'required': 'True'}
            )
        }
        labels = {
            'username': "Username",
            'email': 'E-mail',
            'password1': 'Password',
            'password2': 'Confirm password'
        }
# ---------------------------------------------------------------------------
