import shodan
import os

def get_shodan_data(ip_address):
    try:
        api_key = os.getenv("SHODAN_API_KEY")
        if not api_key:
            return {"error": "Clé API Shodan manquante dans .env"}

        api = shodan.Shodan(api_key)
        result = api.host(ip_address)

        # Résumé nettoyé
        cleaned = {
            "IP": result.get("ip_str", "N/A"),
            "Organisation": result.get("org", "N/A"),
            "Pays": result.get("country_name", "N/A"),
            "Ville": result.get("city", "N/A"),
            "Fournisseur": result.get("isp", "N/A"),
            "Ports ouverts": ", ".join(str(p) for p in result.get("ports", [])) or "Aucun",
            "Hostnames": ", ".join(result.get("hostnames", [])) or "Aucun",
            "Dernière mise à jour": result.get("last_update", "N/A"),
            "Bannière détectée": None  # à définir plus bas
        }

        # Extraire une bannière lisible depuis le 1er service scanné
        for service in result.get("data", []):
            if "data" in service:
                banner = service["data"].strip()
                if banner and len(banner) < 500:  # éviter les blobs immenses
                    cleaned["Bannière détectée"] = banner
                    break

        if not cleaned["Bannière détectée"]:
            cleaned["Bannière détectée"] = "Aucune bannière lisible détectée."

        return cleaned

    except shodan.APIError as e:
        return {"error": f"Erreur Shodan API : {str(e)}"}
    except Exception as e:
        return {"error": f"Erreur Shodan : {str(e)}"}