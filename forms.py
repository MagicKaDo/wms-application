from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Hasło', validators=[DataRequired()])

class ProductForm(FlaskForm):
    name = StringField('Nazwa produktu', validators=[DataRequired()])
    description = TextAreaField('Opis')
    price = FloatField('Cena', validators=[DataRequired()])
    category = SelectField('Kategoria', choices=[
        ('budowlane', 'Materiały budowlane'),
        ('elektryka', 'Elektryka'),
        ('hydraulika', 'Hydraulika'),
        ('narzedzia', 'Narzędzia'),
        ('inne', 'Inne')
    ])
    quantity = IntegerField('Ilość początkowa', validators=[DataRequired()], default=0)
    min_quantity = IntegerField('Minimalna ilość', validators=[DataRequired()], default=5)
    location = SelectField('Lokalizacja', coerce=int)  # Użyjemy ID lokalizacji

class UserForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired(), Length(min=4, max=20)])
    role = SelectField('Rola', choices=[
        ('admin', 'Administrator'),
        ('manager', 'Kierownik magazynu'),
        ('worker', 'Pracownik magazynu'),
        ('accountant', 'Księgowy'),
        ('analyst', 'Analityk biznesowy')
    ])

class RegistrationForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Hasło', validators=[DataRequired()])
    confirm_password = PasswordField('Potwierdź hasło', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Rola', choices=[
        ('admin', 'Administrator'),
        ('manager', 'Kierownik magazynu'),
        ('worker', 'Pracownik magazynu'),
        ('accountant', 'Księgowy'),
        ('analyst', 'Analityk biznesowy')
    ])