import requests
from PIL import Image

# Funzione per ottenere il colore da una specifica coordinata (x, y) dell'immagine
def get_color_from_image(image_path, x, y):
    with Image.open(image_path) as img:
        img = img.convert("RGB")  # Converte in RGB per ottenere il colore
        r, g, b = img.getpixel((x, y))
        return r, g, b

# Funzione per inviare la richiesta POST a Smashrun
def send_color_to_smashrun(x, y, relative_image_url):
    url = "https://it.smashrun.com/services/user-jsonservice.asmx/SaveUserGraphColorFromImage"
    payload = {
        "x": x,
        "y": y,
        "relativeImageUrl": relative_image_url
    }
    
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        print("Colore salvato con successo.")
    else:
        print(f"Errore durante il salvataggio del colore. Status code: {response.status_code}")

# Percorso dell'immagine locale che hai scaricato
image_path = "immagini_color_picker/2014-01-849x565.jpg"

# Seleziona le coordinate (x, y) da cui prendere il colore
x = 425
y = 290

# Ottieni il colore dall'immagine
color = get_color_from_image(image_path, x, y)
print(f"Il colore alla coordinata ({x}, {y}) è: {color}")

# Invia la richiesta POST a Smashrun con le coordinate e l'URL relativo dell'immagine
relative_image_url = "images/color-picker/2020-05-849x565.jpg"
send_color_to_smashrun(x, y, relative_image_url)
