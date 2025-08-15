import os
import base64
from datetime import datetime

import cv2
import dotenv
import openai
import requests
from bs4 import BeautifulSoup


PARSE_MENU_PROMPT = """"Du bist ein Experte im Lesen der Speisekarte.
Die Speisekarte hat für jeden Tag (Montag-Freitag) drei Gerichte (Menü 1-3).

Trage die Ergebnisse in eine Tabelle mit einer Zeile pro Menü und einer Spalte pro Tag ein.
Gib nur die Tabelle formatiert als Markdown aus, sonst nichts.

Beispiel:
```
| Menü    | Montag           | Dienstag               | Mittwoch             | Donnerstag      | Freitag        |
|---------|------------------|------------------------|----------------------|-----------------|----------------|
| Menü 1  | Regenbogen-Pizza | Glitzer-Kartoffelpüree | Marsianer-Lasagne    | Wolken-Suppe    | Drachen-Buffet |
| Menü 2  | Einhorn-Burger   | Zauberstab-Spaghetti   | Feenstaub-Gulasch    | Roboter-Risotto | Drachen-Buffet |
| Menü 3  | Piraten-Sushi    | Vampir-Kroketten       | Magier-Kürbisauflauf | Troll-Schnitzel | Drachen-Buffet |
```
"""


def _get_client():
    dotenv.load_dotenv()
    client = openai.OpenAI(
        base_url=os.environ.get("API_ENDPOINT", "http://localhost:11434/v1"),
        api_key=os.environ.get("API_KEY", "ollama")
    )
    model = os.environ.get("MODEL", "gemma3:12b")
    return client, model


def get_food():
    client, model = _get_client()

    # 1. Prepare cache path for this week
    today = datetime.now()
    year_str = today.strftime("%Y")
    week_str = today.strftime("%V")  # ISO week number
    cache_dir = os.path.join(os.path.dirname(__file__), ".cache")
    os.makedirs(cache_dir, exist_ok=True)
    cache_filename = f"tpk-speisekarte-{year_str}-KW{week_str}.jpg"
    cache_path_jpg = os.path.join(cache_dir, cache_filename)
    cache_path_md = cache_path_jpg.replace(".jpg", ".md")

    # 2. Try to use cached menu (if we have already parsed it in the past)
    if os.path.exists(cache_path_md):
        print("Using cached menu")
        with open(cache_path_md, "r", encoding="utf-8") as f:
            return f.read()

    # 3. Try to load image from cache
    if os.path.exists(cache_path_jpg):
        print("Using cached menu image")
        with open(cache_path_jpg, "rb") as f:
            img_bytes = f.read()
    else:
        # 4. Download the blog page and find the image
        print("Downloading menu image")
        url = "https://joels-cantina.de/blog/"
        resp = requests.get(url)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        links = [
            a['href'] for a in soup.find_all('a', href=True)
        ]
        links = [
            link
            for link in links
            if "tpk-speisekarte" in link.lower() and link.lower().endswith('.jpg')
        ]
        if not links:
            return "No menu images found."

        date_str = today.strftime("%Y-%m-%d")
        prompt = (
            "Given these filenames:\n"
            + "\n".join(links)
            + f"\nWhich filename most likely matches today's date ({date_str}) or calendar week ({week_str})? "
            "Return only the filename."
        )

        completion = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        chosen_filename = completion.choices[0].message.content.strip()
        if chosen_filename not in links:
            matches = [l for l in links if chosen_filename in l]
            if matches:
                chosen_filename = matches[0]
            else:
                chosen_filename = links[0]  # fallback

        if not chosen_filename.startswith("http"):
            image_url = url + chosen_filename
        else:
            image_url = chosen_filename
        img_resp = requests.get(image_url)
        img_resp.raise_for_status()
        img_bytes = img_resp.content

        # 5. Save to cache
        with open(cache_path_jpg, "wb") as f:
            f.write(img_bytes)
        
        # Downsample image and reload it
        img = cv2.imread(cache_path_jpg)
        img = cv2.resize(img, (int(438 * 1.7), int(310*1.7)))
        cv2.imwrite(cache_path_jpg, img)
        with open(cache_path_jpg, "rb") as f:
            img_bytes = f.read()

    # 6. Convert the image into a markdown table using AI
    print("Parsing menu")
    img_b64 = "data:image/jpeg;base64," + base64.b64encode(img_bytes).decode("utf-8")
    completion2 = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": PARSE_MENU_PROMPT},
                {"type": "image_url", "image_url": {"url": img_b64}}
            ]}
        ]
    )
    menu_md = completion2.choices[0].message.content.strip()

    # 6. Return result to user (including picture as markdown)
    with open(cache_path_md, "w", encoding="utf-8") as f:
        f.write(menu_md)
    return menu_md
