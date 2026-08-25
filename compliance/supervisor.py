# -*- coding: utf-8 -*-
r"""
supervisor.py

El supervisor de la matriz: garantiza que todo lo que hace falta para
hacerla está, y está en condiciones.

Ignacio, 25/08/2026: "quiero un supervisor de la Excel, es decir, un modo de
garantizar que todo lo que necesitamos para hacer la Excel lo tenemos y lo
tenemos en perfecto estado".

DOS PREGUNTAS DISTINTAS, Y LAS DOS HACEN FALTA:

    ¿ESTÁ?          completitud  -> falta la entrevista de Compras
    ¿ESTÁ BIEN?     calidad      -> hay 14 controles sin documento

La segunda es la que nadie mira y la que hunde un expediente. Una matriz
puede estar «completa» y no valer nada: todos los campos rellenos, ningún
control con evidencia detrás.

TRES ESTADOS, NO DOS. Igual que el supervisor de Colibrí:

    HECHO      consta que está, y consta dónde
    PENDIENTE  consta que falta
    NO LO SÉ   no puedo comprobarlo  <- va en rojo

Un supervisor que sólo sepa decir «bien» y «mal» miente el día que no puede
mirar. Y aquí importa el doble, porque lo que se firma al final es un
informe con el nombre del despacho.
"""
from __future__ import annotations

from datetime import datetime

import proyectos as pr                              # noqa: E402

HECHO, PENDIENTE, NO_SE = "hecho", "pendiente", "no_se"


def _r(estado, que, detalle="", cuantos=None, fase="", norma=""):
    return {"estado": estado, "que": que, "detalle": detalle,
            "cuantos": cuantos, "fase": fase, "norma": norma}


# ---------------------------------------------------------------------------
# ¿ESTÁ? — completitud
# ---------------------------------------------------------------------------
def _encargo(p):
    faltan = [n for n, c in (("tipo de trabajo", "tipo_trabajo"),
                             ("alcance societario", "alcance"),
                             ("periodo", "periodo"),
                             ("audiencia del entregable", "audiencia"))
              if not p.get(c)]
    if faltan:
        return _r(PENDIENTE, "Encargo y alcance",
                  "falta " + ", ".join(faltan), len(faltan), "encargo",
                  "Sin alcance no se puede limitar una conclusión")
    return _r(HECHO, "Encargo y alcance", "definido", 0, "encargo")


def _contexto(p):
    areas = p.get("areas") or []
    if not areas:
        return _r(PENDIENTE, "Áreas de la organización",
                  "no hay áreas definidas: sin ellas no hay a quién "
                  "entrevistar ni a quién asignar un riesgo", 0, "contexto",
                  "UNE 19601:2025 · 4.5 contexto de la organización")
    return _r(HECHO, "Áreas de la organización",
              f"{len(areas)} áreas", len(areas), "contexto")


def _catalogo(p):
    if not p.get("catalogo_version"):
        return _r(PENDIENTE, "Catálogo de delitos",
                  "sin versión de catálogo asignada", None, "catalogo",
                  "UNE 19601:2025 · 4.5.2 considerar TODOS los delitos")
    if not p.get("catalogo_cotejado"):
        return _r(NO_SE, "Catálogo de delitos",
                  f"versión {p['catalogo_version']}, pero no consta la fecha "
                  f"en que se cotejó contra el Código Penal consolidado: no "
                  f"puedo afirmar que esté al día", None, "catalogo",
                  "UNE 19601:2025 · 4.5.2")
    return _r(HECHO, "Catálogo de delitos",
              f"versión {p['catalogo_version']}, cotejado el "
              f"{p['catalogo_cotejado']}", None, "catalogo")


def _aplicabilidad(p):
    delitos = p.get("delitos") or []
    if not delitos:
        return _r(PENDIENTE, "Aplicabilidad por delito",
                  "sin decidir", 0, "aplicabilidad")
    sin_decidir = [d for d in delitos if d.get("aplica") is None]
    sin_motivo = [d for d in delitos
                  if d.get("aplica") is False and not d.get("motivo")]
    if sin_decidir:
        return _r(PENDIENTE, "Aplicabilidad por delito",
                  f"{len(sin_decidir)} delitos sin decidir si aplican",
                  len(sin_decidir), "aplicabilidad")
    if sin_motivo:
        # EL DESCARTE SIN MOTIVO ES EL AGUJERO CLÁSICO. Un «no aplica» sin
        # razón escrita no se sostiene: la norma pide considerar todos los
        # delitos, y considerar significa dejar constancia de por qué se
        # descarta, no borrarlo de la lista.
        return _r(PENDIENTE, "Aplicabilidad por delito",
                  f"{len(sin_motivo)} descartados SIN motivo escrito",
                  len(sin_motivo), "aplicabilidad",
                  "UNE 19601:2025 · 4.5.2")
    return _r(HECHO, "Aplicabilidad por delito",
              f"{len(delitos)} decididos, los descartes con motivo",
              len(delitos), "aplicabilidad")


def _entrevistas(p):
    areas = p.get("areas") or []
    ents = p.get("entrevistas") or []
    if not areas:
        return _r(NO_SE, "Entrevistas por área",
                  "no sé cuántas faltan porque no hay áreas definidas",
                  None, "entrevistas")
    con = {e.get("area") for e in ents if e.get("area")}
    faltan = [a for a in areas if a not in con]
    if faltan:
        return _r(PENDIENTE, "Entrevistas por área",
                  "sin entrevista: " + ", ".join(faltan[:6])
                  + ("…" if len(faltan) > 6 else ""), len(faltan),
                  "entrevistas")
    return _r(HECHO, "Entrevistas por área",
              f"{len(ents)} entrevistas para {len(areas)} áreas",
              len(ents), "entrevistas")


def _valoracion(p):
    cond = [c for c in (p.get("conductas") or []) if c.get("aplica")]
    if not cond:
        return _r(PENDIENTE, "Valoración de conductas", "sin valorar", 0,
                  "valoracion")
    sin = [c for c in cond
           if c.get("exposicion") is None or c.get("severidad") is None]
    if sin:
        return _r(PENDIENTE, "Valoración de conductas",
                  f"{len(sin)} conductas sin puntuar", len(sin), "valoracion")
    return _r(HECHO, "Valoración de conductas",
              f"{len(cond)} conductas valoradas", len(cond), "valoracion")


def _gobierno(p):
    if p.get("apetito") is None:
        # Ignacio: "umbral NO lo ponemos nosotros". Correcto: es una decisión
        # indelegable del órgano de gobierno. Pero mientras no esté, el
        # informe no puede decir qué está por encima. Es un hallazgo en sí.
        return _r(PENDIENTE, "Apetito de riesgo",
                  "el órgano de gobierno no ha aprobado umbral: sin él no se "
                  "puede decir qué supera el apetito ni qué plan de acción es "
                  "obligatorio", None, "gobierno",
                  "UNE 19601:2025 · gobernanza, responsabilidades indelegables")
    if not p.get("apetito_firmado_por"):
        return _r(NO_SE, "Apetito de riesgo",
                  f"hay umbral ({p['apetito']}) pero no consta quién lo "
                  f"aprobó: no puedo afirmar que esté validado", None,
                  "gobierno")
    return _r(HECHO, "Apetito de riesgo",
              f"umbral {p['apetito']}, aprobado por {p['apetito_firmado_por']} "
              f"el {p.get('apetito_fecha','')}", None, "gobierno")


# ---------------------------------------------------------------------------
# ¿ESTÁ BIEN? — calidad
# ---------------------------------------------------------------------------
def _calidad_controles(p):
    ctrl = p.get("controles") or []
    if not ctrl:
        return [_r(PENDIENTE, "Controles", "no hay ninguno cargado", 0,
                   "controles")]
    fuera = []
    sin_doc = [c for c in ctrl if c.get("evidencia") != "documentada"]
    if sin_doc:
        fuera.append(_r(PENDIENTE, "Controles sin evidencia documental",
                        f"{len(sin_doc)} de {len(ctrl)} se sostienen sólo en "
                        f"lo que alguien dijo. Su eficacia cae al 15 % y así "
                        f"salen en el informe", len(sin_doc), "controles",
                        "Un control sin documento no baja el riesgo ante un juez"))
    huerfanos = [c for c in ctrl if not c.get("conducta")]
    if huerfanos:
        fuera.append(_r(PENDIENTE, "Controles sin conducta asignada",
                        f"{len(huerfanos)} no están enganchados a ninguna "
                        f"conducta: no descuentan nada", len(huerfanos),
                        "controles",
                        "Es el fallo que tenía la matriz anterior: 93 de 603"))
    ignorados = [c for c in ctrl if c.get("estado") == "ignorado"]
    if ignorados:
        fuera.append(_r(PENDIENTE, "Controles en estado ignorado",
                        f"{len(ignorados)} no son controles todavía, son "
                        f"intenciones. No se valoran", len(ignorados),
                        "controles"))
    if not fuera:
        fuera.append(_r(HECHO, "Controles",
                        f"{len(ctrl)} controles, todos con evidencia y "
                        f"enganchados", len(ctrl), "controles"))
    return fuera


def _calidad_trazabilidad(p):
    cond = [c for c in (p.get("conductas") or []) if c.get("aplica")]
    sin_porque = [c for c in cond if not c.get("justificacion")]
    if not cond:
        return _r(NO_SE, "Trazabilidad de la puntuación",
                  "todavía no hay conductas valoradas que comprobar", None,
                  "valoracion")
    if sin_porque:
        return _r(PENDIENTE, "Trazabilidad de la puntuación",
                  f"{len(sin_porque)} conductas puntuadas sin justificación "
                  f"escrita. Un número sin motivo es una opinión",
                  len(sin_porque), "valoracion",
                  "Principio de trazabilidad: criterio + evidencia + alcance")
    return _r(HECHO, "Trazabilidad de la puntuación",
              "todas las conductas llevan su motivo", len(cond), "valoracion")


def _calidad_documental(p):
    """El control documental que pide un sistema de calidad ISO 9001."""
    faltan = [n for n, c in (("código de documento", "codigo"),
                             ("elaborado por", "elaborado"),
                             ("revisado por", "revisado"),
                             ("aprobado por", "aprobado"))
              if not p.get(c)]
    if faltan:
        return _r(PENDIENTE, "Control documental",
                  "falta " + ", ".join(faltan)
                  + ". Sin esto el documento no entra en el sistema de calidad",
                  len(faltan), "entregables",
                  "ISO 9001 · información documentada")
    return _r(HECHO, "Control documental",
              f"{p['codigo']} v{p.get('version','')}, elaborado por "
              f"{p['elaborado']}, aprobado por {p['aprobado']}", None,
              "entregables")


def _calidad_revision(p):
    """El 6.3 nuevo de la UNE 19601:2025: planificación de cambios."""
    if not p.get("disparadores"):
        return _r(PENDIENTE, "Disparadores de revisión",
                  "sin definir qué obliga a rehacer la evaluación (reforma "
                  "del CP, nueva actividad, nuevo centro, incidente, cambio "
                  "del órgano de compliance)", None, "gobierno",
                  "UNE 19601:2025 · 6.3 planificación de los cambios")
    prox = p.get("revision_proxima")
    if not prox:
        return _r(NO_SE, "Disparadores de revisión",
                  "hay disparadores pero no consta fecha de próxima revisión",
                  None, "gobierno", "UNE 19601:2025 · 6.3")
    try:
        if datetime.fromisoformat(prox) < datetime.now():
            return _r(PENDIENTE, "Revisión vencida",
                      f"la revisión estaba prevista para el {prox[:10]} y no "
                      f"consta hecha", None, "gobierno",
                      "UNE 19601:2025 · 6.3")
    except ValueError:
        pass
    return _r(HECHO, "Disparadores de revisión",
              f"{len(p['disparadores'])} definidos, próxima revisión {prox[:10]}",
              None, "gobierno")


def _barrido(p):
    if not p.get("barrido_publico"):
        return _r(NO_SE, "Barrido de fuentes públicas",
                  "no consta hecho. Sin él, el factor de historial de la "
                  "empresa (sanciones, expedientes) no está comprobado y la "
                  "probabilidad se apoya sólo en lo que cuenten en la "
                  "entrevista", None, "evidencias")
    return _r(HECHO, "Barrido de fuentes públicas",
              f"hecho el {p['barrido_publico'][:10]}", None, "evidencias")


# ---------------------------------------------------------------------------
def revisar(clave):
    """El cuadro entero de un proyecto. Sólo mira; no cambia nada."""
    p = pr.leer(clave)
    if p is None:
        return None
    esta = [_encargo(p), _contexto(p), _catalogo(p), _aplicabilidad(p),
            _entrevistas(p), _valoracion(p), _gobierno(p)]
    bien = [_calidad_trazabilidad(p), *_calidad_controles(p), _barrido(p),
            _calidad_documental(p), _calidad_revision(p)]
    todo = esta + bien
    dudas = [x for x in todo if x["estado"] == NO_SE]
    faltan = [x for x in todo if x["estado"] == PENDIENTE]
    listo = not dudas and not faltan
    return {
        "proyecto": p, "esta": esta, "bien": bien,
        "cuando": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "pendientes": len(faltan), "dudas": len(dudas),
        "estado": HECHO if listo else (NO_SE if dudas else PENDIENTE),
        # LO QUE SE PUEDE FIRMAR. Mientras haya una sola duda o una sola
        # falta, el informe sale con limitaciones declaradas. Es la regla de
        # cautela del dossier de traspaso, aplicada por la máquina.
        "puede_firmarse": listo,
        "dicho": ("Se puede emitir el informe sin limitaciones."
                  if listo else
                  "El informe debe salir con limitaciones de alcance "
                  "declaradas: hay cosas que faltan o que no puedo "
                  "comprobar."),
    }
