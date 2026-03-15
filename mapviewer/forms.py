from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile


class LoginForm(AuthenticationForm):
    """Formulario de inicio de sesión con estilos personalizados."""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control auth-input',
            'placeholder': 'Nombre de usuario',
            'autocomplete': 'username',
            'id': 'login-username',
        }),
        label='Usuario'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control auth-input',
            'placeholder': 'Contraseña',
            'autocomplete': 'current-password',
            'id': 'login-password',
        }),
        label='Contraseña'
    )


class RegisterForm(forms.ModelForm):
    """Formulario de registro de nuevo usuario."""
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control auth-input',
            'placeholder': 'Crea una contraseña',
            'id': 'register-password1',
        })
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control auth-input',
            'placeholder': 'Repite la contraseña',
            'id': 'register-password2',
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control auth-input',
                'placeholder': 'Nombre de usuario',
                'id': 'register-username',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control auth-input',
                'placeholder': 'correo@ejemplo.com',
                'id': 'register-email',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control auth-input',
                'placeholder': 'Nombre',
                'id': 'register-first-name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control auth-input',
                'placeholder': 'Apellido',
                'id': 'register-last-name',
            }),
        }

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return p2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('Ya existe un usuario con este correo electrónico.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    """Formulario para editar el perfil extendido del usuario."""
    first_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control auth-input',
            'placeholder': 'Nombre',
        }),
        label='Nombre'
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control auth-input',
            'placeholder': 'Apellido',
        }),
        label='Apellido'
    )
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-control auth-input',
            'placeholder': 'correo@ejemplo.com',
        }),
        label='Correo electrónico'
    )

    class Meta:
        model = UserProfile
        fields = ['institution', 'role', 'bio']
        widgets = {
            'institution': forms.TextInput(attrs={
                'class': 'form-control auth-input',
                'placeholder': 'Ej: UNAM, Instituto de Geofísica',
            }),
            'role': forms.TextInput(attrs={
                'class': 'form-control auth-input',
                'placeholder': 'Ej: Investigador, Estudiante',
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control auth-input',
                'placeholder': 'Cuéntanos sobre ti...',
                'rows': 3,
            }),
        }
