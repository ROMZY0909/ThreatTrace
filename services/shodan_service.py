import os
import requests

def get_shodan_data(ip):
    api_key = os.getenv("SHODAN_API_KEY")
    if not api_key:
        return {"error": "Clé API Shodan absente dans .env"}

    url = f"https://api.shodan.io/shodan/host/{ip}?key={api_key}"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            raw = response.json()

            return {
                "ip": raw.get("ip_str"),
                "hostnames": raw.get("hostnames", []),
                "org": raw.get("org", "Inconnu"),
                "os": raw.get("os", "Non détecté"),
                "ports": raw.get("ports", []),
                "services": [
                    {
                        "port": service.get("port"),
                        "transport": service.get("transport", "tcp"),
                        "product": service.get("product", "Non identifié"),
                        "banner": (service.get("data") or "")[:300].replace("\n", " ")
                    }
                    for service in raw.get("data", [])
                ]
            }

        elif response.status_code == 404:
            return {"error": "Aucune donnée trouvée pour cette IP."}
        elif response.status_code == 403:
            return {"error": "Accès refusé – vérifie ta clé ou ton quota Shodan."}
        else:
            return {"error": f"Erreur Shodan {response.status_code}: {response.text}"}

    except requests.exceptions.RequestException as e:
        return {"error": f"Erreur de requête Shodan : {str(e)}"}
