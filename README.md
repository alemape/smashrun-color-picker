# Smashrun Color Picker

[![License: MIT](https://img.shields.io/github/license/alemape/smashrun-color-picker)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)

Piccola suite di script per impostare il colore del grafico attività su [Smashrun](https://it.smashrun.com/) scegliendolo tramite valori **RGB** invece che cliccando manualmente sull'immagine color-picker del sito.

> **Disclaimer:** progetto personale/educativo, non affiliato né sponsorizzato da Smashrun. Usa un endpoint interno del sito non documentato pubblicamente come API — funziona solo con il proprio account e la propria sessione già autenticata, ma è comunque un uso non ufficiale del servizio: usalo a tuo rischio.

## Come funziona

Il color-picker di Smashrun non accetta un RGB diretto: la sua API (`SaveUserGraphColorFromImage`) vuole una coordinata `(x, y)` e il nome di un'immagine già ospitata sul loro server, e sarà il server a leggere il colore da quel pixel. Questa suite quindi:

1. scarica in locale le immagini color-picker usate dal sito;
2. dato un RGB a piacere, cerca fra tutte le immagini il pixel più vicino a quel colore;
3. prepara la chiamata `(x, y, immagine)` da inviare all'API per applicarlo all'account.

## File

| File | Cosa fa |
|---|---|
| [srcp.py](srcp.py) | Scandaglia `it.smashrun.com/images/color-picker/` per anno/mese (dal 2000 a oggi) e stampa gli URL delle immagini realmente esistenti. |
| [dwlcp.py](dwlcp.py) | Scarica in locale la lista di immagini trovate da `srcp.py`. |
| [pick_color.py](pick_color.py) | **Script principale.** Dato un RGB, cerca fra le immagini locali (cartella `immagini_color_picker/`) il pixel più vicino e mostra le coordinate da usare. |
| [custom.py](custom.py) | Versione originale/dimostrativa: legge un pixel fisso da un'immagine e invia la richiesta a Smashrun (senza gestione di autenticazione). |

## Requisiti

```bash
pip install requests Pillow numpy
```

## Uso

### 0. Scarica le immagini color-picker (non incluse nel repo)

Le immagini sono proprietà di Smashrun e non vengono distribuite in questo repository: vanno scaricate localmente al primo utilizzo.

```bash
python srcp.py    # trova gli URL delle immagini disponibili
python dwlcp.py   # le scarica nella cartella immagini_color_picker/
```

### 1. Trova il pixel più vicino a un colore

```bash
python pick_color.py R G B
```

Esempio (Nike Volt, RGB 206 255 0):

```bash
python pick_color.py 206 255 0
```

Stampa il colore trovato, la distanza dal colore richiesto (0 = identico) e le coordinate/immagine da usare.

### 2. Applica il colore all'account

L'endpoint di Smashrun richiede che tu sia loggato (identifica l'account dai cookie di sessione del browser) — per questo la richiesta va eseguita **dalla console del browser**, mentre sei loggato su smashrun.com, non dallo script Python:

1. Apri smashrun.com e fai login.
2. Apri la Console degli strumenti sviluppatore (F12 → tab "Console").
3. Incolla ed esegui (sostituendo x, y e nome immagine con quelli stampati da `pick_color.py`):

```js
let r = await fetch("https://it.smashrun.com/services/user-jsonservice.asmx/SaveUserGraphColorFromImage", {
  method: "POST",
  credentials: "include",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ x: 780, y: 180, relativeImageUrl: "images/color-picker/2014-01-849x565.jpg" })
});
console.log("status:", r.status);
console.log("body:", await r.text());
```

4. Ricarica la pagina del profilo Smashrun per vedere il nuovo colore applicato.

## Note

- Lo script `pick_color.py` accetta anche un flag `--apply` per inviare la richiesta direttamente da Python, ma **funzionerà solo se hai una sessione autenticata** (cookie) passata alla libreria `requests` — allo stato attuale non è implementato, quindi va usato solo in modalità di ricerca (senza `--apply`) e applicato via console browser come sopra.
- Le immagini locali si trovano in `immagini_color_picker/` (esclusa da git, va scaricata con `dwlcp.py`).
- `dwlcp.py` contiene una lista di URL già nota; `srcp.py` serve per verificarla/aggiornarla se Smashrun pubblica nuove immagini.

## Contributing

Contributi benvenuti, è un progetto piccolo e informale:

1. Fai un fork del repository.
2. Crea un branch per la tua modifica (`git checkout -b feature/nome-modifica`).
3. Apri una Pull Request descrivendo cosa cambia e perché.

Idee utili se vuoi contribuire:
- gestione automatica dell'autenticazione in `pick_color.py --apply` (sessione/cookie), per applicare il colore senza passare dalla console del browser;
- far scrivere a `srcp.py` la lista di URL trovati in un file, letto poi da `dwlcp.py` invece della lista hardcoded;
- test automatici per `find_best_pixel`.

Per bug o richieste, apri una [Issue](https://github.com/alemape/smashrun-color-picker/issues).

## Licenza

[MIT](LICENSE)
