"""Download the pinned MDI font and its upstream license; no credentials required."""
from pathlib import Path
import hashlib
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://raw.githubusercontent.com/Templarian/MaterialDesign-Webfont/v7.4.47/"
FILES = {"fonts/materialdesignicons-webfont.ttf": "materialdesignicons-webfont.ttf", "LICENSE": "LICENSE-MDI.txt"}
EXPECTED_SHA256 = {
    "materialdesignicons-webfont.ttf": "61e8aba5a4e981fe22cf7c8e8bcdbea00476e75c62c37f01bf7ee33361d68428",
    "LICENSE-MDI.txt": "3bae6305bcaa6d10219b999f65c342034c2d40b1c0e8567fa08605e73ccba829",
}


def main():
    target = ROOT / "esphome/fonts"
    target.mkdir(parents=True, exist_ok=True)
    for source, name in FILES.items():
        request = urllib.request.Request(BASE + source, headers={"User-Agent": "esphome-weatherman-fonts"})
        with urllib.request.urlopen(request, timeout=30) as response:
            data = response.read(4 * 1024 * 1024 + 1)
        if len(data) > 4 * 1024 * 1024:
            raise ValueError("Unexpectedly large font resource")
        if name.endswith(".ttf") and data[:4] not in (b"\x00\x01\x00\x00", b"OTTO"):
            raise ValueError("Unexpected font format")
        if hashlib.sha256(data).hexdigest() != EXPECTED_SHA256[name]:
            raise ValueError("Upstream resource checksum did not match the pinned version")
        (target / name).write_bytes(data)
        print(f"{name}: {hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    main()
