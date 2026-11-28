"""Render the project memory as accessible HTML and a print-ready PDF."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import markdown


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "memoria.md"
HTML_OUTPUT = ROOT / "docs" / "memoria.html"
PDF_OUTPUT = ROOT / "docs" / "memoria.pdf"
EDGE_CANDIDATES = (
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
)


def build_html(source: str, institution: str) -> str:
    body = markdown.markdown(
        source,
        extensions=("tables", "fenced_code", "toc", "sane_lists"),
        output_format="html5",
    )
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Memoria del proyecto Sak P'o' Kaab</title>
  <style>
    @page {{ size: A4; margin: 18mm 17mm 20mm; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; color: #23362c; font: 10.5pt/1.55 Arial, sans-serif; }}
    .cover {{ min-height: 255mm; display: flex; flex-direction: column; justify-content: center; text-align: center; page-break-after: always; }}
    .cover .mark {{ width: 38mm; height: 38mm; margin: 0 auto 14mm; }}
    .cover .institution {{ color: #53685a; font-size: 12pt; font-weight: 700; text-transform: uppercase; letter-spacing: .12em; }}
    .cover h1 {{ margin: 14mm auto 5mm; max-width: 160mm; color: #193b2d; font: 600 31pt/1.15 Georgia, serif; }}
    .cover .subtitle {{ color: #7d5526; font-size: 14pt; }}
    .cover .metadata {{ margin: 22mm auto 0; width: 135mm; border-top: 1px solid #d9d0bd; padding-top: 8mm; text-align: left; }}
    .cover .metadata p {{ margin: 3mm 0; }}
    main h1 {{ color: #193b2d; font: 600 25pt/1.2 Georgia, serif; }}
    h2 {{ margin: 11mm 0 4mm; color: #193b2d; font: 600 17pt/1.25 Georgia, serif; page-break-after: avoid; }}
    h3 {{ margin: 7mm 0 3mm; color: #28513c; font-size: 12pt; page-break-after: avoid; }}
    p, li {{ orphans: 3; widows: 3; }}
    table {{ width: 100%; border-collapse: collapse; margin: 5mm 0; font-size: 9pt; }}
    th, td {{ border: 1px solid #d6d2c7; padding: 2.2mm; vertical-align: top; }}
    th {{ background: #193b2d; color: #fff8e7; text-align: left; }}
    tr {{ page-break-inside: avoid; }}
    code {{ color: #254b37; font-family: Consolas, monospace; font-size: .9em; }}
    pre {{ white-space: pre-wrap; overflow-wrap: anywhere; border: 1px solid #ded8ca; background: #f5f1e8; padding: 4mm; font-size: 8pt; page-break-inside: avoid; }}
    blockquote {{ border-left: 3px solid #d3ac5f; margin: 5mm 0; padding: 2mm 5mm; color: #58665d; }}
    a {{ color: #315b43; overflow-wrap: anywhere; }}
    img {{ max-width: 100%; }}
    @media print {{ body {{ -webkit-print-color-adjust: exact; print-color-adjust: exact; }} }}
  </style>
</head>
<body>
  <section class="cover" aria-label="Portada">
    <svg class="mark" viewBox="0 0 64 64" aria-hidden="true">
      <path d="M32 6 53 18v24L32 54 11 42V18L32 6Z" fill="none" stroke="#193b2d" stroke-width="2"/>
      <path d="M32 20c-6 7-9 12-9 17a9 9 0 0 0 18 0c0-5-3-10-9-17Z" fill="#193b2d"/>
    </svg>
    <p class="institution">{institution}</p>
    <h1>Memoria del proyecto integrador</h1>
    <p class="subtitle">Sak P'o' Kaab · Tienda y experiencia multimedia</p>
    <div class="metadata">
      <p><strong>Alumno:</strong> Joshua Israel Cabrera Camacho</p>
      <p><strong>Matrícula:</strong> 202300074</p>
      <p><strong>Programa:</strong> Ingeniería en Software · Plan 2018</p>
      <p><strong>Materia:</strong> Multimedia y Diseño Digital</p>
      <p><strong>Entrega:</strong> 26–27 de noviembre de 2026</p>
    </div>
  </section>
  <main>{body}</main>
</body>
</html>
"""


def find_edge() -> Path:
    configured = os.environ.get("EDGE_PATH")
    candidates = (Path(configured),) if configured else EDGE_CANDIDATES
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise FileNotFoundError("No se encontró Microsoft Edge. Define EDGE_PATH al regenerar el PDF.")


def main() -> None:
    source_text = SOURCE.read_text(encoding="utf-8")
    institution = os.environ.get("INSTITUTION_NAME", "Universidad Politécnica de Quintana Roo (UPQRoo)")
    HTML_OUTPUT.write_text(build_html(source_text, institution), encoding="utf-8")

    edge = find_edge()
    subprocess.run(
        [
            str(edge),
            "--headless=new",
            "--disable-gpu",
            "--no-first-run",
            "--no-pdf-header-footer",
            f"--print-to-pdf={PDF_OUTPUT}",
            HTML_OUTPUT.as_uri(),
        ],
        check=True,
        timeout=120,
    )
    if not PDF_OUTPUT.is_file() or PDF_OUTPUT.stat().st_size < 10_000:
        raise RuntimeError("El PDF no se generó o quedó incompleto.")
    print(f"MEMORY_PDF_OK: {PDF_OUTPUT} ({PDF_OUTPUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
