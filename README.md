📘 Aplikacja do zarządzania wydatkami – Dokumentacja techniczna
Nazwa projektu: Budget Management App
Technologie: Django, Python, HTML/CSS, SQLite/PostgreSQL

📑 Spis treści
Opis projektu

Struktura katalogów

Wymagania i instalacja

Aplikacje i funkcjonalności

Modele danych

Diagram UML

Uwierzytelnianie i autoryzacja

Interfejs użytkownika

Testowanie

Deployment

Załączniki

1. Opis projektu
Budget Management App to aplikacja Django umożliwiająca użytkownikom efektywne zarządzanie domowym i osobistym budżetem. System pozwala na:

tworzenie kont użytkowników,

dodawanie i zarządzanie kategoriami przychodów i wydatków,

rejestrowanie transakcji finansowych,

monitorowanie salda i limitów budżetowych,

przeglądanie miesięcznych i rocznych raportów finansowych.

Dzięki intuicyjnemu interfejsowi oraz funkcjom autoryzacji, użytkownicy mogą bezpiecznie śledzić swoją sytuację finansową.

2. Struktura katalogów
csharp
Copy
Edit
budget_managment_app_django-main/
│
├── budget_managment_app/        # Główna aplikacja Django
│   ├── accounts/                # Zarządzanie kontami użytkowników
│   ├── budget/                  # Obsługa budżetów, transakcji
│   ├── categories/              # Kategorie wydatków i przychodów
│   ├── core/                    # Konfiguracja główna (settings, urls)
│   ├── static/                  # Statyczne zasoby (CSS, JS)
│   ├── templates/               # Szablony HTML
│   ├── tests/                   # Testy jednostkowe
│   └── manage.py                # Uruchamianie projektu
├── requirements/                # Pliki z zależnościami
├── README.md
├── .gitignore
└── pytest.ini
3. Wymagania i instalacja
Wymagania systemowe:

Python 3.8+

Django 4.x

pip

Instalacja:

bash
Copy
Edit
git clone <repo>
cd budget_managment_app_django-main
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements/base.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
4. Aplikacje i funkcjonalności
accounts/
Rejestracja i logowanie

Resetowanie hasła

Edycja danych użytkownika

System uprawnień

budget/
Tworzenie budżetów

Rejestrowanie transakcji (przychody/wydatki)

Monitorowanie salda

Powiązanie z kategoriami

categories/
Tworzenie i zarządzanie kategoriami

Kategorie globalne i przypisane do użytkownika

5. Modele danych (przykład)
python
Copy
Edit
class Category(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(choices=(('income', 'Income'), ('expense', 'Expense')))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
python
Copy
Edit
class Transaction(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True)
6. Diagram UML
Poniższy szablon można wkleić w narzędzie typu PlantUML:

pgsql
Copy
Edit
@startuml
class User {
    +id
    +username
    +email
    +password
}

class Category {
    +id
    +name
    +type
    +user : FK -> User
}

class Transaction {
    +id
    +amount
    +date
    +description
    +category : FK -> Category
}

User "1" -- "many" Category
Category "1" -- "many" Transaction
@enduml
7. Uwierzytelnianie i autoryzacja
Wykorzystanie systemu django.contrib.auth

Middleware chroniące widoki

Obsługa rejestracji, logowania, resetu hasła

Uprawnienia do danych ograniczone do właściciela (użytkownika)

8. Interfejs użytkownika
Szablony HTML z dziedziczeniem z base.html

Stylizacja za pomocą CSS (z opcją dodania Bootstrap)

Widoki: CBV (klasowe) i FBV (funkcyjne)

Formularze Django Forms do interakcji z danymi

9. Testowanie
Testy jednostkowe i integracyjne (pytest)

Lokalizacja testów: katalog tests/

Testowane komponenty: modele, widoki, formularze

10. Deployment
Rekomendowane środowisko produkcyjne:

System: Ubuntu/Debian

Webserver: Gunicorn + Nginx

Baza danych: PostgreSQL

Kroki wdrożenia:

DEBUG=False w settings.py

Ustawienie ALLOWED_HOSTS

Wdrożenie przez gunicorn lub uwsgi

Konfiguracja .env dla danych poufnych

11. Załączniki
README.md – skrócony opis projektu

requirements/ – pliki zależności

pytest.ini – konfiguracja testów

.gitignore – ignorowane pliki w repozytorium
