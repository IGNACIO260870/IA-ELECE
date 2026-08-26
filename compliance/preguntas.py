# -*- coding: utf-8 -*-
r"""
preguntas.py

Lo que hay que preguntar para poder hacer la matriz, en el orden en que se
pregunta.

Ignacio, 26/08/2026: "he abierto un proyecto de Cáritas Monzón, pero no me
preguntas lo que necesitas de la Excel". Justo: habíamos acordado que el
sistema de trabajo era ir preguntando una cosa cada vez, y la pantalla no
preguntaba nada. Esto lo arregla.

UNA CADA VEZ, Y EN ESTE ORDEN. No es un formulario largo: es la siguiente
pregunta. El orden importa porque cada respuesta condiciona a la siguiente
-sin áreas no hay a quién entrevistar, sin alcance no se puede limitar una
conclusión-.

CADA PREGUNTA DICE PARA QUÉ SIRVE. Lo que se pide sin explicar por qué se
contesta a desgana y mal. Y en este trabajo, además, la respuesta acaba en un
informe que firma alguien.

LO QUE NO SE PREGUNTA. Lo que se puede averiguar solo -el catálogo de
delitos, la validez del CIF, lo que está publicado en registros- no se
pregunta: se trae hecho para que sólo haya que confirmarlo.
"""
from __future__ import annotations

# (campo, pregunta, ayuda, para_qué, tipo, opciones)
#   tipo: "texto" · "largo" · "opciones" · "lista" · "fecha_hoy" · "apetito"
PREGUNTAS = [
    ("alcance",
     "¿Qué entra y qué no entra en el trabajo?",
     "Sociedad o sociedades, centros, actividades y lo que se deja fuera "
     "expresamente. Ejemplo: «la asociación y sus tres centros de Monzón; "
     "quedan fuera las delegaciones de otras provincias».",
     "Sin alcance no se puede limitar una conclusión, y toda conclusión de "
     "este trabajo lleva sus limitaciones escritas.",
     "largo", None),

    ("periodo",
     "¿Qué periodo se revisa?",
     "Ejemplo: «ejercicios 2024 y 2025» o «situación a 26/08/2026».",
     "Determina qué evidencia vale y cuál está caducada.",
     "texto", None),

    ("audiencia",
     "¿Para quién es el informe?",
     "Quien lo va a leer decide el tono y la profundidad.",
     "El órgano de administración no lee una matriz; el compliance officer "
     "no se conforma con un resumen.",
     "opciones",
     ["Órgano de administración", "Comisión de auditoría",
      "Órgano de compliance penal", "Dirección", "Auditor externo"]),

    ("areas",
     "¿Qué áreas o departamentos tiene la organización?",
     "Separadas por comas. Si es pequeña, valen tres o cuatro: no hace falta "
     "inventar organigrama.",
     "De aquí salen las entrevistas y el dueño de cada riesgo. Sin áreas no "
     "hay a quién preguntar ni a quién asignar.",
     "lista", None),

    ("catalogo_cotejado",
     "¿Has cotejado el catálogo de delitos contra el Código Penal vigente?",
     "El catálogo que trae la herramienta es la versión 2026.1 y lleva tres "
     "referencias marcadas para verificar.",
     "El apartado 4.5.2 de la UNE 19601:2025 exige considerar todos los "
     "delitos del CP vigente. Mientras no conste la fecha del cotejo, no se "
     "puede afirmar que esté al día.",
     "fecha_hoy", None),

    ("barrido_publico",
     "¿Se ha hecho el barrido de fuentes públicas?",
     "BORME, sanciones, CENDOJ, subvenciones y la propia web. Está en "
     "Herramientas → Documentación de la empresa.",
     "Es lo que comprueba el HISTORIAL de la organización. Sin él, la "
     "probabilidad se apoya sólo en lo que cuenten en la entrevista, que es "
     "por definición la versión de quien responde.",
     "fecha_hoy", None),

    ("elaborado",
     "¿Quién elabora el documento?",
     "Nombre y apellidos, como van a figurar en la portada.",
     "Un documento sin firma no entra en un sistema de calidad.",
     "texto", None),

    ("revisado",
     "¿Quién lo revisa?",
     "Tiene que ser alguien distinto de quien lo elabora.",
     "ISO 9001, información documentada: elaborar y revisar no pueden ser la "
     "misma persona.",
     "texto", None),

    ("aprobado",
     "¿Quién lo aprueba?",
     "Quien responde del entregable ante el cliente.",
     "Es la firma que convierte el borrador en entregable.",
     "texto", None),

    ("disparadores",
     "¿Qué obliga a rehacer la evaluación?",
     "Marca los que apliquen. Se pueden añadir más luego.",
     "El apartado 6.3 de la UNE 19601:2025 -nuevo en esta edición- exige "
     "planificar los cambios. Una matriz sin disparadores envejece sin que "
     "nadie se entere: la anterior tenía cuatro años.",
     "opciones_varias",
     ["Reforma del Código Penal que afecte al catálogo",
      "Nueva actividad, producto o mercado",
      "Nuevo centro, filial o jurisdicción",
      "Incidente, denuncia, inspección o expediente sancionador",
      "Cambio del órgano de compliance o del órgano de gobierno",
      "Resultado de auditoría interna o externa"]),

    ("apetito",
     "¿Qué umbral de riesgo ha aprobado el órgano de gobierno?",
     "De 1 a 25. Por encima de ese número, el plan de acción es obligatorio.",
     "ESTO NO LO PONE ELECE. Decidir qué riesgo se acepta es una "
     "responsabilidad indelegable del órgano de gobierno del cliente. "
     "Mientras esté vacío, el informe lo dice, y esa ausencia es en sí misma "
     "un hallazgo.",
     "apetito", None),
]


def _contestada(p, campo):
    v = p.get(campo)
    if campo == "apetito":
        return v is not None
    if isinstance(v, list):
        return bool(v)
    return bool(str(v or "").strip())


def pendientes(p):
    """Las preguntas que quedan, en orden."""
    return [q for q in PREGUNTAS if not _contestada(p, q[0])]


def siguiente(p):
    """La siguiente, o None si están todas."""
    q = pendientes(p)
    return q[0] if q else None


def cuantas(p):
    return len(PREGUNTAS) - len(pendientes(p)), len(PREGUNTAS)


def guardar_respuesta(p, campo, valor):
    """Deja la respuesta en el proyecto, con el formato que le toca."""
    if campo == "areas":
        p["areas"] = [x.strip() for x in str(valor or "").split(",") if x.strip()]
    elif campo == "disparadores":
        p["disparadores"] = ([valor] if isinstance(valor, str)
                             else list(valor or []))
    elif campo == "apetito":
        try:
            p["apetito"] = int(str(valor).strip())
        except (TypeError, ValueError):
            p["apetito"] = None
    else:
        p[campo] = str(valor or "").strip()
    return p
