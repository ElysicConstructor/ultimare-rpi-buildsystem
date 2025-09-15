# core/patcher.py
from pathlib import Path
import subprocess
import logging
from utils.patch import apply_config_patches

logger = logging.getLogger(__name__)

class Patcher:
    """
    Klasse zum automatischen Anwenden von Patches auf ein Quellverzeichnis.
    Unterstützt:
        - JSON-basierte Config-Änderungen
        - klassische .patch Dateien
    """

    def __init__(self, src_dir: Path, config=None, patches_dir: Path = None):
        self.src_dir = Path(src_dir)
        self.config = config or {}
        self.patches_dir = Path(patches_dir) if patches_dir else None

    def apply(self):
        # 1. Config Patches anwenden
        config_path = self.src_dir / ".config"
        if self.config:
            logger.info("Wende JSON-basierte Config-Patches an …")
            apply_config_patches(
                config_path,
                disabled=self.config.get("disabled_features", []),
                enabled=self.config.get("enabled_features", [])
            )

        # 2. Externe Patch-Dateien
        if self.patches_dir and self.patches_dir.exists():
            for patch_file in sorted(self.patches_dir.glob("*.patch")):
                logger.info("Wende Patch %s an …", patch_file.name)
                subprocess.run(
                    ["patch", "-p1", "-i", str(patch_file)],
                    cwd=self.src_dir,
                    check=True
                )

        logger.info("Alle Patches angewendet auf %s", self.src_dir)
