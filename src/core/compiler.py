import subprocess, os, logging
from pathlib import Path

def configure_build(src_dir: Path, env: dict):
    subprocess.run(["make","defconfig"], cwd=src_dir, env=env, check=True)

def compile_package(src_dir: Path, env: dict, jobs=None, menuconfig=False):
    if menuconfig:
        subprocess.run(["make","menuconfig"], cwd=src_dir, env=env, check=True)
    jobs = jobs or os.cpu_count() or 1
    logging.info(f"Kompiliere mit {jobs} Jobs …")
    subprocess.run(["make", f"-j{jobs}"], cwd=src_dir, env=env, check=True)

def install_package(src_dir: Path, rootfs_dir: Path, env: dict):
    subprocess.run(["make", f"CONFIG_PREFIX={rootfs_dir}", "install"], cwd=src_dir, env=env, check=True)
    logging.info(f"Installation abgeschlossen in {rootfs_dir}")
