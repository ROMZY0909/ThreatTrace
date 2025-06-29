from dotenv import load_dotenv
load_dotenv()
from services.scanner_core import scan_ip


# IP à analyser
ip_to_test = "8.8.8.8"  # tu peux changer l'IP ici

# Appel du scanner
result = scan_ip(ip_to_test)

# Résultat IP-API
print("\n🌍 Résultat IP-API :")
for k, v in result["ipapi"].items():
    print(f"    {k}: {v}")

# Résultat AbuseIPDB
print("\n🛡️ Résultat AbuseIPDB :")
for k, v in result["abuseipdb"].items():
    print(f"    {k}: {v}")

# Résultat Shodan
print("\n📡 Résultat Shodan :")
shodan = result["shodan"]

if "error" in shodan:
    print(f"    Erreur Shodan : {shodan['error']}")
else:
    print(f"    IP : {shodan.get('ip')}")
    print(f"    Organisation : {shodan.get('org')}")
    print(f"    OS : {shodan.get('os')}")
    print(f"    Hostnames : {', '.join(shodan.get('hostnames', []))}")
    print(f"    Ports ouverts : {shodan.get('ports')}")

    print("\n    🔎 Services détectés :")
    for service in shodan.get("services", []):
        print(f"      - Port {service['port']}/{service['transport']} : {service['product']}")
