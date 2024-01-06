# Autor: Sebastian Cristian Micu
# Email: sebastian.micu112@gmail.com
# Data proiectului: Septembrie 2023
# GitHub: https://github.com/MicuSebastianCristian

# Descriere:
# Acest script Python are rolul de a sterge fisierele de tip imagine PNG mai vechi de 10 minute dintr-un director specificat.
# Se bazeaza pe obtinerea timpului curent in secunde si pe compararea acestuia cu marcajul temporal al fisierelor.
# Scopul acestuia este de a elibera memoria din server. Folosind functiile din fisierul functii_principale, noi
# intotdeauna transformam orice fisiere de tip poze in fisiere webp pentru eficienta in stocare, iar cand
# utilizatorul descarca fisierul inapoi din baza de date facem conversia automata la png, pentru eficientizare
# sterge acel png din baza de date dupa ce a fost descarcat, dupa 10 minute.


# Instructiuni de folosire:
# 1. Asigurati-va ca aveti directorul corect in care se afla imaginile setat in variabila "image_directory".
# 2. Rulati acest script pentru a verifica si sterge imaginile PNG mai vechi de 10 minute.
# 3. Puteti ajusta timpul (10 minute) prin modificarea valorii "2 * 60" la linia 39, reprezentand 10 minute in secunde.

import os
import time

# Directorul in care se afla imaginile
image_directory = "/home/sebastianmicu/mysite/static/images/"

# Obtinerea timpului curent in secunde de la 1 ianuarie 1970
current_time = time.time()

# Parcurgerea fisierelor din director
for filename in os.listdir(image_directory):
    # Verificarea daca fisierul este o imagine PNG
    if filename.endswith(".png"):
        file_path = os.path.join(image_directory, filename)

        # Obtinerea atributelor fisierului
        file_stats = os.stat(file_path)

        # Verificarea daca fisierul este mai vechi de 10 minute
        if current_time - file_stats.st_mtime >= 2 * 60:  # 10 minute in secunde
            os.remove(file_path)
            print(f"Fisierul {filename} a fost sters.")
