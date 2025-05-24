from django import forms
from django.core.exceptions import ValidationError
from .models import Transaction
from accounts.models import AccountBalance

from categories.models import Category


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'amount', 'type', 'description', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'amount': forms.NumberInput(attrs={'min': '0.01', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # tylko kategorie tego użytkownika
        if self.user:
            self.fields['category'].queryset = Category.objects.filter(user=self.user)

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise ValidationError("Kwota musi być większa od zera.")
        return amount

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')
        tx_type = cleaned_data.get('type')

        if self.user and tx_type == 'expense':
            account = AccountBalance.objects.filter(user=self.user).first()
            if not account:
                raise ValidationError("Musisz najpierw ustawić stan konta.")
            if amount and amount > account.balance:
                raise ValidationError("Brak wystarczających środków na koncie.")
