import hashlib
import os
import urllib.request

def sha256sum(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def download_source(url, sha256, dest):
    # Download nur wenn Datei nicht existiert
    if not os.path.exists(dest):
        print(f"[*] Lade {url} herunter …")
        try:
            urllib.request.urlretrieve(url, dest)
        except Exception as e:
            raise RuntimeError(f"Fehler beim Download von {url}: {e}")
    else:
        print(f"[*] {dest} existiert, überspringe Download.")

    # Wenn kein SHA256 angegeben ist → überspringen
    if not sha256 or sha256.lower() == "auto":
        print("[*] Keine SHA256-Prüfung aktiviert.")
        return

    # Hash vergleichen
    local_hash = sha256sum(dest)
    if local_hash != sha256:
        raise ValueError(
            f"SHA256 Mismatch für {dest}\n"
            f"  Erwartet: {sha256}\n"
            f"  Gefunden: {local_hash}"
        )
    else:
        print(f"[✔] SHA256-Check erfolgreich für {dest}")
