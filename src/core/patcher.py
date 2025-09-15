from pathlib import Path
from utils.patch import apply_config_patches
import subprocess, logging

def apply_patches(src_dir: Path, config_options: dict, patches_dir: Path = None):
    config_path = src_dir / ".config"
    apply_config_patches(
        config_path,
        disabled=config_options.get("disabled_features", []),
        enabled=config_options.get("enabled_features", [])
    )
    if patches_dir and patches_dir.exists():
        for patch_file in sorted(patches_dir.glob("*.patch")):
            logging.info(f"Wende Patch {patch_file.name} an …")
            subprocess.run(["patch","-p1","-i",str(patch_file)], cwd=src_dir, check=True)
