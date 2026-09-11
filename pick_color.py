import sys
import os
import glob
import numpy as np
from PIL import Image
import requests

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(SCRIPT_DIR, "immagini_color_picker")
SAVE_URL = "https://it.smashrun.com/services/user-jsonservice.asmx/SaveUserGraphColorFromImage"


def find_best_pixel(target_rgb):
    """Cerca in tutte le immagini locali il pixel piu' vicino al colore richiesto."""
    target = np.array(target_rgb, dtype=np.int32)
    best = None  # (dist2, filename, x, y, actual_rgb)

    for path in sorted(glob.glob(os.path.join(IMAGES_DIR, "*.jpg"))):
        with Image.open(path) as img:
            arr = np.asarray(img.convert("RGB"), dtype=np.int32)  # (H, W, 3)

        diff = arr - target
        dist2 = np.sum(diff * diff, axis=2)  # (H, W)
        y, x = np.unravel_index(np.argmin(dist2), dist2.shape)
        d = int(dist2[y, x])

        if best is None or d < best[0]:
            actual = tuple(int(v) for v in arr[y, x])
            best = (d, os.path.basename(path), int(x), int(y), actual)

    return best


def send_color_to_smashrun(x, y, relative_image_url):
    payload = {"x": x, "y": y, "relativeImageUrl": relative_image_url}
    headers = {"Content-Type": "application/json"}
    return requests.post(SAVE_URL, json=payload, headers=headers)


def main():
    if len(sys.argv) not in (4, 5):
        print("Uso: python pick_color.py R G B [--apply]")
        print("  --apply  invia davvero la richiesta a Smashrun (modifica il colore dell'account)")
        sys.exit(1)

    r, g, b = (int(v) for v in sys.argv[1:4])
    apply_change = len(sys.argv) == 5 and sys.argv[4] == "--apply"

    for v in (r, g, b):
        if not 0 <= v <= 255:
            print("I valori RGB devono essere tra 0 e 255.")
            sys.exit(1)

    dist2, filename, x, y, actual = find_best_pixel((r, g, b))
    dist = dist2 ** 0.5

    print(f"Colore richiesto:          RGB({r}, {g}, {b})")
    print(f"Pixel piu' vicino trovato: RGB{actual} in '{filename}' a (x={x}, y={y})")
    print(f"Distanza euclidea:         {dist:.1f}  (0 = colore identico, max teorico ~441)")

    relative_image_url = f"images/color-picker/{filename}"

    if not apply_change:
        print("\n[Modalita' test: nessuna richiesta inviata a Smashrun]")
        print(f"Payload che verrebbe inviato: x={x}, y={y}, relativeImageUrl='{relative_image_url}'")
        print("Rilancia con --apply per applicarlo davvero all'account.")
        return

    print(f"\nInvio richiesta a {SAVE_URL} ...")
    response = send_color_to_smashrun(x, y, relative_image_url)
    print(f"Status code: {response.status_code}")
    print(f"Risposta: {response.text[:500]}")


if __name__ == "__main__":
    main()
