from pathlib import Path

def create_rootfs_dirs(rootfs_dir: Path):
    """
    Erstellt die typischen Verzeichnisse eines Linux RootFS.
    """
    rootfs_dir = Path(rootfs_dir)
    dirs = [
        "bin",
        "sbin",
        "usr/bin",
        "usr/sbin",
        "usr/lib",
        "usr/local/bin",
        "usr/local/sbin",
        "usr/local/lib",
        "lib",
        "lib64",
        "etc",
        "etc/init.d",
        "var",
        "var/log",
        "var/tmp",
        "tmp",
        "home",
        "root",
        "dev",
        "proc",
        "sys",
        "run",
        "mnt",
        "media",
        "opt",
        "srv",
        "boot"
    ]

    for d in dirs:
        path = rootfs_dir / d
        path.mkdir(parents=True, exist_ok=True)
        # Optional: Berechtigungen setzen für tmp / var/tmp
        if d in ["tmp", "var/tmp", "run"]:
            path.chmod(0o1777)  # Sticky bit setzen

    print(f"[*] RootFS-Struktur erstellt unter {rootfs_dir}")
