# utils/rootfs.py
from pathlib import Path
import os
import stat
import logging
import subprocess

class RootFS:
    def __init__(self, rootfs_dir: Path, hostname="raspberrypi"):
        self.rootfs_dir = Path(rootfs_dir)
        self.hostname = hostname
        logging.info(f"RootFS initialized at {self.rootfs_dir}")

    def create_dirs(self):
        dirs = [
            "bin", "sbin", "usr/bin", "usr/sbin", "usr/lib",
            "usr/local/bin", "usr/local/sbin", "usr/local/lib",
            "lib", "lib64", "etc", "etc/init.d", "var", "var/log",
            "var/tmp", "tmp", "home", "root", "dev", "proc", "sys",
            "run", "mnt", "media", "opt", "srv", "boot"
        ]
        for d in dirs:
            path = self.rootfs_dir / d
            path.mkdir(parents=True, exist_ok=True)
            if d in ["tmp", "var/tmp", "run"]:
                path.chmod(0o1777)
        logging.info(f"RootFS directories created at {self.rootfs_dir}")

    def create_dev_nodes(self):
        dev_dir = self.rootfs_dir / "dev"
        dev_dir.mkdir(parents=True, exist_ok=True)
        nodes = [
            ("null", 1, 3), ("zero", 1, 5), ("console", 5, 1),
            ("tty", 5, 0), ("tty0", 4, 0), ("ptmx", 5, 2),
            ("random", 1, 8), ("urandom", 1, 9)
        ]
        for name, major, minor in nodes:
            node_path = dev_dir / name
            if not node_path.exists():
                os.mknod(node_path, mode=stat.S_IFCHR | 0o666, device=os.makedev(major, minor))
        logging.info(f"Device nodes created at {dev_dir}")

    def setup_etc(self, nameservers=None):
        nameservers = nameservers or ["8.8.8.8", "1.1.1.1"]
        etc_dir = self.rootfs_dir / "etc"
        etc_dir.mkdir(parents=True, exist_ok=True)

        # hostname
        (etc_dir / "hostname").write_text(self.hostname + "\n")

        # hosts
        (etc_dir / "hosts").write_text(
            "127.0.0.1\tlocalhost\n"
            f"127.0.1.1\t{self.hostname}\n"
            "::1\tlocalhost ip6-localhost ip6-loopback\n"
            "ff02::1\tip6-allnodes\n"
            "ff02::2\tip6-allrouters\n"
        )

        # resolv.conf
        (etc_dir / "resolv.conf").write_text("".join(f"nameserver {ns}\n" for ns in nameservers))

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
        logging.info(f"Minimal /etc configuration created at {etc_dir}")

    def copy_qemu(self, qemu_binaries=None):
        qemu_binaries = qemu_binaries or [Path("/usr/bin/qemu-aarch64-static")]
        for qemu in qemu_binaries:
            if not qemu.exists():
                logging.warning(f"QEMU binary {qemu} not found, skipping.")
                continue
            dest = self.rootfs_dir / "usr/bin" / qemu.name
            dest.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(["cp", "-v", str(qemu), str(dest)], check=True)
            logging.info(f"QEMU binary {qemu.name} copied to {dest}")
