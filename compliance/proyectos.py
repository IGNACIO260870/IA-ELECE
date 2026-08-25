# -*- coding: utf-8 -*-
r"""
proyectos.py

Un proyecto es una empresa. Cada cliente es el suyo y no se mezclan.
Ignacio, 25/08/2026: "quizá lo mejor sea una tarjeta por proyecto, es decir,
empresa..., empresa... y ahí reproducir todos los puntos que vayamos
haciendo".

CADA PROYECTO ES UN EXPEDIENTE, NO UNA CARPETA. Guarda el encargo, el
alcance, las áreas, las entrevistas, los documentos, la matriz y los
entregables, y sobre todo guarda EL ESTADO: qué fase está hecha, qué falta y
qué no se puede afirmar. De ahí come el supervisor.

EL TRAJE ES A MEDIDA. Del proyecto anterior se hereda el catálogo de delitos
y la biblioteca de controles; NUNCA la valoración. Reutilizar puntuaciones
de otro cliente es el error de la plantilla estandarizada, y es lo primero
que detecta quien revisa un expediente.

TODO SE QUEDA EN EL DISCO. Ignacio, preguntado si la documentación de un
cliente puede salir del equipo: "no". Aquí no hay nube.
"""
from __future__ import annotations

import json
import re
import unicodedata
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DATOS = RAIZ / "datos" / "proyectos"

# Las fases del trabajo, en el orden en que se hacen. El nombre corto es el
# que se ve en la tarjeta del proyecto.
FASES = [
    ("encargo", "Encargo y alcance"),
    ("contexto", "Contexto de la organización"),
    ("catalogo", "Catálogo de delitos"),
    ("aplicabilidad", "Aplicabilidad"),
    ("entrevistas", "Entrevistas por área"),
    ("evidencias", "Documentación y evidencias"),
    ("valoracion", "Valoración de riesgos"),
    ("controles", "Controles y riesgo residual"),
    ("gobierno", "Apetito y gobierno"),
    ("entregables", "Informe y plan de acción"),
]

# Los siete bloques de evidencia documental. Son los del dossier de traspaso
# y coinciden con lo que mira una auditoría de la UNE 19601:2025.
BLOQUES = [
    ("gobierno", "Gobierno y alcance",
     "Alcance del SGCP, organigrama, mapa de procesos, política, actas."),
    ("riesgos", "Riesgos",
     "Metodología, matriz, revisiones, criterios y trazabilidad de controles."),
    ("funcion", "Función de compliance",
     "Nombramiento, estatuto, independencia, autoridad, recursos."),
    ("canal", "Canal e investigaciones",
     "Procedimiento, tramitación, protección del informante, medidas."),
    ("cultura", "Personas y cultura",
     "Formación, competencia, toma de conciencia, liderazgo."),
    ("terceros", "Terceros y filiales",
     "Diligencia debida, cláusulas, seguimiento, despliegue en el grupo."),
    ("mejora", "Evaluación y mejora",
     "Indicadores, auditorías, revisión por dirección, acciones correctivas."),
]


def _clave(nombre):
    """Un nombre de empresa convertido en algo que valga de nombre de fichero."""
    limpio = unicodedata.normalize("NFKD", nombre or "")
    limpio = limpio.encode("ascii", "ignore").decode("ascii").lower()
    limpio = re.sub(r"[^a-z0-9]+", "-", limpio).strip("-")
    return limpio or "sin-nombre"


def carpeta(clave):
    return DATOS / clave


def _fichero(clave):
    return carpeta(clave) / "proyecto.json"


def listar():
    """Todos los proyectos, el más reciente primero."""
    if not DATOS.exists():
        return []
    fuera = []
    for f in DATOS.glob("*/proyecto.json"):
        try:
            fuera.append(json.loads(f.read_text(encoding="utf-8")))
        except Exception:  # noqa: BLE001, S112
            continue
    fuera.sort(key=lambda p: p.get("abierto", ""), reverse=True)
    return fuera


def leer(clave):
    f = _fichero(clave)
    if not f.exists():
        return None
    return json.loads(f.read_text(encoding="utf-8"))


def guardar(p):
    c = carpeta(p["clave"])
    for sub in ("entrevistas", "documentos", "entregables"):
        (c / sub).mkdir(parents=True, exist_ok=True)
    p["tocado"] = datetime.now().isoformat(timespec="seconds")
    _fichero(p["clave"]).write_text(
        json.dumps(p, ensure_ascii=False, indent=2), encoding="utf-8")
    return p


def crear(nombre, **datos):
    """Abre un proyecto. Nace vacío a propósito: nada se hereda valorado."""
    clave = _clave(nombre)
    if leer(clave):
        return leer(clave)
    p = {
        "clave": clave, "empresa": nombre,
        "abierto": datetime.now().isoformat(timespec="seconds"),
        "cif": datos.get("cif", ""),
        "tipo_trabajo": datos.get("tipo_trabajo", ""),
        "alcance": datos.get("alcance", ""),
        "periodo": datos.get("periodo", ""),
        "audiencia": datos.get("audiencia", ""),
        "responsable": datos.get("responsable", "Mamen"),
        # El apetito NO lo ponemos nosotros: lo firma el órgano de gobierno
        # del cliente. Mientras esté a None, el informe lo dice.
        "apetito": None, "apetito_firmado_por": "", "apetito_fecha": "",
        "areas": [], "delitos": [], "conductas": [], "controles": [],
        "entrevistas": [], "documentos": [],
        "catalogo_version": "", "catalogo_cotejado": "",
        "barrido_publico": "",
        # Control documental, para que esto encaje en el sistema de calidad.
        "codigo": datos.get("codigo", ""), "version": "0.1",
        "elaborado": "", "revisado": "", "aprobado": "",
        "revision_proxima": "", "disparadores": [],
    }
    return guardar(p)


# ---------------------------------------------------------------------------
# EL CANAL DE ENTREVISTAS
# ---------------------------------------------------------------------------
# Ignacio, 25/08/2026: "un canal para subir las entrevistas que esté dentro
# de la tarjeta". Las hace Mamen, presenciales, una hora por área con el
# responsable, y se graban como apoyo para la transcripción.
#
# AQUÍ SÓLO SE GUARDA. Transcribir y proponer puntuaciones es el paso
# siguiente y va aparte: primero que el material esté a salvo y ordenado por
# empresa y por área, que es lo que hoy no existe.
AUDIO = {".mp3", ".m4a", ".wav", ".ogg", ".aac", ".wma", ".opus"}
VIDEO = {".mp4", ".mov", ".avi", ".mkv", ".webm"}
NOTAS = {".txt", ".md", ".docx", ".doc", ".pdf", ".rtf"}


def tipo_de(nombre):
    ext = Path(nombre).suffix.lower()
    if ext in AUDIO:
        return "audio"
    if ext in VIDEO:
        return "vídeo"
    if ext in NOTAS:
        return "notas"
    return "otro"


def guardar_entrevista(clave, nombre_fichero, contenido, area="", quien=""):
    """Deja una entrevista en el expediente de la empresa."""
    p = leer(clave)
    if p is None:
        return {"ok": False, "porque": "no existe ese proyecto"}
    destino = carpeta(clave) / "entrevistas"
    destino.mkdir(parents=True, exist_ok=True)
    seguro = re.sub(r"[^\w.\- ]+", "_", Path(nombre_fichero).name)
    sello = datetime.now().strftime("%Y%m%d-%H%M%S")
    sitio = destino / f"{sello}_{seguro}"
    sitio.write_bytes(contenido)
    ficha = {
        "fichero": sitio.name, "area": area, "entrevistado": quien,
        "tipo": tipo_de(seguro), "bytes": len(contenido),
        "subido": datetime.now().isoformat(timespec="seconds"),
        "transcrita": False, "confirmada": False,
    }
    p.setdefault("entrevistas", []).append(ficha)
    guardar(p)
    return {"ok": True, "ficha": ficha}
