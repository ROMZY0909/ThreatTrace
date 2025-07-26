import requests
import os

def get_abuseipdb_report(ip_address):
    try:
        api_key = os.getenv("ABUSEIPDB_API_KEY")
        if not api_key:
            return {"error": "Clé API AbuseIPDB manquante dans .env"}

        url = "https://api.abuseipdb.com/api/v2/check"
        headers = {
            "Key": api_key,
            "Accept": "application/json"
        }
        params = {
            "ipAddress": ip_address,
            "maxAgeInDays": "90"
        }

        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            return {
                "error": f"Erreur AbuseIPDB : statut HTTP {response.status_code} - {response.text}"
            }

    except Exception as e:
        return {"error": f"Erreur AbuseIPDB : {str(e)}"}
