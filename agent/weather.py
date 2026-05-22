import requests
import json
import sys
from datetime import datetime
from typing import Optional

# WMO Weather Code mapping
WMO_CODES = {
    0: "\U00002600 Clear sky",
    1: "\U0001F324 Mainly clear",
    2: "\U000026C5 Partly cloudy",
    3: "\U00002601 Overcast",
    45: "\U0001F32B Foggy",
    48: "\U0001F32B Depositing rime fog",
    51: "\U0001F326 Light drizzle",
    53: "\U0001F326 Moderate drizzle",
    55: "\U0001F326 Dense drizzle",
    56: "\U0001F327 Freezing light drizzle",
    57: "\U0001F327 Freezing dense drizzle",
    61: "\U0001F327 Slight rain",
    63: "\U0001F327 Moderate rain",
    65: "\U0001F327 Heavy rain",
    66: "\U0001F327 Freezing light rain",
    67: "\U0001F327 Freezing heavy rain",
    71: "\U0001F328 Slight snow",
    73: "\U0001F328 Moderate snow",
    75: "\U0001F328 Heavy snow",
    77: "\U00002744 Snow grains",
    80: "\U0001F326 Slight rain showers",
    81: "\U0001F326 Moderate rain showers",
    82: "\U0001F326 Violent rain showers",
    85: "\U0001F328 Slight snow showers",
    86: "\U0001F328 Heavy snow showers",
    95: "\U000026C8 Thunderstorm",
    96: "\U000026C8 Thunderstorm with slight hail",
    99: "\U000026C8 Thunderstorm with heavy hail",
}

def get_weather_description(code: int) -> str:
    return WMO_CODES.get(code, f"\U00002753 Unknown ({code})")

def wind_direction(deg: float) -> str:
    dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
            "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    idx = round(deg / 22.5) % 16
    return dirs[idx]

def search_city(query: str) -> list[dict]:
    """Search for cities using Open-Meteo Geocoding API."""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": query, "count": 10, "language": "en", "format": "json"}
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    results = data.get("results", [])
    if not results:
        return []
    cities = []
    for r in results:
        country = r.get("country", "Unknown")
        admin1 = r.get("admin1", "")
        name = r["name"]
        loc = f"{name}"
        if admin1 and admin1 != name:
            loc += f", {admin1}"
        loc += f", {country}"
        cities.append({
            "name": loc,
            "lat": r["latitude"],
            "lon": r["longitude"],
            "country": country,
            "elevation": r.get("elevation", 0),
        })
    return cities

def fetch_weather(lat: float, lon: float, days: int = 7) -> dict:
    """Fetch current weather and forecast from Open-Meteo."""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": [
            "temperature_2m", "relative_humidity_2m", "apparent_temperature",
            "weather_code", "wind_speed_10m", "wind_direction_10m",
            "pressure_msl", "cloud_cover", "precipitation"
        ],
        "daily": [
            "temperature_2m_max", "temperature_2m_min", "weather_code",
            "precipitation_sum", "precipitation_probability_max",
            "wind_speed_10m_max", "wind_direction_10m_dominant",
            "sunrise", "sunset"
        ],
        "timezone": "auto",
        "forecast_days": min(days, 16),
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()

def display_current(data: dict, city_name: str):
    """Display current weather conditions."""
    current = data["current"]
    units = data["current_units"]
    code = current["weather_code"]
    
    print()
    print("=" * 60)
    print(f"  \U0001F30D  CURRENT WEATHER \u2014 {city_name}")
    print("=" * 60)
    print(f"  \U0001F550  {current['time']}")
    print(f"  {get_weather_description(code)}")
    print(f"  \U0001F321  Temperature:      {current['temperature_2m']}{units['temperature_2m']}")
    print(f"  \U0001F914  Feels like:      {current['apparent_temperature']}{units['apparent_temperature']}")
    print(f"  \U0001F4A7  Humidity:         {current['relative_humidity_2m']}{units['relative_humidity_2m']}")
    print(f"  \U0001F4A8  Wind:             {current['wind_speed_10m']}{units['wind_speed_10m']} {wind_direction(current['wind_direction_10m'])}")
    print(f"  \U0001F300  Pressure:         {current['pressure_msl']}{units['pressure_msl']}")
    if "cloud_cover" in current:
        print(f"  \U00002601  Cloud cover:      {current['cloud_cover']}{units.get('cloud_cover', '%')}")
    if "precipitation" in current and current["precipitation"] > 0:
        print(f"  \U0001F327  Precipitation:    {current['precipitation']}{units.get('precipitation', 'mm')}")
    print("=" * 60)

def display_forecast(data: dict, days: int):
    """Display daily forecast."""
    daily = data["daily"]
    units = data["daily_units"]
    
    print(f"\n  \U0001F4C5  {days}-DAY FORECAST")
    print("-" * 60)
    
    for i in range(len(daily["time"])):
        date = datetime.strptime(daily["time"][i], "%Y-%m-%d")
        day_name = date.strftime("%a")
        date_str = date.strftime("%b %d")
        
        code = daily["weather_code"][i]
        t_max = daily["temperature_2m_max"][i]
        t_min = daily["temperature_2m_min"][i]
        precip = daily["precipitation_sum"][i]
        wind = daily["wind_speed_10m_max"][i]
        wind_dir = wind_direction(daily["wind_direction_10m_dominant"][i]) if "wind_direction_10m_dominant" in daily else ""
        prob = daily.get("precipitation_probability_max", [None] * len(daily["time"]))[i]
        
        emoji = get_weather_description(code).split(" ")[0]
        prob_str = f" (\U0001F327{prob}%)" if prob is not None and prob > 0 else ""
        
        print(f"  {day_name:3s} {date_str:8s}  {emoji}  "
              f"\U0001F321 {t_max:5.1f}\u2191 / {t_min:5.1f}\u2193{units['temperature_2m_max']}  "
              f"\U0001F4A7 {precip:4.1f}mm{prob_str:12s}  "
              f"\U0001F4A8 {wind:4.1f} {units['wind_speed_10m_max']} {wind_dir}")
    
    print("-" * 60)

def display_astronomy(data: dict):
    """Display sunrise/sunset info."""
    daily = data["daily"]
    if "sunrise" not in daily or "sunset" not in daily:
        return
    
    print(f"\n  \U0001F305  SUNRISE / SUNSET")
    print("-" * 60)
    for i in range(len(daily["time"])):
        date = datetime.strptime(daily["time"][i], "%Y-%m-%d")
        day_name = date.strftime("%a")
        sunrise = daily["sunrise"][i].split("T")[1] if "T" in daily["sunrise"][i] else daily["sunrise"][i]
        sunset = daily["sunset"][i].split("T")[1] if "T" in daily["sunset"][i] else daily["sunset"][i]
        print(f"  {day_name:3s}  \U0001F305 {sunrise}  \U0001F307 {sunset}")
    print("-" * 60)

def interactive_mode():
    """Interactive city search and weather display."""
    print()
    print("=" * 60)
    print("  \U0001F324   WEATHER CHECKER \u2014 Open-Meteo CLI")
    print("=" * 60)
    
    while True:
        print("\n  Enter a city name (or 'q' to quit, 'h' for help):")
        query = input("  > ").strip()
        
        if query.lower() in ("q", "quit", "exit"):
            print("  Goodbye! \U00002600")
            break
        
        if query.lower() in ("h", "help"):
            print("\n  Commands:")
            print("    <city name>  - Search for a city and show weather")
            print("    lat,lon      - Use coordinates directly (e.g. 51.5,-0.12)")
            print("    q / quit     - Exit the app")
            print("    h / help     - Show this help")
            continue
        
        # Check if coordinates were entered
        if "," in query and query.replace(".", "").replace("-", "").replace(",", "").strip().isdigit():
            try:
                parts = query.split(",")
                lat = float(parts[0].strip())
                lon = float(parts[1].strip())
                city_name = f"{lat}, {lon}"
                print(f"\n  \U0001F4E1  Using coordinates: {lat}, {lon}")
                data = fetch_weather(lat, lon)
                display_current(data, city_name)
                display_forecast(data, 7)
                display_astronomy(data)
                continue
            except (ValueError, IndexError):
                print("  \U0000274C  Invalid coordinates. Use format: lat,lon (e.g. 51.5,-0.12)")
                continue
        
        # Search for city
        print(f"  \U0001F50D  Searching for '{query}'...")
        try:
            cities = search_city(query)
        except Exception as e:
            print(f"  \U0000274C  Search failed: {e}")
            continue
        
        if not cities:
            print(f"  \U0000274C  No cities found for '{query}'. Try a different name.")
            continue
        
        # If multiple results, let user choose
        if len(cities) > 1:
            print(f"\n  Found {len(cities)} cities. Select one:")
            for i, c in enumerate(cities):
                elev = f", elev. {c['elevation']}m" if c['elevation'] else ""
                print(f"  [{i+1}] {c['name']}{elev}")
            print("  [0] Cancel")
            
            try:
                choice = int(input("  > ").strip())
                if choice == 0:
                    continue
                city = cities[choice - 1]
            except (ValueError, IndexError):
                print("  \U0000274C  Invalid choice.")
                continue
        else:
            city = cities[0]
        
        print(f"\n  \U0001F4CD  Selected: {city['name']}")
        
        # Ask for forecast days
        print("  How many days forecast? (1-16, default 7):")
        days_input = input("  > ").strip()
        try:
            days = max(1, min(16, int(days_input)))
        except ValueError:
            days = 7
        
        try:
            data = fetch_weather(city["lat"], city["lon"], days)
            display_current(data, city["name"])
            display_forecast(data, days)
            display_astronomy(data)
        except Exception as e:
            print(f"  \U0000274C  Failed to fetch weather: {e}")

def main():
    """Main entry point with CLI argument support."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="\U0001F324  Weather Checker \u2014 CLI app using Open-Meteo API (no API key needed)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  weather.py                    Interactive mode
  weather.py London             7-day forecast for London
  weather.py Tokyo --days 3     3-day forecast for Tokyo
  weather.py 51.5,-0.12         Use coordinates directly
  weather.py Paris --current    Show only current weather
  weather.py Berlin --forecast  Show only forecast
        """
    )
    parser.add_argument("city", nargs="?", help="City name or lat,lon coordinates")
    parser.add_argument("--days", type=int, default=7, help="Number of forecast days (1-16)")
    parser.add_argument("--current", action="store_true", help="Show only current weather")
    parser.add_argument("--forecast", action="store_true", help="Show only forecast")
    parser.add_argument("--astronomy", action="store_true", help="Show only sunrise/sunset")
    
    args = parser.parse_args()
    
    if not args.city:
        interactive_mode()
        return
    
    query = args.city
    
    # Check if coordinates
    if "," in query and query.replace(".", "").replace("-", "").replace(",", "").strip().isdigit():
        try:
            parts = query.split(",")
            lat = float(parts[0].strip())
            lon = float(parts[1].strip())
            city_name = f"{lat}, {lon}"
        except (ValueError, IndexError):
            print("\U0000274C  Invalid coordinates. Use format: lat,lon")
            sys.exit(1)
    else:
        # Search city
        try:
            cities = search_city(query)
        except Exception as e:
            print(f"\U0000274C  Search failed: {e}")
            sys.exit(1)
        
        if not cities:
            print(f"\U0000274C  No cities found for '{query}'")
            sys.exit(1)
        
        city = cities[0]
        lat, lon = city["lat"], city["lon"]
        city_name = city["name"]
        print(f"\U0001F4CD  {city_name}")
    
    try:
        data = fetch_weather(lat, lon, args.days)
    except Exception as e:
        print(f"\U0000274C  Failed to fetch weather: {e}")
        sys.exit(1)
    
    show_all = not (args.current or args.forecast or args.astronomy)
    
    if show_all or args.current:
        display_current(data, city_name)
    if show_all or args.forecast:
        display_forecast(data, args.days)
    if show_all or args.astronomy:
        display_astronomy(data)

if __name__ == "__main__":
    main()
