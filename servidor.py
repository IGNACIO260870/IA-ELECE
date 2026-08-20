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

import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse

RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ))

from panel_html import pagina, pagina_tarjeta  # noqa: E402

HOST = "127.0.0.1"   # NO cambiar a 0.0.0.0 sin decidirlo: es un equipo de trabajo
PUERTO = 8100        # el 8000 es de Colibrí

app = FastAPI(title="IA ELECE")


@app.get("/", response_class=HTMLResponse)
def inicio():
    return pagina()


@app.get("/tarjeta/{tid}", response_class=HTMLResponse)
def tarjeta(tid: str):
    return pagina_tarjeta(tid)


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
