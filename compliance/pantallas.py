# -*- coding: utf-8 -*-
r"""
pantallas.py

Las pantallas de la tarjeta de Compliance: una por empresa, con todo lo que
se va haciendo dentro.

Ignacio, 25/08/2026: "quizá lo mejor sea una tarjeta por proyecto, es decir,
empresa..., empresa... y ahí reproducir todos los puntos que vayamos
haciendo".

Se pintan en el servidor y sin librerías: esto acaba en un equipo del
despacho que puede no tener salida a internet, y una pantalla que depende de
un CDN es una pantalla que un día no abre.
"""
from __future__ import annotations

import html

import entregables as en                            # noqa: E402
import proyectos as pr                              # noqa: E402
import supervisor as sp                             # noqa: E402

ROJO = "#8A2742"
GRIS = "#464237"


def E(x):
    return html.escape("" if x is None else str(x))


def _delitos():
    import catalogo                                  # noqa: PLC0415
    return catalogo.DELITOS


_CSS = """
  @font-face { font-family:'Dosis'; src:url('/estatico/dosis.woff2') format('woff2');
               font-weight:200 800; font-display:swap; }
  *{ box-sizing:border-box; }
  body{ margin:0; min-height:100vh; background:%s; color:#111;
        font-family:'Dosis',Arial,Helvetica,sans-serif; font-weight:500;
        padding:26px 30px 60px; }
  a.volver{ color:#fff; text-decoration:none; font-size:14px; letter-spacing:.1em; }
  h1{ color:#fff; font-size:30px; font-weight:600; margin:12px 0 4px; }
  .lema{ color:#fff; opacity:.85; font-size:15px; margin:0 0 20px; }
  .hoja{ background:#fff; border-radius:10px; padding:24px 28px; margin:0 0 20px;
         box-shadow:0 10px 24px rgba(0,0,0,.18); max-width:1100px; }
  .hoja h2{ margin:0 0 4px; font-size:20px; color:%s; font-weight:600; }
  .hoja p.sub{ margin:0 0 16px; color:%s; font-size:14px; }
  .rejilla{ display:grid; grid-template-columns:repeat(auto-fill,minmax(250px,1fr));
            gap:16px; max-width:1100px; }
  .emp{ background:#fff; border-radius:10px; padding:20px; text-decoration:none;
        color:#111; box-shadow:0 10px 24px rgba(0,0,0,.18); display:block;
        border-left:5px solid %s; }
  .emp:hover{ transform:translateY(-2px); }
  .emp h3{ margin:0 0 4px; font-size:19px; font-weight:600; }
  .emp .dato{ color:%s; font-size:13px; }
  .emp .barra{ height:6px; background:#EEE9E2; border-radius:3px; margin-top:12px; }
  .emp .barra i{ display:block; height:6px; border-radius:3px; background:%s; }
  table{ border-collapse:collapse; width:100%%; font-size:14px; }
  th{ text-align:left; background:#F3EFEA; padding:7px 10px; font-weight:600;
      border-bottom:2px solid #E0DAD1; font-size:12.5px; text-transform:uppercase;
      letter-spacing:.04em; }
  td{ padding:7px 10px; border-bottom:1px solid #EEE9E2; vertical-align:top; }
  td.n{ text-align:right; white-space:nowrap; }
  .et{ display:inline-block; padding:2px 9px; border-radius:12px; font-size:12px;
       font-weight:600; white-space:nowrap; }
  .et.hecho{ background:#DFF0E6; color:#0F5F3A; }
  .et.pendiente{ background:#FDF0DC; color:#8A5A00; }
  .et.no_se{ background:#FBE0E0; color:#9B2C2C; }
  .norma{ color:#8a8578; font-size:12.5px; display:block; margin-top:2px; }
  .semaforo{ border-left:6px solid #ccc; padding:14px 18px; border-radius:0 8px 8px 0;
             margin-bottom:16px; background:#FBF8F5; }
  .semaforo.hecho{ border-left-color:#127A4A; }
  .semaforo.pendiente{ border-left-color:#8A5A00; }
  .semaforo.no_se{ border-left-color:#B23B3B; background:#FFF6F6; }
  .semaforo b{ font-size:17px; display:block; margin-bottom:3px; }
  input,select,textarea{ font:inherit; font-size:14px; padding:8px 10px;
       border:1px solid #D8D2C8; border-radius:7px; background:#fff; }
  button{ font:inherit; font-size:14px; font-weight:600; padding:9px 18px;
       border-radius:7px; border:none; background:%s; color:#fff; cursor:pointer; }
  button.claro{ background:#fff; color:%s; border:1px solid #D8D2C8; }
  .fila{ display:flex; gap:10px; flex-wrap:wrap; align-items:center; }
  .enlaces a{ display:inline-block; margin-right:14px; color:%s; font-weight:600;
       text-decoration:none; font-size:14.5px; }
  .enlaces a:hover{ text-decoration:underline; }
  .cod{ font-family:Consolas,monospace; font-size:13px; color:%s; }
  .zona{ border:2px dashed #D8D2C8; border-radius:10px; padding:22px;
         text-align:center; color:%s; background:#FBF8F5; }
  .zona.encima{ border-color:%s; background:#FDF3F5; }
""" % (ROJO, ROJO, GRIS, ROJO, GRIS, ROJO, ROJO, ROJO, ROJO, GRIS, GRIS, ROJO)


def _marco(titulo, cuerpo, volver="/", lema=""):
    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(titulo)} · IA ELECE</title><style>{_CSS}</style></head>
<body>
<a class="volver" href="{E(volver)}">&larr; Volver</a>
<h1>{E(titulo)}</h1>
{f'<p class="lema">{E(lema)}</p>' if lema else ''}
{cuerpo}
</body></html>"""


# ---------------------------------------------------------------------------
def pagina_compliance():
    """La tarjeta de Compliance: los proyectos y las herramientas comunes."""
    ps = pr.listar()
    if ps:
        tarjetas = []
        for p in ps:
            rev = sp.revisar(p["clave"])
            total = len(rev["esta"]) + len(rev["bien"]) if rev else 1
            hechos = sum(1 for x in (rev["esta"] + rev["bien"])
                         if x["estado"] == sp.HECHO) if rev else 0
            pct = int(hechos * 100 / total) if total else 0
            tarjetas.append(f"""
      <a class="emp" href="/compliance/proyecto/{E(p['clave'])}">
        <h3>{E(p['empresa'])}</h3>
        <span class="dato">{E(p.get('tipo_trabajo') or 'sin tipo de trabajo')}
          · abierto {E(p.get('abierto','')[:10])}</span>
        <div class="barra"><i style="width:{pct}%"></i></div>
        <span class="dato">{hechos} de {total} puntos en regla</span>
      </a>""")
        rejilla = f'<div class="rejilla">{"".join(tarjetas)}</div>'
    else:
        rejilla = ('<div class="hoja"><h2>Todavía no hay proyectos</h2>'
                   '<p class="sub">Cada proyecto es una empresa. Abre el '
                   'primero aquí abajo.</p></div>')

    # LA HERRAMIENTA ES LA EXCEL. Ignacio, 25/08/2026: "pon la Excel en
    # herramientas como herramienta principal. Anexo la metodología". Lo
    # demás documenta y explica; el trabajo se hace en la hoja de cálculo, y
    # así se ve nada más entrar.
    cuerpo = f"""
    <div class="hoja">
      <h2>Herramientas</h2>
      <p class="sub">Comunes a todos los proyectos.</p>
      <div style="display:flex; gap:20px; align-items:flex-start; flex-wrap:wrap">
        <a href="/compliance/matriz.xlsx" style="text-decoration:none; flex:1;
           min-width:330px; background:#FBF8F5; border:2px solid {ROJO};
           border-radius:10px; padding:20px 22px; display:block; color:#111">
          <span style="font-size:12px; letter-spacing:.08em; color:{ROJO};
            font-weight:600">HERRAMIENTA PRINCIPAL</span>
          <h3 style="margin:6px 0 6px; font-size:21px; font-weight:600">
            &darr; Matriz de riesgos penales · Excel</h3>
          <p style="margin:0; font-size:14px; color:{GRIS}">
            Plantilla en blanco con la metodología dentro: escalas ancladas,
            catálogo de {E(len(_delitos()))} delitos, controles que multiplican
            y el cálculo hecho por fórmulas. Se abre y funciona sin esta
            herramienta.</p>
        </a>
        <div style="flex:1; min-width:260px">
          <p style="margin:0 0 8px; font-size:12px; letter-spacing:.08em;
             color:{GRIS}; font-weight:600">CON QUÉ SE RELLENA</p>
          <p class="enlaces" style="line-height:2">
            <a href="/compliance/entrevistas">Entrevistas por departamento</a><br>
            <a href="/compliance/documentacion">Documentación de la empresa</a>
          </p>
          <p style="margin:14px 0 8px; font-size:12px; letter-spacing:.08em;
             color:{GRIS}; font-weight:600">ANEXOS</p>
          <p class="enlaces" style="line-height:2">
            <a href="/compliance/metodologia">Anexo I · Metodología y cálculo</a><br>
            <a href="/compliance/informe">Anexo II · Informe ejecutivo</a>
          </p>
        </div>
      </div>
    </div>
    {rejilla}
    <div class="hoja" style="margin-top:20px">
      <h2>Abrir un proyecto</h2>
      <p class="sub">Nace vacío a propósito: se hereda el catálogo de delitos
        y la biblioteca de controles, nunca la valoración de otro cliente.</p>
      <form method="post" action="/compliance/proyecto" class="fila">
        <input name="empresa" placeholder="Empresa" required style="min-width:230px">
        <input name="cif" placeholder="CIF" style="width:130px">
        <!-- EL TRABAJO ES EL SISTEMA, NO EL INFORME. Ignacio, 26/08/2026:
             "necesito que el proyecto se llame sistema de gestión de riesgos
             penales". Es el nombre correcto y ya venía así en la portada de
             la matriz de 2022: el SGRP es lo que se implanta y se mantiene;
             la evaluación de riesgos es uno de sus entregables, no el
             encargo. -->
        <select name="tipo_trabajo">
          <option value="">— tipo de trabajo —</option>
          <option>Sistema de gestión de riesgos penales (SGRP)</option>
          <option>Auditoría interna UNE 19601:2025</option>
          <option>Transición 2017 a 2025</option>
          <option>Seguimiento</option>
        </select>
        <button>Abrir proyecto</button>
      </form>
    </div>"""
    return _marco("Compliance", cuerpo, "/",
                  "Una tarjeta por empresa. Dentro, todo lo que se va haciendo.")


# ---------------------------------------------------------------------------
# DÓNDE SE ARREGLA CADA COSA. Ignacio, 26/08/2026: "¿cómo puedo completar
# lo que falta en el supervisor?". Un supervisor que señala y no dice por
# dónde se empieza convierte cada punto rojo en un acertijo. Así que cada
# línea lleva su puerta.
_COMO_SE_ARREGLA = {
    "encargo": ("Contéstalo en las preguntas de arriba", ""),
    "contexto": ("Contéstalo en las preguntas de arriba", ""),
    "catalogo": ("Contéstalo en las preguntas de arriba", ""),
    "gobierno": ("Contéstalo en las preguntas de arriba", ""),
    "evidencias": ("Herramientas → Documentación de la empresa",
                   "/compliance/documentacion"),
    "entregables": ("Contéstalo en las preguntas de arriba", ""),
    "aplicabilidad": ("Decidir los 43 delitos", "APLICABILIDAD"),
    "entrevistas": ("Ver el guion del área y subir la entrevista aquí abajo",
                    "/compliance/entrevistas"),
    "valoracion": ("Se rellena en la matriz, hoja MATRIZ", "MATRIZ"),
    "controles": ("Se rellenan en la matriz, hoja CONTROLES", "MATRIZ"),
}


def _linea(x, clave=""):
    texto, destino = _COMO_SE_ARREGLA.get(x.get("fase", ""), ("", ""))
    if destino == "APLICABILIDAD":
        destino = f"/compliance/proyecto/{clave}/aplicabilidad"
    elif destino == "MATRIZ":
        destino = f"/compliance/proyecto/{clave}/matriz.xlsx"
    if x["estado"] == "hecho" or not texto:
        accion = ""
    elif destino:
        accion = (f'<a href="{E(destino)}" style="color:{ROJO};'
                  f'font-weight:600;text-decoration:none;font-size:13px">'
                  f'&rarr; {E(texto)}</a>')
    else:
        accion = (f'<span style="color:{GRIS};font-size:13px">&uarr; '
                  f'{E(texto)}</span>')
    return f"""<tr>
      <td class="n"><span class="et {x['estado']}">{
        {'hecho':'está','pendiente':'falta','no_se':'no lo sé'}[x['estado']]
      }</span></td>
      <td><b>{E(x['que'])}</b><br>{E(x['detalle'])}
        {f'<span class="norma">{E(x["norma"])}</span>' if x.get('norma') else ''}</td>
      <td class="n">{accion}</td>
    </tr>"""



def _caja_pregunta(clave, p):
    """La siguiente pregunta, y sólo esa.

    Ignacio, 26/08/2026: "no me preguntas lo que necesitas de la Excel".
    Aquí es donde la herramienta pregunta. Una cada vez, con su porqué
    delante: lo que se pide sin explicar por qué se contesta a desgana, y en
    este trabajo la respuesta acaba en un informe que firma alguien.
    """
    import preguntas as pg                            # noqa: PLC0415
    hechas, total = pg.cuantas(p)
    q = pg.siguiente(p)
    if q is None:
        return (f'<div class="hoja"><h2>Todo preguntado</h2>'
                f'<p class="sub">Las {total} respuestas están. Lo siguiente '
                f'es la aplicabilidad de los 43 delitos y las entrevistas.</p>'
                f'</div>')
    campo, pregunta, ayuda, porque, tipo, opciones = q
    if tipo == "largo":
        campo_html = (f'<textarea name="valor" rows="3" required '
                      f'style="width:100%"></textarea>')
    elif tipo == "opciones":
        ops = "".join(f'<option>{E(o)}</option>' for o in opciones)
        campo_html = f'<select name="valor" required style="min-width:320px">{ops}</select>'
    elif tipo == "opciones_varias":
        campo_html = "".join(
            f'<label style="display:block;margin:5px 0;font-size:14px">'
            f'<input type="checkbox" name="valor" value="{E(o)}" checked> '
            f'{E(o)}</label>' for o in opciones)
    elif tipo == "fecha_hoy":
        campo_html = ('<input name="valor" type="date" required '
                      'value="" style="width:190px">')
    elif tipo == "apetito":
        campo_html = ('<div class="fila">'
                      '<input name="valor" type="number" min="1" max="25" '
                      'placeholder="1-25" style="width:110px">'
                      '<input name="firmado" placeholder="Aprobado por" '
                      'style="min-width:230px">'
                      '<input name="fecha" type="date" style="width:180px">'
                      '</div>')
    else:
        campo_html = '<input name="valor" required style="min-width:420px">'

    return f'''
    <div class="hoja" style="border-left:5px solid {ROJO}">
      <p style="margin:0 0 6px;font-size:12px;letter-spacing:.08em;
         color:{GRIS};font-weight:600">SIGUIENTE PREGUNTA · {hechas} de {total}</p>
      <h2 style="font-size:22px">{E(pregunta)}</h2>
      <p class="sub" style="margin:0 0 6px">{E(ayuda)}</p>
      <p style="margin:0 0 14px;font-size:13.5px;color:{ROJO}">
        <b>Para qué sirve:</b> {E(porque)}</p>
      <form method="post" action="/compliance/proyecto/{E(clave)}/responder">
        <input type="hidden" name="campo" value="{E(campo)}">
        {campo_html}
        <div class="fila" style="margin-top:12px">
          <button>Guardar y siguiente</button>
          <a href="/compliance/proyecto/{E(clave)}?saltar={E(campo)}"
             style="color:{GRIS};font-size:13.5px">lo dejo para luego</a>
        </div>
      </form>
    </div>'''

def pagina_proyecto(clave):
    rev = sp.revisar(clave)
    if rev is None:
        return _marco("No existe", '<div class="hoja"><p>Ese proyecto no está.</p></div>',
                      "/tarjeta/compliance")
    p = rev["proyecto"]
    ent = p.get("entrevistas") or []
    # CADA ENTREVISTA, CON LO QUE SE PUEDE HACER CON ELLA. Ignacio,
    # 26/08/2026: "si subo una, ¿no debería haber un botón de procesar?".
    # Guardar ya se guardaba solo al soltarla; lo que faltaba era el paso
    # siguiente. Y los botones dicen la verdad: el audio no se transcribe
    # todavía porque en este equipo no hay motor y nada sale a la nube.
    import procesar_entrevista as pe                  # noqa: PLC0415
    _filas = []
    for e in ent:
        f = e.get("fichero", "")
        estado = ("confirmada" if e.get("confirmada") else
                  ("transcrita" if e.get("transcrita") else "sin procesar"))
        marca = ("hecho" if e.get("confirmada") else
                 ("pendiente" if e.get("transcrita") else "no_se"))
        base = f"/compliance/proyecto/{E(clave)}/entrevista/{E(f)}"
        if e.get("transcrita"):
            accion = (f'<a href="{base}/texto" style="color:{ROJO};'
                      f'font-weight:600;text-decoration:none;font-size:13px">'
                      f'ver el texto</a>')
            if not e.get("confirmada"):
                accion += (f' · <form method="post" style="display:inline" '
                           f'action="{base}/confirmar"><button class="claro" '
                           f'style="padding:3px 10px;font-size:12.5px">dar por '
                           f'buena</button></form>')
        elif pe.se_puede_leer(f):
            accion = (f'<form method="post" style="display:inline" '
                      f'action="{base}/procesar"><button '
                      f'style="padding:4px 12px;font-size:12.5px">Procesar'
                      f'</button></form>')
        else:
            accion = (f'<a href="{base}/texto" style="color:{ROJO};'
                      f'font-weight:600;text-decoration:none;font-size:13px">'
                      f'pegar la transcripción</a>')
        palabras = (f"<span class='norma'>{e.get('palabras')} palabras</span>"
                    if e.get("palabras") else "")
        _filas.append(f"""<tr><td>{E(e.get('area') or '—')}</td>
        <td>{E(e.get('entrevistado') or '—')}</td><td>{E(e['tipo'])}</td>
        <td>{E(e['subido'][:16].replace('T',' '))}</td>
        <td class="n">{e['bytes']//1024} KB</td>
        <td><span class="et {marca}">{estado}</span>{palabras}</td>
        <td class="n">{accion}</td></tr>""")
    filas_ent_html = "".join(_filas) or (
        '<tr><td colspan="7" style="color:#8a8578">Todavía no hay '
        'ninguna.</td></tr>')

    entregas = en.del_proyecto(p)
    filas_ent2 = "".join(f"""<tr><td class="cod">{E(x['codigo'])}</td>
        <td><b>{E(x['nombre'])}</b><br><span class="norma">{E(x['origen'])}</span></td>
        <td>{E(x['grupo'])}</td><td>{E(x['audiencia'])}</td>
        <td><span class="et pendiente">{E(x['estado'])}</span></td></tr>"""
        for x in entregas)

    areas = ", ".join(p.get("areas") or []) or "sin definir"
    cuerpo = _caja_pregunta(clave, p) + f"""
    <div class="hoja">
      <div class="semaforo {rev['estado']}">
        <b>{'Todo en regla' if rev['estado']=='hecho' else
            ('Hay cosas que no puedo comprobar' if rev['estado']=='no_se'
             else f"Faltan {rev['pendientes']} puntos")}</b>
        {E(rev['dicho'])}
      </div>
      <p class="sub">{E(p.get('tipo_trabajo') or 'sin tipo de trabajo')} ·
        CIF {E(p.get('cif') or '—')} · responsable {E(p.get('responsable'))} ·
        áreas: {E(areas)} · revisado {E(rev['cuando'])}</p>
      <!-- NO HAY BOTÓN DE GUARDAR PORQUE NO HACE FALTA. Ignacio, 26/08/2026:
           "debería haber un botón de guardar cambios en este proyecto, porque
           puede que nos cueste muchos días hacer un proyecto". La
           preocupación es la correcta; la solución no es un botón. Cada
           respuesta, cada entrevista y cada decisión se escriben en el disco
           en el momento, así que no hay nada que se pueda perder por cerrar
           la ventana o apagar el equipo. Un botón de guardar induciría el
           error contrario: creer que lo que no se pulsó, se perdió. Lo que sí
           hacía falta era DECIRLO, y decir dónde está el expediente. -->
      <p class="sub" style="margin:-8px 0 14px; font-size:13px">
        <b style="color:#127A4A">✓ Todo se guarda solo</b>, en el momento.
        Última escritura: {E((p.get('tocado') or '')[:16].replace('T',' '))} ·
        el expediente vive en
        <span class="cod">datos\\proyectos\\{E(p['clave'])}</span> y no sale
        de este equipo.</p>
      <p class="enlaces">
        <a href="/compliance/proyecto/{E(clave)}/matriz.xlsx"><b>&darr;
          Descargar la matriz en Excel</b></a>
        <a href="/compliance/informe">Informe ejecutivo</a>
        <a href="/compliance/metodologia">Metodología</a>
      </p>
    </div>

    <div class="hoja">
      <h2>Supervisor · ¿está?</h2>
      <p class="sub">Lo que hace falta para poder hacer la matriz.</p>
      <table>{"".join(_linea(x, clave) for x in rev["esta"])}</table>
    </div>

    <div class="hoja">
      <h2>Supervisor · ¿está bien?</h2>
      <p class="sub">Una matriz puede estar completa y no valer nada. Esto es
        lo que nadie mira y lo que hunde un expediente.</p>
      <table>{"".join(_linea(x, clave) for x in rev["bien"])}</table>
    </div>

    <div class="hoja">
      <h2>Canal de entrevistas</h2>
      <p class="sub">Audio, vídeo o notas. Se quedan en este equipo, dentro
        del expediente de la empresa.</p>
      <div class="fila" style="margin-bottom:12px">
        <input id="area" placeholder="Área (Compras, RRHH…)" style="min-width:200px">
        <input id="quien" placeholder="Entrevistado" style="min-width:200px">
      </div>
      <div class="zona" id="zona">
        Arrastra aquí el archivo, o
        <button class="claro" onclick="document.getElementById('f').click()">elígelo</button>
        <input type="file" id="f" multiple style="display:none">
        <div id="estado" style="margin-top:10px"></div>
      </div>
      <table style="margin-top:16px">
        <tr><th>Área</th><th>Entrevistado</th><th>Tipo</th><th>Subido</th>
            <th class="n">Tamaño</th><th>Estado</th><th class="n">Qué hacer</th></tr>
        {filas_ent_html}
      </table>
    </div>

    <div class="hoja">
      <h2>Entregables</h2>
      <p class="sub">Con su código desde que nacen. Un documento sin código,
        versión y firma no es un entregable: es un borrador con membrete.</p>
      <table>
        <tr><th>Código</th><th>Documento</th><th>Grupo</th><th>Audiencia</th>
            <th>Estado</th></tr>
        {filas_ent2}
      </table>
    </div>

<script>
const zona=document.getElementById('zona'), campo=document.getElementById('f'),
      dice=document.getElementById('estado');
['dragenter','dragover'].forEach(e=>zona.addEventListener(e,ev=>{{
  ev.preventDefault(); zona.classList.add('encima'); }}));
['dragleave','drop'].forEach(e=>zona.addEventListener(e,ev=>{{
  ev.preventDefault(); zona.classList.remove('encima'); }}));
zona.addEventListener('drop',ev=>subir(ev.dataTransfer.files));
campo.addEventListener('change',()=>subir(campo.files));

async function subir(files){{
  for(const f of files){{
    dice.textContent='Subiendo '+f.name+'…';
    const b64=await new Promise(res=>{{
      const r=new FileReader();
      r.onload=()=>res(r.result.split(',')[1]);
      r.readAsDataURL(f);
    }});
    const r=await fetch('/compliance/proyecto/{E(clave)}/entrevista',{{
      method:'POST', headers:{{'Content-Type':'application/json'}},
      body:JSON.stringify({{nombre:f.name, datos:b64,
        area:document.getElementById('area').value,
        quien:document.getElementById('quien').value}})
    }});
    const d=await r.json();
    dice.textContent = d.ok ? ('Guardada: '+f.name) : ('No se pudo: '+d.porque);
  }}
  setTimeout(()=>location.reload(), 700);
}}
</script>"""
    return _marco(p["empresa"], cuerpo, "/tarjeta/compliance",
                  "Expediente de compliance penal")


# ---------------------------------------------------------------------------
def pagina_metodologia():
    """El anexo de metodología, con el cálculo dentro.

    Ignacio, 25/08/2026: "anexo la metodología y dentro de la metodología
    incluye el cálculo". Van juntos a propósito: unos criterios sin la
    fórmula que los usa no se pueden auditar, y una fórmula sin los criterios
    que la alimentan no se puede defender. Este documento es el que se
    entrega como anexo del informe y el que mira un auditor externo.
    """
    import metodologia as me                         # noqa: PLC0415

    def tabla(d, titulo):
        filas = "".join(f"<tr><td class='n'><b>{k}</b></td><td>{E(v)}</td></tr>"
                        for k, v in sorted(d.items()))
        return f"<h3 style='color:{ROJO};margin:18px 0 6px'>{titulo}</h3>" \
               f"<table>{filas}</table>"

    pesos = "".join(
        f"<tr><td>{E(n)}</td><td class='n'><b>{v:.2f}</b></td><td>{E(d)}</td></tr>"
        for n, v, d in
        [(f"naturaleza · {k}", x, dd) for (k, x), dd in zip(
            me.NATURALEZA.items(),
            ["El que evita que la conducta ocurra.",
             "El que la detecta a tiempo de reaccionar.",
             "Actúa cuando la conducta ya se ha cometido: apenas es un control."])]
        + [(f"estado · {k}", x, dd) for (k, x), dd in zip(
            me.ESTADO.items(),
            ["Funcionando y con rastro de que se aplica.",
             "Comunicado a quien tiene que aplicarlo.",
             "Aprobado: sin esto no se puede implantar ni comunicar.",
             "No se valora: no es un control, es una intención."])]
        + [(f"evidencia · {k}", x, dd) for (k, x), dd in zip(
            me.EVIDENCIA.items(),
            ["Hay un documento que lo acredita.",
             "Sólo consta que alguien lo dijo."])]
        + [(f"origen · {k}", x, dd) for (k, x), dd in zip(
            me.ORIGEN.items(),
            ["Lo hace la empresa por encima de lo exigido: acredita cultura.",
             "Lo impone una norma: es el mínimo exigible."])])

    bandas = "".join(f"<tr><td class='n'>{a}–{b}</td><td><b>{n}</b></td>"
                     f"<td>{E(t)}</td></tr>" for a, b, n, t in me.BANDAS)

    # Un ejemplo trabajado vale más que la fórmula: es lo que se enseña al
    # cliente cuando pregunta de dónde sale su número.
    ej = me.evaluar_conducta({
        "aplica": True, "exposicion": 4, "frecuencia": 4, "historial": 2,
        "severidad": 4, "expuesto": 1,
        "controles": [
            {"descripcion": "Código de conducta", "naturaleza": "preventivo",
             "estado": "implantado", "evidencia": "documentada",
             "origen": "autoimpuesto"},
            {"descripcion": "Manual contable", "naturaleza": "detectivo",
             "estado": "implantado", "evidencia": "declarada",
             "origen": "obligado"}]})
    pasos = "".join(
        f"<tr><td>{E(c['control'])}</td><td>{E(c['porque'])}</td>"
        f"<td class='n'><b>{c['valor']:.0%}</b></td></tr>"
        for c in ej["detalle_residual"]["controles"])

    cuerpo = f"""
    <div class="hoja">
      <h2>1 · El cálculo</h2>
      <p class="sub">Cuatro pasos. Cada uno se explica en una frase delante de
        un cliente, que es la prueba de que el método sirve.</p>
      <table>
        <tr><th>Paso</th><th>Fórmula</th><th>Por qué así</th></tr>
        <tr><td><b>Probabilidad</b></td>
            <td class="cod">0,50·exposición + 0,30·frecuencia + 0,20·historial</td>
            <td>La exposición manda porque es lo único específico de esta
                empresa. La frecuencia es contexto y el historial es señal.</td></tr>
        <tr><td><b>Impacto</b></td>
            <td class="cod">severidad de la pena ± ajuste de empresa</td>
            <td>La pena que el tipo prevé de verdad, corregida por lo que esta
                empresa expone. Aquí está el traje a medida.</td></tr>
        <tr><td><b>Inherente</b></td>
            <td class="cod">probabilidad × impacto</td>
            <td>Producto, no media: si fuera media, «muy probable e inocuo» y
                «rarísimo y catastrófico» valdrían lo mismo.</td></tr>
        <tr><td><b>Residual</b></td>
            <td class="cod">inherente × ∏(1 − eficacia) &nbsp;·&nbsp; suelo del
                {int(me.SUELO_RESIDUAL*100)} %</td>
            <td>Cada control muerde lo que dejó el anterior. El riesgo nunca
                llega a cero, y no hace falta ningún truco para conseguirlo.</td></tr>
      </table>
      <p class="sub" style="margin-top:14px"><b>En la hoja de cálculo</b> el
        producto se hace con <span class="cod">EXP(SUMAR.SI(… LN(1−eficacia)))</span>:
        sigue siendo SUMAR.SI —la función de siempre— pero acumulando
        multiplicando. Y el rango es de columna entera, para que añadir filas
        de control no pueda dejar ninguno fuera del cálculo.</p>
    </div>

    <div class="hoja">
      <h2>2 · Las dos reglas que pesan más que la media</h2>
      <table>
        <tr><td style="width:52%"><b>Si la empresa no realiza la actividad</b>
            (exposición 1)</td>
            <td>La probabilidad es 1 y el delito se marca <b>no aplicable con
                motivo escrito</b>. Descartar no es borrar: la UNE 19601:2025
                pide considerar todos los delitos, y considerar es dejar
                constancia de por qué se descarta.</td></tr>
        <tr><td><b>Si ya la han sancionado</b> en ese ámbito (historial 4 o 5)</td>
            <td>La probabilidad <b>no baja de 4</b>. Nadie puede sostener que
                es improbable aquello por lo que ya le sancionaron. Es la regla
                que más discusiones ahorra.</td></tr>
      </table>
    </div>

    <div class="hoja">
      <h2>3 · Un ejemplo, de principio a fin</h2>
      <p class="sub">Actividad frecuente y relevante, delito de los que más se
        imputan, sin antecedentes, pena con interdictivas serias y una empresa
        que vive de contratación pública.</p>
      <table>
        <tr><th>Paso</th><th>Cuenta</th><th class="n">Resultado</th></tr>
        <tr><td>Probabilidad</td>
            <td>0,50·4 + 0,30·4 + 0,20·2 =
                {str(ej['probabilidad']['media']).replace('.', ',')}</td>
            <td class="n"><b>{ej['probabilidad']['valor']}</b></td></tr>
        <tr><td>Impacto</td><td>severidad 4, ajuste +1</td>
            <td class="n"><b>{ej['impacto']['valor']}</b></td></tr>
        <tr><td>Inherente</td>
            <td>{ej['probabilidad']['valor']} × {ej['impacto']['valor']}</td>
            <td class="n"><b>{ej['inherente']}</b> ·
              {E(ej['banda_inherente']['nivel'])}</td></tr>
      </table>
      <h3 style="color:{ROJO};margin:18px 0 6px">Los controles</h3>
      <table><tr><th>Control</th><th>Factores</th><th class="n">Quita</th></tr>
        {pasos}</table>
      <p class="sub" style="margin-top:12px">Reducción total
        <b>{ej['detalle_residual']['reduccion']} %</b> → riesgo residual
        <b>{ej['residual']}</b>, banda
        <b>{E(ej['banda_residual']['nivel'])}</b>. El segundo control aporta
        mucho menos que el primero: no tiene documento que lo acredite y viene
        impuesto por una norma.</p>
    </div>

    <div class="hoja">
      <h2>4 · Las bandas</h2>
      <p class="sub">Cada banda lleva pegada una decisión. Una banda que no
        dice qué hacer no sirve de nada.</p>
      <table><tr><th>Puntuación</th><th>Nivel</th><th>Tratamiento</th></tr>
        {bandas}</table>
    </div>

    <div class="hoja">
      <h2>5 · Criterios de probabilidad</h2>
      {tabla(me.EXPOSICION, "Exposición de la empresa · peso 50 %")}
      {tabla(me.FRECUENCIA,
             "Frecuencia del delito · peso 30 % · INE, Estadística de "
             "Condenados (Registro Central de Penados) y CGPJ")}
      {tabla(me.HISTORIAL, "Historial de la empresa · peso 20 %")}
    </div>

    <div class="hoja">
      <h2>6 · Criterios de impacto</h2>
      {tabla(me.SEVERIDAD, "Severidad de la pena prevista · art. 33.7 CP")}
      {tabla(me.EXPUESTO, "Ajuste según lo que expone esta empresa")}
    </div>

    <div class="hoja">
      <h2>7 · Eficacia de un control</h2>
      <p class="sub">Base {me.EFICACIA_BASE:.0%} multiplicada por estos cuatro
        factores. La eficacia sale del estado del control: no se pone a mano.</p>
      <table><tr><th>Factor</th><th class="n">Valor</th><th>Criterio</th></tr>
        {pesos}</table>
    </div>

    <div class="hoja">
      <h2>8 · Lo que este anexo no dice</h2>
      <p class="sub">No declara conformidad, certificabilidad ni adecuación
        plena a UNE 19601:2025 de ninguna organización. El apetito de riesgo
        lo aprueba el órgano de gobierno de la empresa: Elece no lo propone.
        Y el riesgo residual nunca es cero: ningún sistema de control elimina
        un riesgo.</p>
    </div>"""
    return _marco("Anexo I · Metodología y cálculo", cuerpo,
                  "/tarjeta/compliance",
                  "Los criterios y la fórmula que los usa, juntos. "
                  "Es el anexo que hace defendible la matriz.")


# ---------------------------------------------------------------------------
def pagina_entrevistas(clave=""):
    """La arquitectura de entrevistas por departamento.

    Ignacio, 25/08/2026: "otro apartado dentro de herramientas, las
    entrevistas. Dentro pon una arquitectura básica de entrevistas por
    departamento". Esto es el guion de quien va a escuchar, no un checklist:
    Mamen entra una hora con el responsable y deja que cuente.
    """
    import entrevistas as ev                         # noqa: PLC0415

    if clave:
        g = ev.guion(clave)
        if g is None:
            return _marco("No existe", '<div class="hoja"><p>Ese departamento '
                          'no está.</p></div>', "/compliance/entrevistas")
        delitos = "".join(
            f"<tr><td class='cod'>{E(d[0])}</td><td>{E(d[1])}</td>"
            f"<td class='cod'>{E(d[3])}</td></tr>" for d in g["delitos"])
        def preguntas(lista):
            return "".join(
                f"<tr><td>{E(p)}</td><td class='n'>"
                f"<span class='et pendiente'>{E(a)}</span></td></tr>"
                for p, a in lista)
        papeles = "".join(f"<li>{E(x)}</li>" for x in g["papeles"])
        cuerpo = f"""
    <div class="hoja">
      <div class="semaforo pendiente"><b>Antes de empezar</b>{E(g['aviso'])}</div>
      <p class="sub">Una hora, presencial, con el responsable del área.
        No se lee la lista: se deja que cuente y se va tachando.</p>
    </div>
    <div class="hoja">
      <h2>Qué delitos le tocan a esta área</h2>
      <p class="sub">Son los que hay que poder valorar al salir de aquí.</p>
      <table><tr><th>ID</th><th>Delito</th><th>Referencia</th></tr>
        {delitos}</table>
    </div>
    <div class="hoja">
      <h2>1 · Para entender el área</h2>
      <p class="sub">Van siempre y van primero: sin el proceso no se puede
        valorar nada de lo que venga después.</p>
      <table><tr><th>Pregunta</th><th class="n">Alimenta</th></tr>
        {preguntas(g['comunes'])}</table>
    </div>
    <div class="hoja">
      <h2>2 · Propias de {E(g['departamento'])}</h2>
      <table><tr><th>Pregunta</th><th class="n">Alimenta</th></tr>
        {preguntas(g['propias'])}</table>
    </div>
    <div class="hoja">
      <h2>3 · Documentación que se pide al salir</h2>
      <p class="sub">Con responsable y plazo. Un control sin documento se
        queda en «declarada» y su eficacia cae al 15 %.</p>
      <ul>{papeles}</ul>
    </div>"""
        return _marco(g["departamento"], cuerpo, "/compliance/entrevistas",
                      "Guion de entrevista · unos 60 minutos")

    tarjetas = "".join(f"""
      <a class="emp" href="/compliance/entrevistas?d={E(d[0])}">
        <h3>{E(d[1])}</h3>
        <span class="dato">{len(d[2])} delitos · {len(d[3])} preguntas propias
          · {len(d[4])} documentos a pedir</span>
      </a>""" for d in ev.DEPARTAMENTOS)
    cuerpo = f"""
    <div class="hoja">
      <h2>Cómo están montadas</h2>
      <p class="sub">Las hace Mamen, presenciales, una hora con el responsable
        de cada área. Eso no cambia: es lo que hace que el traje sea a medida.
        Lo que aporta esto es entrar con las preguntas de los delitos que
        tocan a <b>esa</b> área.</p>
      <p class="sub"><b>Las preguntas son abiertas a propósito.</b>
        «¿Tenéis un procedimiento de compras?» se contesta «sí» y no deja
        nada. «Cuéntame cómo entra un proveedor nuevo, desde que aparece
        hasta que se le paga la primera factura» deja el proceso, los nombres,
        los importes y casi siempre el punto por donde se cuela el riesgo.</p>
      <p class="sub">Cada pregunta va marcada con lo que alimenta:
        <span class="et pendiente">exposición</span>
        <span class="et pendiente">historial</span>
        <span class="et pendiente">control</span>
        <span class="et pendiente">evidencia</span>
        — de ahí sale después la puntuación.</p>
    </div>
    <div class="rejilla">{tarjetas}</div>"""
    return _marco("Entrevistas", cuerpo, "/tarjeta/compliance",
                  "Arquitectura por departamento. Diez guiones.")


def pagina_documentacion(cif="", nombre="", web=""):
    """Todo lo que se saca del CIF sin pedírselo a nadie."""
    import fuentes as fu                             # noqa: PLC0415

    aviso = ""
    if cif:
        v = fu.validar_cif(cif)
        if v["ok"]:
            aviso = (f'<div class="semaforo hecho"><b>CIF válido</b>'
                     f'{E(v["cif"])} · {E(v["tipo"])}</div>')
        else:
            aviso = (f'<div class="semaforo no_se"><b>Ese CIF no cuadra</b>'
                     f'{E(v["porque"])}</div>')

    bloques = ""
    for bloque, lista in fu.por_bloque(cif, nombre, web).items():
        filas = ""
        for f in lista:
            enlace = (f'<a href="{E(f["url"])}" target="_blank" rel="noopener">'
                      f'{E(f["fuente"])}</a>' if f["url"]
                      else f'<span style="color:#8a8578">{E(f["fuente"])}'
                           f' — falta la web</span>')
            marca = ('<span class="et hecho">directo</span>' if f["directo"]
                     else '<span class="et pendiente">buscar a mano</span>')
            filas += (f'<tr><td><b>{enlace}</b><br>'
                      f'<span class="norma">{E(f["aporta"])}</span></td>'
                      f'<td class="n"><span class="et pendiente">'
                      f'{E(f["alimenta"])}</span></td>'
                      f'<td class="n">{marca}</td></tr>')
        bloques += (f'<div class="hoja"><h2>{E(bloque)}</h2>'
                    f'<table><tr><th>Fuente</th><th class="n">Alimenta</th>'
                    f'<th class="n">Acceso</th></tr>{filas}</table></div>')

    no_pedir = "".join(f"<li>{E(x)}</li>" for x in fu.NO_PEDIR)
    cuerpo = f"""
    <div class="hoja">
      <h2>El dato de partida</h2>
      <p class="sub">Con el CIF y la denominación se abre casi todo. Sólo
        persona jurídica: de los administradores no se busca nada sin encargo
        expreso.</p>
      <form method="get" class="fila">
        <input name="cif" placeholder="CIF" value="{E(cif)}" style="width:140px">
        <input name="nombre" placeholder="Denominación social"
               value="{E(nombre)}" style="min-width:280px">
        <input name="web" placeholder="https://web de la empresa"
               value="{E(web)}" style="min-width:230px">
        <button>Preparar los enlaces</button>
      </form>
      {aviso}
    </div>
    {bloques}
    <div class="hoja">
      <h2>Lo que NO hay que pedirle al cliente</h2>
      <p class="sub">Está publicado. Pedir lo que ya se puede consultar hace
        perder tiempo a los dos y resta credibilidad al trabajo.</p>
      <ul>{no_pedir}</ul>
    </div>"""
    return _marco("Documentación de la empresa", cuerpo, "/tarjeta/compliance",
                  "Lo que se saca del CIF sin pedírselo a nadie.")


# ---------------------------------------------------------------------------
# LA APLICABILIDAD: qué delitos le pueden pasar a esta organización
# ---------------------------------------------------------------------------
# Es el punto del supervisor que no tenía dónde hacerse, y es el que más pesa:
# de aquí sale qué se valora y qué se descarta. El 4.5.2 de la UNE 19601:2025
# exige considerar TODOS los delitos del Código Penal vigente, y considerar no
# es borrar de la lista: es dejar escrito por qué se descarta.
#
# LO QUE SE TRAE HECHO. Según lo que es la organización, hay delitos que casi
# con seguridad aplican y otros que casi con seguridad no. Eso se propone
# marcado, con su motivo redactado, para que sólo haya que confirmar o
# corregir. Lo que NO se hace es darlo por decidido: mientras nadie lo
# confirme, cuenta como pendiente.
_SIN_ANIMO_DE_LUCRO = {
    "D22": "Recibe o puede recibir subvenciones y ayudas públicas.",
    "D23": "Puede ser destinataria de fondos europeos.",
    "D18": "Maneja donativos y efectivo.",
    "D24": "Tiene personal contratado y voluntariado.",
    "D20": "Tiene obligaciones tributarias propias.",
    "D21": "Tiene obligaciones con la Seguridad Social.",
    "D06": "Trata datos de personas en situación de vulnerabilidad.",
    "D03": "Trabaja con personas y hay relación de superioridad.",
}
_IMPROBABLES_SIN_LUCRO = {
    "D15": "No opera en mercados de valores.",
    "D19": "No financia partidos políticos.",
    "D30": "No maneja energía nuclear ni radiaciones ionizantes.",
    "D01": "No interviene en trasplantes ni extracción de órganos.",
    "D35": "No fabrica ni distribuye moneda.",
}


def _propuesta(p):
    """Lo que yo propondría para esta organización, y por qué."""
    cif = str(p.get("cif") or "").strip().upper()
    letra = cif[:1]
    if letra in ("G", "R", "N"):          # asociación, fundación, religiosa
        return _SIN_ANIMO_DE_LUCRO, _IMPROBABLES_SIN_LUCRO, (
            "Entidad sin ánimo de lucro. Pesan las ayudas públicas, el "
            "efectivo y las personas; pierden peso el mercado y los negocios.")
    return {}, {}, ""


def pagina_aplicabilidad(clave):
    import catalogo as cat                            # noqa: PLC0415
    p = pr.leer(clave)
    if p is None:
        return _marco("No existe", '<div class="hoja"><p>Ese proyecto no '
                      'está.</p></div>', "/tarjeta/compliance")
    decidido = {d.get("id"): d for d in (p.get("delitos") or [])}
    aplican, no_aplican, porque_propuesta = _propuesta(p)

    filas = []
    for idd, nombre, familia, ref, sev, nota in cat.DELITOS:
        d = decidido.get(idd, {})
        estado = d.get("aplica")
        motivo = d.get("motivo", "")
        sug = ""
        if estado is None:
            if idd in aplican:
                sug = f'<span class="et pendiente">propuesta: SÍ</span> {E(aplican[idd])}'
                motivo = motivo or aplican[idd]
            elif idd in no_aplican:
                sug = f'<span class="et pendiente">propuesta: NO</span> {E(no_aplican[idd])}'
                motivo = motivo or no_aplican[idd]
        marca = ("hecho" if estado is True else
                 ("no_se" if estado is False else "pendiente"))
        etiqueta = ("aplica" if estado is True else
                    ("descartado" if estado is False else "sin decidir"))
        filas.append(f"""
      <tr>
        <td class="n"><span class="et {marca}">{etiqueta}</span></td>
        <td><b>{E(nombre)}</b><span class="norma">{E(ref)} · {E(familia)}
          {(" · " + E(nota)) if nota else ""}</span>{sug}</td>
        <td class="n">
          <label style="margin-right:8px"><input type="radio"
            name="ap_{E(idd)}" value="si" {"checked" if estado is True else ""}> Sí</label>
          <label><input type="radio" name="ap_{E(idd)}" value="no"
            {"checked" if estado is False else ""}> No</label></td>
        <td><input name="mo_{E(idd)}" value="{E(motivo)}" placeholder="motivo"
          style="width:100%; font-size:13px"></td>
      </tr>""")

    decididos = sum(1 for d in decidido.values() if d.get("aplica") is not None)
    aviso = (f'<div class="semaforo pendiente"><b>{porque_propuesta}</b>'
             f'He marcado una propuesta en los que tengo criterio. '
             f'Nada cuenta hasta que lo confirmes: una propuesta mía no es una '
             f'decisión tuya.</div>' if porque_propuesta else "")

    cuerpo = f"""
    <div class="hoja">
      {aviso}
      <h2>Aplicabilidad · {decididos} de {len(cat.DELITOS)} decididos</h2>
      <p class="sub">El apartado <b>4.5.2</b> de la UNE 19601:2025 exige
        considerar <b>todos</b> los delitos del Código Penal vigente.
        Considerar no es borrar de la lista: es dejar escrito por qué se
        descarta. Un «no aplica» sin motivo no se sostiene delante de nadie.</p>
      <form method="post" action="/compliance/proyecto/{E(clave)}/aplicabilidad">
        <table>
          <tr><th></th><th>Delito</th><th class="n">¿Aplica?</th>
              <th>Motivo</th></tr>
          {"".join(filas)}
        </table>
        <div class="fila" style="margin-top:16px">
          <button>Guardar la aplicabilidad</button>
          <a href="/compliance/proyecto/{E(clave)}"
             style="color:{GRIS};font-size:13.5px">volver al expediente</a>
        </div>
      </form>
    </div>"""
    return _marco(p["empresa"], cuerpo,
                  f"/compliance/proyecto/{E(clave)}",
                  "Qué delitos le pueden pasar a esta organización")


def pagina_transcripcion(clave, fichero):
    """El texto de una entrevista: verlo, o pegarlo si no se pudo sacar."""
    import procesar_entrevista as pe                  # noqa: PLC0415
    p = pr.leer(clave)
    if p is None:
        return _marco("No existe", '<div class="hoja"><p>No está.</p></div>',
                      "/tarjeta/compliance")
    ficha = next((e for e in (p.get("entrevistas") or [])
                  if e.get("fichero") == fichero), None)
    texto = pe.leer_transcripcion(clave, fichero)
    aviso = ""
    if not texto:
        aviso = ('<div class="semaforo no_se"><b>Esto todavía no se '
                 'transcribe solo</b>En este equipo no hay motor de '
                 'transcripción instalado, y la entrevista no puede salir a '
                 'la nube. Así que de momento el camino es pegar aquí el '
                 'texto. Prefiero decirlo a poner un botón que parezca que '
                 'transcribe y no lo haga: alguien daría por transcrita una '
                 'entrevista que nadie ha escuchado.</div>')
    cuerpo = f"""
    <div class="hoja">
      {aviso}
      <h2>{E(ficha.get('area') if ficha else '')} ·
        {E(ficha.get('entrevistado') if ficha else '')}</h2>
      <p class="sub">{E(fichero)}
        {(" · " + E(ficha.get('origen_texto'))) if ficha and ficha.get('origen_texto') else ""}</p>
      <form method="post" action="/compliance/proyecto/{E(clave)}/entrevista/{E(fichero)}/texto">
        <textarea name="texto" rows="22" style="width:100%; font-size:13.5px"
          placeholder="Pega aquí la transcripción de la entrevista…">{E(texto)}</textarea>
        <div class="fila" style="margin-top:12px">
          <button>Guardar la transcripción</button>
          <a href="/compliance/proyecto/{E(clave)}"
             style="color:{GRIS};font-size:13.5px">volver al expediente</a>
        </div>
      </form>
    </div>"""
    return _marco(p["empresa"], cuerpo, f"/compliance/proyecto/{E(clave)}",
                  "Entrevista")
