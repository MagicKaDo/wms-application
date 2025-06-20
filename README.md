# 🏭 Warehouse Management App

Aplikacja webowa do zarządzania magazynem, stworzona w Pythonie z użyciem frameworka Flask oraz SQLAlchemy. Umożliwia zarządzanie użytkownikami, produktami, lokalizacjami magazynowymi i stanami magazynowymi.

## 📦 Funkcjonalności

- Rejestracja i logowanie użytkowników z rolami
- Zarządzanie produktami (nazwa, opis, cena, kategoria)
- Zarządzanie lokalizacjami magazynowymi
- Inwentaryzacja produktów (ilość, lokalizacja, ilość minimalna)
- Bezpieczne hashowanie haseł

## 🧱 Technologie

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Werkzeug (hashowanie haseł)
- SQLite / PostgreSQL (dowolna baza obsługiwana przez SQLAlchemy)

## 📁 Struktura modeli

### `User`
| Pole         | Typ           | Opis                          |
|--------------|----------------|-------------------------------|
| `id`         | `Integer`     | ID użytkownika                |
| `username`   | `String(80)`  | Nazwa użytkownika (unikalna) |
| `password_hash` | `String(200)` | Zhashowane hasło           |
| `role`       | `String(50)`  | Rola użytkownika              |

### `Product`
| Pole         | Typ           | Opis                          |
|--------------|----------------|-------------------------------|
| `id`         | `Integer`     | ID produktu                   |
| `name`       | `String(120)` | Nazwa produktu                |
| `description`| `Text`        | Opis produktu                 |
| `price`      | `Float`       | Cena                          |
| `category`   | `String(80)`  | Kategoria                     |

### `Location`
| Pole         | Typ           | Opis                          |
|--------------|----------------|-------------------------------|
| `id`         | `Integer`     | ID lokalizacji                |
| `name`       | `String(80)`  | Nazwa lokalizacji             |
| `description`| `String(200)` | Opis lokalizacji              |

### `Inventory`
| Pole         | Typ           | Opis                          |
|--------------|----------------|-------------------------------|
| `id`         | `Integer`     | ID wpisu inwentaryzacji       |
| `product_id` | `Integer`     | ID produktu (FK)              |
| `location_id`| `Integer`     | ID lokalizacji (FK)           |
| `quantity`   | `Integer`     | Ilość w magazynie             |
| `min_quantity`| `Integer`    | Minimalna ilość               |

## ⚙️ Uruchomienie aplikacji (lokalnie)

1. Zainstaluj zależności:
    ```bash
    pip install flask flask_sqlalchemy flask_login werkzeug
    ```

2. Utwórz bazę danych:
    ```python
    from app import db
    db.create_all()
    ```

3. Uruchom serwer deweloperski:
    ```bash
    flask run
    ```

## 🔐 Uwierzytelnianie

Aplikacja wykorzystuje `Flask-Login` do zarządzania sesją użytkownika i `Werkzeug` do bezpiecznego haszowania haseł.

## 📌 TODO (opcjonalnie)

- Interfejs webowy z Flask lub frontendem (np. React)
- REST API do zarządzania zasobami
- Obsługa uprawnień według ról
- Powiadomienia o niskim stanie magazynowym

## 📄 Licencja

Projekt edukacyjny – możesz używać, rozwijać i modyfikować wedle potrzeb.

---

