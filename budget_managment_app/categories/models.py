from django.db import models
from django.conf import settings

class Category(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Użytkownik"
    )
    name = models.CharField(max_length=100, verbose_name="Nazwa")
    description = models.TextField(blank=True, verbose_name="Opis")
    is_default = models.BooleanField(default=False, verbose_name="Domyślna")
    is_system = models.BooleanField(
        default=False, 
        verbose_name="Kategoria systemowa",
        help_text="Kategorie systemowe nie mogą być usuwane ani modyfikowane"
    )

    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"
        ordering = ['name']

    def __str__(self):
        return f"{self.name}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.is_system and self.pk:
            original = Category.objects.get(pk=self.pk)
            if original.name != self.name:
                raise ValidationError("Nie można modyfikować nazwy kategorii systemowej")


