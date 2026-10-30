#!/usr/bin/env python3
"""Inline data/master.json into index.html so the page also works offline / as a single file.

Usage:  python3 build.py            -> rewrites index.html in place
        python3 build.py out.html   -> writes a standalone copy
"""
import json, re, sys, pathlib

root = pathlib.Path(__file__).parent
html = (root / "index.html").read_text(encoding="utf-8")
data = json.loads((root / "data" / "master.json").read_text(encoding="utf-8"))
payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
html = re.sub(r'(<script type="application/json" id="inline-data">)(.*?)(</script>)',
              lambda m: m.group(1) + payload + m.group(3), html, count=1, flags=re.S)
out = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else root / "index.html"
out.write_text(html, encoding="utf-8")
print(f"wrote {out}")
