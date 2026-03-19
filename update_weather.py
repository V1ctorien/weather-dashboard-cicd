import requests
import os
from datetime import datetime,timezone


# ============================================
# CONFIGURATION
# ============================================

# --La clé API est récupérée depuis les variables
# d'environnement (jamais en dur dans le code !)

API_KEY = os.environ.get("OPENWEATHER_API_KEY")

# --Liste des villes à afficher
# Modifiez cette liste selon vos préférences !

CITIES = ["Paris", "London", "New York", "Tokyo", "Sydney"]

# URL de base de l'API OpenWeatherMap
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# ============================================
# FONCTION : Récupérer la météo d'une ville
# ============================================

def get_weather(city):
 
 #"""Appelle l'API et retourne les données météo."""

    params = {"q": city, # Nom de la ville
              "appid": API_KEY, # Clé API
              "units": "metric", # Températures en Celsius
              "lang": "fr" # Descriptions en français
             }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status() # Lève une erreur si status != 200
        data = response.json()
        return {
            "city": city,
            "temp": round(data["main"]["temp"], 1),
            "feels_like": round(data["main"]["feels_like"], 1),
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"],
            "wind": round(data["wind"]["speed"] * 3.6, 1),
            "icon": get_weather_emoji(data["weather"][0]["main"])
            }
    except Exception as e:
        print(f"Erreur pour {city}: {e}")
        return None
 
# ============================================
# FONCTION : Emoji selon la condition météo
# ============================================
def get_weather_emoji(condition):
    """Retourne un emoji selon la condition météo."""
    emojis = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Rain": "🌧️",
    "Drizzle": "🌦️",
    "Thunderstorm": "⛈️",
    "Snow": "❄️",
    "Mist": "🌫️",
    "Fog": "🌫️",
    "Haze": "🌫️"
    }
    return emojis.get(condition, "🌡️")
# ============================================
# FONCTION : Générer le contenu du README
# ============================================
def generate_readme(weather_data):
 """Crée le contenu Markdown du README."""
 now = datetime.now(timezone.utc).strftime("%d/%m/%Y à %H:%M UTC")
 readme = f"""# Dashboard Météo - CI/CD 🌤️
> Ce README est mis à jour automatiquement
> par GitHub Actions toutes les 6 heures !

## Meteo actuelle - {now}

| Ville | Météo | Temp | Ressenti | Humidité | Vent |
|-------|-------|------|----------|----------|------|
"""
 
 for w in weather_data:
    if w:
        readme += (
        f"| {w['icon']} {w['city']} "
        f"| {w['description'].capitalize()} "
        f"| {w['temp']}°C "
        f"| {w['feels_like']}°C "
        f"| {w['humidity']}% "
        f"| {w['wind']} km/h |\n"
        )
 return readme

# ============================================
# POINT D'ENTRÉE DU SCRIPT
# ============================================
if __name__ == "__main__":
 # Vérifier que la clé API est définie
 if not API_KEY:
    print("ERREUR : OPENWEATHER_API_KEY non définie !")
    exit(1)
 # Récupérer la météo de chaque ville
 print("Récupération des données météo...")
 weather_data = []
 for city in CITIES:
    data = get_weather(city)
    weather_data.append(data)
    if data:
        print(f" {city}: {data['temp']}°C")
 # Générer et écrire le README
 print("Génération du README...")
 readme_content = generate_readme(weather_data)
 with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)
 print("README.md mis à jour avec succès !")
