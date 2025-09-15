# utils/patch.py
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def apply_config_patches(config_path: Path, disabled=None, enabled=None):
    """
    Bearbeitet eine BusyBox .config Datei.
    
    Args:
        config_path: Path zur .config Datei
        disabled: Liste von Features, die auf "# CONFIG_X is not set" gesetzt werden
        enabled: Liste von Features, die auf "CONFIG_X=y" gesetzt werden
    """
    disabled = disabled or []
    enabled = enabled or []

    config_path = Path(config_path)
    if not config_path.exists():
        raise FileNotFoundError(f".config Datei nicht gefunden: {config_path}")

    # Datei einlesen
    with config_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        stripped = line.strip()

        # Deaktivierungen
        if any(stripped.startswith(opt + "=") or stripped.startswith("# " + opt) for opt in disabled):
            opt = next(opt for opt in disabled if stripped.startswith(opt) or stripped.startswith("# " + opt))
            new_lines.append(f"# {opt} is not set\n")
            continue

        # Aktivierungen
        if any(stripped.startswith(opt + "=") or stripped.startswith("# " + opt) for opt in enabled):
            opt = next(opt for opt in enabled if stripped.startswith(opt) or stripped.startswith("# " + opt))
            new_lines.append(f"{opt}=y\n")
            continue

        new_lines.append(line)

    # Prüfen, ob neue Optionen ergänzt werden müssen
    for opt in disabled:
        if not any(l.startswith(opt) or l.startswith("# " + opt) for l in new_lines):
            new_lines.append(f"# {opt} is not set\n")

    for opt in enabled:
        if not any(l.startswith(opt) or l.startswith("# " + opt) for l in new_lines):
            new_lines.append(f"{opt}=y\n")

    # Datei überschreiben
    with config_path.open("w", encoding="utf-8") as f:
        f.writelines(new_lines)

    logger.info("Patches angewendet auf %s", config_path)
