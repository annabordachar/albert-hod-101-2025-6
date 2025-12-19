import requests
from bs4 import BeautifulSoup



#On déclare une fonciton 'web_crawler' qui permettra de scrappé le contenu d'une page web, à partir d'un url
# Ici le site ets libre d'accès, mais pour d'autre cas il faudra penser aussi à des clé, licences, proxies etc 
def web_crawler(base_url="https://quotes.toscrape.com"):
    #ici on initialise la première page à visiter
    url = "/page/1/"
    #on prépare la liste où on stockera toutes les citations extraites au fur et à mesure.
    all_quotes = []

    while url: # Sécurité pour s'assurer d'executer la suite du code uniquement SI L'URL EXISTE
        response = requests.get(base_url + url) # requête HTTP GET à l’URL compelt de la page donc (base+page)
        soup = BeautifulSoup(response.text, 'html.parser') #On parse le contenu HTML avec BeautifulSoup pour pouvoir le manipuler

        #Après inspection de 'soup' donc le html parser, 
        #on voit bien que chaque citation était encapsulée dans une balise <div class="quote"> </div>.
        #Et dans chaque sitation il y a : <span class="text">, <small class="author">, <div class="tags">
        # Donc pour extraire proprement chaque donnée :  

        for quote in soup.select('.quote'): # Pour chaque bloc <div class="quote"> trouvé dans la page
            text = quote.select_one('.text').get_text(strip=True) # On extrait le texte de la citation (sans espace ni balise)
            author = quote.select_one('.author').get_text(strip=True) # On extrait le nom de l’auteur
            tags = [tag.get_text(strip=True) for tag in quote.select('.tags .tag')] # On extrait tous les tags associés, dans une liste
            # Attention ici tags identifie la division dans laquel il y a une liste de lien classé selon : <a class="tag" ...>, 
            # c'est pour celà qu'on boucle dessus

            # On feed notre liste du début 'all_quotes', avec des dictionnaire structuré à partir des données extraites. 
            all_quotes.append({
                'text': text,       # Contenu de la citation
                'author': author,   # Auteur de la citation
                'tags': tags        # Liste des tags associés
})
        # Une fois qu'on a fini de récupérer les info de la prmeiere page 'page1' au debut, On cherche le bouton "Next" 
        # pour savoir s’il y a une page suivante
        next_btn = soup.select_one('.next > a')

        # S’il existe, on récupère 'href' ( lien associé au bouton next qui devriat donc nous mener à la page d'après)
        # Sinon, on met url = None → ce qui stoppera la boucle while
        url = next_btn['href'] if next_btn else None

    return all_quotes # On renvoie notre liste remplie de dicitonnaire une fois qu'on ne trouve plus le button next page 
