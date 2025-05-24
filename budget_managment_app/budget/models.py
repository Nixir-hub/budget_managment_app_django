from django.db import models, transaction
from django.conf import settings
from django.core.exceptions import ValidationError
from categories.models import Category

from accounts.models import AccountBalance


class Transaction(models.Model):
    INCOME = 'income'
    EXPENSE = 'expense'
    TRANSACTION_TYPES = [
        (INCOME, 'Przychód'),
        (EXPENSE, 'Wydatek'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions',
        verbose_name="Użytkownik"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Kategoria"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Kwota"
    )
    type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPES,
        default=EXPENSE,
        verbose_name="Typ"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Opis"
    )
    date = models.DateField(
        verbose_name="Data"
    )

    class Meta:
        verbose_name = "Transakcja"
        verbose_name_plural = "Transakcje"
        ordering = ['-date']

    def clean(self):
        if not self.pk:  # tylko dla nowych transakcji
            is_balance_category = self.category and self.category.name.lower() == "saldo"

            # Walidacja typu
            if not is_balance_category and self.type == self.INCOME:
                raise ValidationError({
                    'type': 'Tylko transakcje w kategorii \"saldo\" mogą być przychodami.'
                })


    def save(self, *args, **kwargs):
        with transaction.atomic():
            self.full_clean()

            account, _ = AccountBalance.objects.get_or_create(user=self.user)

            if self.pk:  # aktualizacja
                old = Transaction.objects.get(pk=self.pk)

                # Cofnij starą wartość
                if old.type == 'income':
                    account.balance -= old.amount
                elif old.type == 'expense':
                    account.balance += old.amount

            # Dodaj nową wartość
            if self.type == 'income':
                account.balance += self.amount
            elif self.type == 'expense':
                account.balance -= self.amount

            account.save()
            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        account = AccountBalance.objects.get(user=self.user)
        if self.type == 'income':
            account.balance -= self.amount
        elif self.type == 'expense':
            account.balance += self.amount
        account.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.date} - {self.category.name} - {self.amount}"