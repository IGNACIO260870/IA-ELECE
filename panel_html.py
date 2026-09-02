# -*- coding: utf-8 -*-
"""
panel_html.py

La pantalla de IA ELECE: una sola pagina con las tarjetas del despacho.

LA MARCA ES LA DEL DESPACHO, NO LA DE COLIBRI. Los colores y la letra estan
sacados de elecelegal.es leyendo la web, no de memoria:

    #8A2742   el rojo corporativo (el de los botones y las franjas)
    #464237   el gris pardo del texto de la web
    Dosis     la tipografia, en peso 500, que es la que usa en todo el sitio

Y la instruccion de Ignacio del 20/08/2026, literal: "el fondo de la
pantalla en rojo, tarjetas en blanco y letras en negro".

LAS TARJETAS ESTAN VACIAS A PROPOSITO. Tambien es suyo: "de momento las
tarjetas en blanco... me refiero en blanco al contenido, las tarjetas deben
existir". Primero se ve la casa, despues se amuebla. Lo que hay dentro de
cada una lo dira Mamen, que es quien las va a usar.

LA LETRA, DESCARGADA AL DISCO. La pagina no sale a internet a buscar nada:
esto acabara en un servidor del despacho y tiene que funcionar igual el dia
que ese equipo no tenga salida. Si la fuente no esta, cae a Arial y la
pantalla se ve igual de bien.
"""

ROJO = "#8A2742"
ROJO_OSCURO = "#6E1F35"
TEXTO = "#000000"
GRIS_MARCA = "#464237"

TARJETAS = [
    {"id": "demandas", "titulo": "Demandas",
     "pie": "Por definir con Mamen"},
    {"id": "facturacion", "titulo": "Facturación",
     "pie": "Por definir con Mamen"},
    {"id": "correo", "titulo": "Gestión de correo",
     "pie": "Por definir con Mamen"},
    # LA BIBLIOTECA ES GENERAL, NO DE COMPLIANCE. Ignacio, 28/08/2026,
    # preguntado si colgaba de Compliance o era propia: "general". Mañana
    # valdra tambien para Demandas o Facturacion.
    {"id": "herramientas", "titulo": "Herramientas",
     "pie": "Modelos y biblioteca por sector · se nutre de cada proyecto"},
    {"id": "proyectos", "titulo": "Proyectos",
     "pie": "Por definir con Mamen"},
    # La primera tarjeta con contenido, desde el 25/08/2026: un proyecto por
    # empresa, con su supervisor, su canal de entrevistas y sus entregables.
    {"id": "compliance", "titulo": "Compliance",
     "pie": "Un proyecto por empresa · matriz de riesgos penales"},
    # LOS DOS QUE VIENEN DE FUERA. Ignacio, 02/09/2026: "debes poner en IA
    # ELECE los proyectos que están en el chat que son de Mamen... se llaman
    # Compliance Digital y Auditoría Compliance".
    #
    # SE ABREN VACÍAS, COMO SE ABRIERON LAS DEMÁS. El trabajo de esos dos
    # está en sendos proyectos de Claude chat, que desde aquí no se pueden
    # leer. Así que primero existen -Mamen ya las ve y sabe que son suyas- y
    # el contenido se trae cuando Ignacio baje esos documentos a una carpeta.
    # Es lo mismo que se hizo con Demandas, Facturación y Correo: "de momento
    # las tarjetas en blanco... las tarjetas deben existir".
    # EL PREGUNTADOR ESTÁ POR ENCIMA DE LOS PROYECTOS, no dentro de ninguno.
    # Ignacio, 02/09/2026: "una herramienta que sirva para lo que hacemos tú y
    # yo aquí". Por eso su enlace no es /tarjeta/... sino su propia pantalla.
    {"id": "preguntador", "titulo": "Preguntador", "url": "/preguntador",
     "pie": "Preguntar sobre todos los proyectos a la vez"},
    # LAWSCALE: el proyecto especial de Mamen, con su propio usuario. El
    # material sale de la carpeta datos/lawscale, una tarjeta por documento.
    {"id": "lawscale", "titulo": "LawScale", "url": "/material/lawscale",
     "pie": "Compliance Digital de RRHH · material del proyecto"},
    # Lo mismo para la casa. Ignacio, 02/09/2026: "aquí está el de
    # compliance, este es para elece". Su buzón es Downloads\ELECELEGAL.
    {"id": "elece", "titulo": "elece Legal", "url": "/material/elece",
     "pie": "Briefings, propuestas y protocolos del despacho"},
    {"id": "compliance_digital", "titulo": "Compliance Digital",
     "pie": "Pendiente de traer el material del proyecto de chat"},
    {"id": "auditoria_compliance", "titulo": "Auditoría Compliance",
     "pie": "Pendiente de traer el material del proyecto de chat"},
]


def _tarjeta(t):
    # Casi todas llevan a /tarjeta/<id>. Alguna tiene pantalla propia y
    # entonces trae su "url" -el Preguntador, que no es un expediente-.
    destino = t.get("url") or f"/tarjeta/{t['id']}"
    return f"""
      <a class="tarjeta" href="{destino}" id="tarjeta-{t['id']}">
        <h2>{t['titulo']}</h2>
        <div class="hueco"></div>
        <p class="pie">{t['pie']}</p>
      </a>"""


def pagina():
    tarjetas = "".join(_tarjeta(t) for t in TARJETAS)
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>IA ELECE</title>
<style>
  @font-face {{
    font-family: 'Dosis';
    src: url('/estatico/dosis.woff2') format('woff2');
    font-weight: 200 800;
    font-display: swap;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    min-height: 100vh;
    background: {ROJO};
    color: #fff;
    font-family: 'Dosis', Arial, Helvetica, sans-serif;
    font-weight: 500;
    display: flex;
    flex-direction: column;
  }}
  header {{
    padding: 34px 40px 10px;
    display: flex;
    align-items: center;
    gap: 22px;
  }}
  header img {{ height: 54px; filter: brightness(0) invert(1); }}
  header .nombre {{
    font-size: 30px;
    letter-spacing: .16em;
    text-transform: uppercase;
  }}
  header .nombre small {{
    display: block;
    font-size: 13px;
    letter-spacing: .22em;
    opacity: .8;
    text-transform: none;
    margin-top: 2px;
  }}
  main {{
    flex: 1;
    padding: 26px 40px 50px;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 26px;
    align-content: start;
    max-width: 1280px;
  }}
  .tarjeta {{
    background: #fff;
    color: {TEXTO};
    border-radius: 10px;
    padding: 26px 26px 20px;
    min-height: 230px;
    display: flex;
    flex-direction: column;
    text-decoration: none;
    box-shadow: 0 10px 24px rgba(0,0,0,.18);
    transition: transform .12s ease, box-shadow .12s ease;
  }}
  .tarjeta:hover {{
    transform: translateY(-3px);
    box-shadow: 0 16px 30px rgba(0,0,0,.26);
  }}
  .tarjeta h2 {{
    margin: 0;
    font-size: 25px;
    font-weight: 600;
    color: {TEXTO};
  }}
  .hueco {{ flex: 1; }}
  .pie {{
    margin: 0;
    font-size: 13px;
    color: {GRIS_MARCA};
    opacity: .75;
    border-top: 1px solid #E7E4DC;
    padding-top: 10px;
  }}
  footer {{
    padding: 0 40px 26px;
    font-size: 12.5px;
    opacity: .75;
    letter-spacing: .04em;
  }}
</style>
</head>
<body>
  <header>
    <img src="/estatico/logo.svg" alt="Elece Legal">
    <div class="nombre">IA ELECE
      <small>Abogacía · Elece Legal</small>
    </div>
  </header>
  <main>{tarjetas}
  </main>
  <footer>Servidor propio de IA ELECE · Colibrí sigue en el suyo, aparte.</footer>
</body>
</html>"""


def pagina_tarjeta(tid):
    t = next((x for x in TARJETAS if x["id"] == tid), None)
    if t is None:
        titulo, cuerpo = "No existe esa tarjeta", ""
    else:
        titulo = t["titulo"]
        cuerpo = ("Esta tarjeta todavía no tiene contenido. Se llenará con lo "
                  "que necesite Mamen para su trabajo.")
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titulo} · IA ELECE</title>
<style>
  @font-face {{
    font-family: 'Dosis';
    src: url('/estatico/dosis.woff2') format('woff2');
    font-weight: 200 800; font-display: swap;
  }}
  body {{
    margin: 0; min-height: 100vh; background: {ROJO}; color: #fff;
    font-family: 'Dosis', Arial, Helvetica, sans-serif; font-weight: 500;
    padding: 40px;
  }}
  a {{ color: #fff; text-decoration: none; font-size: 14px; letter-spacing: .1em; }}
  .hoja {{
    background: #fff; color: {TEXTO}; border-radius: 10px;
    padding: 30px; margin-top: 20px; max-width: 900px; min-height: 320px;
    box-shadow: 0 10px 24px rgba(0,0,0,.18);
  }}
  h1 {{ margin: 0 0 12px; font-size: 27px; font-weight: 600; }}
  p {{ color: {GRIS_MARCA}; }}
</style>
</head>
<body>
  <a href="/">&larr; Volver</a>
  <div class="hoja">
    <h1>{titulo}</h1>
    <p>{cuerpo}</p>
  </div>
</body>
</html>"""


# ---------------------------------------------------------------------------
# LA PUERTA. Sólo se ve cuando IA ELECE está en el servidor del despacho; en
# el puesto de Ignacio no aparece nunca. En rojo, que es el color de la casa.
# ---------------------------------------------------------------------------
PUERTA_HTML = """<!doctype html><meta charset="utf-8"><title>Entrar en IA ELECE</title>
<style>
 body{{margin:0;height:100vh;display:flex;align-items:center;
      justify-content:center;background:#1a1113;color:#f1e7e8;
      font:15px/1.5 -apple-system,Segoe UI,Roboto,sans-serif}}
 form{{background:#2a1a1d;padding:38px 40px;border-radius:14px;width:320px;
       box-shadow:0 18px 50px rgba(0,0,0,.5)}}
 h1{{margin:0 0 4px;font-size:21px;color:#fff;letter-spacing:.04em}}
 p.sub{{margin:0 0 24px;color:#c9a9ad;font-size:13px}}
 label{{display:block;margin:14px 0 5px;font-size:12px;color:#c9a9ad;
       text-transform:uppercase;letter-spacing:.06em}}
 input{{width:100%;box-sizing:border-box;padding:10px 12px;border-radius:8px;
       border:1px solid #4a2f34;background:#1a1113;color:#f1e7e8;font-size:15px}}
 input:focus{{outline:none;border-color:#c0272d}}
 button{{width:100%;margin-top:22px;padding:11px;border:0;border-radius:8px;
        background:#c0272d;color:#fff;font-size:15px;font-weight:600;
        cursor:pointer}}
 button:hover{{background:#a01f25}}
 .mal{{margin-top:16px;padding:9px 11px;border-radius:8px;background:#7f1d1d;
      color:#fecaca;font-size:13px}}
</style>
<form method="post" action="/entrar">
  <h1>IA ELECE</h1><p class="sub">La parte de abogacía del despacho</p>
  <label for="u">Usuario</label>
  <input id="u" name="usuario" autocomplete="username" autofocus>
  <label for="c">Clave</label>
  <input id="c" name="clave" type="password" autocomplete="current-password">
  <button type="submit">Entrar</button>{aviso}
</form>"""
