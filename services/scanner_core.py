from services.ipapi_service import get_ipapi_data
from services.abuseipdb_service import get_abuseipdb_data
from services.shodan_service import get_shodan_data

def scan_ip(ip):
    result = {}

    # 🌍 Données de ip-api.com
    try:
        ipapi_data = get_ipapi_data(ip)
        result["ipapi"] = ipapi_data
    except Exception as e:
        result["ipapi"] = {"error": f"Erreur ip-api: {str(e)}"}

    # 🛡️ Données d'AbuseIPDB
    try:
        abuse_data = get_abuseipdb_data(ip)
        result["abuseipdb"] = abuse_data
    except Exception as e:
        result["abuseipdb"] = {"error": f"Erreur AbuseIPDB: {str(e)}"}

    # 📡 Données de Shodan
    try:
        shodan_data = get_shodan_data(ip)
        result["shodan"] = shodan_data
    except Exception as e:
        result["shodan"] = {"error": f"Erreur Shodan: {str(e)}"}

    return result
