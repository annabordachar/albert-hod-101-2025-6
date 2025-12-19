import os
import json
from bs4 import BeautifulSoup
from datetime import datetime

from parser import (
    extract_order_data,
    extract_restaurant_data,
    extract_customer_data,
    extract_order_items
)
from save_module import save_json

DATA_FOLDER = "Email_Parsing/data"

if __name__ == "__main__":
    print("Lancement du email parseur...")

    files = [f for f in os.listdir(DATA_FOLDER) if f.endswith('.html')]
    all_orders = []

    print(f"Traitement de {len(files)} fichiers HTML...\n")

    for i, file in enumerate(files, 1):
        try:
            with open(os.path.join(DATA_FOLDER, file), 'r', encoding='utf-8') as f:
                content = f.read()
                soup = BeautifulSoup(content, 'html.parser')

                order_data = extract_order_data(soup, file)
                restaurant_data = extract_restaurant_data(soup)
                customer_data = extract_customer_data(soup)
                order_items = extract_order_items(soup)

                complete_order = {
                    "order": order_data,
                    "restaurant": restaurant_data,
                    "customer": customer_data,
                    "order_items": order_items
                }

                all_orders.append(complete_order)

                if i % 10 == 0:
                    print(f"{i}/{len(files)} fichiers traités")

        except Exception as e:
            print(f"Erreur sur {file}: {e}")

    save_json(all_orders)
    print(f"{len(all_orders)} commandes sauvegardées dans results/")
