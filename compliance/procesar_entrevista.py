# -*- coding: utf-8 -*-
r"""
procesar_entrevista.py

Qué se puede hacer con una entrevista una vez subida.

Ignacio, 26/08/2026: "en el canal de entrevistas, si subo una, ¿no debería
haber un botón de procesar o guardar?". Guardar ya se guardaba solo al
soltar el fichero -por eso no había botón-, pero PROCESAR no existía: el
archivo se quedaba ahí y no pasaba nada más. Esto es ese paso.

LO QUE HOY SE PUEDE Y LO QUE NO, dicho sin adornos:

  NOTAS (.txt, .md)     se lee el texto y queda dentro del expediente.
  WORD (.docx)          se lee sin necesidad de librerías: un .docx es un
                        zip con XML dentro, y de ahí se sacan los párrafos.
  PDF                   no se lee todavía. Hace falta un extractor y, si
                        viene escaneado, OCR.
  AUDIO Y VÍDEO         NO se transcriben. En este equipo no hay ningún
                        motor de transcripción instalado -se ha comprobado-,
                        y todo tiene que quedarse en local, así que no se
                        puede mandar fuera a transcribir.

POR QUÉ SE DICE EN VEZ DE DISIMULARLO. Un botón que parece que hace algo y
no lo hace es peor que no tener botón: alguien daría por transcrita una
entrevista que nadie ha escuchado. Mientras no haya motor, el camino es
pegar la transcripción a mano, y eso sí está.

LO QUE VIENE DESPUÉS, cuando haya texto: sacar de la transcripción los
procesos, las cifras, los controles mencionados y las evidencias prometidas,
y proponer una puntuación por conducta CON LA CITA LITERAL de dónde se dijo.
Proponer. Confirmar sigue siendo de Mamen.
"""
from __future__ import annotations

import re
import zipfile
from pathlib import Path

import proyectos as pr                               # noqa: E402

TEXTO_PLANO = {".txt", ".md", ".csv"}


def _de_docx(ruta):
    """El texto de un .docx sin librerías: es un zip con XML dentro."""
    with zipfile.ZipFile(ruta) as z:
        xml = z.read("word/document.xml").decode("utf-8", "ignore")
    xml = re.sub(r"</w:p>", "\n", xml)
    return re.sub(r"<[^>]+>", "", xml).strip()


def se_puede_leer(nombre):
    ext = Path(nombre).suffix.lower()
    return ext in TEXTO_PLANO or ext == ".docx"


def procesar(clave, fichero):
    """Saca el texto si se puede. Si no, lo dice claramente."""
    p = pr.leer(clave)
    if p is None:
        return {"ok": False, "dicho": "no existe ese proyecto"}
    ruta = pr.carpeta(clave) / "entrevistas" / fichero
    if not ruta.exists():
        return {"ok": False, "dicho": "no encuentro ese fichero"}

    ext = ruta.suffix.lower()
    try:
        if ext in TEXTO_PLANO:
            texto = ruta.read_text(encoding="utf-8", errors="replace")
        elif ext == ".docx":
            texto = _de_docx(ruta)
        elif ext == ".pdf":
            return {"ok": False, "dicho": (
                "los PDF todavía no se leen aquí: falta el extractor, y si "
                "viene escaneado hace falta OCR. Pega la transcripción a mano "
                "mientras tanto")}
        else:
            return {"ok": False, "dicho": (
                "el audio y el vídeo no se transcriben todavía: en este "
                "equipo no hay motor de transcripción instalado y nada puede "
                "salir a la nube. Pega la transcripción a mano")}
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "dicho": f"no he podido leerlo: {exc!s:.70}"}

    return guardar_transcripcion(clave, fichero, texto,
                                 de_donde=f"leído del {ext}")


def guardar_transcripcion(clave, fichero, texto, de_donde="pegada a mano"):
    """Deja la transcripción junto a la entrevista, en el expediente."""
    p = pr.leer(clave)
    if p is None:
        return {"ok": False, "dicho": "no existe ese proyecto"}
    texto = (texto or "").strip()
    if not texto:
        return {"ok": False, "dicho": "no había texto"}
    destino = pr.carpeta(clave) / "entrevistas" / (fichero + ".txt")
    destino.write_text(texto, encoding="utf-8")
    for e in p.get("entrevistas") or []:
        if e.get("fichero") == fichero:
            e["transcrita"] = True
            e["transcripcion"] = destino.name
            e["palabras"] = len(texto.split())
            e["origen_texto"] = de_donde
    pr.guardar(p)
    return {"ok": True, "palabras": len(texto.split()),
            "dicho": f"transcripción guardada, {len(texto.split())} palabras "
                     f"({de_donde})"}


def leer_transcripcion(clave, fichero):
    sitio = pr.carpeta(clave) / "entrevistas" / (fichero + ".txt")
    if not sitio.exists():
        return ""
    return sitio.read_text(encoding="utf-8", errors="replace")


def confirmar(clave, fichero, si=True):
    """Mamen da por buena la entrevista. Sin esto no cuenta como hecha."""
    p = pr.leer(clave)
    if p is None:
        return {"ok": False}
    for e in p.get("entrevistas") or []:
        if e.get("fichero") == fichero:
            e["confirmada"] = bool(si)
    pr.guardar(p)
    return {"ok": True}
