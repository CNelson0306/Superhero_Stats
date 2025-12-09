"""
superhero_api.py

Handles:
- Fetching individual hero data (SuperheroAPI)
- Fetching ALL heroes instantly (Akabab dataset)
- Caching using functools.lru_cache
"""
import os
import requests
from functools import lru_cache
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Read token from environment
TOKEN = os.getenv("SUPERHERO_API_TOKEN")

if not TOKEN:
    raise ValueError("Missing SUPERHERO_API_TOKEN in .env file!")

BASE_URL = f"https://superheroapi.com/api/{TOKEN}"

# Akabab dataset 
AKABAB_ALL_URL = "https://akabab.github.io/superhero-api/api/all.json"


@lru_cache(maxsize=256)
def get_hero(hero_id: int) -> dict:
    """
    Fetch details for an individual hero from SuperheroAPI.
    Cached to avoid repeated calls.
    """

    # Shows caching is working
    # print(f"Fetching hero {hero_id} from API (or cache miss)")

    url = f"{BASE_URL}/{hero_id}"

    response = requests.get(url)
    response.raise_for_status()

    return response.json()


@lru_cache(maxsize=1)
def get_all_heroes() -> list:
    """
    Fetches all 563 heroes in a single request using Akabab.
    This replaces slow iteration over 731 IDs.
    """

    print("Loading ALL heroes from Akabab dataset…")

    response = requests.get(AKABAB_ALL_URL)
    response.raise_for_status()

    heroes = response.json()
    print(f"Loaded {len(heroes)} heroes successfully.")

    return heroes
