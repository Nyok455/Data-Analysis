import requests
from colorama import init, Fore, Style

init(autoreset=True)


def get_public_ip():
    r = requests.get('https://api.ipify.org?format=json', timeout=10)
    return r.json().get('ip')


def geolocate_ip(ip):
    r = requests.get(f'https://ipapi.co/{ip}/json', timeout=10)
    j = r.json()

    return {
        "city": j.get("city") or "",
        "region": j.get("region") or "",
        "country": j.get("country_name") or "",
        "lat": j.get("latitude"),
        "lon": j.get("longitude"),
    }


def fet_weather_ascii(lat, lon, units="u"):
    url = f"https://wttr.in/{lat},{lon}?{units}"
    r = requests.get(url, timeout=15)
    return r.text


def main():
    ip = get_public_ip()
    print(Fore.GREEN + f"Your public IP: {ip}")
    loc = geolocate_ip(ip)
    print(Fore.YELLOW +
          f"Location: {loc['city']}, {loc['region']}, {loc['country']}")
    print(fet_weather_ascii(loc['lat'], loc['lon']))


if __name__ == "__main__":
    main()
