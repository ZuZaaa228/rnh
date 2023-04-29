from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import MyUser, Appeal


# class LoginForm(AuthenticationForm):
#     username = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True, 'placeholder': 'Email'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'autofocus': True,
                   'placeholder': 'Email',
                   'class': 'form-control'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password',
                   'class': 'form-control'}
        )
    )


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'autofocus': True,
                   'placeholder': 'Email',
                   'class': 'sign-up-htm'}
        )
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password',
                   'class': 'sign-up-htm'}
        )
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Confirm password',
                   'class': 'sign-up-htm'}
        )
    )

    class Meta:
        model = MyUser
        fields = ('email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class AppealForm(forms.ModelForm):
    class Meta:
        model = Appeal
        fields = ('title', 'priority', 'text_appeal')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'text_appeal': forms.Textarea(attrs={'class': 'form-control'}),
        }

        labels = {
            'title': 'Название обращения',
            'text_appeal': 'Текст обращения',
            'priority': 'Приоритет обращения',
        }

        CHOICES = (
            ('св', 'Самый высокий'),
            ('вы', 'Высокий'),
            ('ср', 'Средний'),
            ('ни', 'Низкий'),
        )

        priority = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=CHOICES)

class AppealForm(forms.ModelForm):
    class Meta:
        model = Appeal
        fields = ['is_activate']
        widgets = {'is_activate': forms.HiddenInput()}

class UserAppealsForm(forms.Form):
    def __init__(self, user=None, *args, **kwargs):
        super(UserAppealsForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['appeals'] = forms.ModelMultipleChoiceField(
                queryset=Appeal.objects.filter(author=user),
                widget=forms.CheckboxSelectMultiple,
                label='Обращения'
        )

class AppealForm(forms.ModelForm):
    class Meta:
        model = Appeal
        fields = ['title', 'priority', 'text_appeal']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'text_appeal': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Название обращения',
            'priority': 'Приоритет',
            'text_appeal': 'Текст обращения'
        }