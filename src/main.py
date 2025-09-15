#!/usr/bin/env python3
# main.py


from utils.terminal import AnimatedTerminal
from utils.paths import CONF_DIR, BUILD_DIR, ROOTFS_DIR, init_directories
from utils.config import load_config
from utils.rootfs import create_rootfs_dirs

from core.builder import build_package

from pathlib import Path
import time





def welcome():
    cur = AnimatedTerminal(width=50)
    cur.println("Ultimate Firmware-Builder started !!! ::::....::..:.")
    time.sleep(5)  
    cur.stop()     
    
    

if __name__ == "__main__":
    # Verzeichnisse anlegen
    init_directories()

    # BusyBox Config laden
    busybox_cfg = load_config(CONF_DIR / "busybox.json")

    # Pfad zu Patches
    busybox_patches = Path(__file__).parent.parent / "patches" / "busybox"

    # Build starten
    build_package(busybox_cfg, BUILD_DIR, ROOTFS_DIR, patches_dir=busybox_patches)
