import os
import requests

# Lista degli URL forniti
url_list = [
    "https://it.smashrun.com/images/color-picker/2012-03-849x565.jpg",
    "https://it.smashrun.com/images/color-picker/2012-08-849x565.jpg",
    "https://it.smashrun.com/images/color-picker/2014-01-849x565.jpg",
    "https://it.smashrun.com/images/color-picker/2014-12-849x565.jpg",
    "https://it.smashrun.com/images/color-picker/2015-03-849x565.jpg",
    "https://it.smashrun.com/images/color-picker/2015-06-849x565.jpg",
    "https://it.smashrun.com/images/color-picker/2015-10-849x565.jpg",
    "https://it.smashrun.com/images/color-picker/2016-01-849x565.jpg",
    "https://it.smashrun.com/images/color-picker/2016-02-849x565.jpg",
    "https://it.smashrun.com/images/color-picker/2016-03-849x565.jpg",
    "https://it.smashrun.com/images/color-picker/2016-06-849x565.jpg",
    "https://it.smashrun.com/images/color-picker/2016-07-849x565.jpg",
    "https://it.smashrun.com/images/color-picker/2016-08-849x565.jpg",
    "https://it.smashrun.com/images/color-picker/2016-09-849x565.jpg",
    "https://it.smashrun.com/images/color-picker/2016-12-849x565.jpg",
    "https://it.smashrun.com/images/color-picker/2017-01-849x565.jpg",
    "https://it.smashrun.com/images/color-picker/2017-02-849x565.jpg",
    "https://it.smashrun.com/images/color-picker/2017-04-849x565.jpg",
    "https://it.smashrun.com/images/color-picker/2017-06-849x565.jpg",
    "https://it.smashrun.com/images/color-picker/2017-10-849x565.jpg",
    "https://it.smashrun.com/images/color-picker/2017-12-849x565.jpg",
    "https://it.smashrun.com/images/color-picker/2018-01-849x565.jpg",
    "https://it.smashrun.com/images/color-picker/2018-03-849x565.jpg",
    "https://it.smashrun.com/images/color-picker/2018-06-849x565.jpg",
    "https://it.smashrun.com/images/color-picker/2018-11-849x565.jpg",
    "https://it.smashrun.com/images/color-picker/2018-12-849x565.jpg",
    "https://it.smashrun.com/images/color-picker/2019-01-849x565.jpg",
    "https://it.smashrun.com/images/color-picker/2019-03-849x565.jpg",
    "https://it.smashrun.com/images/color-picker/2019-05-849x565.jpg",
    "https://it.smashrun.com/images/color-picker/2019-07-849x565.jpg",
    "https://it.smashrun.com/images/color-picker/2019-09-849x565.jpg",
    "https://it.smashrun.com/images/color-picker/2019-10-849x565.jpg",
    "https://it.smashrun.com/images/color-picker/2020-05-849x565.jpg"
]

# Definisci la cartella di destinazione per salvare le immagini
output_folder = "immagini_color_picker"

# Crea la cartella se non esiste
os.makedirs(output_folder, exist_ok=True)

# Funzione per scaricare una singola immagine
def download_image(url):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            # Estrae il nome del file dall'URL
            file_name = url.split("/")[-1]
            file_path = os.path.join(output_folder, file_name)

            # Salva l'immagine nella cartella
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Immagine salvata: {file_name}")
        else:
            print(f"Errore nel download dell'immagine: {url}")
    except Exception as e:
        print(f"Errore nel download: {url}, Errore: {e}")

# Ciclo per scaricare tutte le immagini dalla lista
for url in url_list:
    download_image(url)

print("Download completato!")
