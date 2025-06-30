# services/ipapi_service.py

import requests

def scan_ip(ip):
    try:
        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            raw = response.json()
            if raw["status"] == "fail":
                return {"error": f"Erreur API ip-api : {raw.get('message', 'inconnue')}"}

            data = {
                "ip": ip,
                "country": raw.get("country"),
                "region": raw.get("regionName"),
                "city": raw.get("city"),
                "lat": raw.get("lat"),
                "lon": raw.get("lon"),
                "org": raw.get("org"),
                "timezone": raw.get("timezone"),
                "isp": raw.get("isp")
            }

            if data["lat"] is not None and data["lon"] is not None:
                lat = str(data["lat"]).strip()
                lon = str(data["lon"]).strip()
                data["google_maps_link"] = f"https://www.google.com/maps?q={lat},{lon}"
            else:
                data["google_maps_link"] = None

            return data
        else:
            return {"error": "Erreur HTTP ip-api"}
    except Exception as e:
        return {"error": f"Erreur ip-api: {str(e)}"}
