#!/usr/bin/env python3
"""WCAG contrast ratios for the colour tokens in assets/css/styles.css (light and dark). AA needs 4.5:1 for text, 3:1 for UI components."""
import re, sys
from pathlib import Path
css = (Path(__file__).resolve().parent.parent / "assets/css/styles.css").read_text()
def lum(h):
    h = h.lstrip("#"); r, g, b = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b)
def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + .05) / (lb + .05)
def tokens(block):
    full = lambda h: "#" + "".join(c * 2 for c in h[1:]) if len(h) == 4 else h
    return {k: full(v) for k, v in re.findall(r"--([\w-]+):(#[0-9a-fA-F]{3,6})\b", block)}
light = tokens(re.search(r":root\{[^}]*\}", css).group(0))
dark = tokens(re.search(r"prefers-color-scheme:dark\)\{:root\{([^}]*)\}", css).group(1))
dark = {**light, **dark}
pairs = [("tx","bg","body text",4.5),("tx","sf","text on card",4.5),("mu","bg","muted text",4.5),("mu","sf","muted text on card",4.5),("pri","bg","link / heading",4.5),("pri","sf","link on card",4.5),("pri","tint","link on tint",4.5),("tx","tint","text on tint",4.5),("ok","bg","verified text",4.5),("warn","bg","warning text",4.5),("acc","bg","accent border (UI)",3.0),("ctl","bg","form control border (UI)",3.0),("ctl","sf","form control border on card (UI)",3.0),("bd","bg","border (decorative)",0)]
bad = 0
for name, t in (("light", light), ("dark", dark)):
    print(name)
    for fg, bg, label, need in pairs:
        r = ratio(t[fg], t[bg]); ok = r >= need; bad += (not ok and need > 0)
        print(f"  {'PASS' if ok or need == 0 else 'FAIL'} {r:5.2f}:1  {label} ({fg} on {bg}, needs {need or 'n/a'})")
# buttons / hero (white or dark text on a fill)
for name, t, btn_txt in (("light", light, "#ffffff"), ("dark", dark, "#06122a")):
    for fill, label in (("pri", "button"),):
        r = ratio(btn_txt, t[fill]); ok = r >= 4.5; bad += (not ok); print(f"  {'PASS' if ok else 'FAIL'} {r:5.2f}:1  {name} {label} text on {fill}")
print("white text on hero (light #004494):", f"{ratio('#ffffff', '#004494'):.2f}:1", "| tag #9bdcff on #004494:", f"{ratio('#9bdcff', '#004494'):.2f}:1", "| mark #000 on #ffe08a:", f"{ratio('#000000', '#ffe08a'):.2f}:1")
sys.exit(1 if bad else 0)
