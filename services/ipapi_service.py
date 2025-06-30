# services/ipapi_service.py

import requests

def scan_ip(ip):
    try:
        url = f"http://ip-api.com/json/{ip}"
        headers = {"User-Agent": "ThreatTraceAI/1.0"}
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code == 200:
            raw = response.json()

            if raw.get("status") == "fail":
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

            # Lien Google Maps
            if data["lat"] is not None and data["lon"] is not None:
                data["google_maps_link"] = f"https://www.google.com/maps?q={data['lat']},{data['lon']}"
            else:
                data["google_maps_link"] = None

            return data

        else:
            return {"error": f"Erreur HTTP ip-api : {response.status_code}"}

    except Exception as e:
        return {"error": f"Erreur ip-api: {str(e)}"}
