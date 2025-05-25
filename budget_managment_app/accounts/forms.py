from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, AccountBalance

from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'nazwa@przykład.pl'})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dodajemy klasy Bootstrap i placeholdery dla wszystkich pól
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nazwa użytkownika'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Hasło'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Powtórz hasło'
        })

        # Aktualizacja etykiet
        self.fields['username'].label = 'Nazwa użytkownika'
        self.fields['password1'].label = 'Hasło'
        self.fields['password2'].label = 'Powtórz hasło'
        self.fields['email'].label = 'Adres e-mail'


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        label="Adres e-mail",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )

    username = forms.CharField(
        label="username",
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        return self.instance.email

    def clean_username(self):
        return self.instance.username



class AccountBalanceForm(forms.ModelForm):
    class Meta:
        model = AccountBalance
        fields = ['balance']