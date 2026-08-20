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
    {"id": "proyectos", "titulo": "Proyectos",
     "pie": "Por definir con Mamen"},
    {"id": "compliance", "titulo": "Compliance",
     "pie": "Por definir con Mamen"},
]


def _tarjeta(t):
    return f"""
      <a class="tarjeta" href="/tarjeta/{t['id']}" id="tarjeta-{t['id']}">
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
