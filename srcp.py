import requests
from datetime import datetime

# Definizione del formato base dell'URL
base_url = "https://it.smashrun.com/images/color-picker/"

# Definizione dell'intervallo di anni (dal 2000 a oggi)
start_year = 2000
end_year = datetime.now().year

# Lista dei mesi in formato "MM"
months = [f"{month:02d}" for month in range(1, 13)]

# Lista per memorizzare gli URL validi
valid_urls = []

# Funzione per verificare se un URL esiste
def check_url_exists(url):
    try:
        response = requests.head(url)
        return response.status_code == 200
    except requests.RequestException:
        return False

# Ciclo sugli anni e mesi per costruire e verificare gli URL
for year in range(start_year, end_year + 1):
    for month in months:
        # Costruzione dell'URL
        url = f"{base_url}{year}-{month}-849x565.jpg"
        
        # Verifica se l'URL esiste
        if check_url_exists(url):
            valid_urls.append(url)

# Stampa la lista completa degli URL validi
for url in valid_urls:
    print(url)

# Stampa del numero totale di URL validi trovati
print(f"Totale URL validi trovati: {len(valid_urls)}")
