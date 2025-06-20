# reset_db.py
from app import app, db
from models import User

with app.app_context():
    # Usuń wszystkie tabele
    db.drop_all()
    
    # Utwórz nowe tabele z aktualnym schematem
    db.create_all()
    
    # Utwórz domyślnego użytkownika
    admin = User(username='admin', role='admin')
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()
    
    print("Baza danych została zresetowana!")
    print("Utworzono użytkownika: admin/admin123")