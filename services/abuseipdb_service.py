## === services/abuseipdb_service.py ===
import requests
import os

def get_abuseipdb_data(ip):
    try:
        API_KEY = os.getenv("ABUSEIPDB_API_KEY")
        url = f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}&maxAgeInDays=90"
        headers = {
            "Key": API_KEY,
            "Accept": "application/json"
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            return {"error": "Erreur AbuseIPDB"}
    except Exception as e:
        return {"error": f"Erreur AbuseIPDB: {str(e)}"}


## === services/shodan_service.py ===
import shodan
import os

def get_shodan_data(ip):
    try:
        SHODAN_API_KEY = os.getenv("SHODAN_API_KEY")
        api = shodan.Shodan(SHODAN_API_KEY)
        result = api.host(ip)
        return result
    except shodan.APIError as e:
        return {"error": str(e)}