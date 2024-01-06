# Autor: Micu Sebastian Cristian
# Email: sebastian.micu112@gmail.com
# Data proiectului: Septembrie 2023
# GitHub: https://github.com/MicuSebastianCristian

# Descriere:
# Acest fișier conține definirea modelelor pentru baza de date a unei aplicații de Management al Garanțiilor Produselor.
# Aplicația este dezvoltată de către autor în limbajul de programare Python.
# Modelele sunt create cu ajutorul SQLAlchemy și includ un model pentru utilizatori și un model pentru produse.

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import String

# Inițializăm SQLAlchemy pentru gestionarea bazei de date.
db = SQLAlchemy()

# Modelul pentru utilizatori.
class User(db.Model, UserMixin):
    # ID-ul este cheia primară, unică pentru fiecare utilizator.
    id = db.Column(db.Integer, primary_key=True)
    # Numele de utilizator trebuie să fie unic și este obligatoriu.
    username = db.Column(db.String(80), unique=True, nullable=False)
    # Parola utilizatorului este obligatorie.
    password = db.Column(db.String(120), nullable=False)

# Modelul pentru produse.
class Product(db.Model):
    # Fiecare produs are un ID unic.
    id = db.Column(db.Integer, primary_key=True)
    # Numele produsului este obligatoriu.
    name = db.Column(db.String(100), nullable=False)
    # Calea către imaginea de referință pentru produs.
    reference_image_file = db.Column(db.String(100), nullable=True, default='default.jpg')
    # Calea către imaginea facturii produsului.
    invoice_image_file = db.Column(db.String(100), nullable=False)
    # Perioada de garanție a produsului.
    warranty_period = db.Column(db.Integer, nullable=True)
    # Data achiziției produsului.
    purchase_date = db.Column(db.Date, nullable=True)
    # Prețul produsului.
    price = db.Column(db.Float, nullable=True)
    # Moneda în care este exprimat prețul.
    currency = db.Column(String(10), nullable=True)
    # Magazinul de unde a fost cumpărat.
    store = db.Column(db.String(100), nullable=True)
    # Orașul magazinului.
    city = db.Column(db.String(100), nullable=True)
    # Legătura cu utilizatorul care a adăugat produsul.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Instrucțiuni de folosire a codului:
# 1. Asigurați-vă că ați instalat toate bibliotecile necesare, inclusiv Flask, Flask-SQLAlchemy, Werkzeug și altele asemenea,
#    utilizând comanda "pip install nume_bibliotecii" în terminal sau linia de comandă.
# 2. Configurați calea către baza de date în fișierul Python, utilizând variabila "app.config['SQLALCHEMY_DATABASE_URI']".
#    În exemplul dat, se utilizează baza de date SQLite, iar calea către fișierul bazei de date este specificată ca 'sqlite:///site.db'.
#    Puteți modifica această cale în funcție de preferințele dvs.

# Acest cod reprezintă structura bazei de date și modelele pentru utilizatori și produse.
