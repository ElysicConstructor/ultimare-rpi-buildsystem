#!/usr/bin/env python3
from pathlib import Path
import subprocess
from utils.paths import ROOTFS_DIR

def copy_qemu_binaries(qemu_binaries=None):
    """
    Kopiert QEMU-Binaries ins RootFS für ARM64 Emulation.
    
    Args:
        qemu_binaries (list[Path] | None): Liste der QEMU-Binaries.
            Standard: ['/usr/bin/qemu-aarch64-static']
    """
    if qemu_binaries is None:
        qemu_binaries = [Path("/usr/bin/qemu-aarch64-static")]

    for qemu in qemu_binaries:
        if not qemu.exists():
            print(f"[!] QEMU Binary {qemu} nicht gefunden, überspringe.")
            continue

        dest = ROOTFS_DIR / "usr/bin" / qemu.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["cp", "-v", str(qemu), str(dest)], check=True)
        print(f"[*] QEMU Binary {qemu.name} kopiert nach {dest}")
