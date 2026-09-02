# -*- coding: utf-8 -*-
"""
servidor.py  -  IA ELECE

El servidor propio de la parte de ABOGACIA del despacho.

POR QUE OTRO SERVIDOR Y NO UNA PESTAÑA DE COLIBRI. En Elece conviven dos
actividades -Ignacio, 20/08/2026-: la abogacia (Mamen y Marta) y la procura
(Ignacio Tarton y Pilar Pastor). Colibri se hizo para la procura y todo lo
que lleva dentro es de procurador: bandeja de notificaciones, macros,
tasaciones, NIG, presentaciones. Lo que necesita una abogada no se parece a
eso, asi que IA ELECE es otro producto: su carpeta, su servidor, su puerta.

En unos dias los dos iran a un servidor del despacho para que cada uno abra
lo suyo. Por eso desde el primer dia:

  - vive en su propia carpeta, fuera del repositorio de Colibri;
  - escucha en su propio puerto (8100; Colibri usa el 8000), asi que los dos
    pueden estar levantados a la vez sin estorbarse;
  - no da por hecho que corre en el ordenador de Ignacio.

ESCUCHA SOLO EN LOCAL. Igual que Colibri: 127.0.0.1, nunca 0.0.0.0. El dia
que se ponga en el servidor del despacho se abrira con lo que corresponda
-y con quien tenga que entrar-, pero eso se decide entonces, no se deja
abierto por descuido hoy.
"""

import base64
import os
import sys
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "compliance"))

from panel_html import pagina, pagina_tarjeta  # noqa: E402

# DÓNDE ESCUCHA. En el puesto de Ignacio, 127.0.0.1 y nada más. En el
# servidor del despacho se pone IA_ELECE_HOST=0.0.0.0 para que Mamen entre
# desde su navegador, y entonces se enciende sola la puerta de abajo.
HOST = os.environ.get("IA_ELECE_HOST", "127.0.0.1")
PUERTO = int(os.environ.get("IA_ELECE_PUERTO", "8100"))   # el 8000 es de Colibrí

app = FastAPI(title="IA ELECE")

# --------------------------------------------------------------------------- #
# LA PUERTA
#
# DE DÓNDE VIENE. Ignacio, 02/09/2026: "lo de Mamen ya está claro: todo IA
# ELECE debe estar a su disposición, no hace falta ni usuario ni contraseña.
# Yo debo tener acceso a todo para ayudarle".
#
# LA CONTRASEÑA SÍ HACE FALTA, Y ES POR ESTO. Mientras IA ELECE viviera en el
# ordenador de Ignacio, "sin contraseña" quería decir "sin estorbar a quien
# ya está sentado delante". En el servidor del despacho quiere decir otra
# cosa: que cualquiera que se enchufe a la red de la oficina abre el trabajo
# de compliance, las entrevistas y las demandas. No es lo mismo, así que se
# pide una vez.
#
# QUE NO ESTORBE: la sesión dura doce horas y la cookie se queda en su
# navegador, así que Mamen escribe la clave por la mañana y no la vuelve a
# ver en todo el día. Aquí no hay tarjetas ni permisos: quien entra, entra a
# todo. Los permisos por tarjeta son cosa de Colibrí.
# --------------------------------------------------------------------------- #
# SE CARGA POR RUTA, NO METIENDO LA CARPETA EN sys.path. La primera versión
# hacía `sys.path.insert(0, ...colibri-servidor/webapp)` y con eso el
# `import supervisor` de IA ELECE dejaba de encontrar el suyo -el de
# compliance- y se traía el de Colibrí, que se llama igual y no tiene nada
# que ver. La pantalla de compliance se caía con un 500.
def _cargar_usuarios():
    import importlib.util                                # noqa: PLC0415
    ruta = Path(os.environ.get(
        "COLIBRI_WEBAPP",
        r"C:/Users/Ignacio/Desktop/colibri-servidor/webapp")) / "usuarios.py"
    spec = importlib.util.spec_from_file_location("colibri_usuarios", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


_U = _cargar_usuarios()

COOKIE = "iaelece_sesion"
# LAWSCALE entra aquí también: es el proyecto especial de Mamen, y su
# material vive en IA ELECE como una tarjeta más.
PUEDEN = ("mamen", "ignacio", "lawscale")


@app.middleware("http")
async def _puerta(request: Request, call_next):
    if HOST == "127.0.0.1" or request.url.path.startswith(
            ("/entrar", "/salir", "/estatico/")):
        return await call_next(request)
    quien = _U.de_la_cookie(request.cookies.get(COOKIE))
    if quien not in PUEDEN:
        return RedirectResponse("/entrar", status_code=303)
    request.state.usuario = quien
    return await call_next(request)


@app.get("/entrar", response_class=HTMLResponse)
def puerta(mal: int = 0):
    from panel_html import PUERTA_HTML                   # noqa: PLC0415
    return PUERTA_HTML.format(aviso=(
        '<div class="mal">Ese usuario o esa clave no son.</div>' if mal else ""))


@app.post("/entrar")
def puerta_abrir(usuario: str = Form(...), clave: str = Form(...)):
    quien = (usuario or "").strip().lower()
    if quien not in PUEDEN or not _U.comprobar(quien, clave):
        return RedirectResponse("/entrar?mal=1", status_code=303)
    r = RedirectResponse("/", status_code=303)
    r.set_cookie(COOKIE, _U.firmar(quien), httponly=True, samesite="lax",
                 max_age=_U.DURACION)
    return r


@app.get("/salir")
def puerta_cerrar():
    r = RedirectResponse("/entrar", status_code=303)
    r.delete_cookie(COOKIE)
    return r


@app.get("/", response_class=HTMLResponse)
def inicio():
    return pagina()


@app.get("/preguntador", response_class=HTMLResponse)
def preguntador(request: Request, aviso: str = ""):
    """La conversación de quien haya entrado, y la caja para preguntar."""
    import pantallas, preguntador as P                   # noqa: PLC0415
    quien = getattr(request.state, "usuario", "") or "mamen"
    return pantallas.pagina_preguntador(quien, P.historial(quien), aviso)


@app.post("/preguntador/preguntar")
def preguntador_preguntar(request: Request, texto: str = Form("")):
    """Una pregunta. Se guarda el turno y se vuelve a la conversación.

    SE VUELVE CON UN 303 Y NO SE PINTA LA RESPUESTA AQUÍ: así, al recargar la
    página, no se repite la pregunta.
    """
    import preguntador as P                              # noqa: PLC0415
    quien = getattr(request.state, "usuario", "") or "mamen"
    r = P.preguntar(quien, texto)
    if r.get("ok"):
        return RedirectResponse("/preguntador", status_code=303)
    from urllib.parse import quote                       # noqa: PLC0415
    return RedirectResponse(f"/preguntador?aviso={quote(r.get('dicho', ''))}",
                            status_code=303)


@app.get("/preguntador/limpiar")
def preguntador_limpiar(request: Request):
    import preguntador as P                              # noqa: PLC0415
    P.borrar(getattr(request.state, "usuario", "") or "mamen")
    return RedirectResponse("/preguntador", status_code=303)


@app.get("/material/{clave}", response_class=HTMLResponse)
def material(clave: str):
    """El material de una marca: LawScale o elece Legal."""
    import material as M, pantallas                      # noqa: PLC0415
    if clave not in M.COLECCIONES:
        return RedirectResponse("/", status_code=303)
    return pantallas.pagina_material(clave)


@app.get("/material/{clave}/leer/{nombre}", response_class=HTMLResponse)
def material_leer(clave: str, nombre: str):
    import material as M, pantallas                      # noqa: PLC0415
    if clave not in M.COLECCIONES:
        return RedirectResponse("/", status_code=303)
    texto = M.texto_de(M.COLECCIONES[clave], nombre)
    if texto is None:
        return RedirectResponse(f"/material/{clave}", status_code=303)
    return pantallas.pagina_material_leer(clave, nombre, texto)


@app.get("/material/{clave}/doc/{nombre}")
def material_doc(clave: str, nombre: str):
    """Sirve un fichero del material. La ruta la valida `material.py`."""
    import material as M                                 # noqa: PLC0415
    if clave not in M.COLECCIONES:
        return RedirectResponse("/", status_code=303)
    ruta = M.ruta_de(M.COLECCIONES[clave], nombre)
    if ruta is None:
        return RedirectResponse(f"/material/{clave}", status_code=303)
    # LAS IMÁGENES SE VEN, NO SE DESCARGAN: pasar `filename` obliga al
    # navegador a bajarse el fichero y el logo salía como icono roto.
    if ruta.suffix.lower() in (".png", ".jpg", ".jpeg", ".gif", ".svg"):
        return FileResponse(str(ruta))
    return FileResponse(str(ruta), filename=ruta.name)


@app.get("/lawscale")
def lawscale_viejo():
    """La dirección de antes sigue valiendo: puede estar en un favorito."""
    return RedirectResponse("/material/lawscale", status_code=308)


@app.get("/tarjeta/{tid}", response_class=HTMLResponse)
def tarjeta(tid: str):
    # COMPLIANCE YA TIENE CONTENIDO. Las demas tarjetas siguen esperando a
    # que Mamen diga que va dentro; esta se empezo el 25/08/2026.
    if tid == "compliance":
        import pantallas
        return pantallas.pagina_compliance()
    if tid == "herramientas":
        import pantallas
        return pantallas.pagina_herramientas()
    return pagina_tarjeta(tid)


@app.get("/compliance/informe", response_class=HTMLResponse)
def compliance_informe():
    """El informe ejecutivo: base, metodologia y sistema de trabajo."""
    from informe_html import INFORME
    return INFORME


@app.get("/compliance/metodologia", response_class=HTMLResponse)
def compliance_metodologia():
    """Las escalas y los pesos, para poder ensenarlos."""
    import pantallas
    return pantallas.pagina_metodologia()


@app.get("/compliance/proyecto/{clave}", response_class=HTMLResponse)
def compliance_proyecto(clave: str, editar: str = ""):
    """El expediente de una empresa, con su supervisor y sus entrevistas.

    `editar` trae el campo que se quiere corregir: todo lo contestado se
    puede volver a tocar."""
    import pantallas
    return pantallas.pagina_proyecto(clave, editar)


@app.post("/compliance/proyecto/{clave}/datos")
async def compliance_datos(clave: str, peticion: Request):
    """Corrige el nombre, el CIF, el tipo de trabajo o el responsable."""
    from urllib.parse import parse_qs, unquote_plus
    import proyectos
    p = proyectos.leer(clave)
    if p is None:
        return RedirectResponse("/tarjeta/compliance", status_code=303)
    crudo = parse_qs((await peticion.body()).decode("utf-8"))
    datos = {k: unquote_plus(v[0]) for k, v in crudo.items()}
    for campo in ("empresa", "cif", "tipo_trabajo", "responsable"):
        if campo in datos:
            p[campo] = datos[campo].strip()
    proyectos.guardar(p)
    return RedirectResponse(f"/compliance/proyecto/{clave}", status_code=303)


@app.post("/compliance/proyecto/{clave}/entrevista/{fichero}/procesar")
def compliance_procesar(clave: str, fichero: str):
    """Saca el texto de una entrevista, si se puede sacar."""
    import procesar_entrevista
    procesar_entrevista.procesar(clave, fichero)
    return RedirectResponse(
        f"/compliance/proyecto/{clave}/entrevista/{fichero}/texto",
        status_code=303)


@app.get("/compliance/proyecto/{clave}/entrevista/{fichero}/texto",
         response_class=HTMLResponse)
def compliance_texto(clave: str, fichero: str):
    """El texto de la entrevista: verlo o pegarlo."""
    import pantallas
    return pantallas.pagina_transcripcion(clave, fichero)


@app.post("/compliance/proyecto/{clave}/entrevista/{fichero}/texto")
async def compliance_texto_guardar(clave: str, fichero: str,
                                   peticion: Request):
    from urllib.parse import parse_qs, unquote_plus
    import procesar_entrevista
    crudo = parse_qs((await peticion.body()).decode("utf-8"))
    texto = unquote_plus((crudo.get("texto") or [""])[0])
    procesar_entrevista.guardar_transcripcion(clave, fichero, texto)
    return RedirectResponse(f"/compliance/proyecto/{clave}", status_code=303)


@app.post("/compliance/proyecto/{clave}/entrevista/{fichero}/confirmar")
def compliance_confirmar(clave: str, fichero: str):
    """Mamen da por buena la entrevista. Sin esto no cuenta como hecha."""
    import procesar_entrevista
    procesar_entrevista.confirmar(clave, fichero, True)
    return RedirectResponse(f"/compliance/proyecto/{clave}", status_code=303)


@app.get("/compliance/proyecto/{clave}/aplicabilidad", response_class=HTMLResponse)
def compliance_aplicabilidad(clave: str):
    """Los 43 delitos, uno a uno, con su motivo."""
    import pantallas
    return pantallas.pagina_aplicabilidad(clave)


@app.post("/compliance/proyecto/{clave}/aplicabilidad")
async def compliance_aplicabilidad_guardar(clave: str, peticion: Request):
    """Guarda la decision de cada delito. Un descarte sin motivo no vale."""
    from urllib.parse import parse_qs, unquote_plus
    import catalogo, proyectos
    p = proyectos.leer(clave)
    if p is None:
        return RedirectResponse("/tarjeta/compliance", status_code=303)
    crudo = parse_qs((await peticion.body()).decode("utf-8"))
    datos = {k: unquote_plus(v[0]) for k, v in crudo.items()}
    fuera = []
    for idd, nombre, _fam, ref, _sev, _nota in catalogo.DELITOS:
        elegido = datos.get(f"ap_{idd}")
        fuera.append({
            "id": idd, "nombre": nombre, "referencia": ref,
            "aplica": (True if elegido == "si"
                       else (False if elegido == "no" else None)),
            "motivo": (datos.get(f"mo_{idd}") or "").strip(),
        })
    p["delitos"] = fuera
    proyectos.guardar(p)
    return RedirectResponse(f"/compliance/proyecto/{clave}", status_code=303)


@app.post("/compliance/proyecto/{clave}/responder")
async def compliance_responder(clave: str, peticion: Request):
    """Guarda una respuesta y pasa a la siguiente pregunta."""
    from urllib.parse import parse_qs, unquote_plus
    import preguntas, proyectos
    p = proyectos.leer(clave)
    if p is None:
        return RedirectResponse("/tarjeta/compliance", status_code=303)
    crudo = parse_qs((await peticion.body()).decode("utf-8"))
    datos = {k: [unquote_plus(x) for x in v] for k, v in crudo.items()}
    campo = (datos.get("campo") or [""])[0]
    valores = datos.get("valor") or [""]
    valor = valores if campo == "disparadores" else valores[0]
    preguntas.guardar_respuesta(p, campo, valor)
    if campo == "apetito":
        # El umbral no vale sin saber QUIEN lo aprobo: es una decision
        # indelegable del organo de gobierno, no un numero suelto.
        p["apetito_firmado_por"] = (datos.get("firmado") or [""])[0].strip()
        p["apetito_fecha"] = (datos.get("fecha") or [""])[0].strip()
    proyectos.guardar(p)
    return RedirectResponse(f"/compliance/proyecto/{clave}", status_code=303)


@app.get("/compliance/herramientas", response_class=HTMLResponse)
def compliance_herramientas(sector: str = ""):
    """La biblioteca de la casa, por sector."""
    import pantallas
    return pantallas.pagina_herramientas(sector)


@app.post("/compliance/herramientas/nutrir")
async def compliance_nutrir(peticion: Request):
    """Vuelca las conductas y controles de un proyecto a la biblioteca."""
    from urllib.parse import parse_qs, unquote_plus
    import biblioteca
    crudo = parse_qs((await peticion.body()).decode("utf-8"))
    datos = {k: unquote_plus(v[0]) for k, v in crudo.items()}
    biblioteca.nutrir_desde(datos.get("clave", ""), datos.get("sector", "general"))
    return RedirectResponse(
        f"/compliance/herramientas?sector={datos.get('sector','')}",
        status_code=303)


@app.get("/compliance/proyecto/{clave}/entrevista/{fichero}/editor",
         response_class=HTMLResponse)
def compliance_editor(clave: str, fichero: str):
    """El editor de la entrevista: turnos, hablante y resaltado."""
    import pantallas
    return pantallas.pagina_editor(clave, fichero)


@app.post("/compliance/proyecto/{clave}/entrevista/{fichero}/edicion")
async def compliance_edicion(clave: str, fichero: str, datos: dict):
    """Guarda la edicion. NO toca la transcripcion original."""
    import editor_entrevistas
    editor_entrevistas.guardar(clave, fichero, datos)
    return {"ok": True}


@app.post("/compliance/proyecto/{clave}/entrevista/{fichero}/ficha")
def compliance_ficha_entrevista(clave: str, fichero: str, datos: dict):
    """Identifica area y entrevistado."""
    import proyectos
    p = proyectos.leer(clave)
    if p is None:
        return {"ok": False}
    for e in p.get("entrevistas") or []:
        if e.get("fichero") == fichero:
            e["area"] = (datos.get("area") or "").strip()
            e["entrevistado"] = (datos.get("quien") or "").strip()
    proyectos.guardar(p)
    return {"ok": True}


@app.get("/compliance/entrevistas", response_class=HTMLResponse)
def compliance_entrevistas(d: str = ""):
    """La arquitectura de entrevistas por departamento."""
    import pantallas
    return pantallas.pagina_entrevistas(d)


@app.get("/compliance/documentacion", response_class=HTMLResponse)
def compliance_documentacion(cif: str = "", nombre: str = "", web: str = ""):
    """Todo lo que se saca del CIF sin pedirselo a nadie."""
    import pantallas
    return pantallas.pagina_documentacion(cif, nombre, web)


@app.get("/compliance/matriz.xlsx")
def compliance_plantilla():
    """La matriz en blanco: la herramienta principal de la tarjeta.

    Sale siempre recien generada, con el catalogo y los criterios vigentes.
    Nadie trabaja sobre una copia vieja sin saberlo."""
    import generar_excel
    sitio = (RAIZ / "datos" / "plantillas" /
             "ELC-CP-PLANTILLA-MTZ_Matriz_riesgos_penales.xlsx")
    generar_excel.generar(sitio, None)
    return FileResponse(sitio, filename=sitio.name, media_type=(
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"))


@app.get("/compliance/proyecto/{clave}/entregable/{nombre}")
def compliance_entregable(clave: str, nombre: str):
    """Abre un entregable ya generado del expediente.

    Ignacio, 26/08/2026: "no puedo descargar". Estaban en el disco pero sin
    puerta desde la pantalla que los anuncia."""
    import proyectos
    if "/" in nombre or "\\" in nombre or nombre.startswith("."):
        return HTMLResponse("no", status_code=400)
    sitio = proyectos.carpeta(clave) / "entregables" / nombre
    if not sitio.is_file():
        return HTMLResponse("ese entregable no esta generado todavia",
                            status_code=404)
    return FileResponse(sitio, filename=nombre)


@app.get("/compliance/proyecto/{clave}/matriz.xlsx")
def compliance_matriz(clave: str):
    """La matriz en Excel, con la metodologia dentro y calculando sola.

    Se genera cada vez: asi el fichero sale siempre con el catalogo y los
    criterios vigentes, y nunca con una copia vieja de hace tres meses."""
    import entregables, generar_excel, proyectos
    p = proyectos.leer(clave)
    if p is None:
        return HTMLResponse("no existe ese proyecto", status_code=404)
    if not p.get("codigo"):
        p["codigo"] = entregables.codigo(p["empresa"], "MTZ")
        proyectos.guardar(p)
    nombre = f"{p['codigo']}_Matriz_riesgos_penales.xlsx"
    sitio = proyectos.carpeta(clave) / "entregables" / nombre
    generar_excel.generar(sitio, p)
    return FileResponse(sitio, filename=nombre, media_type=(
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"))


@app.post("/compliance/proyecto")
async def compliance_crear(peticion: Request):
    """Abre un proyecto. Llega del formulario de la tarjeta."""
    import proyectos
    cuerpo = (await peticion.body()).decode("utf-8")
    from urllib.parse import parse_qs, unquote_plus
    datos = {k: unquote_plus(v[0]) for k, v in parse_qs(cuerpo).items()}
    nombre = (datos.get("empresa") or "").strip()
    if not nombre:
        return RedirectResponse("/tarjeta/compliance", status_code=303)
    p = proyectos.crear(nombre, cif=datos.get("cif", ""),
                        tipo_trabajo=datos.get("tipo_trabajo", ""))
    return RedirectResponse(f"/compliance/proyecto/{p['clave']}",
                            status_code=303)


@app.post("/compliance/proyecto/{clave}/entrevista")
def compliance_entrevista(clave: str, datos: dict):
    """El canal de entrevistas: audio, video o notas, al expediente.

    Llega en base64 desde el navegador para no depender de multipart: un
    equipo del despacho no tiene por que tener nada instalado."""
    import proyectos
    try:
        crudo = base64.b64decode(datos.get("datos", ""), validate=True)
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "porque": f"el fichero no llego entero: {e!s:.50}"}
    if not crudo:
        return {"ok": False, "porque": "el fichero venia vacio"}
    return proyectos.guardar_entrevista(
        clave, datos.get("nombre", "entrevista"), crudo,
        area=(datos.get("area") or "").strip(),
        quien=(datos.get("quien") or "").strip())


@app.get("/estatico/{nombre}")
def estatico(nombre: str):
    """El logo y la letra, servidos del disco.

    Se comprueba que el nombre no traiga rutas: un fichero estatico es un
    fichero de esta carpeta, no una excusa para leer el disco entero."""
    if "/" in nombre or "\\" in nombre or nombre.startswith("."):
        return HTMLResponse("no", status_code=400)
    sitio = RAIZ / "estatico" / nombre
    if not sitio.is_file():
        return HTMLResponse("no está", status_code=404)
    return FileResponse(sitio)


def main():
    import uvicorn
    print("=" * 62)
    print("  IA ELECE  ·  la parte de abogacía del despacho")
    print(f"  http://{HOST}:{PUERTO}")
    print("  Colibrí sigue en el 8000: los dos pueden estar a la vez.")
    print("  Para pararlo: Ctrl+C")
    print("=" * 62)
    uvicorn.run(app, host=HOST, port=PUERTO, log_level="info")


if __name__ == "__main__":
    main()
