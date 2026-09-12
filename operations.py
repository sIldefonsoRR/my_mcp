import csv
from pathlib import Path
import unicodedata
from pydantic import Field

_CITIES_PATH = Path(__file__).with_name("cities.csv")
try:
    with open(_CITIES_PATH, "r") as f:
        _cities = list(csv.DictReader(f))
except Exception as e:
    print(e)
    _cities = []


def _normalize_city_name(city_name: str) -> str:
    # 1.  NFD normalize
    normalized_text = unicodedata.normalize("NFD", city_name)

    # 2. Rebuild ignoring accents
    no_accent_text = "".join(
        c for c in normalized_text if unicodedata.category(c) != "Mn"
    )

    # 3. Convert to lowercase
    return no_accent_text


def get_city_details(
    country_code: str = Field(description="The country code in 2 letter"),
    city_name: str = Field(description="The city name"),):
    norm_city_name = _normalize_city_name(city_name=city_name)
    found_record = next(
        (
            item
            for item in _cities
            if item.get("City", "").lower() == norm_city_name.lower()
            and item.get("Country", "").lower() == country_code.lower()
        ),
        None,
    )
    return found_record


def get_cities_in_country(
    country_code: str = Field(description="The country code in 2 letter"),):
    found_records = [
        item["AccentCity"] for item in _cities if item["Country"] == country_code
    ]
    return found_records


def get_countries():
    _COUNTRIES_PATH = Path(__file__).with_name("countries.csv")
    try:
        with open(_COUNTRIES_PATH, "r") as f:
            _countries = f.read()
            return _countries
    except Exception as e:
        print(e)
        _countries = ""


def country_name(
    country_code: str = Field(description="The country code in 2 letter"),):
    _COUNTRIES_PATH = Path(__file__).with_name("countries.csv")
    try:
        with open(_COUNTRIES_PATH, "r") as f:
            _countries = list(csv.DictReader(f))
            found_record = next(
                (
                    item
                    for item in _countries
                    if item.get("Code", "").lower() == country_code.lower()
                ),
                None,
            )
            return found_record["Name"]
    except Exception as e:
        print(e)
        return ""

def get_city_details_prompt(
    city: str = Field(description="The name of the city"),
    country_code: str = Field(description="The 2-letter ISO country code (e.g., pt, us, fr)")) -> str:
    prompt = f"""
    Your goal is to provide comprehensive details about this city: {city} on a country with this Country Code: {country_code}

    Use the 'get_city_details' tool and compile key information about this city:
    - Country
    - City
    - AccentCity
    - Region
    - Population
    - Latitude
    - Longitude

    Present all of this information strictly in a clean, well-structured HTML table (`<table>`). Ensure the table is easy to read, uses proper table headers (`<th>`), and does not include any markdown styling around the HTML code.
    """

    return prompt