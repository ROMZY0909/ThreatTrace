## === services/log_service.py ===
def save_full_log(email, user_ip, scanned_ip, ipapi_data, abuseipdb_data, shodan_data):
    from datetime import datetime
    import os

    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"logs/log_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Date: {timestamp}\n")
        f.write(f"Email: {email}\n")
        f.write(f"User IP: {user_ip}\n")
        f.write(f"Scanned IP: {scanned_ip}\n\n")
        f.write("[IP-API]\n")
        f.write(str(ipapi_data) + "\n\n")
        f.write("[AbuseIPDB]\n")
        f.write(str(abuseipdb_data) + "\n\n")
        f.write("[Shodan]\n")
        f.write(str(shodan_data) + "\n")