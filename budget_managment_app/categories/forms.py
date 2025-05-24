from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.is_system:
            for field in self.fields.values():
                field.disabled = True

    def clean(self):
        cleaned_data = super().clean()
        if self.instance and self.instance.is_system:
            raise forms.ValidationError("Nie można edytować kategorii systemowej.")
        return cleaned_data


