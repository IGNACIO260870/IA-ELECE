# -*- coding: utf-8 -*-
"""
preguntador.py

PREGUNTARLE A CLAUDE, POR ENCIMA DE TODOS LOS PROYECTOS.

DE DÓNDE VIENE. Ignacio, 02/09/2026: "necesito que crees un preguntador, es
decir, una herramienta que sirva para lo que hacemos tú y yo aquí, en la que
Mamen pueda preguntarte todo lo que necesite, que esté por encima de todos
los proyectos".

QUÉ SIGNIFICA «POR ENCIMA». Las demás pantallas de IA ELECE trabajan dentro
de un expediente: el proyecto de Cáritas, el de Salgar. Esto no. Aquí se
puede preguntar «¿en qué se parecen los controles de Cáritas Zaragoza y los
de Salgar?» o «¿qué me falta por cerrar en todos?», y para eso la respuesta
necesita ver todos los proyectos a la vez. Así que en cada pregunta va, como
contexto, el resumen de todos.

EL RESUMEN, NO LOS EXPEDIENTES ENTEROS. Va la ficha de cada proyecto -qué
empresa, qué trabajo, en qué punto está, cuántas áreas, conductas, controles
y entrevistas tiene, si el apetito está firmado- y no las transcripciones ni
las valoraciones una a una. Con eso se contesta lo transversal; para el
detalle de un expediente está su propia pantalla, que lo enseña entero.

LA CONVERSACIÓN SE GUARDA POR PERSONA. Mamen puede cerrar el navegador y
volver: lo suyo sigue ahí. Y lo de cada una es suyo: no se mezclan.

LO QUE NO HACE. No toca ningún expediente. Lee y contesta. Cambiar un dato
de un proyecto se hace en su pantalla, donde queda constancia de quién lo
cambió; que un chat pudiera escribir en los expedientes sería perder eso.
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ / "compliance") not in sys.path:
    sys.path.insert(0, str(RAIZ / "compliance"))

CARPETA = RAIZ / "datos" / "preguntador"
MODELO = "claude-opus-5"
MAX_TOKENS = 16000

# Cuántos turnos se mandan de vuelta. La conversación entera se guarda; al
# modelo se le manda la cola, que es lo que hace falta para seguir el hilo
# sin que cada pregunta cueste como la primera.
TURNOS = 30


# ---------------------------------------------------------------------------
# La clave de la API
# ---------------------------------------------------------------------------
def _cliente():
    """El cliente de Anthropic, con la clave que ya usa Colibrí.

    LA CLAVE NO SE DUPLICA. Está en `kmaleon/.env` y de ahí la lee el
    notificador desde hace meses. Tener una segunda copia aquí sería tener
    dos sitios donde caducar.
    """
    import anthropic                                     # noqa: PLC0415
    if not os.environ.get("ANTHROPIC_API_KEY"):
        env = Path(os.environ.get(
            "COLIBRI_ENV",
            r"C:/Users/Ignacio/Desktop/colibri-servidor/kmaleon/.env"))
        try:
            for linea in env.read_text(encoding="utf-8").splitlines():
                if linea.strip().startswith("ANTHROPIC_API_KEY"):
                    os.environ["ANTHROPIC_API_KEY"] = \
                        linea.split("=", 1)[1].strip().strip('"').strip("'")
                    break
        except Exception:                                # noqa: BLE001
            pass
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise RuntimeError(
            "no encuentro la clave de la API (ANTHROPIC_API_KEY). Está en "
            "colibri-servidor/kmaleon/.env")
    return anthropic.Anthropic()


# ---------------------------------------------------------------------------
# El contexto: todos los proyectos, resumidos
# ---------------------------------------------------------------------------
def _ficha(p):
    conductas = p.get("conductas") or []
    valoradas = sum(1 for c in conductas
                    if c.get("probabilidad") or c.get("impacto"))
    entrevistas = p.get("entrevistas") or []
    partes = [
        f"· {p.get('empresa') or p.get('clave')}",
        f"  clave interna: {p.get('clave')}",
        f"  trabajo: {p.get('tipo_trabajo') or '(sin especificar)'}",
    ]
    if p.get("cif"):
        partes.append(f"  CIF: {p['cif']}")
    if p.get("responsable"):
        partes.append(f"  responsable: {p['responsable']}")
    if p.get("alcance"):
        partes.append(f"  alcance: {p['alcance']}")
    if p.get("periodo"):
        partes.append(f"  periodo: {p['periodo']}")
    partes.append(
        f"  tamaño: {len(p.get('areas') or [])} áreas, {len(conductas)} "
        f"conductas ({valoradas} valoradas), "
        f"{len(p.get('controles') or [])} controles, "
        f"{len(entrevistas)} entrevistas, "
        f"{len(p.get('documentos') or [])} documentos")
    if p.get("apetito") is None:
        partes.append("  apetito de riesgo: SIN FIRMAR por el órgano de "
                      "gobierno del cliente")
    else:
        partes.append(f"  apetito de riesgo: {p['apetito']} "
                      f"(firmado por {p.get('apetito_firmado_por') or '?'})")
    if entrevistas:
        areas = sorted({str(e.get("area") or "").strip()
                        for e in entrevistas if e.get("area")})
        if areas:
            partes.append("  entrevistas por área: " + ", ".join(areas))
    if p.get("nota_metodologica"):
        partes.append(f"  nota metodológica: "
                      f"{' '.join(str(p['nota_metodologica']).split())[:300]}")
    return "\n".join(partes)


def contexto():
    """Todo lo que hay abierto en IA ELECE, en texto."""
    import proyectos                                     # noqa: PLC0415
    try:
        ps = proyectos.listar()
    except Exception as e:                               # noqa: BLE001
        return f"(no he podido leer los proyectos: {e})"
    if not ps:
        return "No hay ningún proyecto abierto todavía."
    cabeza = (f"Hay {len(ps)} proyectos abiertos en IA ELECE. Ficha de cada "
              f"uno:\n\n")
    return cabeza + "\n\n".join(_ficha(p) for p in ps)


def _metodologia():
    """Las reglas con las que se valora, para no inventarse otras."""
    try:
        import metodologia                               # noqa: PLC0415
        texto = getattr(metodologia, "RESUMEN", None) or \
            (metodologia.__doc__ or "")
        return " ".join(str(texto).split())[:4000]
    except Exception:                                    # noqa: BLE001
        return ""


SISTEMA_BASE = """Eres el asistente de IA ELECE, la parte de abogacía del \
despacho Elece Legal (Zaragoza). Trabajas sobre todo con Mamen, que es la \
abogada que lleva los proyectos de compliance, e Ignacio Tartón, procurador \
y socio.

QUÉ ES ESTA PANTALLA. Es el «Preguntador»: está por encima de los \
expedientes, así que aquí se pregunta lo transversal -comparar proyectos, \
ver qué falta, resolver una duda de método o de norma- y no el detalle de \
un expediente concreto, que se ve en su propia pantalla.

CÓMO CONTESTAS.
- En español, directa y brevemente. Sin preámbulos ni resúmenes de lo que te \
acaban de preguntar.
- Si la respuesta está en los proyectos, dices en cuál. Si no está, lo dices \
en vez de rellenar el hueco: «eso no consta en ningún proyecto».
- Distingues siempre lo que sabes por los datos de los proyectos de lo que \
sabes por conocimiento general de la materia. Son dos cosas distintas y \
confundirlas es lo peor que puedes hacer aquí.
- No inventas cifras, valoraciones, artículos ni fechas. Si un dato no está, \
falta, y decirlo es la respuesta correcta.
- Cuando te pidan criterio jurídico, lo das razonado, pero recordando que la \
decisión y la firma son de la abogada.

LO QUE NO PUEDES HACER. No escribes en los expedientes. Si de la \
conversación sale algo que hay que guardar, dices en qué pantalla se hace, \
y lo hace la persona."""


def _sistema():
    partes = [SISTEMA_BASE]
    met = _metodologia()
    if met:
        partes.append("METODOLOGÍA CON LA QUE SE VALORA EN ESTA CASA "
                      "(no uses otra sin avisar):\n" + met)
    partes.append("ESTADO DE LOS PROYECTOS ABIERTOS:\n" + contexto())

    # EL MATERIAL DE LAS DOS MARCAS. Los briefings que subió Ignacio traen lo
    # que hace falta para contestar bien: quién es quién, las dos identidades,
    # los proyectos activos, la formación de RRHH y lo que quedó pendiente.
    # Sin esto, el Preguntador sabría de los expedientes y de nada más.
    try:
        import material as MAT                           # noqa: PLC0415
        material = MAT.para_el_preguntador()
        if material:
            partes.append(
                "MATERIAL DE LAS DOS MARCAS -elece Legal y LawScale Digital-: "
                "briefings, propuestas y documentos base. Cítalos por su "
                "nombre de fichero cuando los uses.\n\n" + material)
    except Exception:                                    # noqa: BLE001
        pass
    return "\n\n".join(partes)


# ---------------------------------------------------------------------------
# La conversación, guardada por persona
# ---------------------------------------------------------------------------
def _fichero(usuario):
    # El nombre viene de la sesión, pero se limpia igual: nunca se construye
    # una ruta con algo que venga de fuera sin filtrarlo.
    limpio = re.sub(r"[^a-z0-9_-]", "", (usuario or "anonimo").lower()) or "anonimo"
    CARPETA.mkdir(parents=True, exist_ok=True)
    return CARPETA / f"{limpio}.json"


def historial(usuario):
    try:
        return json.loads(_fichero(usuario).read_text(encoding="utf-8"))
    except Exception:                                    # noqa: BLE001
        return []


def _guardar(usuario, turnos):
    _fichero(usuario).write_text(
        json.dumps(turnos, indent=2, ensure_ascii=False), encoding="utf-8")


def borrar(usuario):
    """Empezar de cero. La conversación anterior no se recupera."""
    f = _fichero(usuario)
    if f.exists():
        f.unlink()
    return True


def preguntar(usuario, texto):
    """Una pregunta, con el hilo y el estado de todos los proyectos."""
    import anthropic                                     # noqa: PLC0415

    texto = (texto or "").strip()
    if not texto:
        return {"ok": False, "dicho": "no has escrito nada"}

    turnos = historial(usuario)
    mensajes = [{"role": t["quien"], "content": t["texto"]}
                for t in turnos[-TURNOS:]]
    mensajes.append({"role": "user", "content": texto})

    try:
        cli = _cliente()
        r = cli.messages.create(
            model=MODELO,
            max_tokens=MAX_TOKENS,
            # El sistema lleva el estado de TODOS los proyectos y no cambia
            # entre preguntas seguidas: cachearlo evita pagarlo cada vez.
            system=[{"type": "text", "text": _sistema(),
                     "cache_control": {"type": "ephemeral"}}],
            thinking={"type": "adaptive"},
            messages=mensajes,
        )
    except anthropic.AuthenticationError:
        return {"ok": False, "dicho": "la clave de la API no vale"}
    except anthropic.RateLimitError:
        return {"ok": False, "dicho": "hay demasiadas peticiones ahora mismo; "
                                      "espera un momento y repite"}
    except anthropic.APIConnectionError:
        return {"ok": False, "dicho": "no hay salida a internet desde este "
                                      "equipo"}
    except anthropic.APIStatusError as e:                # noqa: BLE001
        return {"ok": False, "dicho": f"la API ha respondido {e.status_code}: "
                                      f"{str(e.message)[:120]}"}
    except Exception as e:                               # noqa: BLE001
        return {"ok": False, "dicho": f"no he podido preguntar: {str(e)[:140]}"}

    if r.stop_reason == "refusal":
        return {"ok": False, "dicho": "no puedo contestar a eso"}

    respuesta = "\n".join(b.text for b in r.content if b.type == "text").strip()
    if not respuesta:
        return {"ok": False, "dicho": "ha vuelto vacío; prueba a reformular"}

    ahora = datetime.now().isoformat(timespec="seconds")
    turnos.append({"quien": "user", "texto": texto, "cuando": ahora})
    turnos.append({"quien": "assistant", "texto": respuesta,
                   "cuando": datetime.now().isoformat(timespec="seconds")})
    _guardar(usuario, turnos)
    return {"ok": True, "respuesta": respuesta, "turnos": len(turnos)}
