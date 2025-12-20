import os
import json
from datetime import datetime
from crawler import web_crawler



def save_json(data):
    """
    Sauvegarde les données au format JSON dans le dossier 'results'.
    Le nom du fichier contient la date et l'heure : 'YYYY-MM-DD_HH-MM_quotes.json'
    Et écrase si nécessaire l'ancien fichier, si doublons
    """
    # Formatage du nom du fichier
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M") #on récupère la date actuelle et on la transorme en string selon le format voulu 
    filename = f"{timestamp}_quotes.json" # on crée le nom final du fichier
    folder = "Crawler/results" # nom du dossier pour le stockage

    # Création du dossier 'results' si nécessaire
    os.makedirs(folder, exist_ok=True)

    # on crée le chemin où stocker nos data à partir du nom du dossier et nom du fichier défini juste avant 
    filepath = os.path.join(folder, filename) 

    # Sauvegarde
    with open(filepath, 'w', encoding='utf-8') as f: # on ouvre un fichier selon le chemin qu'on a défini, en mode write ('w') pour écrire dnas ce fichier
        # ecrit en json le contenu de la variable 'data' ici c'est un dictionnaire donc ça se fait très bien,
        # grace à f defini juste au dessus on peut écrire ce fichier json directement dans le repertoire selon filepath
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Fichier sauvegardé dans : {filepath}")


if __name__ == "__main__":
    print("Lancement du crawler...")

    # on récupère le dictionaire final renvoyé par la foncution web_crawler dans le module 'crawler.py'
    quotes = web_crawler()
    # on sauvegarde les resultats dans un dossier 'result' grace à la fonction 'save_json' 
    save_json(quotes)
    print(f"{len(quotes)} citations sauvegardées dans results/quotes.json")
