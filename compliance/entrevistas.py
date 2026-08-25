# -*- coding: utf-8 -*-
r"""
entrevistas.py

La arquitectura de entrevistas por departamento.

Ignacio, 25/08/2026: "otro apartado dentro de herramientas, las entrevistas.
Dentro pon una arquitectura básica de entrevistas por departamento".

CÓMO SE HACEN HOY, que es lo que hay que respetar: las hace Mamen,
presenciales, en la empresa, una hora larga con el responsable del área. Van
explicando todo lo referente a su área y se les pide documentación y
evidencias. Eso no se toca: es lo que hace que el traje sea a medida. Lo que
aporta esta arquitectura es que Mamen entre con las preguntas de los delitos
que tocan a ESA área, y no con un cuestionario igual para todos.

LAS PREGUNTAS SON ABIERTAS A PROPÓSITO. Una pregunta cerrada -"¿tenéis un
procedimiento de compras?"- se contesta "sí" y no deja nada. La misma en
abierto -"cuéntame cómo entra un proveedor nuevo, desde que aparece hasta que
se le paga la primera factura"- deja el proceso, los nombres, los importes y,
casi siempre, el punto por donde se cuela el riesgo. En una hora no da tiempo
a leer una lista: da tiempo a que alguien cuente cómo trabaja.

CADA PREGUNTA ALIMENTA ALGO. Va marcado, porque de ahí sale la puntuación:

    exposición   ¿hace la empresa esto, y cuánto?
    historial    ¿ha pasado algo ya?
    control      ¿qué lo contiene?
    evidencia    ¿qué documento lo demuestra?

LO QUE NO ES ESTO. No es un checklist de auditoría ni un cuestionario para
mandar por correo. Es el guion de quien va a escuchar.
"""
from __future__ import annotations

# Un aviso de una línea al empezar. Informar no es pedir permiso: no corta la
# conversación y quita de encima el único punto por el que podrían levantar
# un hallazgo en el propio sistema del despacho.
AVISO_GRABACION = (
    "«Voy a grabar la conversación sólo para transcribirla y poder trabajar "
    "después con lo que me cuentes. No se comparte fuera del equipo del "
    "proyecto y se borra al cerrar el expediente.»")

# Preguntas que valen para cualquier área. Van siempre, y van primero: sin
# entender el proceso no se puede valorar nada de lo que venga después.
COMUNES = [
    ("Cuéntame qué hace tu área, de principio a fin: por dónde entra el "
     "trabajo y por dónde sale.", "exposición"),
    ("¿Cuántas personas sois y quién decide qué? ¿Qué puedes firmar tú solo "
     "y a partir de dónde necesitas a alguien más?", "control"),
    ("¿Con qué terceros trabajáis: proveedores, agentes, intermediarios, "
     "subcontratas? ¿Cuántos y desde cuándo?", "exposición"),
    ("¿Qué volumen movéis al año, en euros o en operaciones?", "exposición"),
    ("En los últimos tres años, ¿habéis tenido alguna inspección, "
     "reclamación, denuncia interna o expediente? ¿En qué quedó?", "historial"),
    ("Si algo se hiciera mal en tu área, ¿por dónde crees que se colaría?",
     "exposición"),
    ("¿Qué está escrito y dónde? Procedimientos, instrucciones, plantillas.",
     "evidencia"),
]

# (clave, departamento, delitos del catálogo que le tocan, preguntas, papeles)
DEPARTAMENTOS = [
    ("direccion", "Dirección y Corporativo",
     ["D16", "D18", "D19", "D37", "D38", "D15", "D41"],
     [("¿Cómo se toman las decisiones que comprometen a la sociedad? "
       "¿Consejo, administrador único, apoderados?", "control"),
      ("¿Quién tiene poderes y con qué límites de importe? ¿Cuándo se "
       "revisaron por última vez?", "control"),
      ("¿Hacéis regalos, invitaciones o atenciones a clientes o a "
       "funcionarios? ¿Hay algún límite escrito?", "exposición"),
      ("¿Participáis en licitaciones o recibís subvenciones? ¿Quién prepara "
       "esas ofertas?", "exposición"),
      ("¿Hay operaciones con partes vinculadas, préstamos a socios o "
       "sociedades del grupo?", "exposición"),
      ("¿Cómo se comunica a la plantilla lo que la dirección espera en "
       "materia de conducta? ¿Hay algo más que un documento colgado?",
       "control")],
     ["Escritura, estatutos y poderes vigentes", "Actas de los dos últimos años",
      "Código de conducta y evidencia de su difusión",
      "Política de regalos y atenciones", "Mapa del grupo y participadas"]),

    ("rrhh", "Recursos Humanos",
     ["D24", "D03", "D04", "D25", "D40", "D02"],
     [("¿Cómo se contrata a alguien, desde que se abre el puesto hasta que "
       "entra? ¿Quién comprueba la documentación?", "exposición"),
      ("¿Trabajáis con ETT, subcontratas o autónomos? ¿Cómo verificáis que "
       "están de alta y al corriente?", "exposición"),
      ("¿Qué pasa si alguien denuncia un acoso o un trato indebido? "
       "Cuéntame el último caso que recuerdes.", "historial"),
      ("¿Hay canal de denuncias? ¿Quién lo gestiona y cómo se garantiza que "
       "no haya represalias?", "control"),
      ("¿Cómo se controla la jornada, las horas extra y la prevención de "
       "riesgos?", "exposición"),
      ("¿Qué formación reciben y cómo se acredita que la hicieron?",
       "evidencia")],
     ["Plantilla y organigrama", "Modelos de contrato",
      "Procedimiento del canal de denuncias y registro de comunicaciones",
      "Protocolo de acoso", "Registro de formación",
      "Contratos con ETT y subcontratas"]),

    ("finanzas", "Control de Gestión y Finanzas",
     ["D20", "D21", "D22", "D23", "D18", "D07", "D08", "D09", "D14"],
     [("Cuéntame cómo se paga una factura, desde que llega hasta que sale el "
       "dinero. ¿Quién autoriza en cada paso?", "control"),
      ("¿Se admiten cobros o pagos en efectivo? ¿Hasta qué importe?",
       "exposición"),
      ("¿Cómo se comprueba a quién se está pagando? ¿Verificáis titularidad "
       "de cuenta y domicilio fiscal?", "control"),
      ("¿Quién prepara los impuestos y quién los revisa antes de "
       "presentarlos?", "control"),
      ("¿Habéis tenido requerimientos, actas o sanciones de la Agencia "
       "Tributaria o de la Seguridad Social? ¿Cuándo y por qué?", "historial"),
      ("Si cobráis subvenciones o fondos europeos, ¿quién justifica el "
       "gasto?", "exposición"),
      ("¿Cómo se detecta un cambio de cuenta bancaria de un proveedor?",
       "control")],
     ["Manual contable y de impuestos", "Cuentas anuales y memoria",
      "Política de autorizaciones y límites de gasto",
      "Requerimientos y actas de inspección", "Auditoría externa, si la hay",
      "Justificación de subvenciones"]),

    ("compras", "Compras y Cadena de Suministro",
     ["D16", "D14", "D18", "D43", "D02", "D28"],
     [("¿Cómo entra un proveedor nuevo, desde que aparece hasta que se le "
       "paga la primera factura?", "exposición"),
      ("¿Qué le pedís antes de trabajar con él? ¿Alguna comprobación de "
       "quién está detrás?", "control"),
      ("¿Hay agentes, comisionistas o intermediarios? ¿Cómo se fija su "
       "comisión?", "exposición"),
      ("¿Compráis fuera de la Unión Europea? ¿Quién se ocupa de la aduana?",
       "exposición"),
      ("¿Cómo se adjudica una compra grande? ¿Se piden varias ofertas?",
       "control"),
      ("¿Habéis rechazado o roto con algún proveedor por un problema de "
       "conducta?", "historial")],
     ["Procedimiento de compras y de homologación de proveedores",
      "Listado de proveedores con antigüedad y volumen",
      "Contratos tipo y cláusulas de compliance",
      "Contratos con agentes e intermediarios",
      "Documentación aduanera"]),

    ("comercial", "Comercial y Ventas",
     ["D07", "D16", "D14", "D12", "D13", "D06"],
     [("¿Cómo se cierra una venta y quién puede dar un descuento o una "
       "condición especial?", "control"),
      ("¿Qué se le promete al cliente por escrito y qué se le promete de "
       "palabra?", "exposición"),
      ("¿Hay incentivos o comisiones por objetivos? ¿Qué pasa si alguien no "
       "llega?", "exposición"),
      ("¿Vendéis a administraciones públicas? ¿Cómo se preparan esas "
       "ofertas?", "exposición"),
      ("¿Cómo se trata la información de clientes y sus datos?", "control"),
      ("¿Ha habido alguna reclamación por publicidad o por lo que se "
       "ofreció?", "historial")],
     ["Política comercial y de descuentos", "Plan de incentivos",
      "Contratos tipo con clientes", "Reclamaciones de los últimos tres años"]),

    ("marketing", "Marketing y Producto",
     ["D14", "D12", "D13", "D40", "D33"],
     [("¿Quién aprueba una campaña antes de publicarla?", "control"),
      ("¿Cómo se comprueba que lo que se anuncia es lo que el producto "
       "hace?", "control"),
      ("¿Usáis imágenes, marcas, música o contenidos de terceros? ¿Con qué "
       "licencia?", "exposición"),
      ("¿Hacéis comparativas con la competencia?", "exposición"),
      ("¿Ha habido alguna reclamación de consumo, de un competidor o de "
       "Autocontrol?", "historial")],
     ["Procedimiento de aprobación de campañas",
      "Licencias de contenidos y marcas", "Fichas y etiquetado de producto",
      "Reclamaciones recibidas"]),

    ("produccion", "Producción y Operaciones",
     ["D24", "D28", "D31", "D33", "D29", "D30"],
     [("Cuéntame el proceso productivo y dónde están los puntos peligrosos.",
       "exposición"),
      ("¿Qué residuos generáis y a dónde van? ¿Quién los retira?",
       "exposición"),
      ("¿Manejáis sustancias peligrosas, explosivos o gases?", "exposición"),
      ("¿Qué autorizaciones o licencias necesitáis y cuándo caducan?",
       "evidencia"),
      ("¿Cómo se controla la seguridad de quien está en la línea? ¿Y la de "
       "las subcontratas que entran?", "control"),
      ("¿Ha habido accidentes, vertidos o incidentes? ¿Qué se hizo después?",
       "historial")],
     ["Licencias y autorizaciones ambientales",
      "Contratos de gestión de residuos y justificantes de retirada",
      "Plan de prevención y evaluaciones de riesgos",
      "Registro de accidentes e incidentes",
      "Fichas de seguridad de sustancias"]),

    ("calidad", "Calidad y Medioambiente",
     ["D28", "D33", "D29", "D24", "D32"],
     [("¿Qué certificaciones tenéis y quién las audita?", "evidencia"),
      ("¿Cómo se abre y se cierra una no conformidad? Enséñame una.",
       "control"),
      ("¿Cómo se verifica que una acción correctiva ha servido, no sólo que "
       "se hizo?", "control"),
      ("¿Qué mediciones ambientales hacéis y con qué frecuencia?",
       "evidencia"),
      ("¿Ha habido alguna inspección ambiental o sanitaria?", "historial")],
     ["Certificados vigentes e informes de auditoría",
      "Procedimiento de no conformidades y acciones correctivas",
      "Registros de mediciones y controles",
      "Actas de inspección"]),

    ("sistemas", "Sistemas y Tecnología",
     ["D11", "D06", "D12", "D18"],
     [("¿Quién tiene acceso a qué, y qué pasa cuando alguien se va?",
       "control"),
      ("¿Cómo se detecta un acceso indebido o una fuga de información?",
       "control"),
      ("¿Todo el software está licenciado? ¿Quién lo controla?",
       "exposición"),
      ("¿Habéis tenido un incidente de seguridad, un ransomware, un correo "
       "fraudulento que colara?", "historial"),
      ("¿Hay copias de seguridad y se ha probado alguna vez restaurarlas?",
       "control")],
     ["Política de accesos y altas/bajas",
      "Inventario de licencias de software",
      "Registro de incidentes de seguridad",
      "Política de copias y evidencia de pruebas de restauración"]),

    ("legal", "Legal y Compliance",
     ["D17", "D08", "D09", "D41", "D42", "D35", "D36"],
     [("¿Quién es el órgano de compliance y de quién depende? ¿Puede llegar "
       "al órgano de gobierno sin filtros?", "control"),
      ("¿Con qué medios cuenta: personas, presupuesto, tiempo?", "control"),
      ("¿Qué procedimientos judiciales o administrativos hay abiertos?",
       "historial"),
      ("¿Cómo se atiende una inspección cuando se presenta sin avisar?",
       "control"),
      ("¿Cuándo se revisó por última vez el mapa de riesgos y por qué?",
       "evidencia"),
      ("¿Qué se hizo con los hallazgos de la última revisión?", "control")],
     ["Nombramiento y estatuto del órgano de compliance",
      "Mapa de riesgos anterior y sus revisiones",
      "Relación de procedimientos abiertos",
      "Informes al órgano de gobierno",
      "Actas de la última revisión por la dirección"]),
]


def departamento(clave):
    return next((d for d in DEPARTAMENTOS if d[0] == clave), None)


def delitos_de(clave):
    """Los delitos del catálogo que le tocan a un departamento."""
    import catalogo                                  # noqa: PLC0415
    d = departamento(clave)
    if not d:
        return []
    ids = set(d[2])
    return [x for x in catalogo.DELITOS if x[0] in ids]


def guion(clave):
    """El guion completo de una entrevista: comunes + propias + papeles."""
    d = departamento(clave)
    if not d:
        return None
    return {"clave": d[0], "departamento": d[1],
            "aviso": AVISO_GRABACION,
            "delitos": delitos_de(clave),
            "comunes": COMUNES, "propias": d[3], "papeles": d[4],
            "minutos": 60}
