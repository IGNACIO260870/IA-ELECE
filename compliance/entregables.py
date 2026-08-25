# -*- coding: utf-8 -*-
r"""
entregables.py

Qué se entrega, con qué nombre, quién lo firma y cómo entra en el sistema de
calidad.

Ignacio, 25/08/2026: "quiero un diseño de entregables" y "mucha atención a la
ISO y a la calidad".

LA REGLA QUE ORDENA TODO ESTO: un documento que no lleva código, versión y
firma no es un entregable, es un borrador con membrete. En un sistema de
calidad, la información documentada tiene que estar identificada, revisada,
aprobada y controlada -si no, la propia auditoría de calidad lo levanta como
no conformidad-. Así que el código no se pone al final: se pone al crearlo.

EL CÓDIGO. ELC-CP-<CLIENTE>-<TIPO>-<nn>, donde CP es compliance penal:

    ELC-CP-CLIENTE-MTZ-01 v1.0     la matriz de riesgos
    ELC-CP-CLIENTE-INF-01 v1.0     el informe
    ELC-CP-CLIENTE-PAC-01 v1.0     el plan de acción

CUATRO ESTADOS Y NO SE SALTAN: borrador -> revisado -> aprobado -> emitido.
Lo que está en borrador no sale del despacho. Lo que se emite, se registra.

LO QUE SE VUELCA A CALIDAD. Ignacio quería las dos cosas -codificación y
volcado-, así que cada hallazgo del informe genera su ficha con responsable,
plazo y VERIFICACIÓN DE EFICACIA, que es la parte que casi nadie cierra y la
que de verdad demuestra que el sistema funciona.
"""
from __future__ import annotations

from datetime import datetime, timedelta

# Los cuatro grupos son los del dossier de traspaso: ejecutivos, técnicos,
# operativos y de grupo societario. Se conservan porque son los que espera
# cada audiencia distinta -el Consejo no lee una matriz, y el compliance
# officer no se conforma con un resumen-.
CATALOGO = [
    # (tipo, nombre, grupo, audiencia, de dónde sale)
    ("INF", "Informe ejecutivo de evaluación de riesgos penales", "Ejecutivo",
     "Órgano de administración",
     "Se genera del proyecto: alcance, método, resultados y limitaciones."),
    ("CDM", "Cuadro de mando de riesgos", "Ejecutivo",
     "Órgano de administración · dirección",
     "Distribución por bandas, no medias. Inherente contra residual."),
    ("MTZ", "Matriz de riesgos penales", "Técnico",
     "Órgano de compliance penal",
     "Delito, conducta, probabilidad, impacto, controles y residual."),
    ("MET", "Metodología de evaluación (anexo)", "Técnico",
     "Órgano de compliance · auditor externo",
     "Escalas, criterios, pesos y reglas. Es lo que hace defendible la matriz."),
    ("PLA", "Plan de trabajo y muestreo", "Técnico", "Interno · cliente",
     "Alcance, entidades, procesos, periodo, exclusiones y razón del muestreo."),
    ("REV", "Registro de evidencias", "Operativo", "Interno",
     "Recibidas, pendientes y no aplicables, con fecha y quién las aportó."),
    ("HAL", "Registro de hallazgos", "Operativo", "Órgano de compliance",
     "Criterio, evidencia, hecho, riesgo, clasificación y fundamento."),
    ("PAC", "Plan de acción", "Operativo", "Dirección · responsables de área",
     "Acción, responsable, plazo y método de verificación de eficacia."),
    ("MAD", "Mapa de filiales y madurez", "Grupo", "Órgano de administración",
     "Sólo en grupos: despliegue efectivo por filial."),
]

# La clasificación de hallazgos del dossier. Cada uno arrastra un plazo
# distinto porque no es lo mismo un fallo sistémico que una sugerencia.
HALLAZGOS = {
    "nc_mayor": ("No conformidad mayor",
                 "Ausencia total de un requisito, fallo sistémico, ineficacia "
                 "significativa, incumplimiento legal relevante o falta de "
                 "despliegue en una filial crítica.", 30),
    "nc_menor": ("No conformidad menor",
                 "Desviación puntual que no compromete globalmente la eficacia "
                 "del sistema.", 90),
    "observacion": ("Observación",
                    "Debilidad o tendencia que podría desembocar en "
                    "incumplimiento si no se gestiona.", 180),
    "mejora": ("Oportunidad de mejora",
               "Recomendación para reforzar el sistema sin que exista "
               "incumplimiento acreditado.", 365),
}

# Las cuatro conclusiones graduadas, tal cual venían en el dossier. No se
# inventan otras: una conclusión que no está en esta lista es una opinión.
CONCLUSIONES = [
    "Adaptado plenamente a UNE 19601:2025.",
    "Adaptado con desviaciones menores.",
    "Parcialmente adaptado y pendiente de cierre de brechas.",
    "No preparado para una auditoría externa de transición.",
]

ESTADOS = ["borrador", "revisado", "aprobado", "emitido"]


# Formas societarias y palabras que no identifican a nadie: si el código
# saliera de las primeras letras, "COMERCIAL RIOJANA, S.L." daría COMERCIA, y
# el que identifica al cliente es RIOJANA.
_RELLENO = {"SL", "SA", "SLU", "SAU", "SCP", "SC", "SLL", "SAL", "SOCIEDAD",
            "LIMITADA", "ANONIMA", "ANÓNIMA", "UNIPERSONAL", "COMERCIAL",
            "INDUSTRIAL", "GRUPO", "COMPANIA", "COMPAÑIA", "COMPAÑÍA", "DE",
            "DEL", "LA", "EL", "LOS", "LAS", "Y", "E"}


def codigo(cliente, tipo, orden=1):
    """El código del documento. Se asigna al crearlo, no al terminarlo."""
    palabras = [
        "".join(ch for ch in p.upper() if ch.isalnum())
        for p in (cliente or "").replace(",", " ").replace(".", " ").split()]
    utiles = [p for p in palabras if p and p not in _RELLENO]
    corto = (max(utiles, key=len) if utiles
             else ("".join(palabras)[:8] or "XXXX"))
    return f"ELC-CP-{corto[:10]}-{tipo}-{orden:02d}"


def portada(proyecto, tipo, orden=1, version="1.0"):
    """Los datos de control documental que exige un sistema de calidad."""
    entrada = next((c for c in CATALOGO if c[0] == tipo), None)
    if entrada is None:
        return None
    _, nombre, grupo, audiencia, origen = entrada
    return {
        "codigo": codigo(proyecto.get("empresa", ""), tipo, orden),
        "titulo": nombre, "grupo": grupo, "audiencia": audiencia,
        "origen": origen, "version": version, "estado": "borrador",
        "empresa": proyecto.get("empresa", ""),
        "elaborado": proyecto.get("elaborado", ""),
        "revisado": proyecto.get("revisado", ""),
        "aprobado": proyecto.get("aprobado", ""),
        "fecha": datetime.now().strftime("%d/%m/%Y"),
        # SIN CONFORMIDAD DECLARADA. Va en todos, siempre, aunque el
        # resultado sea bueno: este trabajo no certifica nada.
        "aviso": ("Documento de trabajo de Elece Legal. No declara "
                  "conformidad, certificabilidad ni adecuación plena a "
                  "UNE 19601:2025."),
    }


def ficha_de_calidad(hallazgo, abierto=None):
    """Un hallazgo convertido en no conformidad para el sistema de calidad.

    Aquí es donde el informe deja de ser un PDF y pasa a ser trabajo con
    responsable y fecha. Sin la verificación de eficacia, una acción
    correctiva sólo demuestra que alguien hizo algo, no que sirviera.
    """
    clase = hallazgo.get("clase", "observacion")
    nombre, criterio, dias = HALLAZGOS.get(clase, HALLAZGOS["observacion"])
    inicio = abierto or datetime.now()
    return {
        "clase": clase, "clase_nombre": nombre, "criterio_uso": criterio,
        "criterio": hallazgo.get("criterio", ""),
        "evidencia": hallazgo.get("evidencia", ""),
        "hecho": hallazgo.get("hecho", ""),
        "riesgo": hallazgo.get("riesgo", ""),
        "accion": hallazgo.get("accion", ""),
        "responsable": hallazgo.get("responsable", ""),
        "abierto": inicio.strftime("%d/%m/%Y"),
        "plazo": (inicio + timedelta(days=dias)).strftime("%d/%m/%Y"),
        "verificacion": hallazgo.get("verificacion", ""),
        "eficacia_verificada": False,
        "cerrado": False,
    }


def del_proyecto(proyecto):
    """Los entregables que le tocan a este proyecto, con su código ya puesto."""
    hay_grupo = bool((proyecto.get("alcance") or "").strip()) and \
        "filial" in (proyecto.get("alcance") or "").lower()
    fuera = []
    for tipo, nombre, grupo, audiencia, origen in CATALOGO:
        if tipo == "MAD" and not hay_grupo:
            continue
        fuera.append({
            "tipo": tipo, "nombre": nombre, "grupo": grupo,
            "audiencia": audiencia, "origen": origen,
            "codigo": codigo(proyecto.get("empresa", ""), tipo),
            "estado": (proyecto.get("entregables_estado", {}) or {})
                      .get(tipo, "pendiente"),
        })
    return fuera
