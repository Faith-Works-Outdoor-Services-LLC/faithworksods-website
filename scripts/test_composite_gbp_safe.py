"""GBP-safe composite CLI emits a 4:3 JPEG without failing on --gbp-safe."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build-before-process-after-composite.py"


def test_gbp_safe_flag_writes_gbp_jpeg(tmp_path: Path) -> None:
    folder = tmp_path / "shots"
    folder.mkdir()
    Image.new("RGB", (800, 600), (20, 80, 20)).save(folder / "before-01.jpg", "JPEG")
    Image.new("RGB", (800, 600), (40, 120, 40)).save(folder / "process-01.jpg", "JPEG")
    Image.new("RGB", (800, 600), (80, 160, 80)).save(folder / "after-01.jpg", "JPEG")
    out = tmp_path / "out"
    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            str(folder),
            "--title",
            "Land Clearing Job",
            "--basename",
            "before-process-after-land-clearing-test",
            "--out",
            str(out),
            "--also-jpeg",
            "--gbp-safe",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    gbp = Path(payload["gbp_jpg"])
    assert gbp.is_file()
    with Image.open(gbp) as im:
        assert im.size == (1600, 1200)


if __name__ == "__main__":
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        test_gbp_safe_flag_writes_gbp_jpeg(Path(tmp))
    print("test_composite_gbp_safe: OK")
