# -*- coding: utf-8 -*-
"""
informe_html.py

El informe ejecutivo de la metodología de la matriz de riesgos penales.

Ignacio, 25/08/2026: "quiero que me hagas un informe ejecutivo sobre la
Excel, es decir, su metodología, base... además que me propongas un sistema
de trabajo para nutrirla de manera que sea lo más automático posible".

Va dentro de IA ELECE y no sale de aquí: los números son de un
cliente real. Se lee en pantalla y se imprime a PDF con Ctrl+P.
"""

ROJO = "#8A2742"
GRIS = "#464237"

INFORME = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Informe ejecutivo · Matriz de riesgos penales · IA ELECE</title>
<style>
  @font-face { font-family:'Dosis'; src:url('/estatico/dosis.woff2') format('woff2');
               font-weight:200 800; font-display:swap; }
  *{ box-sizing:border-box; }
  body{ margin:0; background:#8A2742; color:#111;
        font-family:'Dosis',Arial,Helvetica,sans-serif; font-weight:500;
        padding:30px 20px 60px; }
  .volver{ color:#fff; text-decoration:none; font-size:14px; letter-spacing:.1em; }
  .hoja{ background:#fff; max-width:940px; margin:16px auto 0; border-radius:10px;
         padding:44px 52px 54px; box-shadow:0 12px 30px rgba(0,0,0,.22); }
  h1{ font-size:30px; margin:0 0 4px; font-weight:600; }
  .sub{ color:#464237; margin:0 0 6px; font-size:16px; }
  .meta{ color:#8a8578; font-size:13px; margin:0 0 26px;
         border-bottom:2px solid #8A2742; padding-bottom:14px; }
  h2{ font-size:20px; margin:34px 0 10px; color:#8A2742; font-weight:600;
      border-bottom:1px solid #E7E4DC; padding-bottom:6px; }
  h3{ font-size:16px; margin:20px 0 6px; font-weight:600; }
  p,li{ color:#2a2a2a; line-height:1.62; font-size:15px; }
  ul,ol{ padding-left:20px; }
  .caja{ background:#FBF8F5; border-left:4px solid #8A2742; padding:12px 16px;
         margin:16px 0; border-radius:0 6px 6px 0; }
  .caja.aviso{ background:#FFF6F6; border-left-color:#B23B3B; }
  .caja p{ margin:5px 0; font-size:14.5px; }
  table{ border-collapse:collapse; width:100%; margin:14px 0; font-size:14px; }
  th{ background:#F3EFEA; text-align:left; padding:8px 10px; font-weight:600;
      border-bottom:2px solid #E0DAD1; }
  td{ padding:7px 10px; border-bottom:1px solid #EEE9E2; vertical-align:top; }
  td.n{ text-align:right; white-space:nowrap; font-variant-numeric:tabular-nums; }
  .mal{ color:#B23B3B; font-weight:600; }
  .bien{ color:#127A4A; font-weight:600; }
  .formula{ font-family:Consolas,monospace; background:#F5F2ED; padding:2px 7px;
            border-radius:4px; font-size:14px; }
  .paso{ display:flex; gap:14px; margin:10px 0; align-items:flex-start; }
  .paso .num{ background:#8A2742; color:#fff; width:26px; height:26px; flex:0 0 26px;
              border-radius:50%; display:flex; align-items:center;
              justify-content:center; font-size:14px; font-weight:600; }
  .paso .txt{ flex:1; }
  .paso .txt b{ display:block; }
  .auto{ font-size:12px; text-transform:uppercase; letter-spacing:.06em;
         padding:1px 7px; border-radius:10px; margin-left:6px; }
  .auto.total{ background:#DFF0E6; color:#0F5F3A; }
  .auto.asistido{ background:#FDF0DC; color:#8A5A00; }
  .auto.persona{ background:#F1EDF7; color:#4A2E7A; }
  footer{ margin-top:34px; padding-top:14px; border-top:1px solid #E7E4DC;
          color:#8a8578; font-size:12.5px; }
  @media print{ body{ background:#fff; padding:0; } .volver{ display:none; }
                .hoja{ box-shadow:none; margin:0; max-width:none; } }
</style>
</head>
<body>
<a class="volver" href="/tarjeta/compliance">&larr; Volver</a>
<div class="hoja">

<h1>Matriz de riesgos penales</h1>
<p class="sub">Informe ejecutivo: base documental, metodología y sistema de trabajo</p>
<p class="meta">Elece Legal · 25 de agosto de 2026 · Documento interno · Uso: dirección del área</p>

<h2>1. Objeto</h2>
<p>Este informe hace tres cosas: describe <b>de dónde parte</b> la metodología
de evaluación de riesgos penales de Elece, señala <b>qué funciona y qué no</b>
en las herramientas actuales con datos medidos, y propone <b>cómo alimentarla
de forma automática</b> sin que deje de ser un traje a medida para cada
empresa.</p>

<h2>2. La base: qué hay hoy</h2>
<p>Se han analizado íntegramente dos ficheros. Ninguno se ha modificado.</p>

<h3>2.1 · <span class="formula">Análisis de riesgos de compliance · matriz de cliente, v02</span></h3>
<p>Julio de 2022. La matriz de un cliente real y, con ella, el método de la
casa. 50 hojas, <b>42 delitos, 227 conductas, 603 controles</b> y 9 áreas.</p>
<ul>
<li>Una hoja por delito y un catálogo único de conductas en una hoja maestra.</li>
<li>La <b>unidad de análisis es la conducta</b>, no el delito. Cada conducta
tiene código propio y sus controles enganchados por ese código.</li>
<li>Probabilidad e impacto de 0 a 5. Riesgo =
<span class="formula">((P + I) / 2) × 0,2</span>, escala 0,1 a 1,0.</li>
<li>Los controles <b>restan</b> puntos y se acumulan con <span class="formula">SUMIF</span>.</li>
<li>Suelo de 0,5 por eje: el riesgo residual nunca baja de 0,1.</li>
<li>Una macro exporta las fichas de riesgo a PDF.</li>
</ul>

<h3>2.2 · <span class="formula">mapa_aplicabilidad_delitos_persona_juridica_v2.xlsx</span></h3>
<p>Julio de 2026. La evolución del criterio. 39 delitos o familias, todos
pendientes de clasificar.</p>
<ul>
<li>Riesgo inherente = <span class="formula">P × I</span>, producto, escala 1 a 25.</li>
<li><b>Escalas ancladas</b> en criterios objetivos, con una columna de
<b>evidencia mínima</b> por nivel: objeto social, número de operaciones,
volumen anual, porcentaje de ingresos.</li>
<li>Impacto anclado en las <b>penas del art. 33.7 CP</b>, con las siete letras
y su criterio de severidad.</li>
<li>Aplicabilidad separada de la valoración. Fuentes al BOE consolidado.
Fecha de revisión y versión. Hoja de limitaciones.</li>
</ul>

<h2>3. Diagnóstico</h2>

<h3>3.1 · Lo que se conserva</h3>
<ul>
<li>La <b>conducta</b> como unidad de análisis.</li>
<li>El <b>producto</b> P × I y la escala 1–25 con cuatro bandas.</li>
<li>Las <b>escalas ancladas</b> y la columna de evidencia mínima.</li>
<li>El impacto anclado en las <b>penas</b> del art. 33.7.</li>
<li>La <b>hoja de limitaciones</b>, que dice expresamente que no declara
conformidad ni certificabilidad. Eso es honestidad profesional y se queda.</li>
</ul>

<h3>3.2 · Lo que falla, con los números</h3>

<p><b class="mal">a) El riesgo se calculaba como media, y el riesgo no es una
media.</b> Con <span class="formula">(P+I)/2</span>, probabilidad 5 con
impacto 1 y probabilidad 1 con impacto 5 dan lo mismo: 0,6. Un incumplimiento
constante e inocuo puntúa igual que uno rarísimo que se lleva la empresa por
delante.</p>

<p><b class="mal">b) La media entre conductas tapa lo grave.</b> Cinco delitos
de esa matriz llegan al informe con una puntuación muy inferior a la
de su peor conducta:</p>
<table>
<tr><th>Delito</th><th>Peor conducta</th><th class="n">P</th><th class="n">I</th>
    <th class="n">Su valor</th><th class="n">Lo que sale en el informe</th></tr>
<tr><td>Estafa</td><td>EST1</td><td class="n">5</td><td class="n">4</td>
    <td class="n"><b>0,90</b></td><td class="n">0,40</td></tr>
<tr><td>Dchos. propiedad intelectual</td><td>PINT1</td><td class="n">3</td><td class="n">4</td>
    <td class="n">0,70</td><td class="n">0,30</td></tr>
<tr><td>Fraudes tributarios y Seg. Social</td><td>FTSS1</td><td class="n">2</td><td class="n">4</td>
    <td class="n">0,60</td><td class="n">0,32</td></tr>
<tr><td>Explosivos</td><td>EXP1</td><td class="n">3</td><td class="n">3</td>
    <td class="n">0,60</td><td class="n">0,35</td></tr>
<tr><td>Insolvencias punibles</td><td>INS6</td><td class="n">2</td><td class="n">3</td>
    <td class="n">0,50</td><td class="n">0,25</td></tr>
</table>

<p><b class="mal">c) El eje de impacto no discrimina.</b> En el mapa v2,
<b>38 de 39 delitos puntúan 4 o 5 en impacto</b>. Es lógico: si el ancla es
«penas imponibles a la persona jurídica», casi todo el catálogo puede acabar
en disolución. El resultado es que P × I es en la práctica P × 4,5, y toda la
discriminación la hace la probabilidad. Consecuencia: la banda <b>Crítico
(16-25) es hoy inalcanzable</b> y el «Crítico: 0» del resumen parece un
hallazgo tranquilizador cuando es un artefacto de la escala.</p>

<p><b class="mal">d) Los controles restaban puntos, sin límite y sin mirar su
estado.</b> Diez controles flojos sumaban −5 y hundían cualquier riesgo hasta
el suelo. Y el campo ESTADO no entraba en la fórmula: un control meramente
comunicado descontaba igual que uno implantado.</p>

<p><b class="mal">e) 93 controles no descuentan nada.</b> El rango del
<span class="formula">SUMIF</span> se fijó a mano y nunca se amplió cuando se
añadieron filas debajo. De los 603 controles del libro, <b>93 (el 15 %) caen
fuera del rango</b>: están escritos y no cuentan.</p>
<table>
<tr><th>Hoja</th><th class="n">Controles</th><th class="n">Fuera</th>
    <th class="n">Residual hoy</th><th class="n">Si contaran</th></tr>
<tr><td>Fraudes tributarios y Seg. Social</td><td class="n">84</td><td class="n">40</td>
    <td class="n">0,158</td><td class="n">0,100</td></tr>
<tr><td>Estafa</td><td class="n">72</td><td class="n">19</td><td class="n">0,181</td><td class="n">0,181</td></tr>
<tr><td>Insolvencias punibles</td><td class="n">107</td><td class="n">12</td><td class="n">0,136</td><td class="n">0,136</td></tr>
<tr><td>Frustración de la ejecución</td><td class="n">33</td><td class="n">11</td>
    <td class="n">0,225</td><td class="n">0,142</td></tr>
<tr><td>Corrupción entre particulares</td><td class="n">93</td><td class="n">7</td><td class="n">0,100</td><td class="n">0,100</td></tr>
<tr><td>Contrabando</td><td class="n">24</td><td class="n">3</td><td class="n">0,109</td><td class="n">0,109</td></tr>
<tr><td>Daños informáticos</td><td class="n">8</td><td class="n">1</td><td class="n">0,342</td><td class="n">0,325</td></tr>
</table>
<p>En Fraudes tributarios quedan fuera el Manual de configuración contable, el
Manual de Impuestos, una certificación de formación y el contrato con el asesor
laboral: cuarenta controles reales que el modelo no le reconoce al cliente.</p>

<p><b class="mal">f) Un delito entero no llega al informe.</b> Hay 43 hojas de
delito y 42 líneas en el resumen. La que falta es <b>Trata de seres humanos
(art. 177 bis CP)</b>: tiene su hoja de 151 filas, se evaluó, y no está
enlazada.</p>

<p><b class="mal">g) Las dos medias del resumen no se calculan sobre el mismo
conjunto.</b> La media inherente sale de 16 delitos y la residual de 13,
porque tres caen al suelo con los controles y se salen del cálculo. Comparar
0,38 con 0,22 no es comparar lo mismo; sobre los mismos 16 sería 0,38 → 0,20.</p>

<p><b class="mal">h) Precisión falsa.</b> El resumen muestra 0,3416666666666666
sobre una escala donde alguien eligió «3» en un desplegable.</p>

<h3>3.3 · El catálogo, incompleto</h3>
<p>Frente al catálogo vigente —el décimo desde 2010, fijado por la
<b>LO 4/2023, de 27 de abril</b>—, al mapa v2 le faltan cuatro delitos:</p>
<table>
<tr><th>Delito</th><th>Artículos</th><th>Observación</th></tr>
<tr><td><b>Derechos de los trabajadores</b></td><td>311 a 318 CP</td>
    <td class="mal">De los que más se imputan en la práctica. Estaba en la matriz anterior y aquí desapareció</td></tr>
<tr><td>Organizaciones y grupos criminales</td><td>570 bis a 570 quater CP</td><td>Estaba en la matriz anterior</td></tr>
<tr><td>Negativa a actuaciones inspectoras</td><td>294 CP</td><td>Estaba en la matriz anterior</td></tr>
<tr><td>Alteración de precios en concursos y subastas</td><td>262 CP</td>
    <td>No queda cubierto por la familia 278-288</td></tr>
</table>
<p>Bien resueltas, en cambio, las incorporaciones de trata (177 bis), acoso
sexual (184), fraude de subvenciones (308) y fraude a los presupuestos de la
UE (306). Y bien retiradas manipulación genética y asociación ilícita: son
art. 129, consecuencias accesorias, no art. 31 bis.</p>

<h2>4. La metodología nueva</h2>

<h3>4.1 · Cuatro preguntas, en este orden</h3>
<table>
<tr><th>Pregunta</th><th>Cómo se responde</th></tr>
<tr><td><b>¿Puede pasar aquí?</b></td>
    <td>Aplicabilidad sí/no <b>con motivo escrito</b>. Deja de escribirse como un 0,5 dentro de la puntuación</td></tr>
<tr><td><b>¿Cómo de probable?</b></td>
    <td>Exposición (50 %) + frecuencia del delito (30 %) + historial de la empresa (20 %)</td></tr>
<tr><td><b>¿Cómo de grave?</b></td>
    <td>Severidad de la pena realmente prevista, ajustada por lo que expone esta empresa</td></tr>
<tr><td><b>¿Qué lo contiene?</b></td>
    <td>Controles que multiplican, con cuatro factores de eficacia</td></tr>
</table>

<h3>4.2 · Probabilidad: tres factores objetivos</h3>
<div class="caja">
<p><b>Exposición</b> — ¿hace la empresa la actividad, y cuánto? Objeto social,
mapa de procesos, volumen anual, número de terceros, geografías, licitaciones.</p>
<p><b>Frecuencia del delito</b> — cuántas condenas hay en España por ese
delito, según la Estadística de Condenados del INE (explotación del Registro
Central de Penados) y del CGPJ. <b>Es el dato que convierte «me parece raro»
en «en toda España hay N al año».</b></p>
<p><b>Historial de la empresa</b> — sanciones, expedientes, denuncias,
requerimientos e incidentes previos. Ignorar las infracciones administrativas
anteriores es uno de los errores clásicos de una matriz.</p>
</div>
<p>Y <b>dos reglas que pesan más que la media</b>, porque se explican en una
frase delante de un cliente:</p>
<ul>
<li>Si la empresa <b>no realiza la actividad</b>, la probabilidad es 1 y el
delito se marca como no aplicable con su motivo.</li>
<li>Si <b>ya la han sancionado</b> por ese ámbito, la probabilidad no baja de
4. Nadie puede sostener que es improbable aquello por lo que ya le
sancionaron.</li>
</ul>

<h3>4.3 · Impacto: la pena que de verdad prevé el tipo</h3>
<p>El 5 se reserva a los delitos donde la <b>disolución, la prohibición
definitiva o la inhabilitación severa</b> están realmente sobre la mesa: las
letras b) a g) del art. 33.7 sólo se imponen si el tipo las prevé y concurren
los requisitos del art. 66 bis. Con eso la escala se abre sola.</p>
<p>Encima va un <b>ajuste de −1, 0 o +1 según lo que exponga la empresa</b>: la
inhabilitación para contratar con el sector público es la muerte para quien
vive de licitaciones y da igual a quien no se presenta a ninguna.
<b>Ahí es donde el impacto deja de ser una propiedad del delito y pasa a ser
una propiedad del cliente.</b> El traje a medida está en este ajuste.</p>

<h3>4.4 · Controles: multiplican, no restan</h3>
<p><span class="formula">Residual = Inherente × Π (1 − eficacia del control)</span>,
con suelo. Cada control se lleva un porcentaje de lo que dejó el anterior, así
que el segundo vale menos que el primero —como en la realidad— y el riesgo
<b>nunca llega a cero por construcción</b>, sin necesidad de trucos en la
fórmula.</p>
<table>
<tr><th>Factor</th><th>Valores</th><th>Criterio</th></tr>
<tr><td>Naturaleza</td><td>preventivo 1,00 · detectivo 0,90 · reactivo 0,30</td>
    <td>El reactivo pesa poco: cuando actúa, la conducta ya se ha cometido</td></tr>
<tr><td>Estado</td><td>implantado 1,00 · comunicado 0,90 · aprobado 0,60 · ignorado <b>se descarta</b></td>
    <td>Lo ignorado no es un control, es una intención</td></tr>
<tr><td>Evidencia</td><td>documentada 1,00 · declarada 0,15</td>
    <td>Un control sin documento no baja el riesgo delante de un juez</td></tr>
<tr><td>Origen</td><td><b>autoimpuesto 1,00</b> · obligado por norma 0,70</td>
    <td>Cumplir la ley es el mínimo exigible; lo que acredita cultura es lo que se hace por encima</td></tr>
</table>
<p>Eficacia base del 35 %. Un control preventivo, implantado, documentado y
autoimpuesto se lleva el 35 % del riesgo restante; el mismo sin documento, el
5 %; aprobado pero no implantado, el 21 %.</p>

<h3>4.5 · El delito lo manda su peor conducta</h3>
<p>Nivel del delito = <b>máximo</b> de sus conductas, con el recuento por banda
al lado. La media se calcula y se guarda, pero nunca como titular: es la que
hacía que Estafa saliera en 0,4 con una conducta en 0,9 dentro.</p>

<h3>4.6 · El apetito de riesgo lo firma el cliente</h3>
<p>La herramienta <b>no propone umbral</b>. Decidir qué riesgo se acepta es una
decisión indelegable del órgano de gobierno, y la UNE 19601:2025 refuerza
precisamente eso. Mientras no haya umbral aprobado, el informe lo dice —y esa
ausencia ya es, en sí misma, un hallazgo.</p>

<h2>5. Encaje con la UNE 19601:2025</h2>
<table>
<tr><th>Requisito</th><th>Cómo lo cubre la metodología</th></tr>
<tr><td><b>4.5.2</b> · considerar todos los delitos del CP vigente</td>
    <td>Catálogo completo y versionado, con los cuatro delitos que faltaban</td></tr>
<tr><td><b>4.5</b> · identificación, análisis y valoración</td>
    <td>Criterios escritos por nivel y evidencia mínima exigida en cada uno</td></tr>
<tr><td><b>4.5</b> · revisión y documentación</td>
    <td>Fecha, versión, autor y motivo de cada cambio</td></tr>
<tr><td><b>6.3</b> · planificación de cambios <span class="bien">(nuevo en 2025)</span></td>
    <td>Disparadores de revisión: reforma del Código Penal, nueva actividad,
        nuevo centro o filial, incidente o denuncia, cambio del órgano de compliance</td></tr>
<tr><td>Gobernanza y responsabilidades indelegables</td>
    <td>Dueño por riesgo y apetito firmado por el órgano de gobierno</td></tr>
<tr><td>Trazabilidad de controles</td>
    <td>Cada control enganchado a su conducta y a su documento de evidencia</td></tr>
</table>

<h2>6. Sistema de trabajo para nutrirla</h2>
<p>Cuatro fuentes. Cada paso lleva marcado quién lo hace.</p>
<p style="margin-top:-4px">
<span class="auto total">automático</span>
<span class="auto asistido">asistido</span>
<span class="auto persona">siempre una persona</span></p>

<h3>6.1 · La entrevista</h3>
<p>Hoy: Mamen, presencial, una hora con el responsable de cada área,
personalizada, solicitando documentación y evidencias. Eso no cambia — es lo
que hace que el traje sea a medida. Lo que cambia es lo que pasa antes y
después.</p>
<div class="paso"><div class="num">1</div><div class="txt">
<b>Antes · el guion se genera solo <span class="auto total">automático</span></b>
A partir del catálogo y del área, la herramienta saca las preguntas de los
delitos que tocan a esa área, más lo que ya se sepa de la empresa por el
barrido público. Mamen entra con las preguntas que importan, no con un
cuestionario genérico.</div></div>
<div class="paso"><div class="num">2</div><div class="txt">
<b>Durante · se graba como apoyo <span class="auto persona">persona</span></b>
La grabación es para transcribir. Basta con una frase al empezar diciendo
para qué se graba y cuánto se conserva: informar no es pedir permiso y no
corta la conversación.</div></div>
<div class="paso"><div class="num">3</div><div class="txt">
<b>Después · transcripción en el propio equipo <span class="auto total">automático</span></b>
La transcripción se hace en local. Ni el audio ni el nombre de nadie salen
del ordenador.</div></div>
<div class="paso"><div class="num">4</div><div class="txt">
<b>Extracción <span class="auto asistido">asistido</span></b>
De la transcripción salen: procesos descritos, cifras y volúmenes citados,
controles mencionados, evidencias prometidas. Y una propuesta de puntuación
por conducta <b>con la cita literal y el minuto en que se dijo</b>.</div></div>
<div class="paso"><div class="num">5</div><div class="txt">
<b>Confirmación <span class="auto persona">persona</span></b>
Mamen confirma o corrige cada propuesta. Nada entra en la matriz sin ese
paso.</div></div>
<div class="paso"><div class="num">6</div><div class="txt">
<b>Salida · la lista de documentación pedida <span class="auto total">automático</span></b>
Con responsable y plazo. Es el registro de evidencias.</div></div>

<h3>6.2 · La documentación de la empresa</h3>
<p>Una carpeta por cliente. Al dejar caer un documento: OCR si viene
escaneado, clasificación en los siete bloques de evidencia (gobierno y
alcance · riesgos · función de compliance · canal e investigaciones · personas
y cultura · terceros y filiales · evaluación y mejora), lectura de fecha,
versión y firma, y enganche al control que acredita.</p>
<div class="caja">
<p><b>La presión hacia la evidencia es automática:</b> un control sin documento
enganchado se queda en «declarada» y su eficacia cae al 15 %. Nadie tiene que
perseguir a nadie: el número baja solo y se ve en el informe.</p>
</div>

<h3>6.3 · Fuentes públicas y reputación <span class="auto total">automático</span></h3>
<p>Sólo persona jurídica. De las personas físicas no se busca nada sin encargo
expreso y documentado.</p>
<table>
<tr><th>Bloque</th><th>Fuentes</th><th>Alimenta</th></tr>
<tr><td>Identidad y estructura</td><td>BORME, objeto social, administradores, cuentas depositadas</td>
    <td>Exposición · aplicabilidad</td></tr>
<tr><td>Sanciones</td><td>BOE y boletines autonómicos, resoluciones de medio ambiente,
    consumo e industria, Inspección de Trabajo, deudores AEAT</td>
    <td><b>Historial</b> (la regla del suelo 4)</td></tr>
<tr><td>Judicial</td><td>CENDOJ</td><td>Historial</td></tr>
<tr><td>Estadística</td><td>INE — Estadística de Condenados · CGPJ</td>
    <td><b>Frecuencia del delito</b></td></tr>
<tr><td>La propia empresa</td><td>Web, memoria, política, código de conducta,
    canal publicado, certificaciones</td>
    <td>Controles ya existentes, con su documento</td></tr>
</table>
<p>Barrido al abrir el expediente y otro al cerrarlo, para que el informe no
salga con datos de hace tres meses.</p>

<h3>6.4 · El histórico de Elece</h3>
<p>La biblioteca de conductas y de controles se reutiliza entre clientes: cada
auditoría empieza con la biblioteca cargada, no con una hoja en blanco.
<b>Pero la puntuación empieza siempre a cero.</b> Se hereda el catálogo, nunca
la valoración — reutilizar puntuaciones es exactamente el error de la
plantilla estandarizada, y es lo primero que detecta quien revisa.</p>

<h3>6.5 · El circuito completo</h3>
<p>Encargo → alta de la empresa → barrido público → guion de entrevistas →
entrevistas y transcripción → propuesta de puntuación → <b>confirmación de
Mamen</b> → solicitud de evidencias → enganche documento-control → cálculo del
residual → <b>informe y plan de acción</b> → volcado al sistema de calidad
como no conformidades y acciones correctivas, con responsable, plazo y
verificación de eficacia.</p>
<div class="caja">
<p><b>Cuatro cosas no se automatizan nunca:</b> la aplicabilidad, la puntuación
final, la clasificación del hallazgo y la conclusión. La herramienta propone y
justifica; la persona decide y firma.</p>
</div>

<h2>7. Limitaciones</h2>
<div class="caja aviso">
<p><b>La norma no entra en la herramienta.</b> La UNE 19601:2025 y la guía de
Casanovas son documentos protegidos. Se trabaja citando cláusulas y
requisitos por su número y redactando nosotros los criterios; el texto de la
norma no se incorpora al sistema.</p>
<p><b>Nada de esto declara conformidad ni certificabilidad</b> de ninguna
organización, ni sustituye a una auditoría con evidencias del caso.</p>
<p><b>El catálogo de delitos y las referencias legales</b> de este informe
proceden de fuentes secundarias y deben cotejarse contra el Código Penal
consolidado antes de emitir nada hacia un cliente. Tres referencias del mapa
v2 quedan marcadas para verificar: patrimonio histórico (323 CP), sustancias
destructoras del ozono (348 CP) y el alcance de terrorismo (576 y 580 bis).</p>
</div>

<footer>IA ELECE · Documento interno de Elece Legal · Contiene datos de un
expediente de cliente: no sale de este equipo.</footer>
</div>
</body>
</html>
"""
