# Autor: Micu Sebastian Cristian
# Email: sebastian.micu112@gmail.com
# Data proiectului: Septembrie 2023
# GitHub: https://github.com/MicuSebastianCristian

# Descriere:
# Acest fisier contine functii si rute pentru o aplicatie de Management al Garantiilor Produselor dezvoltata in limbajul Python
# cu ajutorul framework-ului Flask. Aplicatia permite utilizatorilor sa adauge, editeze, stearga si sa descarce produse si documente
# asociate acestora intr-un mediu sigur si eficient. De asemenea, asigura autentificarea utilizatorilor si restricționeaza accesul neautorizat.

# Instructiuni de folosire a codului:
# 1. Asigurati-va ca ati instalat toate bibliotecile necesare, inclusiv Flask, Flask-SQLAlchemy, Werkzeug si altele asemenea,
#    utilizand comanda "pip install nume_bibliotecii" in terminal sau linia de comanda.
# 2. Configurati calea catre baza de date in fisierul Python, utilizand variabila "app.config['SQLALCHEMY_DATABASE_URI']".
#    In exemplul dat, se utilizeaza baza de date SQLite, iar calea catre fisierul bazei de date este specificata ca 'sqlite:///site.db'.
#    Puteti modifica aceasta cale in functie de preferintele dvs.
# 3. Asigurati-va ca aveti fisierele HTML necesare pentru functionarea aplicatiei, inclusiv 'home.html', 'login.html', 'register.html' si altele,
#    si ca acestea sunt prezente in directorul 'templates'.
# 4. Puteti rula acest fisier Python in terminal sau linia de comanda folosind comanda "python nume_fisier.py", unde 'nume_fisier.py'
#    reprezinta numele acestui fisier.
# 5. Dupa rulare, aplicatia va deveni accesibila la adresa "http://localhost:5000/" intr-un browser web, iar utilizatorii pot utiliza
#    functionalitatile oferite pentru gestionarea garantiilor produselor si a documentelor aferente.

# Acest cod reprezinta partea din spate a aplicatiei de Management al Garantiilor Produselor si asigura functionalitati de gestionare
# a produselor si a documentelor, precum si autentificare si restrictie acces la resursele aplicatiei.


from flask import render_template, redirect, url_for, request, flash, send_from_directory, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timedelta  # Import clasele 'datetime' și 'timedelta' din modulul 'datetime'
from PIL import Image
from models import User, Product
from models import db
from app import app

# Stabilim o limita pentru marimea imaginilor incarcate.
# Nu import aceasta variabila din app.py pentru a evita pe cat posibil situatia importurilor circulare
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10 MB in bytes

# Definim extensiile permise pentru incarcare.
# Nu import aceasta variabila din app.py pentru a evita pe cat posibil situatia importurilor circulare
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

# Functie pentru conversia imaginilor din formatul WEBP în PNG.
def convert_to_png(webp_path):
    try:
        with Image.open(webp_path) as img:
            # Determinam calea unde va fi salvata noua imagine PNG.
            png_path = webp_path.rsplit('.', 1)[0] + '.png'
            # Salvam imaginea in format PNG.
            img.save(png_path, 'PNG')
        return png_path
    except Exception as e:
        # Daca apar probleme, afisam eroarea.
        print(f"Eroare la conversia în PNG: {e}")
        return None


# Functie pentru conversia imaginilor in formatul WEBP.
def convert_to_webp(image_path):
    with Image.open(image_path) as img:
        # Determinam calea unde va fi salvată noua imagine WEBP.
        webp_path = image_path.rsplit('.', 1)[0] + '.webp'
        # Salvam imaginea in format WEBP.
        img.save(webp_path, 'WEBP')
    return webp_path

# Verificam daca extensia fisierului este permisa.
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@login_required
def edit_product(id):
    product = Product.query.get_or_404(id)

    # SECURITY --> Verificam daca produsul apartine utilizatorului curent.
    if product.user_id != current_user.id:
        # SECURITY --> Dacă nu, aruncam o eroare 403 (interzis).
        abort(403)

    # Verificam daca metoda este POST (daca a fost trimis formularul).
    if request.method == 'POST':

        # Validam numele produsului.
        new_name = request.form.get('product_name')
        if not new_name or len(new_name) > 30:
            flash('Numele produsului este invalid sau prea lung.')
            return redirect(url_for('edit_product_route', id=id))

        # Validam numele magazinului.
        new_store = request.form.get('store')
        if not new_store or len(new_store) > 30:
            flash('Numele magazinului este invalid sau prea lung.')
            return redirect(url_for('edit_product_route', id=id))

        # Validam moneda.
        new_currency = request.form.get('currency')
        if not new_currency or len(new_currency) > 30:
            flash('Moneda este invalidă sau prea lungă.')
            return redirect(url_for('edit_product_route', id=id))

        # Validam orasul.
        new_city = request.form.get('city')
        if not new_city or len(new_city) > 30:
            flash('Orașul este invalid sau prea lung.')
            return redirect(url_for('edit_product_route', id=id))

        # Validam perioada de garantie.
        new_warranty_period_str = request.form.get('warranty_period')
        try:
            new_warranty_period = int(new_warranty_period_str)
        except ValueError:
            flash('Perioada de garanție trebuie să fie un număr întreg.')
            return redirect(url_for('edit_product_route', id=id))

        # Validam data achiziției.
        new_purchase_date_str = request.form.get('purchase_date')
        try:
            new_purchase_date = datetime.strptime(new_purchase_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Data achiziției este invalidă.')
            return redirect(url_for('edit_product_route', id=id))

        # Actualizam informatiile produsului.
        product.name = new_name
        product.store = new_store
        product.currency = new_currency
        product.city = new_city
        product.warranty_period = new_warranty_period
        product.purchase_date = new_purchase_date

        # Salvam schimbarile in baza de date.
        db.session.commit()

        flash('Produsul a fost actualizat cu succes!')
        return redirect(url_for('home_route'))

    # Pregatim datele existente pentru a fi afișate în formular.
    context = {
        'existing_product_name': product.name,
        'existing_store_name': product.store,
        'existing_currency': product.currency,
        'existing_city': product.city,
        'existing_warranty_period': product.warranty_period,
        'existing_purchase_date': product.purchase_date.strftime('%Y-%m-%d') if product.purchase_date else '',
    }

    return render_template('edit_product.html', product=product, **context)

def register():
    # Verificam daca s-a trimis formularul de înregistrare.
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Verificam daca numele de utilizator exista deja.
        user = User.query.filter_by(username=username).first()

        if user:
            flash('Acest nume de utilizator există deja. Alegeți altul.')
            return redirect(url_for('register_route'))

        # Construim noul utilizator si il adăugam in baza de date.
        new_user = User(username=username, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        flash('Înregistrare reușită! Acum vă puteți autentifica.')
        return redirect(url_for('login_route'))

    return render_template('register.html')

# Ruta principala redirecționează catre pagina de acasa.
def index():
    return redirect(url_for('home_route'))

# Definim ruta pentru autentificare.
def login():
    # Verificam daca s-a trimis formularul de autentificare.
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Cautam utilizatorul după numele de utilizator.
        user = User.query.filter_by(username=username).first()

        # Verificam dacă parola se potriveste cu cea din baza de date.
        if not user or not check_password_hash(user.password, password):
            flash('Nume de utilizator sau parolă invalidă. Vă rugăm să încercați din nou.')
            return redirect(url_for('login_route'))

        # Autentificam utilizatorul.
        login_user(user)
        return redirect(url_for('home_route'))

    return render_template('login.html')

# Definim ruta pentru delogare.
@login_required
def logout():
    logout_user()
    flash('Delogare reușită.')
    return redirect(url_for('login_route'))

# Definim ruta pentru pagina de acasa.
@login_required
def home():
    products = Product.query.filter_by(user_id=current_user.id).all()
    current_time = datetime.utcnow()

    for product in products:
        if product.purchase_date and product.warranty_period:
            warranty_expiry = product.purchase_date + timedelta(days=product.warranty_period * 30)
            product.warranty_expiry = warranty_expiry
            product.under_warranty = warranty_expiry >= current_time.date()

    context = {
        'products': products,
        'current_time': current_time,
    }

    return render_template('home.html', **context)


@login_required
def download_invoice_file(filename):
    # Trimite fisierul specificat din directorul UPLOAD_FOLDER ca si atasament
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@login_required
def add_product():
    # Inițializăm un dicționar gol pentru a stoca datele formularului
    form_data = {}

    # Verificam daca metoda este POST (adăugare produs)
    if request.method == 'POST':
        # Colectam datele introduse de utilizator
        form_data = {
            'product_name': request.form.get('product_name'),
            'store': request.form.get('store'),
            'city': request.form.get('city'),
            'warranty_period': request.form.get('warranty_period'),
            'purchase_date': request.form.get('purchase_date'),
            'price': request.form.get('price'),
            'currency': request.form.get('currency')
        }

        # Verificam daca campul 'currency' este completat
        if not form_data['currency']:
            flash('Introduceți o valoare pentru câmpul Monedă.')
            return render_template('add_product.html', form_data=form_data)

        # Colectam imaginile incarcate de utilizator
        image = request.files['invoice_image_file']
        reference_image = request.files['reference_image_file']

        # Convertim data de achizitie in formatul corespunzător
        try:
            purchase_date = datetime.strptime(form_data['purchase_date'], '%Y-%m-%d').date()
        except ValueError:
            flash('Formatul datei de achiziție este invalid. Vă rugăm să utilizați formatul YYYY-MM-DD.')
            return render_template('add_product.html', form_data=form_data)

        # Verificam dimensiunea imaginilor
        if image and len(image.read()) > MAX_IMAGE_SIZE:
            flash('Dimensiunea imaginii facturii/bonului fiscal depășește 10 MB. Vă rugăm să încărcați o imagine mai mică.')
            return render_template('add_product.html', form_data=form_data)
        if reference_image and len(reference_image.read()) > MAX_IMAGE_SIZE:
            flash('Dimensiunea imaginii de referință depășește 10 MB. Vă rugăm să încărcați o imagine mai mică.')
            return render_template('add_product.html', form_data=form_data)

        # Revenim la începutul fisierelor pentru a le citi din nou
        if image:
            image.seek(0)
        if reference_image:
            reference_image.seek(0)

        # Verificam extensia si salvam imaginea facturii
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            if not filename.lower().endswith('.pdf'):
                webp_path = convert_to_webp(image_path)
                os.remove(image_path)
                filename = os.path.basename(webp_path)

        # Verificam extensia si salvam imaginea de referinta
        if reference_image and allowed_file(reference_image.filename):
            reference_filename = secure_filename(reference_image.filename)
            reference_image_path = os.path.join(app.config['UPLOAD_FOLDER'], reference_filename)
            reference_image.save(reference_image_path)
            reference_webp_path = convert_to_webp(reference_image_path)
            os.remove(reference_image_path)
            reference_filename = os.path.basename(reference_webp_path)
        else:
            reference_filename = None

        # Construin si salvam noul produs in baza de date
        new_product = Product(
            name=form_data['product_name'],
            invoice_image_file=filename,
            reference_image_file=reference_filename,
            user_id=current_user.id,
            warranty_period=form_data['warranty_period'],
            purchase_date=purchase_date,
            store=form_data['store'],
            city=form_data['city'],
            price=form_data['price'],
            currency=form_data['currency']
        )
        db.session.add(new_product)
        db.session.commit()

        # Afisam mesajul de succes si redirectionam utilizatorul
        flash('Produs adăugat cu succes!')
        return redirect(url_for('home_route'))

    # Randam template-ul pentru adaugarea unui produs.
    return render_template('add_product.html', form_data=form_data)


def delete_product(id):
    # Incercam sa obtinem produsul din baza de date folosind ID-ul dat
    product = Product.query.get_or_404(id)

    # Verificam daca produsul apartine utilizatorului curent
    if product.user_id != current_user.id:
        # Daca nu, avortam cererea cu un cod de eroare 403 (Forbidden)
        abort(403)

    # Stergem produsul din baza de date
    db.session.delete(product)
    db.session.commit()

    # Redirectionam utilizatorul catre pagina principala
    return redirect(url_for('home_route'))


def send_png_file(directory, filename):
    # Trimite un fisier PNG din directorul specificat ca atasament
    return send_from_directory(directory, filename, as_attachment=True)

@login_required
def download_file(filename):
    try:
        # Logam incercarea de descarcare
        print(f"Incercare descarcare: {filename}")

        # Construim calea completa a fisierului
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Verificam daca fisierul exista
        if not os.path.exists(file_path):
            print(f"Fisierul '{file_path}' nu exista.")
            return "Fisierul nu exista", 404

        # Verificam daca fisierul este o imagine .webp
        if filename.lower().endswith('.webp'):
            # Daca este, convertim imaginea la formatul PNG
            png_image_path = convert_to_png(file_path)

            # Daca conversia esueaza, returnam o eroare
            if png_image_path is None:
                print("Eroare la conversia catre PNG.")
                return "A aparut o eroare", 500

            print(f"Calea catre imaginea PNG: {png_image_path}")

            # Trimite imaginea convertita in PNG ca atasament
            return send_png_file(app.config['UPLOAD_FOLDER'], os.path.basename(png_image_path))
        else:
            # Pentru alte tipuri de fisiere, le trimitem ca atasamente fara nicio conversie
            return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except Exception as e:
        # Logam orice exceptie care apare si returnam un mesaj de eroare
        print(f"Eroare: {e}")
        return "A aparut o eroare", 500

