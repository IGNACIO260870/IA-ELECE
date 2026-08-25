# -*- coding: utf-8 -*-
r"""
fuentes.py

La documentación de la empresa: todo lo que se puede sacar del CIF sin
pedírselo a nadie.

Ignacio, 25/08/2026: "otra herramienta es la documentación de la empresa.
Ahí haremos los enlaces a la web, registros... todo lo que se pueda
automatizar desde el CIF de la empresa".

PARA QUÉ SIRVE DE VERDAD. No es una lista de enlaces bonita: cada fuente
alimenta un factor concreto de la valoración, y va marcado cuál. El
barrido público es lo que evita que la probabilidad se apoye sólo en lo que
cuenten en la entrevista -que es, por definición, la versión de quien
responde-.

    identidad   -> exposición   (a qué se dedica de verdad, dónde, tamaño)
    sanciones   -> historial    (y con él la regla del suelo 4)
    judicial    -> historial
    estadística -> frecuencia del delito
    la empresa  -> controles que ya existen y están publicados

LO QUE NO SE HACE. Sólo persona jurídica. De los administradores y demás
personas físicas no se busca nada sin encargo expreso y documentado: buscar
sobre una persona es tratamiento de datos personales y tiene sus propias
reglas.

HONESTIDAD CON LOS ENLACES. Los registros españoles casi nunca aceptan una
consulta por URL: hay que entrar y buscar. Así que cada fuente dice si el
enlace lleva DIRECTO al resultado o si deja en el buscador con el dato listo
para pegar. Prometer automatismo donde no lo hay sería el mejor modo de que
alguien diera por mirado lo que no ha mirado.
"""
from __future__ import annotations

import re
from urllib.parse import quote_plus

# ---------------------------------------------------------------------------
# EL CIF
# ---------------------------------------------------------------------------
# Comprobar la letra es lo primero que se puede automatizar y lo primero que
# evita un expediente abierto con un dígito mal copiado.
_LETRAS_ORG = "ABCDEFGHJNPQRSUVW"
_CONTROL = "JABCDEFGHI"


def validar_cif(cif):
    """Dice si el CIF es válido y de qué tipo de entidad es."""
    c = re.sub(r"[^0-9A-Za-z]", "", (cif or "")).upper()
    if len(c) != 9:
        return {"ok": False, "porque": "un CIF tiene 9 caracteres"}
    org, cuerpo, ultimo = c[0], c[1:8], c[8]
    if org not in _LETRAS_ORG or not cuerpo.isdigit():
        return {"ok": False, "porque": f"«{org}» no es una letra de organización"}
    pares = sum(int(cuerpo[i]) for i in (1, 3, 5))
    impares = 0
    for i in (0, 2, 4, 6):
        d = int(cuerpo[i]) * 2
        impares += d // 10 + d % 10
    resto = (10 - (pares + impares) % 10) % 10
    if org in "PQRSNW":                     # sólo letra de control
        bien = _CONTROL[resto] == ultimo
    elif org in "ABEH":                     # sólo dígito
        bien = str(resto) == ultimo
    else:                                   # cualquiera de los dos
        bien = ultimo in (str(resto), _CONTROL[resto])
    TIPOS = {"A": "Sociedad anónima", "B": "Sociedad limitada",
             "C": "Sociedad colectiva", "D": "Comanditaria",
             "E": "Comunidad de bienes", "F": "Cooperativa",
             "G": "Asociación o fundación", "H": "Comunidad de propietarios",
             "J": "Sociedad civil", "N": "Entidad extranjera",
             "P": "Corporación local", "Q": "Organismo público",
             "R": "Congregación religiosa", "S": "Órgano de la Administración",
             "U": "Unión temporal de empresas", "V": "Otros tipos",
             "W": "Establecimiento de no residente"}
    return {"ok": bien, "cif": c, "tipo": TIPOS.get(org, "—"),
            "porque": "" if bien else "la letra o el dígito de control no cuadra"}


# ---------------------------------------------------------------------------
# LAS FUENTES
# ---------------------------------------------------------------------------
# (bloque, nombre, qué aporta, alimenta, plantilla de URL, directo)
#   {cif} y {nombre} se sustituyen.
#   directo=True  -> el enlace lleva al resultado
#   directo=False -> lleva al buscador y el dato hay que pegarlo
FUENTES = [
    ("Identidad y estructura", "BORME · Boletín Oficial del Registro Mercantil",
     "Constitución, cambios de objeto social, nombramientos, ceses, "
     "traslados, ampliaciones y depósito de cuentas.",
     "exposición", "https://www.boe.es/buscar/borme.php", False),
    ("Identidad y estructura", "Registro Mercantil Central",
     "Denominación, datos registrales y solicitud de nota simple o informe.",
     "exposición", "https://www.rmc.es/", False),
    ("Identidad y estructura", "BOE · búsqueda por denominación",
     "Todo lo publicado sobre la sociedad en el boletín del Estado.",
     "exposición", "https://www.boe.es/buscar/boe.php?campo%5B0%5D=TIT&"
     "dato%5B0%5D={nombre}", False),
    ("Identidad y estructura", "Sede Electrónica del Catastro",
     "Inmuebles y centros de trabajo a nombre de la sociedad.",
     "exposición", "https://www.sedecatastro.gob.es/", False),

    ("Contratación y fondos públicos",
     "Plataforma de Contratación del Sector Público",
     "Licitaciones y adjudicaciones. Si vive de esto, la inhabilitación de "
     "la letra f) del art. 33.7 es letal: sube el ajuste de impacto.",
     "impacto", "https://contrataciondelestado.es/wps/portal/plataforma",
     False),
    ("Contratación y fondos públicos",
     "BDNS · Base de Datos Nacional de Subvenciones",
     "Subvenciones y ayudas concedidas. Alimenta el fraude de subvenciones "
     "y el fraude a los presupuestos de la UE.",
     "exposición", "https://www.infosubvenciones.es/bdnstrans/GE/es/index",
     False),

    ("Sanciones y expedientes", "AEAT · listado de deudores",
     "Deudores a la Hacienda Pública por encima del umbral legal.",
     "historial", "https://sede.agenciatributaria.gob.es/", False),
    ("Sanciones y expedientes", "Boletines autonómicos",
     "Resoluciones sancionadoras de medio ambiente, consumo, industria y "
     "trabajo. Es donde aparece casi todo lo que nadie cuenta en la "
     "entrevista.",
     "historial", "https://www.boe.es/legislacion/otros_diarios_oficiales.php",
     False),
    ("Sanciones y expedientes", "Inspección de Trabajo y Seguridad Social",
     "Actuación inspectora y sanciones en el ámbito laboral.",
     "historial", "https://www.mites.gob.es/itss/web/", False),

    ("Judicial", "CENDOJ · buscador de jurisprudencia",
     "Sentencias en las que aparece la sociedad. Una condena o una "
     "absolución por los pelos cambia la valoración entera.",
     "historial", "https://www.poderjudicial.es/search/indexAN.jsp", False),

    ("Estadística", "INE · Estadística de Condenados",
     "Cuántas condenas hay en España por cada tipo de delito. Es lo que "
     "convierte «me parece raro» en un dato.",
     "frecuencia", "https://www.ine.es/jaxiT3/Tabla.htm?t=25997", True),
    ("Estadística", "CGPJ · condenados, Registro Central de Penados",
     "La misma explotación, con desglose judicial.",
     "frecuencia", "https://www.poderjudicial.es/cgpj/es/Temas/"
     "Estadistica-Judicial/", True),

    ("La propia empresa", "Web corporativa",
     "Política de compliance, código de conducta, canal de denuncias, "
     "memoria, certificaciones. Muchas veces el control ya está publicado y "
     "se puede dar por documentado sin pedir nada.",
     "controles", "{web}", True),
    ("La propia empresa", "Búsqueda de prensa y reputación",
     "Lo que se ha publicado sobre la sociedad. Sólo persona jurídica.",
     "historial", "https://www.google.com/search?q={nombre_comillas}", True),
    ("La propia empresa", "ENAC · entidades y certificados acreditados",
     "Comprueba si una certificación que enseñan está realmente acreditada.",
     "evidencia", "https://www.enac.es/", False),
]


def enlaces(cif="", nombre="", web=""):
    """Las fuentes con el dato ya metido donde se puede meter."""
    n = quote_plus(nombre or "")
    nc = quote_plus(f'"{nombre}"') if nombre else ""
    fuera = []
    for bloque, fuente, aporta, alimenta, plantilla, directo in FUENTES:
        url = (plantilla.replace("{cif}", quote_plus(cif or ""))
               .replace("{nombre_comillas}", nc)
               .replace("{nombre}", n)
               .replace("{web}", web or ""))
        if "{web}" in plantilla and not web:
            url = ""
        fuera.append({"bloque": bloque, "fuente": fuente, "aporta": aporta,
                      "alimenta": alimenta, "url": url, "directo": directo})
    return fuera


def por_bloque(cif="", nombre="", web=""):
    fuera = {}
    for f in enlaces(cif, nombre, web):
        fuera.setdefault(f["bloque"], []).append(f)
    return fuera


# QUÉ SE PIDE Y QUÉ NO. Lo que sale del barrido público no hay que pedirlo:
# pedir al cliente lo que ya está publicado hace perder tiempo a los dos y
# resta credibilidad al trabajo.
NO_PEDIR = [
    "Escritura de constitución y objeto social (BORME)",
    "Nombramientos y ceses de administradores (BORME)",
    "Depósito de cuentas (BORME)",
    "Licitaciones y adjudicaciones públicas (PLACSP)",
    "Subvenciones concedidas (BDNS)",
    "Sentencias publicadas (CENDOJ)",
    "Política y código de conducta si están en su web",
]
