

from django import forms
from .models import Transaction
from accounts.models import AccountBalance

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'amount', 'type', 'description', 'date']  # ← dodaj 'date'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')
        tx_type = cleaned_data.get('type')

        if self.user and tx_type == 'expense':
            from accounts.models import AccountBalance
            account = AccountBalance.objects.filter(user=self.user).first()

            if not account:
                raise forms.ValidationError("Musisz najpierw ustawić saldo konta przed dokonaniem wydatku.")

            if amount and amount > account.balance:
                raise forms.ValidationError("Brak wystarczających środków na koncie.")

