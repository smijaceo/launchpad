"""Brand checks: WCAG 2.x contrast for palette.json."""

from __future__ import annotations

import json
from pathlib import Path


def _lin(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_: str) -> float:
    h = hex_.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast(a: str, b: str) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def check_palette(path: Path) -> tuple[list[str], list[str]]:
    """Return (report lines, failures) for every mode × pair in palette.json."""
    pal = json.loads(Path(path).read_text())
    lines, fails = [], []
    for mode in ("light", "dark"):
        for fg, bg, need in pal["pairs"]:
            r = contrast(pal[mode][fg], pal[mode][bg])
            ok = r >= need
            lines.append(f"{mode:5} {fg:>12} on {bg:<8} {r:5.2f} (need {need}) {'ok' if ok else 'FAIL'}")
            if not ok:
                fails.append(f"{mode}: {fg} on {bg} = {r:.2f} < {need}")
    return lines, fails
