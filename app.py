"""
Autor: Micu Sebastian Cristian
Email: sebastian.micu112@gmail.com
Data proiectului: Septembrie 2023
GitHub: https://github.com/MicuSebastianCristian

Descriere:
Acest fisier reprezinta partea din spate a unei aplicatii de Management al Garantiilor Produselor dezvoltata de autor in limbajul de programare Python.
Aplicatia este construita utilizand framework-ul Flask si isi propune sa gestioneze, sa actualizeze si sa stocheze informatii despre produse si detaliile acestora intr-un sistem.
Este componenta de baza a aplicatiei care faciliteaza functionarea acesteia, inclusiv interactiunea cu baza de date, gestionarea cererilor utilizatorilor si manipularea datelor referitoare la produsele cu garantie.


Instructiuni de folosire a codului:

Asigurati-va ca aveti toate bibliotecile necesare instalate, inclusiv Flask, Flask-SQLAlchemy, Werkzeug si altele asemenea.
Puteti instala aceste biblioteci utilizand comanda "pip install nume_bibliotecii" in terminal sau linia de comanda.

Configurati calea catre baza de date in fisierul Python utilizand variabila "app.config['SQLALCHEMY_DATABASE_URI']".
In exemplul dat, se utilizeaza baza de date SQLite, iar calea catre fisierul bazei de date este specificata ca 'sqlite:///site.db'.
Puteti modifica aceasta cale in functie de preferintele dvs.

Pentru a porni serverul Flask, rulati acest fisier Python in terminal sau linia de comanda folosind comanda "python nume_fisier.py", unde 'nume_fisier.py' reprezinta numele acestui fisier.
Dupa rulare, aplicatia va deveni accesibila la adresa "http://localhost:5001/" intr-un browser web.

Asigurati-va ca aveti toate fisierele HTML necesare pentru functionarea aplicatiei.
Detalii specifice despre aceste fisiere HTML nu sunt furnizate in comentariile din cod, dar ele sunt esentiale pentru afisarea si interactiunea cu aplicatia.
Aceste fisiere HTML ar trebui sa fie parte a frontend-ului aplicatiei si sa ofere utilizatorilor o interfata de utilizare adecvata pentru gestionarea garantiilor produselor.

In esenta, codul reprezinta o aplicatie de management al garantiilor produselor, in care utilizatorii pot adauga, edita si sterge produse, precum si descarca imagini si facturi asociate acestora.
De asemenea, aplicatia ofera functionalitate de autentificare a utilizatorilor, iar fiecare utilizator poate gestiona propriile sale produse.
Pentru a utiliza aplicatia, este necesar sa aveti Python instalat si sa respectati instructiunile mentionate mai sus.
"""

from flask import Flask
from flask_login import LoginManager, login_required
from flask_migrate import Migrate
from models import User
from models import db
import os

# Initializam aplicatia Flask.
app = Flask(__name__)

# Setam configurarea bazei de date - folosim SQLite.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# Definim o cheie secreta pentru sesiuni. Important: sa o schimbam in productie!
app.secret_key = 'Sebastian.1234'

# Dezactivam alertele legate de modificarile bazei de date.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initializam baza de date cu Flask.
db.init_app(app)

# Initializam managerul de autentificare.
login_manager = LoginManager()

# Integram managerul de autentificare in aplicatie.
login_manager.init_app(app)

# Redirectionam utilizatorii neautentificati spre pagina de login.
login_manager.login_view = 'login'

# Stabilim o limita pentru marimea imaginilor incarcate.
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10 MB in bytes

# Definim calea unde vor fi stocate imaginile incarcate.
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'images')

# Definim extensiile permise pentru incarcare.
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

# Adaugam calea in configuratia aplicatiei.
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from functii_principale import convert_to_png, convert_to_webp, edit_product, register, index, login, logout, home, \
    download_invoice_file, add_product, delete_product, send_png_file, download_file


# Functie pentru conversia imaginilor din formatul WEBP în PNG.
def convert_to_png_route(webp_path):
    return convert_to_png()


# Incarcam utilizatorul in funcție de ID-ul sau pentru autentificare.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Functie pentru conversia imaginilor in formatul WEBP.
def convert_to_webp_route(image_path):
    return convert_to_webp()


# Verificam daca extensia fisierului este permisa.
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Definim ruta pentru editarea produselor.
@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
# Trebuie sa fii autentificat pentru a putea edita produse.
@login_required
def edit_product_route(id):
    return edit_product(id)


# Definim ruta pentru înregistrare.
@app.route('/register', methods=['GET', 'POST'])
def register_route():
    return register()


# Ruta principala redirecționează catre pagina de acasa.
@app.route('/')
def index_route():
    return index()


# Definim ruta pentru autentificare.
@app.route('/login', methods=['GET', 'POST'])
def login_route():
    return login()


# Definim ruta pentru delogare.
@app.route('/logout')
@login_required
def logout_route():
    return logout()


# Definim ruta pentru pagina de acasa.
@app.route('/home')
@login_required
def home_route():
    return home()


# Definim ruta pentru functia de download a facturii/bonului.
@app.route('/download_invoice/<filename>')
@login_required
def download_invoice_file_route(filename):
    return download_invoice_file(filename)


# Definim ruta pentru a apela functia de adaugare produs in contul utilizatorului.
@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product_route():
    return add_product()


# Definim ruta pentru a apela functia de stergere a unui produs din contul utilizatorului.
@app.route('/delete_product/<int:id>', methods=['POST'])
@login_required
def delete_product_route(id):
    return delete_product(id)


# Definim functia care returneaza fisierul in format png in momentul descarcarii.
def send_png_file_route(directory, filename):
    return send_png_file(directory, filename)


# Definim functia care porneste descarcarea.
@app.route('/download/<filename>')
@login_required
def download_file_route(filename):
    return download_file(filename)


# Punctul de intrare principal al aplicatiei
if __name__ == '__main__':
    # Asiguram ca toate tabelele bazei de date sunt create
    with app.app_context():
        db.create_all()

    # Pornim aplicatia pe portul 5001, cu modul de depanare activat
    app.run(debug=True, port=5001)

# Initializam extensia Migrate pentru a gestiona migrarile bazei de date
migrate = Migrate(app, db)
