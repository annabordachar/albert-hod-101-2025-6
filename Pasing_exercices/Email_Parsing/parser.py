import pandas as pd
from bs4 import BeautifulSoup
import re


def extract_order_data(soup, filename):
    """Extrait les données de commande depuis le HTML"""

    order = {
        "order_datetime": None,
        "order_number": None,
        "delivery_fee": None,
        "order_total_paid": None
    }

    # 1. Extraction de la date depuis le nom du fichier
    # Le fichier s'appelle par exemple: Fri_4_Jun_2021_18_12_55_.html
    # On transforme en: Fri 4 Jun 2021 18:12:55
    parts = filename.replace('_', ' ').replace('.html', '').strip().split()
    if len(parts) >= 6:
        date_str = ' '.join(parts[:-3]) + ' ' + ':'.join(parts[-3:])
        order["order_datetime"] = date_str

    # 2. Extraction du numéro de commande
    # On cherche dans tous les titres H2 le pattern "Commande n° XXXX"
    h2_tags = soup.find_all('h2')
    for h2 in h2_tags:
        text = h2.get_text()
        order_num_match = re.search(r'Commande n° (\d+)', text)
        if order_num_match:
            order["order_number"] = order_num_match.group(1)
            break

    # 3. Extraction des frais de livraison
    # On parcourt toutes les lignes de tableau pour trouver "Frais de livraison"
    all_tr = soup.find_all('tr')
    for tr in all_tr:
        tds = tr.find_all('td')
        if len(tds) >= 2:
            first_td_text = tds[0].get_text(strip=True)
            if first_td_text == 'Frais de livraison':
                price_text = tds[1].get_text(strip=True)
                price_match = re.search(r'€([\d.]+)', price_text)
                if price_match:
                    order["delivery_fee"] = float(price_match.group(1))
                break

    # 4. Extraction du total payé
    # On cherche les paragraphes avec la classe "total"
    for tr in all_tr:
        total_p = tr.find_all('p', class_='total')
        if len(total_p) >= 2:
            price_text = total_p[1].get_text(strip=True)
            price_match = re.search(r'€([\d.]+)', price_text)
            if price_match:
                order["order_total_paid"] = float(price_match.group(1))
            break

    return order


def extract_restaurant_data(soup):
    """Extrait les données du restaurant depuis le HTML"""

    restaurant = {
        "name": None,
        "address": None,
        "city": None,
        "postcode": None,
        "phone_number": None
    }

    # 1. Trouver les tables qui contiennent les infos du restaurant
    # Le restaurant est dans une table avec class="fluid", width="200" et align="left"
    fluid_tables = soup.find_all('table', class_='fluid', width='200', align='left')

    # 2. Parcourir chaque table trouvée
    for table in fluid_tables:
        ps = table.find_all('p')

        # 3. Vérifier qu'on a au moins 5 paragraphes
        if len(ps) >= 5:
            first_p_style = ps[0].get('style', '')
            # Le restaurant est identifié par le premier paragraphe en gras
            if 'bolder' in first_p_style:
                # Extraire les 5 infos du restaurant (on garde les emojis)
                restaurant["name"] = ps[0].get_text(strip=True)
                restaurant["address"] = ps[1].get_text(strip=True)
                restaurant["city"] = ps[2].get_text(strip=True)
                restaurant["postcode"] = ps[3].get_text(strip=True)
                restaurant["phone_number"] = ps[4].get_text(strip=True)
                break

    return restaurant


def extract_customer_data(soup):
    """Extrait les données du client depuis le HTML"""

    customer = {
        "name": None,
        "address": None,
        "city": None,
        "postcode": None,
        "phone_number": None
    }

    # 1. Trouver les tables qui peuvent contenir les infos du client
    # Le client est dans une table avec class="fluid" et width="200"
    fluid_tables = soup.find_all('table', class_='fluid', width='200')

    # 2. Parcourir chaque table trouvée
    for table in fluid_tables:
        ps = table.find_all('p', class_='alignleft')

        # 3. Vérifier qu'on a au moins 5 paragraphes
        if len(ps) >= 5:
            first_p_style = ps[0].get('style', '')
            # Le client est identifié par text-align:right dans le style
            if 'text-align:right' in first_p_style:
                # Extraire les 5 infos du client
                customer["name"] = ps[0].get_text(strip=True)
                customer["address"] = ps[1].get_text(strip=True)
                customer["city"] = ps[2].get_text(strip=True)
                customer["postcode"] = ps[3].get_text(strip=True)
                customer["phone_number"] = ps[4].get_text(strip=True)
                break

    return customer


def extract_order_items(soup):
    """Extrait tous les articles commandés depuis le HTML"""

    order_items = []

    # 1. Trouver toutes les tables contenant des articles
    # Les articles sont dans des tables avec role="listitem"
    listitem_tables = soup.find_all('table', {'role': 'listitem'})

    # 2. Parcourir chaque table d'articles
    for table in listitem_tables:
        # Trouver toutes les lignes (il peut y avoir plusieurs articles)
        trs = table.find_all('tr')

        # 3. Parcourir chaque ligne de la table
        for tr in trs:
            tds = tr.find_all('td')

            # Vérifier qu'on a 3 colonnes: quantité, nom, prix
            if len(tds) >= 3:
                # Extraire la quantité (format "1x", "2x", etc.)
                quantity_text = tds[0].get_text(strip=True)
                quantity_match = re.match(r'(\d+)x', quantity_text)

                # Extraire le nom (premier paragraphe uniquement)
                name = None
                for child in tds[1].children:
                    if child.name == 'p':
                        name = child.get_text(strip=True)
                        break

                # Extraire le prix (format "12,55 €")
                price_text = tds[2].get_text(strip=True)
                price_match = re.search(r'([\d,]+)\s*€', price_text)

                # Si on a réussi à extraire les 3 infos, ajouter l'article
                if quantity_match and name and price_match:
                    quantity = int(quantity_match.group(1))
                    price = float(price_match.group(1).replace(',', '.'))

                    order_items.append({
                        "name": name,
                        "quantity": quantity,
                        "price": price
                    })

    return order_items