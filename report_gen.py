from services.abuseipdb_service import get_abuseipdb_report
from services.shodan_service import get_shodan_data
from services.ipapi_service import get_ipapi_data
# from services.openai_summary import generate_summary_text  # Prévu pour usage IA

def generate_summary(ip):
    result = {}

    # IP-API
    try:
        result['ipapi'] = get_ipapi_data(ip)
    except Exception as e:
        result['ipapi'] = {'error': f'Erreur IP-API : {str(e)}'}

    # AbuseIPDB
    try:
        result['abuseipdb'] = get_abuseipdb_report(ip)
    except Exception as e:
        result['abuseipdb'] = {'error': f'Erreur AbuseIPDB : {str(e)}'}

    # Shodan
    try:
        result['shodan'] = get_shodan_data(ip)
    except Exception as e:
        result['shodan'] = {'error': f'Erreur Shodan : {str(e)}'}

    # Résumé IA ou par défaut
    try:
        # result['summary'] = generate_summary_text(ip, result)  # si IA activée
        result['summary'] = f"Analyse complète de l’adresse IP {ip} terminée avec succès."
    except Exception as e:
        result['summary'] = f"Erreur lors de la génération du résumé : {str(e)}"

    return result
