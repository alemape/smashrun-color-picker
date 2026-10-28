# Smashrun Color Picker

[![License: MIT](https://img.shields.io/github/license/alemape/smashrun-color-picker)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)

**English** | [Italiano](README.md)

A small set of scripts to set your activity graph color on [Smashrun](https://www.smashrun.com/) using **RGB** values, instead of clicking on the site's color-picker image.

> **Disclaimer:** personal/educational project, not affiliated with or endorsed by Smashrun. It uses an internal site endpoint that is not publicly documented as an API. It only works with your own account and an already-authenticated session, but it is still an unofficial use of the service: use it at your own risk.

## How it works

Smashrun's color picker does not accept an RGB value directly: its API (`SaveUserGraphColorFromImage`) takes an `(x, y)` coordinate and the name of an image already hosted on their server, and the server reads the color from that pixel. This suite therefore:

1. downloads the color-picker images used by the site;
2. given any RGB value, searches all the images for the closest matching pixel;
3. builds the `(x, y, image)` call to send to the API to apply the color to your account.

## Files

| File | Description |
|---|---|
| [srcp.py](srcp.py) | Probes `it.smashrun.com/images/color-picker/` by year/month (2000 to today) and prints the URLs of the images that actually exist. |
| [dwlcp.py](dwlcp.py) | Downloads the list of images found by `srcp.py`. |
| [pick_color.py](pick_color.py) | **Main script.** Given an RGB value, finds the closest pixel among the local images (`immagini_color_picker/` folder) and prints the coordinates to use. |
| [custom.py](custom.py) | Original/demo version: reads a fixed pixel from an image and sends the request to Smashrun (no authentication handling). |

## Requirements

```bash
pip install requests Pillow numpy
```

## Usage

### 0. Download the color-picker images (not included in the repo)

The images are Smashrun's property and are not distributed in this repository: download them locally on first use.

```bash
python srcp.py    # finds the available image URLs
python dwlcp.py   # downloads them into immagini_color_picker/
```

### 1. Find the closest pixel to a color

```bash
python pick_color.py R G B
```

Example (Nike Volt, RGB 206 255 0):

```bash
python pick_color.py 206 255 0
```

It prints the color found, its distance from the requested color (0 = identical) and the coordinates/image to use.

### 2. Apply the color to your account

The Smashrun endpoint requires you to be logged in (it identifies your account through the browser's session cookies), so the request must be run **from the browser console** while you are logged in to smashrun.com, not from the Python script:

1. Open smashrun.com and log in.
2. Open the developer tools Console (F12 → "Console" tab).
3. Paste and run the following (replacing x, y and the image name with the values printed by `pick_color.py`):

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

4. Reload your Smashrun profile page to see the new color applied.

## Notes

- `pick_color.py` also accepts an `--apply` flag to send the request directly from Python, but it **only works with an authenticated session** (cookies) passed to the `requests` library. This is not implemented yet, so use the script in search-only mode (without `--apply`) and apply the color through the browser console as shown above.
- The local images live in `immagini_color_picker/` (git-ignored; download them with `dwlcp.py`).
- `dwlcp.py` contains a hardcoded list of known URLs; `srcp.py` is there to verify/update it if Smashrun publishes new images.

## Contributing

Contributions are welcome; this is a small, informal project:

1. Fork the repository.
2. Create a branch for your change (`git checkout -b feature/your-change`).
3. Open a Pull Request describing what changes and why.

Ideas if you want to contribute:
- automatic authentication handling in `pick_color.py --apply` (session/cookies), to apply the color without going through the browser console;
- make `srcp.py` write the URLs it finds to a file that `dwlcp.py` reads, instead of the hardcoded list;
- automated tests for `find_best_pixel`.

For bugs or requests, open an [Issue](https://github.com/alemape/smashrun-color-picker/issues).

## License

[MIT](LICENSE)
