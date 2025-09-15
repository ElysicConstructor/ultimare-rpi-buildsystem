# core/builder.py
import os
import subprocess
import logging
from pathlib import Path

from core.downloader import download_source
from core.patcher import apply_config_patches  # angepasst auf core/patcher.py

def build_package(config: dict, build_dir: Path, rootfs_dir: Path, patches_dir: Path = None):
    """
    Baut ein Paket (z.B. BusyBox) für ARM64 Cross-Compile.

    Args:
        config: Dict mit URL, SHA256, Features etc.
        build_dir: Path zum Build-Ordner
        rootfs_dir: Path zum RootFS-Ordner
        patches_dir: Optional Path zu Patch-Dateien
    """
    url = config.get("url")
    sha256 = config.get("sha256", "auto")
    name = f"{config.get('name')}-{config.get('version')}"
    archive = build_dir / Path(url).name
    src_dir = build_dir / name

    logging.info(f"=== Build starten: {name} ===")

    # 1. Download
    try:
        download_source(url, sha256, archive)
    except Exception as e:
        logging.error(f"Download fehlgeschlagen: {e}")
        return

    # 2. Entpacken
    if not src_dir.exists():
        logging.info(f"Entpacke {archive} nach {build_dir} …")
        subprocess.run(["tar", "xf", str(archive), "-C", str(build_dir)], check=True)

    # 3. Environment für Cross-Compile
    env = os.environ.copy()
    cc_prefix = config.get("config", {}).get("cross_compile", "")
    if cc_prefix:
        env["CROSS_COMPILE"] = cc_prefix
    env["ARCH"] = "arm64"

    # Default Config
    logging.info("Setze Default-Konfiguration …")
    subprocess.run(["make", "defconfig"], cwd=src_dir, env=env, check=True)

    # JSON-basierte Config-Patches
    config_path = src_dir / ".config"
    apply_config_patches(
        config_path,
        disabled=config.get("disabled_features", []),
        enabled=config.get("enabled_features", [])
    )

    # Optionale externe Patch-Dateien
    if patches_dir and patches_dir.exists():
        for patch_file in sorted(patches_dir.glob("*.patch")):
            logging.info(f"Wende Patch {patch_file.name} an …")
            subprocess.run(["patch", "-p1", "-i", str(patch_file)], cwd=src_dir, check=True)

    # Menuconfig falls statisch
    if config.get("config", {}).get("static", False):
        logging.info("Starte make menuconfig …")
        subprocess.run(["make", "menuconfig"], cwd=src_dir, env=env, check=True)

    # 4. Kompilieren
    jobs = os.cpu_count() or 1
    logging.info(f"Kompiliere {name} mit {jobs} Jobs …")
    subprocess.run(["make", f"-j{jobs}"], cwd=src_dir, env=env, check=True)

    # 5. Installation ins RootFS
    logging.info(f"Installiere {name} nach {rootfs_dir} …")
    subprocess.run(["make", f"CONFIG_PREFIX={rootfs_dir}", "install"], cwd=src_dir, env=env, check=True)

    logging.info(f"=== Build abgeschlossen: {name} ===\n")
