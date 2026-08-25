# -*- coding: utf-8 -*-
r"""
metodologia.py

Cómo se calcula un riesgo penal en Elece. El motor, y el porqué de cada
número.

DE DÓNDE VIENE. Ignacio, 25/08/2026: "necesitamos mejorar el cálculo de
probabilidad, el impacto y la evaluación de riesgos, de manera que
consigamos crear un sistema más preciso y más científico y que su
explicación a un cliente sea más fácil y más eficiente". Y la frase que
manda sobre todo lo demás: "hacemos un TRAJE A MEDIDA para cada empresa".

QUÉ SE ARREGLA RESPECTO A LO QUE HABÍA. En la matriz que había (julio 2022)
el riesgo era ((P+I)/2)×0,2. Una media hace que probabilidad 5 con impacto 1
valga lo mismo que probabilidad 1 con impacto 5 -los dos 0,6- y eso no hay
cliente que lo acepte cuando se le explica. Aquí el riesgo es PRODUCTO, como
en el mapa de aplicabilidad v2, y cada eje se construye con criterios
objetivos en vez de con una impresión.

LAS TRES PREGUNTAS QUE RESPONDE, EN ESTE ORDEN:

    ¿Puede pasar aquí?     -> aplicabilidad (sí/no, con motivo escrito)
    ¿Cómo de probable?     -> exposición + frecuencia del delito + historial
    ¿Cómo de grave?        -> penas del art. 33.7 + lo que la empresa expone
    ¿Qué lo contiene?      -> controles, que multiplican, no restan

NO PUNTÚA NADIE MÁS QUE UNA PERSONA. La herramienta propone el número y
escribe por qué; quien lo confirma y lo firma es Mamen. Un número puesto por
una máquina y sin firma no se sostiene delante de un juez, y menos con la
doctrina del Supremo de 2025 -SSTS 768/2025 y 836/2025-, que exige a la
acusación probar el defecto estructural: lo que hay que poder enseñar es
criterio humano trazable, no una salida de un programa.
"""
from __future__ import annotations

# ---------------------------------------------------------------------------
# LA ESCALA
# ---------------------------------------------------------------------------
# Entera de 1 a 5 en los dos ejes. Ignacio, sobre si conservar el 0,5 de la
# matriz vieja: "lo que sea más acorde con la ISO". La ISO 31000 y las
# escalas al uso son enteras; el 0,5 no era un nivel, era el truco para
# escribir "no aplica" dentro de la puntuación. Ahora "no aplica" es un
# campo con su motivo y desaparece de la aritmética.
MINIMO, MAXIMO = 1, 5

# Las bandas son las del mapa de aplicabilidad v2, que ya estaban decididas.
# Cada una lleva pegada una decisión: una banda que no dice qué hacer no
# sirve de nada.
BANDAS = [
    (1, 4, "Bajo", "Seguimiento ordinario."),
    (5, 9, "Medio", "Revisión de exposición y evidencias."),
    (10, 15, "Alto", "Análisis prioritario y contraste con controles."),
    (16, 25, "Crítico", "Escalado y análisis inmediato."),
]


def banda(puntuacion):
    """Nivel y tratamiento de una puntuación de 1 a 25."""
    for desde, hasta, nombre, trato in BANDAS:
        if desde <= puntuacion <= hasta:
            return {"nivel": nombre, "tratamiento": trato}
    return {"nivel": "?", "tratamiento": ""}


def _acotar(x):
    return max(MINIMO, min(MAXIMO, x))


# ---------------------------------------------------------------------------
# PROBABILIDAD
# ---------------------------------------------------------------------------
# Ignacio, 25/08/2026: "una de tus misiones es ayudarme a determinar unos
# criterios objetivos de probabilidad e impacto, más allá del número de
# departamentos. Podemos usar el número de condenas que haya por ese delito o
# sanciones que haya recibido la empresa".
#
# De ahí salen los tres factores. Cada uno se puede enseñar y discutir:
#
#   EXPOSICIÓN        ¿hace la empresa la actividad que produce ese delito, y
#                     cuánto? Sale de la entrevista y de la documentación:
#                     objeto social, mapa de procesos, volumen anual, número
#                     de terceros, geografías, licitaciones.
#   FRECUENCIA        ¿cuántas condenas hay en España por ese delito? Sale de
#                     la Estadística de Condenados del INE (explotación del
#                     Registro Central de Penados) y del CGPJ. Es el dato que
#                     convierte "me parece raro" en "en toda España hay N al
#                     año".
#   HISTORIAL         ¿le ha pasado ya a ESTA empresa? Sanciones, expedientes,
#                     denuncias, requerimientos, incidentes internos. Ignorar
#                     las infracciones administrativas previas es uno de los
#                     errores clásicos de una matriz de riesgos.
#
# PESOS. La exposición manda porque es lo único específico de esta empresa, y
# el traje es a medida. La frecuencia es contexto y el historial es señal.
PESO_EXPOSICION, PESO_FRECUENCIA, PESO_HISTORIAL = 0.50, 0.30, 0.20

EXPOSICION = {
    1: "La empresa no realiza la actividad, o sólo de forma anecdótica.",
    2: "Existe de forma ocasional, con volumen bajo o en un solo punto.",
    3: "Es recurrente y forma parte de procesos ordinarios.",
    4: "Es frecuente, económicamente relevante o con terceros e intermediarios.",
    5: "Es estructural o crítica para el negocio, o se hace en varias "
       "geografías o filiales.",
}

FRECUENCIA = {
    1: "Prácticamente no se condena a personas jurídicas por este delito.",
    2: "Condenas aisladas en la serie estadística.",
    3: "Condenas regulares, sin ser de los tipos más frecuentes.",
    4: "Está entre los tipos que más se imputan a personas jurídicas.",
    5: "Es de los más condenados y con criterio consolidado del Supremo.",
}

HISTORIAL = {
    1: "Sin antecedentes ni incidentes conocidos.",
    2: "Consultas o dudas internas, sin expediente.",
    3: "Requerimiento, inspección o denuncia interna sin sanción.",
    4: "Sanción administrativa o expediente en el ámbito de este delito.",
    5: "Condena, sanción firme grave o reincidencia.",
}


def probabilidad(exposicion, frecuencia, historial):
    """Los tres factores en un número de 1 a 5, y por qué sale ese.

    DOS REGLAS QUE PESAN MÁS QUE LA MEDIA, y las dos se explican en una
    frase delante de un cliente:

      - Si la empresa NO hace la actividad, no hay media que valga: es un 1
        y el delito debería estar marcado como no aplicable, con su motivo.
      - Si ya la han sancionado por eso, no se puede sostener que sea poco
        probable. El suelo es 4. Ésta es la que más discusiones ahorra.
    """
    e, f, h = _acotar(exposicion), _acotar(frecuencia), _acotar(historial)
    bruto = PESO_EXPOSICION * e + PESO_FRECUENCIA * f + PESO_HISTORIAL * h
    valor = int(round(bruto))
    razones = [f"exposición {e} ({EXPOSICION[e]})",
               f"frecuencia {f} ({FRECUENCIA[f]})",
               f"historial {h} ({HISTORIAL[h]})"]
    if e == 1:
        valor = 1
        razones.append("REGLA: la empresa no realiza la actividad, así que la "
                       "probabilidad es 1 al margen de los demás factores.")
    elif h >= 4:
        if valor < 4:
            razones.append(f"REGLA: hay antecedente sancionador, así que la "
                           f"probabilidad no baja de 4 (la media daba {valor}).")
        valor = max(valor, 4)
    return {"valor": _acotar(valor), "media": round(bruto, 2),
            "porque": razones}


# ---------------------------------------------------------------------------
# IMPACTO
# ---------------------------------------------------------------------------
# El mapa v2 ancló el impacto en las penas del art. 33.7 CP, y eso está bien
# pensado. El problema medido en ese fichero: 38 de 39 delitos puntuaban 4 o
# 5, porque casi cualquier delito del catálogo puede acabar en disolución.
# Un eje que no varía no es un eje.
#
# Se arregla con dos piezas:
#
#   SEVERIDAD   la pena que el tipo concreto prevé de verdad. Las letras b) a
#               g) del 33.7 -disolución, suspensión, clausura, prohibición,
#               inhabilitación, intervención- sólo se imponen si el delito las
#               prevé y concurren los requisitos del art. 66 bis. Reservar el
#               5 a los delitos donde la disolución está de verdad sobre la
#               mesa abre la escala sola.
#   EXPUESTO    lo que esa pena le hace A ESTA empresa. La inhabilitación para
#               contratar con el sector público es la muerte para quien vive
#               de licitaciones y da igual a quien no se presenta a ninguna.
#               Aquí es donde el impacto deja de ser una propiedad del delito
#               y pasa a ser una propiedad del cliente: el traje a medida.
SEVERIDAD = {
    1: "Multa de menor entidad, sin penas interdictivas.",
    2: "Multa o consecuencia económica relevante, sin afectación estructural.",
    3: "Multa relevante y posibilidad de penas interdictivas limitadas.",
    4: "Multa elevada o proporcional y posible suspensión, clausura, "
       "prohibición temporal o intervención judicial.",
    5: "Posible disolución, prohibición definitiva o inhabilitación severa.",
}

EXPUESTO = {
    -1: "La pena tipo apenas afecta a este negocio (no contrata con el sector "
        "público, no depende de un único centro, no necesita licencia).",
    0: "Afectación normal.",
    +1: "La pena tipo golpea el núcleo del negocio (vive de contratación "
        "pública o subvenciones, centro único, actividad licenciada o "
        "regulada).",
}


def impacto(severidad, expuesto=0):
    """La pena que prevé el tipo, corregida por lo que esta empresa expone."""
    s = _acotar(severidad)
    m = max(-1, min(1, int(expuesto)))
    valor = _acotar(s + m)
    razones = [f"severidad penal {s} ({SEVERIDAD[s]})"]
    if m:
        razones.append(f"ajuste {m:+d}: {EXPUESTO[m]}")
    return {"valor": valor, "porque": razones}


# ---------------------------------------------------------------------------
# CONTROLES
# ---------------------------------------------------------------------------
# En la matriz vieja cada control RESTABA puntos y se acumulaban sin límite:
# diez controles flojos sumaban -5 y hundían cualquier riesgo hasta el suelo.
# Aquí cada control quita un PORCENTAJE de lo que queda, así que el segundo
# control vale menos que el primero -que es como funciona en la realidad- y
# el riesgo nunca llega a cero por construcción, sin necesidad de trucos.
#
# Los pesos son los que dictó Ignacio el 25/08/2026, literal donde importa:
#
#   NATURALEZA  "preventivo debe ser mucho peso, detectivo mucho peso y
#               reactivo menos peso porque ya se ha incurrido en la conducta.
#               Realmente no es un control".
#   ESTADO      "implantado y comunicado mucho peso, aprobado mucho porque si
#               no lo está no lo puedes implantar ni comunicar, ignorado no lo
#               valoramos porque no es un control".
#   EVIDENCIA   "evidencia con mucho peso y sin muy poco".
#   ORIGEN      "debemos determinar los controles que reducen más o menos el
#               riesgo por venir determinados por normas de obligado
#               cumplimiento, o si son los que la empresa se impone, que son
#               los que más reducen". Cumplir la ley es el mínimo exigible; lo
#               que acredita cultura de compliance -y lo que mira un juez- es
#               lo que la empresa hace por encima de lo que le obligan.
EFICACIA_BASE = 0.35

NATURALEZA = {"preventivo": 1.00, "detectivo": 0.90, "reactivo": 0.30}
ESTADO = {"implantado": 1.00, "comunicado": 0.90, "aprobado": 0.60,
          "ignorado": 0.00}
EVIDENCIA = {"documentada": 1.00, "declarada": 0.15}
ORIGEN = {"autoimpuesto": 1.00, "obligado": 0.70}

# EL RIESGO NO SE APAGA. Por muchos controles que haya, queda un residuo: la
# propia norma parte de que existe riesgo residual, y un informe que dijera
# "riesgo cero" sería el primero en no creerse. El suelo es un porcentaje del
# inherente, no un número mágico metido en una fórmula.
SUELO_RESIDUAL = 0.20


def eficacia(control):
    """Cuánto quita un control, de 0 a 1. Y por qué.

    Un control IGNORADO no se valora: no es un control, es una intención.
    """
    nat = NATURALEZA.get(control.get("naturaleza", "preventivo"), 0.0)
    est = ESTADO.get(control.get("estado", "ignorado"), 0.0)
    evi = EVIDENCIA.get(control.get("evidencia", "declarada"), 0.0)
    ori = ORIGEN.get(control.get("origen", "obligado"), 0.0)
    valor = EFICACIA_BASE * nat * est * evi * ori
    return {"valor": round(valor, 4),
            "porque": (f"{control.get('naturaleza','?')} × "
                       f"{control.get('estado','?')} × "
                       f"{control.get('evidencia','?')} × "
                       f"{control.get('origen','?')}")}


def residual(inherente, controles):
    """El riesgo que queda después de los controles.

    R_res = R_inh × Π(1 − eficacia_i), con suelo. Multiplicativo: cada
    control muerde lo que dejó el anterior.
    """
    queda = 1.0
    detalle = []
    for c in controles or []:
        ef = eficacia(c)
        if ef["valor"] <= 0:
            detalle.append({**ef, "control": c.get("descripcion", ""),
                            "cuenta": False})
            continue
        queda *= (1 - ef["valor"])
        detalle.append({**ef, "control": c.get("descripcion", ""),
                        "cuenta": True})
    bruto = inherente * queda
    suelo = inherente * SUELO_RESIDUAL
    return {"valor": round(max(bruto, suelo), 2),
            "sin_suelo": round(bruto, 2),
            "reduccion": round((1 - queda) * 100, 1),
            "en_el_suelo": bruto < suelo,
            "controles": detalle}


# ---------------------------------------------------------------------------
# UNA CONDUCTA, Y UN DELITO
# ---------------------------------------------------------------------------
def evaluar_conducta(datos):
    """Una conducta delictiva concreta, de punta a punta.

    La unidad de análisis es la CONDUCTA, no el delito. Eso ya lo hacía bien
    la matriz anterior -227 conductas para 42 delitos- y se conserva: nadie
    controla "el blanqueo", se controla "aceptar cobros en efectivo por
    encima de X sin verificar el origen".
    """
    if not datos.get("aplica", True):
        return {"aplica": False,
                "motivo": datos.get("motivo_no_aplica", ""),
                "inherente": None, "residual": None}
    p = probabilidad(datos["exposicion"], datos["frecuencia"],
                     datos["historial"])
    i = impacto(datos["severidad"], datos.get("expuesto", 0))
    inh = p["valor"] * i["valor"]
    res = residual(inh, datos.get("controles"))
    return {"aplica": True,
            "probabilidad": p, "impacto": i,
            "inherente": inh, "banda_inherente": banda(inh),
            "residual": res["valor"],
            "banda_residual": banda(int(round(res["valor"]))),
            "detalle_residual": res}


def evaluar_delito(conductas):
    """El delito lo manda su PEOR conducta, no la media de sus conductas.

    POR QUÉ, con el caso que lo demostró. En la matriz anterior la hoja de
    Estafa tiene una conducta valorada con probabilidad 5 e impacto 4 -la
    puntuación más alta de todo el libro- y el delito llega al informe con un
    0,4, porque se promedia con siete conductas al mínimo. Pasa en cinco
    delitos de ese fichero. Una media reparte el peligro entre las conductas
    tranquilas hasta hacerlo desaparecer.

    Así que el nivel del delito es el máximo, y al lado va el recuento por
    banda, que es lo que de verdad se gestiona. La media se calcula y se
    guarda, pero como dato secundario y nunca como titular.
    """
    vivas = [c for c in conductas if c.get("aplica")]
    if not vivas:
        return {"aplica": False, "conductas": len(conductas)}
    inh = [c["inherente"] for c in vivas]
    res = [c["residual"] for c in vivas]
    reparto = {}
    for c in vivas:
        n = c["banda_residual"]["nivel"]
        reparto[n] = reparto.get(n, 0) + 1
    return {"aplica": True,
            "inherente": max(inh), "residual": max(res),
            "banda": banda(int(round(max(res)))),
            "media_inherente": round(sum(inh) / len(inh), 2),
            "media_residual": round(sum(res) / len(res), 2),
            "conductas": len(vivas), "reparto": reparto,
            "peor": max(vivas, key=lambda c: c["residual"])}


# ---------------------------------------------------------------------------
# EL APETITO DE RIESGO
# ---------------------------------------------------------------------------
# Ignacio, 25/08/2026, preguntado por el umbral: "umbral NO lo ponemos
# nosotros". Correcto, y además es lo que pide la UNE 19601:2025 al reforzar
# las responsabilidades indelegables del órgano de gobierno: decidir qué
# riesgo se acepta es una decisión de la empresa, no del auditor.
#
# Así que aquí no hay valor por defecto. Mientras esté vacío, el informe lo
# dice: "sin umbral aprobado" -y eso ya es un hallazgo-.
def sobre_el_umbral(evaluaciones, umbral):
    """Lo que supera el apetito aprobado. Sin umbral, no se puede afirmar."""
    if umbral is None:
        return {"hay_umbral": False,
                "aviso": ("el órgano de gobierno no ha aprobado un apetito de "
                          "riesgo: no se puede decir qué está por encima ni "
                          "qué plan de acción es obligatorio")}
    fuera = [e for e in evaluaciones
             if e.get("aplica") and e.get("residual", 0) > umbral]
    return {"hay_umbral": True, "umbral": umbral, "por_encima": fuera,
            "cuantos": len(fuera)}
