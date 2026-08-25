# -*- coding: utf-8 -*-
r"""
catalogo.py

El catálogo de delitos con responsabilidad penal de la persona jurídica.

VERSIÓN 2026.1. Sale de fundir los dos ficheros que había y de completar lo
que le faltaba a cada uno:

  - del mapa de aplicabilidad v2 (julio 2026): las 39 familias, la
    agrupación y el anclaje del impacto en las penas del art. 33.7;
  - de la matriz anterior (julio 2022): los cuatro delitos que el mapa
    había perdido por el camino.

LOS CUATRO QUE FALTABAN, y el primero no es menor:

    311-318  Derechos de los trabajadores    de los que más se imputan
    570 bis  Organizaciones y grupos criminales
    294      Negativa a actuaciones inspectoras
    262      Alteración de precios en concursos y subastas

Y DOS QUE SOBRABAN en la matriz vieja: manipulación genética y asociación
ilícita. No son del art. 31 bis, son consecuencias accesorias del art. 129:
otro régimen. Se pueden trabajar, pero no en esta lista.

SEVERIDAD INICIAL: es una PROPUESTA, no un dato. Marca si el tipo prevé sólo
multa (1-2), multa con interdictivas limitadas (3), interdictivas serias (4)
o disolución y prohibición definitiva (5). Cada asunto la confirma o la
corrige, porque el traje es a medida.

SIN COTEJAR CONTRA EL BOE. Las referencias vienen de fuentes secundarias.
Las tres marcadas con «verificar» son las que no cuadran a la primera y hay
que mirarlas en el Código Penal consolidado antes de entregar nada.
"""

VERSION = "2026.1"

# (id, delito, familia, referencia, severidad propuesta, nota)
DELITOS = [
    ("D01", "Tráfico ilegal de órganos humanos", "Bienes personales",
     "156 bis CP", 5, ""),
    ("D02", "Trata de seres humanos", "Derechos fundamentales",
     "177 bis CP", 5, ""),
    ("D03", "Delitos contra la integridad moral", "Personas y entorno laboral",
     "173.1 CP", 4, "la matriz vieja lo citaba como 173 bis: revisar"),
    ("D04", "Acoso sexual", "Personas y entorno laboral", "184 CP", 4,
     "responsabilidad de la PJ vía art. 189 bis, LO 4/2023"),
    ("D05", "Prostitución, explotación sexual y corrupción de menores",
     "Derechos fundamentales", "187 a 189 bis CP", 5, ""),
    ("D06", "Descubrimiento y revelación de secretos", "Intimidad y datos",
     "197 a 197 quinquies CP", 4, ""),
    ("D07", "Estafas y fraudes", "Patrimonio", "248 a 251 bis CP", 4, ""),
    ("D08", "Frustración de la ejecución", "Patrimonio",
     "257 a 258 ter CP", 4, ""),
    ("D09", "Insolvencias punibles", "Patrimonio", "259 a 261 bis CP", 4, ""),
    ("D10", "Alteración de precios en concursos y subastas públicas",
     "Patrimonio", "262 CP", 3, "recuperado de la matriz anterior"),
    ("D11", "Daños informáticos", "Sistemas de información",
     "264 a 264 quater CP", 4, ""),
    ("D12", "Propiedad intelectual", "Mercado", "270 a 272 CP", 3, ""),
    ("D13", "Propiedad industrial", "Mercado", "273 a 277 CP", 4, ""),
    ("D14", "Mercado y consumidores", "Mercado", "278 a 288 CP", 4,
     "incluye secretos de empresa, publicidad, facturación y detracción"),
    ("D15", "Abuso de mercado e información privilegiada", "Mercado",
     "284 a 285 quater CP", 5, ""),
    ("D16", "Corrupción en los negocios", "Corrupción",
     "286 bis a 286 quater CP", 5, ""),
    ("D17", "Negativa a actuaciones inspectoras", "Mercado", "294 CP", 3,
     "recuperado de la matriz anterior"),
    ("D18", "Blanqueo de capitales", "Blanqueo y financiación",
     "301 a 304 CP", 5, ""),
    ("D19", "Financiación ilegal de partidos políticos",
     "Blanqueo y financiación", "304 bis CP", 4, ""),
    ("D20", "Hacienda Pública", "Fraudes públicos", "305 a 310 bis CP", 5, ""),
    ("D21", "Seguridad Social", "Fraudes públicos", "307 a 310 bis CP", 5, ""),
    ("D22", "Fraude de subvenciones y ayudas públicas", "Fraudes públicos",
     "308 a 310 bis CP", 5, ""),
    ("D23", "Fraude a los presupuestos de la Unión Europea",
     "Fraudes públicos", "306 y 310 bis CP", 5, ""),
    ("D24", "Derechos de los trabajadores", "Personas y entorno laboral",
     "311 a 318 CP", 4,
     "RECUPERADO: de los que más se imputan en la práctica"),
    ("D25", "Derechos de los ciudadanos extranjeros",
     "Derechos fundamentales", "318 bis CP", 4, ""),
    ("D26", "Ordenación del territorio y urbanismo", "Territorio y entorno",
     "319 CP", 4, ""),
    ("D27", "Patrimonio histórico", "Territorio y entorno", "323 CP", 4,
     "verificar el precepto que atribuye la responsabilidad a la PJ"),
    ("D28", "Recursos naturales y medio ambiente", "Territorio y entorno",
     "325 a 331 CP", 5, ""),
    ("D29", "Flora, fauna y animales", "Territorio y entorno",
     "334 a 340 quater CP", 4, ""),
    ("D30", "Energía nuclear y radiaciones ionizantes", "Riesgo colectivo",
     "343 CP", 5, ""),
    ("D31", "Riesgos por explosivos y sustancias peligrosas",
     "Riesgo colectivo", "348 CP", 5, ""),
    ("D32", "Sustancias destructoras del ozono", "Territorio y entorno",
     "348 CP", 4, "verificar: aparece con el mismo artículo que explosivos"),
    ("D33", "Salud pública: medicamentos, alimentos y productos sanitarios",
     "Salud pública", "359 a 366 CP", 5, ""),
    ("D34", "Tráfico de drogas", "Salud pública", "368 a 369 bis CP", 5, ""),
    ("D35", "Falsificación de moneda", "Falsedades", "386 CP", 4, ""),
    ("D36", "Falsificación de tarjetas y medios de pago", "Falsedades",
     "399 bis CP", 4, ""),
    ("D37", "Cohecho", "Corrupción", "424 y 427 bis CP", 5, ""),
    ("D38", "Tráfico de influencias", "Corrupción", "429 y 430 CP", 5, ""),
    ("D39", "Malversación", "Corrupción", "432 a 435 CP", 5, ""),
    ("D40", "Delitos de odio y discriminación", "Derechos fundamentales",
     "510 y 510 bis CP", 4, ""),
    ("D41", "Organizaciones y grupos criminales", "Criminalidad organizada",
     "570 bis a 570 quater CP", 5, "recuperado de la matriz anterior"),
    ("D42", "Terrorismo y financiación del terrorismo",
     "Criminalidad organizada", "576 y 580 bis CP", 5,
     "verificar el alcance frente a 571-580 bis"),
    ("D43", "Contrabando", "Fraudes públicos",
     "art. 2 LO 12/1995, de represión del contrabando", 5, ""),
]

# Fuera del art. 31 bis: consecuencias accesorias del art. 129. Se guardan
# aparte para que nadie los mezcle en la matriz sin saberlo.
ART_129 = [
    ("A01", "Manipulación genética", "159 a 161 CP"),
    ("A02", "Asociación ilícita", "515 CP"),
]


def por_familia():
    fuera = {}
    for d in DELITOS:
        fuera.setdefault(d[2], []).append(d)
    return fuera


def a_verificar():
    return [d for d in DELITOS if "verificar" in (d[5] or "").lower()]
