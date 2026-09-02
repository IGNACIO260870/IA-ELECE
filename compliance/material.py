# -*- coding: utf-8 -*-
"""
material.py

EL MATERIAL DE CADA MARCA, RECOGIDO SOLO DE SU CARPETA.

DE DÓNDE VIENE. Primero fue LawScale -Ignacio, 02/09/2026: "vamos a colgar
como tarjetas todo lo que hay aquí"- y se hizo un módulo para esa carpeta.
Al rato llegó lo de elece: "aquí está el de compliance, este es para elece",
con otra carpeta y otros cinco ZIP. Dos marcas con el mismo problema, así
que una sola pieza con dos configuraciones, y no dos copias del mismo código
que mañana se separan.

CÓMO FUNCIONA. Cada colección tiene un BUZÓN -la carpeta donde Ignacio deja
las cosas, normalmente en Descargas- y un ALMACÉN dentro de IA ELECE. Al
abrir la pantalla se mira el buzón: lo que falte se copia, los ZIP se
descomprimen, y lo que venga corregido reemplaza a lo anterior. Así la
respuesta a "¿qué tengo que hacer para que esté en el servidor?" es "nada".

SE COPIA, NO SE MUEVE. Lo de Descargas se queda en Descargas: si esto se
llevara los ficheros, un fallo aquí sería perder el original.
"""
from __future__ import annotations

import os
import re
import shutil
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DESCARGAS = Path.home() / "Downloads"

TIPOS = {
    ".md": ("documento", True), ".txt": ("texto", True),
    ".docx": ("Word", False), ".doc": ("Word", False),
    ".pptx": ("PowerPoint", False), ".ppt": ("PowerPoint", False),
    ".pdf": ("PDF", False), ".xlsx": ("Excel", False), ".xls": ("Excel", False),
    ".png": ("imagen", False), ".jpg": ("imagen", False),
    ".jpeg": ("imagen", False), ".csv": ("datos", False),
}


@dataclass
class Coleccion:
    clave: str
    titulo: str
    lema: str
    buzon: Path
    azul: str                      # el color principal de la marca
    oro: str                       # el de acento
    logo: str = ""                 # fichero del logo, si lo hay
    descripciones: dict = field(default_factory=dict)

    @property
    def almacen(self) -> Path:
        return RAIZ / "datos" / self.clave


# ---------------------------------------------------------------------------
# LAS DOS MARCAS
#
# Los colores salen de los briefings que subió Ignacio el 02/09/2026, que son
# la fuente de marca. Costó fijarlos: hay dos parejas de LawScale dando
# vueltas -#323E53/#E8BF25 son los corporativos, sacados del logo real, y
# #233046/#E7C236 las variantes registradas que se usaron en el PPTX de RRHH
# porque venían del PDF del curso eIDAS-01-. Los briefings de formación
# modular y el general coinciden: mandan los primeros.
# ---------------------------------------------------------------------------
LAWSCALE = Coleccion(
    clave="lawscale", titulo="LawScale",
    lema="Acercando la ley, respaldando tus valores",
    buzon=Path(os.environ.get("LAWSCALE_BUZON", str(DESCARGAS / "LAWSCALE"))),
    azul="#323E53", oro="#E8BF25", logo="logo.png",
    descripciones={
        "compliance-digital-rrhh-base.md":
            "El documento base: el encargo, el análisis norma por norma de su "
            "impacto en RRHH y la estructura en seis pilares.",
        "BRIEFING_CONTEXTO_SESION.md":
            "Briefing de la sesión: partes, marca, la formación de RRHH "
            "diapositiva a diapositiva y lo que quedó pendiente.",
        "BRIEFING_CONTEXTO FROMACION MODULAR.md":
            "Briefing de la formación modular: «Visión 360º», módulos por rol "
            "e inversión.",
        "README.md": "El briefing original del proyecto.",
        "Propuesta_Formacion_LawScale.docx": "La propuesta de formación, editable.",
        "Propuesta_Formacion_LawScale.pdf": "La misma propuesta, para mandar.",
        "RRHH_compliance_digital_LawScale.pptx":
            "La presentación de RRHH, con la marca LawScale.",
        "RRHH_compliance_digital.pptx":
            "La misma presentación en la identidad de elece Legal.",
        "Notas_orador_RRHH_LawScale.docx": "La guía del ponente.",
        "logo.png": "El logo de LawScale Digital.",
    })

# elece Legal: #9D203E (Pantone 7420C) y el azul oscuro #1F3864 de secundario.
# Lo dicen los dos briefings; el rojo de la portada de IA ELECE (#8A2742) se
# tomó en su día muestreando elecelegal.es y no coincide.
ELECE = Coleccion(
    clave="elece", titulo="elece Legal",
    lema="Compliance penal y sistemas de gestión",
    buzon=Path(os.environ.get("ELECE_BUZON", str(DESCARGAS / "ELECELEGAL"))),
    azul="#9D203E", oro="#1F3864",
    descripciones={
        "BRIEFING CONTEXTO GENERAL COMPOLIANCE.docx":
            "El briefing general: quién es quién, las dos marcas, los "
            "proyectos activos y las identidades visuales.",
        "BRIEFING DESCONEXION DE DESPACHOS.docx":
            "Documentación laboral del propio despacho: plantilla, convenio "
            "de Oficinas y Despachos de Zaragoza y desconexión digital.",
        "Protocolo_Desconexion_Digital_Zaragoza.docx":
            "El protocolo de desconexión digital, listo para firmar.",
        "Propuesta_eleceLegal_ProclinicGroup_UNE19601_ISO37001.docx":
            "La propuesta de auditoría integrada para Proclinic Group, en "
            "dos fases.",
        "Anexo_Entregables_ProclinicGroup.docx":
            "Qué se entrega en cada fase de Proclinic.",
        "Propuesta_ProclinicGroup_Visual.pptx":
            "La misma propuesta en presentación.",
        "Informe_Auditoria_Compliance_CerlerGlobal_2026.docx":
            "El informe de auditoría de compliance penal de Cerler.",
        "Informe_Auditoria_Compliance_CerlerGlobal_2026.md":
            "El mismo informe en texto, para leerlo aquí. OJO: éste dice «8 "
            "de 12 documentos» y el Word dice «10 de 12»; hay que cuadrarlo "
            "antes de usarlo.",
        "01_Agente_Compliance_Instrucciones.docx":
            "Instrucciones del agente de compliance del Kit.",
        "02_Herramientas_Compliance.xlsx":
            "Checklist y matriz de riesgos del Kit.",
        "03_Guia_Agentes_Compliance.md":
            "La guía de agentes: hoja de ruta en tres fases.",
        "Resumen_Sesion_elece_legal.docx":
            "Resumen de la sesión de trabajo del despacho.",
    })

COLECCIONES = {c.clave: c for c in (LAWSCALE, ELECE)}


# ---------------------------------------------------------------------------
def _tamano(n):
    if n < 1024:
        return f"{n} B"
    if n < 1024 * 1024:
        return f"{n / 1024:.0f} KB"
    return f"{n / (1024 * 1024):.1f} MB"


# CARPETAS QUE NO SON MATERIAL. Uno de los ZIP de elece traía dentro un
# repositorio git entero, y al aplanar los nombres aparecieron en la pantalla
# treinta ficheros como HEAD, config, index y los hooks de ejemplo. Nada de
# eso es un documento.
BASURA = {".git", "__macosx", "node_modules", ".venv", "__pycache__",
          ".idea", ".vscode"}


def _es_material(nombre_en_zip):
    """¿Esta entrada del ZIP es un documento, o son tripas de otra cosa?"""
    partes = [x.lower() for x in Path(nombre_en_zip).parts]
    if any(x in BASURA for x in partes[:-1]):
        return False
    # Y sólo lo que tiene una extensión que sepamos enseñar: así no entran
    # los ficheros sin extensión ni los .sample de los hooks.
    return Path(nombre_en_zip).suffix.lower() in TIPOS


def _sin_pisar(destino, tamano, de_donde):
    """Evita que dos ZIP con un README.md se pisen en silencio."""
    if not destino.exists() or destino.stat().st_size == tamano:
        return destino
    return destino.with_name(f"{destino.stem} ({de_donde}){destino.suffix}")


def _hay_que_traer(origen, destino):
    if not destino.exists():
        return True
    o, d = origen.stat(), destino.stat()
    return o.st_size != d.st_size or o.st_mtime > d.st_mtime + 2


def recoger(col: Coleccion):
    """Trae del buzón lo que no esté ya, y descomprime los ZIP.

    NO REVIENTA LA PANTALLA SI FALLA. Si el buzón no existe -otro equipo, la
    carpeta borrada- o un ZIP viene mal, se sigue con lo que ya hay dentro:
    que no se pueda recoger un fichero nuevo no puede impedir ver los que ya
    estaban.
    """
    traidos = []
    try:
        if not col.buzon.is_dir():
            return traidos
        col.almacen.mkdir(parents=True, exist_ok=True)
        for f in sorted(col.buzon.iterdir()):
            if not f.is_file():
                continue
            try:
                if f.suffix.lower() == ".zip":
                    with zipfile.ZipFile(f) as z:
                        for i in z.infolist():
                            if i.is_dir() or not _es_material(i.filename):
                                continue
                            destino = _sin_pisar(
                                col.almacen / Path(i.filename).name,
                                i.file_size, f.stem[:24])
                            if destino.exists() and \
                                    destino.stat().st_size == i.file_size:
                                continue
                            with z.open(i) as dentro, open(destino, "wb") as fuera:
                                shutil.copyfileobj(dentro, fuera)
                            traidos.append(destino.name)
                else:
                    destino = col.almacen / f.name
                    if _hay_que_traer(f, destino):
                        shutil.copy2(f, destino)
                        traidos.append(f.name)
            except Exception:                            # noqa: BLE001, PERF203
                continue                                 # uno malo no para el resto
    except Exception:                                    # noqa: BLE001
        pass
    return traidos


def listar(col: Coleccion, recogiendo=True):
    """Lo que hay en el almacén, ordenado y con su ficha."""
    if recogiendo:
        recoger(col)
    if not col.almacen.exists():
        return []
    fuera = []
    for f in sorted(col.almacen.iterdir(), key=lambda x: x.name.lower()):
        if not f.is_file():
            continue
        tipo, se_lee = TIPOS.get(f.suffix.lower(), ("fichero", False))
        fuera.append({"nombre": f.name, "tipo": tipo, "se_lee": se_lee,
                      "tamano": _tamano(f.stat().st_size),
                      "que_es": col.descripciones.get(f.name, "")})
    # Primero lo que se puede leer en pantalla: ahí está el criterio.
    fuera.sort(key=lambda x: (not x["se_lee"], x["nombre"].lower()))
    return fuera


def ruta_de(col: Coleccion, nombre):
    """La ruta de un fichero del almacén, o None.

    SE COMPRUEBA QUE ESTÉ DENTRO. El nombre llega por la URL, así que no
    basta con pegarlo detrás de la carpeta: un «../../» sacaría de aquí y
    serviría cualquier fichero del disco.
    """
    limpio = re.sub(r"[/\\]", "", nombre or "")
    if not limpio or limpio.startswith("."):
        return None
    ruta = (col.almacen / limpio).resolve()
    try:
        ruta.relative_to(col.almacen.resolve())
    except ValueError:
        return None
    return ruta if ruta.is_file() else None


def _texto_docx(ruta):
    """El texto de un Word, sin depender de python-docx.

    Un .docx es un ZIP con XML dentro. Leerlo así evita añadir una
    dependencia sólo para esto -en el entorno de Colibrí no está instalada- y
    para lo que hace falta aquí, que es dárselo al Preguntador, sobra.
    """
    import zipfile as zf                                 # noqa: PLC0415
    from xml.etree import ElementTree as ET              # noqa: PLC0415
    W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    try:
        with zf.ZipFile(ruta) as z:
            raiz = ET.fromstring(z.read("word/document.xml"))
    except Exception:                                    # noqa: BLE001
        return ""
    lineas = []
    for p in raiz.iter(W + "p"):
        t = "".join(x.text or "" for x in p.iter(W + "t")).strip()
        if t:
            lineas.append(t)
    return "\n".join(lineas)


def texto_de(col: Coleccion, nombre):
    """El contenido de un fichero que se pueda leer en pantalla."""
    ruta = ruta_de(col, nombre)
    if ruta is None:
        return None
    tipo, se_lee = TIPOS.get(ruta.suffix.lower(), ("fichero", False))
    if not se_lee:
        return None
    try:
        return ruta.read_text(encoding="utf-8", errors="replace")
    except Exception:                                    # noqa: BLE001
        return None


def para_el_preguntador(tope=45000):
    """Todo el material legible de las dos marcas, para el contexto.

    ENTRAN TAMBIÉN LOS WORD. El briefing general de elece vino en .docx, y
    dejarlo fuera habría sido tener al Preguntador sin lo más importante que
    se ha subido: quién es quién, las dos marcas y los proyectos activos.
    Los .pptx no: lo que llevan dentro ya lo cuentan los briefings.
    """
    fuera = []
    for col in COLECCIONES.values():
        gastado, trozos = 0, []
        recoger(col)
        if not col.almacen.exists():
            continue
        legibles = (sorted(col.almacen.glob("*.md"))
                    + sorted(col.almacen.glob("*.txt"))
                    + sorted(col.almacen.glob("*.docx")))
        for f in legibles:
            t = (_texto_docx(f) if f.suffix.lower() == ".docx"
                 else f.read_text(encoding="utf-8", errors="replace")).strip()
            if not t:
                continue
            queda = tope - gastado
            if queda <= 0:
                break
            recorte = t[:queda]
            trozos.append(f"--- {f.name} ---\n{recorte}")
            gastado += len(recorte)
        if trozos:
            fuera.append(f"### MATERIAL DE {col.titulo.upper()}\n"
                         + "\n\n".join(trozos))
    return "\n\n".join(fuera)
