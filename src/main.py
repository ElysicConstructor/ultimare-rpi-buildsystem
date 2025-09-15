#!/usr/bin/env python3
# main.py

import time
import logging
from pathlib import Path
from utils.terminal import AnimatedTerminal

from utils.paths import init_directories, BUILD_DIR, ROOTFS_DIR
from utils.configurator import load_config
from utils.rootfs import RootFS
from core.builder import build_package

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def welcome(show=True, width=50, duration=2):
    """Optionales animiertes Willkommen"""
    if not show:
        return
    cur = AnimatedTerminal(width=width)
    cur.println("Ultimate Firmware-Builder gestartet !!!")
    time.sleep(duration)
    cur.stop()


def main():
    # Willkommen
    welcome(show=True)

    # Standardverzeichnisse anlegen
    init_directories()

    # RootFS vorbereiten
    rootfs = RootFS(ROOTFS_DIR, hostname="rpi5")
    rootfs.create_dirs()
    rootfs.create_dev_nodes()
    rootfs.setup_etc(nameservers=["8.8.8.8", "1.1.1.1"])
    rootfs.copy_qemu()

    # BusyBox Config laden
    config_path = Path(__file__).parent / "conf/busybox.json"
    busybox_cfg = load_config(config_path)

    # Pfad zu Patches
    patches_dir = Path(__file__).parent.parent / "patches/busybox"

    # Build starten mit Fehlerbehandlung
    try:
        build_package(busybox_cfg, BUILD_DIR, ROOTFS_DIR, patches_dir)
    except Exception as e:
        logging.error(f"Build fehlgeschlagen: {e}")
        return

    logging.info("Build erfolgreich abgeschlossen!")


if __name__ == "__main__":
    main()
