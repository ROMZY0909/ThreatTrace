# services/log_service.py

import os
from datetime import datetime

def save_full_log(email, ip, result):
    """
    Enregistre dans un fichier texte l'adresse email, l'IP analysée
    et le résultat complet de l'analyse (AbuseIPDB, IP-API, Shodan, etc.)
    """
    # Créer le dossier logs/ s'il n'existe pas
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # Générer le nom du fichier avec la date et l'heure
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"log_{timestamp}.txt"
    log_path = os.path.join(log_dir, log_filename)

    # Écrire les informations dans le fichier
    with open(log_path, "w", encoding="utf-8") as log_file:
        log_file.write(f"Email utilisateur : {email}\n")
        log_file.write(f"Adresse IP analysée : {ip}\n\n")
        log_file.write("Résultat de l'analyse :\n")
        log_file.write("-" * 40 + "\n")
        log_file.write(str(result))  # Conversion en texte si dict

    print(f"[+] Log enregistré : {log_path}")
