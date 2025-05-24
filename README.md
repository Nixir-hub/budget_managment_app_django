``` markdown
# System Zarządzania Wydatkami

## Opis projektu
Aplikacja webowa stworzona w Django do śledzenia i analizowania wydatków osobistych.

## Wymagania systemowe
- Python 3.10.12
- Django
- virtualenv

## Zainstalowane pakiety
- coverage
- django
- pip
- pytest
- wheel

## Instalacja

1. Sklonuj repozytorium:
```
bash git clone [adres-repozytorium]
``` 

2. Utwórz i aktywuj środowisko wirtualne:
```
bash python -m virtualenv venv source venv/bin/activate # Linux/Mac
# lub
venv\Scripts\activate # Windows
``` 

3. Zainstaluj wymagane pakiety:
```
bash pip install -r requirements.txt
``` 

4. Skonfiguruj ustawienia Django:
   - Utwórz plik `.env` w głównym katalogu projektu
   - Dodaj wymagane zmienne środowiskowe (jak SECRET_KEY)
   - Skonfiguruj bazę danych w `settings.py`

5. Wykonaj migracje bazy danych:
```
bash python manage.py migrate
``` 

6. Skonfiguruj pliki statyczne:
```
bash
# Dodaj do settings.py:
STATIC_ROOT = BASE_DIR / 'staticfiles' STATIC_URL = 'static/' STATICFILES_DIRS = [ BASE_DIR / 
# Następnie wykonaj:
python manage.py collectstatic
latex_unknown_tag
``` 

7. Uruchom serwer deweloperski:
```
bash python manage.py runserver
``` 

## Struktura projektu
```
project/ ├── manage.py ├── static/ │ └── css/ │ └── charts.css ├── templates/ │ └── base.html ├── staticfiles/ # Katalog dla zebranych plików statycznych ├── venv/ └── requirements.txt
``` 

## Funkcjonalności
- Śledzenie wydatków
- Generowanie wykresów i raportów
- Kategoryzacja transakcji
- Analiza wydatków

## Testy
Aby uruchomić testy:
```
bash pytest
``` 

## Rozwój projektu
1. Upewnij się, że masz zainstalowane wszystkie zależności deweloperskie
2. Utwórz nową gałąź dla swoich zmian
3. Napisz testy dla nowych funkcjonalności
4. Wykonaj testy przed wysłaniem pull request
```


## Autorzy
Ernest Zduńczyk

## Wsparcie
W przypadku problemów, proszę utworzyć nowe zgłoszenie w systemie issues.
