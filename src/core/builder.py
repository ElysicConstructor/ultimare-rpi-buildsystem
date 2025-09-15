import subprocess
import os
from pathlib import Path
from utils.download import download_source
from utils.patch import apply_config_patches

def build_package(config, build_dir: Path, rootfs_dir: Path, patches_dir: Path = None):
    """
    Baut ein Paket (z.B. BusyBox) für ARM64 Cross-Compile.

    config: dict mit URL, SHA256, Features etc.
    build_dir: Path zum Build-Ordner
    rootfs_dir: Path zum RootFS-Ordner
    patches_dir: Optional Path zu Patch-Dateien
    """
    url = config["url"]
    sha256 = config["sha256"]
    name = f"{config['name']}-{config['version']}"
    archive = build_dir / Path(url).name
    src_dir = build_dir / name

    # 1. Download
    download_source(url, sha256, archive)

    # 2. Entpacken
    if not src_dir.exists():
        print(f"[*] Entpacke {archive} nach {build_dir} …")
        subprocess.run(["tar", "xf", str(archive), "-C", str(build_dir)], check=True)

    # 3. Konfigurieren & Patches anwenden
    cc_prefix = config["config"].get("cross_compile", "")
    env = os.environ.copy()
    if cc_prefix:
        env["CROSS_COMPILE"] = cc_prefix
    env["ARCH"] = "arm64"

    # Default Config
    subprocess.run(["make", "defconfig"], cwd=src_dir, env=env, check=True)

    # Config-Patches aus JSON
    config_path = src_dir / ".config"
    apply_config_patches(
        config_path,
        disabled=config.get("disabled_features", []),
        enabled=config.get("enabled_features", [])
    )

    # Externe Patchfiles einspielen (optional)
    if patches_dir and patches_dir.exists():
        for patch_file in sorted(patches_dir.glob("*.patch")):
            print(f"[*] Wende Patch {patch_file.name} an …")
            subprocess.run(
                ["patch", "-p1", "-i", str(patch_file)],
                cwd=src_dir,
                check=True
            )

    # Menuconfig falls statisch gebaut werden soll
    if config["config"].get("static", False):
        print("[*] Öffne make menuconfig …")
        subprocess.run(["make", "menuconfig"], cwd=src_dir, env=env, check=True)

    # 4. Kompilieren
    jobs = os.cpu_count() or 1
    print(f"[*] Kompiliere {name} mit {jobs} Jobs …")
    subprocess.run(["make", f"-j{jobs}"], cwd=src_dir, env=env, check=True)

    # 5. Installation ins RootFS
    subprocess.run(
        ["make", f"CONFIG_PREFIX={rootfs_dir}", "install"],
        cwd=src_dir,
        env=env,
        check=True,
    )

    print(f"[✔] {config['name']} installiert in {rootfs_dir}")
