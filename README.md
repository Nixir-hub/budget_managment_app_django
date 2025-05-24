# System Zarządzania Wydatkami

## Opis projektu
Aplikacja webowa stworzona w Django do śledzenia i analizowania wydatków osobistych.

---

## Wymagania systemowe
- Python 3.10.12
- Django
- virtualenv

---

## Zainstalowane pakiety
- coverage
- django
- pip
- pytest
- wheel

---

## Instalacja

1. Sklonuj repozytorium:  
   ```bash
   git clone [adres-repozytorium]
Utwórz i aktywuj środowisko wirtualne:
Linux/Mac:

bash
Copy
Edit
python -m virtualenv venv
source venv/bin/activate
Windows:

bash
Copy
Edit
venv\Scripts\activate
Zainstaluj wymagane pakiety:

bash
Copy
Edit
pip install -r requirements.txt
Skonfiguruj ustawienia Django:

Utwórz plik .env w głównym katalogu projektu.

Dodaj wymagane zmienne środowiskowe (np. SECRET_KEY).

Skonfiguruj bazę danych w settings.py.

Wykonaj migracje bazy danych:

bash
Copy
Edit
python manage.py migrate
Skonfiguruj pliki statyczne:
W settings.py dodaj:

python
Copy
Edit
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
Następnie wykonaj:

bash
Copy
Edit
python manage.py collectstatic
Uruchom serwer deweloperski:

bash
Copy
Edit
python manage.py runserver
Struktura projektu
csharp
Copy
Edit
project/
├── manage.py
├── static/
│   └── css/
│       └── charts.css
├── templates/
│   └── base.html
├── staticfiles/          # Katalog dla zebranych plików statycznych
├── venv/
└── requirements.txt
Funkcjonalności
Śledzenie wydatków

Generowanie wykresów i raportów

Kategoryzacja transakcji

Analiza wydatków

Testy
Aby uruchomić testy:

bash
Copy
Edit
pytest
Rozwój projektu
Upewnij się, że masz zainstalowane wszystkie zależności deweloperskie.

Utwórz nową gałąź dla swoich zmian.

Napisz testy dla nowych funkcjonalności.

Wykonaj testy przed wysłaniem pull request.

Autorzy
Ernest Zduńczyk

Wsparcie
W przypadku problemów proszę utworzyć nowe zgłoszenie w systemie issues.
