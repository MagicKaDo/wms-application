from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from models import db, User, Product, Inventory, Location
from forms import LoginForm, ProductForm, UserForm, RegistrationForm
from flask_migrate import Migrate  


app = Flask(__name__)
app.config['SECRET_KEY'] = '7855531576E619592168A1F5ABFF8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://warehouse_user:admin123@localhost/warehouse_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)  
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Rozwiązanie problemu z before_first_request
with app.app_context():
    db.create_all()
    
    # Sprawdź czy istnieje przynajmniej jeden użytkownik
    if not User.query.first():
        admin = User(username='admin', role='admin')
        admin.set_password('admin123')  # Użyj metody set_password z modelu
        db.session.add(admin)
        db.session.commit()
        print("Utworzono domyślnego użytkownika: admin/admin123")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routy autentykacji
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Zalogowano pomyślnie!', 'success')
            return redirect(url_for('dashboard'))
        flash('Nieprawidłowy login lub hasło', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Dashboard
@app.route('/')
@login_required
def dashboard():
    # Dołącz powiązane produkty i lokalizacje
    low_stock = db.session.query(Inventory).join(Product).join(Location).filter(
        Inventory.quantity < Inventory.min_quantity
    ).all()
    
    return render_template('dashboard.html', low_stock=low_stock)

# Zarządzanie produktami
@app.route('/products')
@login_required
def product_list():
    products = Product.query.all()
    return render_template('products/list.html', products=products)

@app.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    # Pobierz dostępne lokalizacje
    form.location.choices = [(loc.id, loc.name) for loc in Location.query.all()]
    
    if form.validate_on_submit():
        # Utwórz produkt
        product = Product(
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            category=form.category.data
        )
        db.session.add(product)
        db.session.flush()  # Uzyskaj ID produktu
        
        # Utwórz wpis inwentarzowy
        inventory = Inventory(
            product_id=product.id,
            location_id=form.location.data,
            quantity=form.quantity.data,
            min_quantity=form.min_quantity.data
        )
        db.session.add(inventory)
        db.session.commit()
        
        flash('Produkt dodany pomyślnie!', 'success')
        return redirect(url_for('product_list'))
    
    return render_template('products/add.html', form=form)

# Zarządzanie użytkownikami
@app.route('/users')
@login_required
def user_list():
    users = User.query.all()
    return render_template('users/list.html', users=users)
# Rejestracja nowego użytkownika
@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    # Tylko admin może rejestrować nowych użytkowników
    if current_user.role != 'admin':
        flash('Brak uprawnień!', 'danger')
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, role=form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Użytkownik został zarejestrowany!', 'success')
        return redirect(url_for('user_list'))
    
    return render_template('users/register.html', form=form)

# Edycja użytkownika
@app.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    inventory = Inventory.query.filter_by(product_id=product_id).first()
    form = ProductForm()
    
    # Pobierz dostępne lokalizacje
    form.location.choices = [(loc.id, loc.name) for loc in Location.query.all()]
    
    if form.validate_on_submit():
        product.name = form.name.data
        product.description = form.description.data
        product.price = form.price.data
        product.category = form.category.data
        
        # Aktualizuj inwentarz
        if inventory:
            inventory.location_id = form.location.data
            inventory.quantity = form.quantity.data
            inventory.min_quantity = form.min_quantity.data
        else:
            # Utwórz nowy wpis inwentarzowy jeśli nie istnieje
            inventory = Inventory(
                product_id=product_id,
                location_id=form.location.data,
                quantity=form.quantity.data,
                min_quantity=form.min_quantity.data
            )
            db.session.add(inventory)
        
        db.session.commit()
        flash('Produkt został zaktualizowany!', 'success')
        return redirect(url_for('product_list'))
    
    # Ustaw początkowe wartości
    form.name.data = product.name
    form.description.data = product.description
    form.price.data = product.price
    form.category.data = product.category
    
    if inventory:
        form.quantity.data = inventory.quantity
        form.min_quantity.data = inventory.min_quantity
        form.location.data = inventory.location_id
    
    return render_template('products/edit.html', form=form, product=product)

# Zarządzanie lokalizacjami
@app.route('/locations')
@login_required
def location_list():
    locations = Location.query.all()
    return render_template('locations/list.html', locations=locations)

@app.route('/locations/add', methods=['GET', 'POST'])
@login_required
def add_location():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        
        location = Location(name=name, description=description)
        db.session.add(location)
        db.session.commit()
        
        flash('Lokalizacja dodana pomyślnie!', 'success')
        return redirect(url_for('location_list'))
    
    return render_template('locations/add.html')

@app.route('/locations/edit/<int:location_id>', methods=['GET', 'POST'])
@login_required
def edit_location(location_id):
    location = Location.query.get_or_404(location_id)
    
    if request.method == 'POST':
        location.name = request.form['name']
        location.description = request.form['description']
        db.session.commit()
        
        flash('Lokalizacja zaktualizowana pomyślnie!', 'success')
        return redirect(url_for('location_list'))
    
    return render_template('locations/edit.html', location=location)

@app.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    # Tylko admin może edytować użytkowników
    if current_user.role != 'admin':
        flash('Brak uprawnień!', 'danger')
        return redirect(url_for('dashboard'))
    
    user = User.query.get_or_404(user_id)
    form = UserForm()
    
    if form.validate_on_submit():
        user.username = form.username.data
        user.role = form.role.data
        db.session.commit()
        flash('Dane użytkownika zostały zaktualizowane!', 'success')
        return redirect(url_for('user_list'))
    
    # Ustaw początkowe wartości
    form.username.data = user.username
    form.role.data = user.role
    
    return render_template('users/edit.html', form=form, user=user)

# API dla HTMX
@app.route('/inventory/check/<int:product_id>')
@login_required
def check_inventory(product_id):
    inventory = Inventory.query.filter_by(product_id=product_id).first()
    return f'<span class="text-red-500">{inventory.quantity}</span>' if inventory.quantity < inventory.min_quantity else ''

if __name__ == '__main__':
    app.run(debug=True)