"""
Flask app using:
SuperheroAPI for hero data
Akabab API for hero images (Superhero API blocking images in all browsers?)
"""

import os
from flask import Flask, render_template
from flask_cors import CORS
import requests
from superhero_api import get_all_heroes, get_hero

app = Flask(__name__)
CORS(app)

# Load Akabab image metadata once at startup 
AKABAB_URL = "https://akabab.github.io/superhero-api/api/all.json"

akabab_data = requests.get(AKABAB_URL).json()

# Build fast lookup: hero_name.lower() - image_url.
akabab_images = {}

for hero in akabab_data:
    name = hero["name"].lower()
    image_url = hero["images"].get("md")
    akabab_images[name] = image_url

print(f"Loaded {len(akabab_images)} Akabab hero images.")


@app.route("/")
def index():
    # Show list of heroes from SuperheroAPI.
    # Limited the number of heroes to load in.
    heroes = get_all_heroes()
    return render_template("index.html", heroes=heroes)


@app.route("/hero/<int:hero_id>")
def hero_page(hero_id):
    """Display hero details + Akabab image."""
    hero = get_hero(hero_id)

    hero_name = hero["name"].lower()

    # Get image from Akabab by hero name
    hero_image_url = akabab_images.get(hero_name)

    return render_template(
        "hero.html",
        hero=hero,
        hero_image_url=hero_image_url
    )


if __name__ == "__main__":
    app.run(debug=True)
