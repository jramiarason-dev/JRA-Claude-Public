#!/usr/bin/env python3
"""Assemble Mirage City : src/template.html + src/js/*.js (dans l'ordre) -> index.html.

Usage :
  python build.py          # régénère index.html
  python build.py --check  # échoue si index.html n'est pas à jour (utilisé par la CI)
"""
import sys
from pathlib import Path

ROOT = Path(__file__).parent
MARK = "/*@@SCRIPT@@*/"


def assemble() -> str:
    template = (ROOT / "src" / "template.html").read_text(encoding="utf-8")
    parts = sorted((ROOT / "src" / "js").glob("*.js"))
    if not parts:
        sys.exit("Aucun module trouvé dans src/js")
    script = "\n\n".join(p.read_text(encoding="utf-8").rstrip("\n") for p in parts)
    if template.count(MARK) != 1:
        sys.exit("Le gabarit doit contenir exactement un marqueur " + MARK)
    return template.replace(MARK, script)


def main() -> None:
    out = assemble()
    target = ROOT / "index.html"
    if "--check" in sys.argv:
        current = target.read_text(encoding="utf-8") if target.exists() else ""
        if current != out:
            sys.exit("index.html n'est pas à jour : lancez `python mirage_city/build.py`.")
        print("index.html est à jour.")
        return
    target.write_text(out, encoding="utf-8")
    print(f"index.html généré ({len(out.splitlines())} lignes).")


if __name__ == "__main__":
    main()
