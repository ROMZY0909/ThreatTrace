# services/log_service.py

import os
from datetime import datetime

def save_full_log(email, user_ip, scanned_ip, ipapi_data, abuseipdb_data, shodan_data):
    """
    Enregistre un log complet de l'analyse IP dans un fichier texte horodaté.

    Paramètres :
    - email (str) : adresse email de l'utilisateur (peut être vide)
    - user_ip (str) : adresse IP réelle de l'utilisateur (request.remote_addr)
    - scanned_ip (str) : adresse IP entrée et scannée
    - ipapi_data (dict) : résultat de l'API ip-api
    - abuseipdb_data (dict) : résultat de l'API AbuseIPDB
    - shodan_data (dict) : résultat de l'API Shodan
    """

    # Crée le dossier "logs" s'il n'existe pas
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # Nom du fichier : log_YYYYMMDD_HHMMSS.txt
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"log_{timestamp}.txt"
    filepath = os.path.join(log_dir, filename)

    # Construction du contenu du log
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("=== THREATTRACE AI – Rapport d'analyse IP ===\n")
        f.write(f"📅 Date        : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"🧑‍💻 IP Utilisateur : {user_ip}\n")
        f.write(f"🔍 IP Scannée   : {scanned_ip}\n")
        f.write(f"📧 Email        : {email or 'Non fourni'}\n")
        f.write("\n--- Résultats IP-API ---\n")
        f.write(str(ipapi_data) + "\n")
        f.write("\n--- Résultats AbuseIPDB ---\n")
        f.write(str(abuseipdb_data) + "\n")
        f.write("\n--- Résultats Shodan ---\n")
        f.write(str(shodan_data) + "\n")

    print(f"[✔] Log enregistré : {filepath}")
