from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests
from urllib.parse import quote
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from pathlib import Path

def envoyer_hello_world(bot_token, channel_id, texte= "Hello World from Groupe 6 AFTERNOON"):

    # Création du client Slack avec le token du bot
    client = WebClient(token=bot_token)

    try: # On tentes une action, si Slack renvoie une erreur on la gère dans except
        # Envoi du message dans le channel
        resp = client.chat_postMessage(channel=channel_id, text=texte)
        return resp["ts"]# la fonction renovie l'identifiant temporel Slack du message en gusie de confirmation de l'envoie du message
    
    

    except SlackApiError as e:# gestion des erreurs au cas où 
        # Affiche l'erreur Slack 
        raise RuntimeError(f"Erreur Slack: {e.response['error']}") from e


def envoyer_tous_les_png(bot_token: str, channel_id: str, data_dir="data") :
    
    #On récupère le chemin jusqu'au file png qui sont stocké dans "data"
    data_dir = Path(data_dir)

    # Liste tous les PNG du dossier
    png_files = sorted(data_dir.glob("*.png")) #le code cherche tout les fichier du dossier "data_dir"="data", qui finissent par .png
    
    if not png_files:# gestion du cas où la liste de file .png crée juste avant est vide
        raise FileNotFoundError(f"Aucun .png dans {data_dir.resolve()}")

    # Même création du client Slack avec le token du bot que tout à l'heure
    client = WebClient(token=bot_token)

    # Envoi fichier par fichier
    for i, fp in enumerate(png_files, start=1): #on boucle sur chaque image de la liste qu'on a créé png_files
        try: # on tente d'envoyer l'image de la liste dans le canal
            #On vient simplement mapper les differente info necessaire à l'envoie comme le contenu du message 
            # le contenu du file qu'on envoie, le canale dans lequel on veut envoyer etc 
            client.files_upload_v2(
                channel=channel_id,
                file=str(fp),
                filename=fp.name,
                title=fp.stem,
                initial_comment=f"Image {i}/{len(png_files)} : {fp.name}", # on sait ou on en est du coup (ex: 1/4, 2/4....)
            )
        except SlackApiError as e: # Si on a rencontré un probleme on aur aun log dans le terminale
        
            raise RuntimeError(f"Erreur Slack sur {fp.name}: {e.response['error']}") from e

    return len(png_files) #Une fois que c'est fait on recoit comme log de confirmation le nombre de fichier .png 
                          #qu'on a trouvé dans data et qu'on a envoyé 


def wikipedia_premier_paragraphe(titre: str, lang: str = "en"):

    # On vient créer l'url qui servira à répondre à Woody 
    url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{quote(titre)}"

    try: 
        r = requests.get(url, headers={"User-Agent": "SlackWikipediaBot/1.0"}, timeout=10) #Envoie une requête GET à Wikipedia.

        if r.status_code == 404: # Si le sujet ne permet pas de trouver une page Wiki associé alors erreur
            return None, f"Page introuvable: {titre}"

        r.raise_for_status() # Si le code HTTP est du type 400/500 (sauf 404 déjà géré) ça lève une exception.
        data = r.json() # Convertit le JSON de réponse en dictionnaire Python.

        if data.get("type") == "disambiguation": # Wikipedia  dit que le titre à plusieurs sens il faut préciser.
            return None, f"Terme ambigu: {titre}. Sois plus précis."

        extract = (data.get("extract") or "").strip() #On récupère le texte du résumé
        if not extract:
            return None, f"Pas de résumé dispo pour: {titre}"# On envoie le résumé si il existe

        #Coupe le résumé en 2 au premier paragraphe, normalement identifié par double saut de ligne :
        paragraphe = extract.split("\n\n", 1)[0].strip()# On récupère que la prmeiere partie du split (premier paragraphe ducoup) 
        return paragraphe, None

    except requests.RequestException as e:# Si y a eu un probleme autre que ceux qu'on a deja pu identifier 
                                          # set erreur et faudra aller chercher plus loin 
        return None, f"Erreur Wikipedia: {e}"


def lancer_ecoute_wikipedia_socket_mode( bot_token: str, app_token: str, channel_id: str, woody_user_id: str, lang: str = "en", ) -> None:

    # On crée une application Slack Bolt qui va orchestrer la logique d’écoute des events Slack et l’envoi de réponses.
    app = App(token=bot_token)

    @app.event("message") # ça appelle à chaque message reçu la fonction juste en dessous
    def handle_message(event, say): #Fonction appelée automatiquement à chaque message

        # Ignore certains messages système comme des messages édités, messages de bots
        if event.get("subtype"):
            return

        # on ignore tous les messages qui ne viennent pas du channel ciblé.
        if event.get("channel") != channel_id:
            return

        # uniquement les messages envoyés par Woody
        if event.get("user") != woody_user_id:
            return
        # On récupère le texte du message de Woody.
        texte = (event.get("text") or "").strip()
        #Le bot ne réagit que si le message commence par "wikipedia:"
        if not texte.lower().startswith("wikipedia:"):
            return

        titre = texte.split(":", 1)[1].strip()# Coupe le message en deux et on vient récupérer la deuxieme partie du split avec [1]
        if not titre: #Si y a rien bah on fait rien 
            say("Format: Wikipedia:Nom_de_page")
            return

        #On appel l'api de wikipedia à travers la fonction dédier juste au dessus "wikipedia_premier_paragraphe"
        para, e = wikipedia_premier_paragraphe(titre, lang=lang)
        if e:
            say(e)
            return

        # Slack limite la taille des messages donc on tronque proprement
        if len(para) > 2900:
            para = para[:2897] + "..."  # On tronque proprement le texte pour éviter une erreur 

        #On envoie enfin le premier paragraphe Wikipedia dans le channel.
        say(para)

    # Démarre l'écoute en Socket Mode 
    SocketModeHandler(app, app_token).start()
