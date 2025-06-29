import requests
import os

def get_abuseipdb_data(ip):
    api_key = os.getenv("ABUSEIPDB_API_KEY")
    if not api_key:
        return {"error": "Clé API AbuseIPDB non définie."}

    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {
        "Key": api_key,
        "Accept": "application/json"
    }
    params = {
        "ipAddress": ip,
        "maxAgeInDays": "90"
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json().get("data", {})
            return {
                "ip": data.get("ipAddress"),
                "isWhitelisted": data.get("isWhitelisted"),
                "abuseConfidenceScore": data.get("abuseConfidenceScore"),
                "countryCode": data.get("countryCode"),
                "usageType": data.get("usageType"),
                "domain": data.get("domain"),
                "totalReports": data.get("totalReports"),
                "lastReportedAt": data.get("lastReportedAt")
            }
        else:
            return {"error": f"Erreur API AbuseIPDB : {response.status_code}"}
    except Exception as e:
        return {"error": f"Exception AbuseIPDB : {str(e)}"}
