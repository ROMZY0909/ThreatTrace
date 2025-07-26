import os
import requests
from dotenv import load_dotenv

load_dotenv()

# ----------- IP-API -----------
def ip_api_lookup(ip):
    try:
        url = f"{os.getenv('IP_API_URL', 'http://ip-api.com/json/')}{ip}"
        response = requests.get(url, timeout=10)
        return response.json()
    except Exception as e:
        return {"error": f"Erreur IP-API: {str(e)}"}

# ----------- AbuseIPDB -----------
def abuseipdb_lookup(ip):
    try:
        headers = {
            "Key": os.getenv("ABUSEIPDB_KEY"),
            "Accept": "application/json"
        }
        params = {
            "ipAddress": ip,
            "maxAgeInDays": "90"
        }
        response = requests.get("https://api.abuseipdb.com/api/v2/check", headers=headers, params=params, timeout=10)
        data = response.json()
        return data.get("data", {})
    except Exception as e:
        return {"error": f"Erreur AbuseIPDB: {str(e)}"}

# ----------- Shodan -----------
def shodan_lookup(ip):
    try:
        api_key = os.getenv("SHODAN_KEY")
        url = f"https://api.shodan.io/shodan/host/{ip}?key={api_key}"
        response = requests.get(url, timeout=10)
        return response.json()
    except Exception as e:
        return {"error": f"Erreur Shodan: {str(e)}"}
