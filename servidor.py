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
import sys
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(RAIZ / "compliance"))

from panel_html import pagina, pagina_tarjeta  # noqa: E402

HOST = "127.0.0.1"   # NO cambiar a 0.0.0.0 sin decidirlo: es un equipo de trabajo
PUERTO = 8100        # el 8000 es de Colibrí

app = FastAPI(title="IA ELECE")


@app.get("/", response_class=HTMLResponse)
def inicio():
    return pagina()


@app.get("/tarjeta/{tid}", response_class=HTMLResponse)
def tarjeta(tid: str):
    # COMPLIANCE YA TIENE CONTENIDO. Las demas tarjetas siguen esperando a
    # que Mamen diga que va dentro; esta se empezo el 25/08/2026.
    if tid == "compliance":
        import pantallas
        return pantallas.pagina_compliance()
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
def compliance_proyecto(clave: str):
    """El expediente de una empresa, con su supervisor y sus entrevistas."""
    import pantallas
    return pantallas.pagina_proyecto(clave)


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
