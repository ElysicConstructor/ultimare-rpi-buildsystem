import json
from pathlib import Path

def load_config(path: Path):
    """Lädt eine JSON-Konfigurationsdatei und gibt sie als dict zurück."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Config-Datei nicht gefunden: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
