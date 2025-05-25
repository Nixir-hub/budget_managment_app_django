
# 📄 Dokumentacja techniczna

**Nazwa projektu:** Budget Management App  
**Technologie:** Django, Python, HTML/CSS, SQLite/PostgreSQL

---

## 1. Opis projektu

Aplikacja Django do zarządzania budżetem osobistym i domowym. Użytkownicy mogą tworzyć konta, kategorie wydatków, dodawać przychody i wydatki, a także przeglądać raporty finansowe.

---

## 2. Struktura katalogów

```
budget_managment_app_django-main/
│
├── budget_managment_app/        # Główna aplikacja Django
│   ├── accounts/                # Zarządzanie kontami użytkowników
│   ├── budget/                  # Obsługa budżetów
│   ├── categories/              # Kategorie wydatków i przychodów
│   ├── core/                    # Konfiguracja główna (settings, urls)
│   ├── static/                  # Statyczne zasoby (CSS, JS)
│   ├── templates/               # Szablony HTML
│   ├── tests/                   # Testy jednostkowe i integracyjne
│   └── manage.py                # Uruchamianie projektu
├── requirements/                # Pliki z zależnościami
├── .gitignore
├── README.md
└── pytest.ini
```

---

## 3. Wymagania i instalacja

**Wymagania systemowe:**
- Python 3.8+
- Django 4.x
- pip

**Instalacja:**
```bash
git clone <repo>
cd budget_managment_app_django-main
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements/base.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## 4. Aplikacje i funkcjonalności

### `accounts/`
- Rejestracja, logowanie, zarządzanie kontem użytkownika
- Resetowanie hasła
- Uprawnienia dostępu

### `budget/`
- Tworzenie budżetów 
- Dodawanie przychodów i wydatków
- Saldo i limity

### `categories/`
- Tworzenie kategorii przychodów/wydatków


---

## 5. Modele danych (przykład)

@startuml

' Klasy użytkowników
class CustomUser {
  + username: String
  + email: String
  + first_name: String
  + last_name: String
  + is_active: Boolean
  + is_staff: Boolean
  + date_joined: DateTime
}

class AccountBalance {
  + balance: Decimal
  + __str__(): String
}

' Klasy transakcji i kategorii
class Transaction {
  + amount: Decimal
  + date: Date
  + description: Text
  + type: String
  + created_at: DateTime
}

class Category {
  + name: String
  + description: Text
  + is_system: Boolean
  + is_default: Boolean
  + created_at: DateTime
  + __str__(): String
}

' Relacje
CustomUser "1" -- "1" AccountBalance : has >
CustomUser "1" -- "*" Transaction : owns >
CustomUser "1" -- "*" Category : owns >
Transaction "*" -- "1" Category : belongs to >

' Dziedziczenie
AbstractUser <|-- CustomUser

@enduml


```python
class Category(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(choices=(('income', 'Income'), ('expense', 'Expense')))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
```

```python
class Transaction(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True)
```

---

## 6. Uwierzytelnianie i autoryzacja

- Django Auth
- Middleware chroniący dostęp do widoków budżetu i transakcji
- System rejestracji i aktywacji kont

---

## 7. Interfejs użytkownika

- Szablony HTML (Django templates)
- System bazowy oparty o `base.html`
- Widoki klasowe i funkcyjne (`views.py`)
- Stylizacja przy użyciu CSS (możliwie Bootstrap)

---

## 8. Testowanie

- `pytest` jako główne narzędzie testowe (`pytest.ini`)
- Testy jednostkowe w katalogu `tests/`
- Możliwość testowania modeli, widoków, formularzy

---

## 9. Deployment

**Rekomendowane środowisko:**
- Serwer Ubuntu/Debian
- Gunicorn + Nginx
- Baza danych PostgreSQL
- Użycie `.env` do konfiguracji produkcyjnej

**Podstawowe kroki:**
- Ustawienie `ALLOWED_HOSTS`, `DEBUG=False`
- Wdrożenie z użyciem `gunicorn` lub `uwsgi`
- Konfiguracja bazy danych w `settings.py`

---

## 10. Załączniki

- `README.md` – podstawowy opis projektu
- `requirements` – wymagane pakiety
