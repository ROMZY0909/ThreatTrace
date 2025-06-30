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