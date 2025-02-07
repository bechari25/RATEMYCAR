# ricerca.py

import requests

class RicercaImmagini:
    def __init__(self, api_key, search_engine_id):
        self.api_key = api_key
        self.search_engine_id = search_engine_id

    def get_car_image_google(self, car_name):
        """Funzione per ottenere l'immagine di un'auto usando l'API di Google Custom Search"""
        url = f"https://www.googleapis.com/customsearch/v1?q={car_name}+car&cx={self.search_engine_id}&searchType=image&key={self.api_key}"
        
        response = requests.get(url).json()
        
        if "items" in response:
            return response["items"][0]["link"]  # Restituisce l'URL della prima immagine trovata
        else:
            return None  # Nessuna immagine trovata
