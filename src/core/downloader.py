import urllib.request, hashlib, logging
from pathlib import Path

def sha256sum(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def download_source(url: str, sha256: str, dest: Path):
    if not dest.exists():
        logging.info(f"Lade {url} herunter …")
        urllib.request.urlretrieve(url, dest)
    else:
        logging.info(f"{dest} existiert, überspringe Download.")

    if sha256 and sha256.lower() != "auto":
        local_hash = sha256sum(dest)
        if local_hash != sha256:
            raise ValueError(f"SHA256 Mismatch: erwartet {sha256}, gefunden {local_hash}")
        logging.info(f"SHA256 korrekt für {dest}")
