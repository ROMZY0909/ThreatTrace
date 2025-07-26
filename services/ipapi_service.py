import requests

def get_ipapi_data(ip_address):
    try:
        url = f"http://ip-api.com/json/{ip_address}"
        response = requests.get(url, timeout=5)

        if response.status_code != 200:
            return {"error": f"Erreur HTTP ip-api : statut {response.status_code}"}

        raw = response.json()

        if raw.get("status") == "fail":
            return {"error": f"Erreur API ip-api : {raw.get('message', 'inconnue')}"}

        data = {
            "ip": ip_address,
            "country": raw.get("country", "N/A"),
            "region": raw.get("regionName", "N/A"),
            "city": raw.get("city", "N/A"),
            "lat": raw.get("lat"),
            "lon": raw.get("lon"),
            "org": raw.get("org", "N/A"),
            "timezone": raw.get("timezone", "N/A"),
            "isp": raw.get("isp", "N/A")
        }

        # Ajout lien Google Maps si latitude/longitude disponibles
        if data["lat"] and data["lon"]:
            data["google_maps_link"] = f"https://www.google.com/maps?q={data['lat']},{data['lon']}"
        else:
            data["google_maps_link"] = "Indisponible"

        return data

    except Exception as e:
        return {"error": f"Erreur ip-api : {str(e)}"}
