# utils/paths.py
from pathlib import Path

# Projektbasis ermitteln (relativ zu src/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Standardverzeichnisse
CONF_DIR = BASE_DIR / "conf"
BUILD_DIR = BASE_DIR / "build"
OUTPUT_DIR = BASE_DIR / "output"
ROOTFS_DIR = OUTPUT_DIR / "rootfs"
BOOTFS_DIR = OUTPUT_DIR / "bootfs"

def init_directories():
    """Erstellt alle Standardverzeichnisse, falls sie fehlen."""
    for d in [BUILD_DIR, ROOTFS_DIR, BOOTFS_DIR]:
        d.mkdir(parents=True, exist_ok=True)
