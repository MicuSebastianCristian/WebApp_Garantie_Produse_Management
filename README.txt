"""
Autor: Micu Sebastian Cristian
Email: sebastian.micu112@gmail.com
Data proiectului: Septembrie 2023
GitHub: https://github.com/MicuSebastianCristian

Descriere:
Acest fisier reprezinta o aplicatie de Management al Garantiilor Produselor dezvoltata de autor in limbajul de programare Python.
Aplicatia este construita utilizand framework-ul Flask si isi propune sa gestioneze, sa actualizeze si sa stocheze informatii despre produse si detaliile acestora intr-un sistem individual si securizat.
In esenta, codul reprezinta o aplicatie de management al garantiilor produselor, in care utilizatorii pot adauga, edita si sterge produse, precum si descarca imagini si facturi asociate acestora.
De asemenea, aplicatia ofera functionalitate de autentificare a utilizatorilor, iar fiecare utilizator poate gestiona propriile sale produse.

Proiectul este realizat pentru examenul de obtinere a certificatului de "Ajutor Programator" de la finalul cursului pe care l-am parcurs la compania IT Factory .


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


Pentru a utiliza aplicatia, este necesar sa aveti Python instalat si sa respectati instructiunile mentionate mai sus sau o puteti accesa introducand credetialele "test" si "test, intrand pe urmatorul url securizat: https://sebastianmicu.pythonanywhere.com/login 
"""