from pathlib import Path

def setup_minimal_etc(rootfs_dir: Path, hostname="raspberrypi"):
    etc_dir = rootfs_dir / "etc"
    etc_dir.mkdir(parents=True, exist_ok=True)

    # hostname
    (etc_dir / "hostname").write_text(hostname + "\n")
    
    # hosts
    (etc_dir / "hosts").write_text(
        "127.0.0.1\tlocalhost\n"
        f"127.0.1.1\t{hostname}\n"
        "::1\tlocalhost ip6-localhost ip6-loopback\n"
        "ff02::1\tip6-allnodes\n"
        "ff02::2\tip6-allrouters\n"
    )

    # resolv.conf
    (etc_dir / "resolv.conf").write_text("nameserver 8.8.8.8\nnameserver 1.1.1.1\n")

    # rcS init script
    initd_dir = etc_dir / "init.d"
    initd_dir.mkdir(parents=True, exist_ok=True)
    rcS_file = initd_dir / "rcS"
    rcS_file.write_text(
        "#!/bin/sh\n"
        "mount -t proc proc /proc\n"
        "mount -t sysfs sys /sys\n"
        "mount -t devtmpfs devtmpfs /dev\n"
        "echo 'Welcome to Minimal ARM64 Linux'\n"
    )
    rcS_file.chmod(0o755)
    print(f"[*] Minimale /etc Konfiguration erstellt unter {etc_dir}")
