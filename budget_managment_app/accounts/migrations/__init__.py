from django.db import migrations

def create_balance_category(apps, schema_editor):
    Category = apps.get_model('categories', 'Category')
    User = apps.get_model('accounts', 'CustomUser')
    
    # Dla każdego istniejącego użytkownika
    for user in User.objects.all():
        Category.objects.get_or_create(
            name='Saldo',
            user=user,
            defaults={
                'description': 'Kategoria systemowa do śledzenia salda',
                'is_system': True,
                'is_default': False
            }
        )

def remove_balance_category(apps, schema_editor):
    Category = apps.get_model('categories', 'Category')
    Category.objects.filter(name='Saldo', is_system=True).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('categories', '0001_initial'),  # Zamień na ostatnią migrację w twojej aplikacji
    ]

    operations = [
        migrations.RunPython(create_balance_category, remove_balance_category),
    ]