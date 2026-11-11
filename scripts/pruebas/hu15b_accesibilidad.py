"""HU-15b · Accesibilidad de la sección «Atención al estudiante» (RNF-03, WCAG 2.1 AA). Solo biblioteca estándar.

Revisa el HTML que sirve el sitio local, sin navegador: etiquetas de los campos de formulario, textos alternativos,
jerarquía de encabezados, atributos ARIA y lo que anunciaría un lector de pantalla en cada formulario.
Uso, desde la raíz del repositorio y con el sitio local arrancado:
    python scripts/pruebas/hu15b_accesibilidad.py            (comprueba y escribe el resultado)
    python scripts/pruebas/hu15b_accesibilidad.py --guardar carpeta   (además guarda el HTML de cada página)
Solo cuentan como fallo los problemas del contenido de la página (lo que hay dentro de <main>); los de la cabecera
y el pie, que son del tema y de la portada (HU-15a), se listan como aviso. Código de salida 1 si hay fallos.
"""
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

BASE = 'http://localhost/proyecto_gsi/cms-wordpress'
PAGINAS = [
    ('Atención al estudiante', '/atencion-al-estudiante/'),
    ('Buzón de consultas', '/atencion-al-estudiante/buzon-de-consultas/'),
    ('Seguimiento de ticket', '/atencion-al-estudiante/seguimiento-de-ticket/'),
    ('Mediación estudiantil', '/atencion-al-estudiante/mediacion-estudiantil/'),
    ('Preguntas frecuentes', '/atencion-al-estudiante/preguntas-frecuentes/'),
    ('Aviso de privacidad', '/aviso-de-privacidad/'),
]
VACIOS = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
sys.stdout.reconfigure(encoding='utf-8')
fallos, avisos = [], []


class Nodo:
    def __init__(self, tag, attrs, padre):
        self.tag, self.attrs, self.padre, self.hijos, self.texto = tag, dict(attrs), padre, [], ''

    def todos(self):
        for hijo in self.hijos:
            yield hijo
            yield from hijo.todos()

    def ancestros(self):
        nodo = self.padre
        while nodo is not None:
            yield nodo
            nodo = nodo.padre

    def contenido(self):
        """Texto que leería un lector de pantalla: el propio, el de los hijos y el alt de las imágenes."""
        partes = [self.texto]
        for hijo in self.hijos:
            if hijo.tag in ('script', 'style') or hijo.attrs.get('aria-hidden') == 'true':
                continue
            if hijo.tag == 'img':
                partes.append(hijo.attrs.get('alt') or '')
            partes.append(hijo.attrs.get('aria-label') or hijo.contenido())
        return ' '.join(' '.join(partes).split())


class Arbol(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.raiz = Nodo('#raiz', [], None)
        self.actual = self.raiz

    def handle_starttag(self, tag, attrs):
        nodo = Nodo(tag, [(k, v if v is not None else '') for k, v in attrs], self.actual)
        self.actual.hijos.append(nodo)
        if tag not in VACIOS:
            self.actual = nodo

    def handle_startendtag(self, tag, attrs):
        self.actual.hijos.append(Nodo(tag, [(k, v if v is not None else '') for k, v in attrs], self.actual))

    def handle_endtag(self, tag):
        nodo = self.actual
        while nodo is not None and nodo.tag != tag:
            nodo = nodo.padre
        if nodo is not None and nodo.padre is not None:
            self.actual = nodo.padre

    def handle_data(self, data):
        self.actual.texto += data


def pedir(ruta, datos=None):
    peticion = urllib.request.Request(BASE + ruta, data=urllib.parse.urlencode(datos).encode() if datos else None)
    try:
        with urllib.request.urlopen(peticion, timeout=45) as r:
            return r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', 'replace')


def oculto(nodo):
    """Fuera del árbol de accesibilidad: hidden, aria-hidden o display:none (como el campo trampa del formulario)."""
    for n in (nodo, *nodo.ancestros()):
        estilo = n.attrs.get('style', '').replace(' ', '').lower()
        if 'hidden' in n.attrs or n.attrs.get('aria-hidden') == 'true' or 'display:none' in estilo:
            return True
    return False


def en_contenido(nodo):
    return any(n.tag == 'main' or n.attrs.get('role') == 'main' for n in (nodo, *nodo.ancestros()))


def nombre_accesible(nodo, ids, etiquetas):
    if nodo.attrs.get('aria-labelledby'):
        return ' '.join(ids[i].contenido() for i in nodo.attrs['aria-labelledby'].split() if i in ids)
    if nodo.attrs.get('aria-label'):
        return nodo.attrs['aria-label']
    if nodo.attrs.get('id') in etiquetas:
        return etiquetas[nodo.attrs['id']].contenido()
    for n in nodo.ancestros():
        if n.tag == 'label':
            return n.contenido()
    return nodo.attrs.get('title', '')


def revisar(nombre, html):
    """Devuelve la lista de (regla, correcto, detalle, dentro_del_contenido) y el guion del lector de pantalla."""
    arbol = Arbol()
    arbol.feed(html)
    nodos = [n for n in arbol.raiz.todos() if n.tag not in ('script', 'style')]
    ids, etiquetas, res, guion = {}, {}, [], []
    repetidos = set()
    for n in nodos:
        if n.attrs.get('id'):
            if n.attrs['id'] in ids:
                repetidos.add(n.attrs['id'])
            ids[n.attrs['id']] = n
        if n.tag == 'label' and n.attrs.get('for'):
            etiquetas[n.attrs['for']] = n

    def anotar(regla, ok, detalle='', dentro=True):
        res.append((regla, ok, detalle, dentro))

    html_tag = next((n for n in nodos if n.tag == 'html'), None)
    anotar('La página declara su idioma (lang="es")', bool(html_tag) and html_tag.attrs.get('lang', '').lower().startswith('es'),
           html_tag.attrs.get('lang', 'sin lang') if html_tag else 'sin <html>')
    titulo = next((n for n in nodos if n.tag == 'title'), None)
    anotar('La página tiene título', bool(titulo and titulo.contenido()))
    anotar('Hay una región principal <main>', any(n.tag == 'main' or n.attrs.get('role') == 'main' for n in nodos))

    # Encabezados: un solo h1 y sin saltos de nivel (de h1 a h3, por ejemplo).
    encabezados = [n for n in nodos if re.fullmatch(r'h[1-6]', n.tag) and not oculto(n)]
    h1 = [n for n in encabezados if n.tag == 'h1']
    anotar('Hay un único encabezado h1', len(h1) == 1, f'{len(h1)} h1: ' + ' | '.join(n.contenido()[:40] for n in h1))
    anterior = 0
    for n in encabezados:
        nivel = int(n.tag[1])
        dentro = en_contenido(n)
        if not n.contenido():
            anotar('Encabezado sin texto', False, n.tag, dentro)
        if anterior and nivel > anterior + 1:
            anotar('Jerarquía de encabezados sin saltos', False, f'de h{anterior} a {n.tag} en «{n.contenido()[:50]}»', dentro)
        anterior = nivel
    if not any(r[0] == 'Jerarquía de encabezados sin saltos' for r in res):
        anotar('Jerarquía de encabezados sin saltos', True, ' > '.join(n.tag for n in encabezados))

    # Imágenes: todas con atributo alt (vacío si son decorativas).
    imagenes = [n for n in nodos if n.tag == 'img' and not oculto(n)]
    for n in imagenes:
        if 'alt' not in n.attrs:
            anotar('Imagen sin texto alternativo', False, n.attrs.get('src', '')[-60:], en_contenido(n))
    if not any(r[0] == 'Imagen sin texto alternativo' for r in res):
        anotar('Todas las imágenes tienen texto alternativo', True, f'{len(imagenes)} imágenes')

    # Campos de formulario: cada uno con su nombre accesible; las ayudas y etiquetas enlazadas existen.
    campos = [n for n in nodos if n.tag in ('input', 'select', 'textarea')
              and n.attrs.get('type', 'text') not in ('hidden', 'submit', 'button', 'reset', 'image') and not oculto(n)]
    sin_nombre = 0
    for n in campos:
        nombre_campo = nombre_accesible(n, ids, etiquetas)
        dentro = en_contenido(n)
        if not nombre_campo.strip():
            sin_nombre += 1
            anotar('Campo de formulario sin etiqueta', False, f'<{n.tag} name="{n.attrs.get("name", "")}">', dentro)
        for atributo in ('aria-describedby', 'aria-labelledby'):
            for ref in n.attrs.get(atributo, '').split():
                if ref not in ids:
                    anotar('Referencia ARIA a un id que no existe', False, f'{atributo}="{ref}" en {n.attrs.get("name", n.tag)}', dentro)
        if dentro:
            ayuda = ' '.join(ids[i].contenido() for i in n.attrs.get('aria-describedby', '').split() if i in ids)
            tipo = {'select': 'desplegable', 'textarea': 'área de texto'}.get(n.tag, {'checkbox': 'casilla', 'radio': 'opción',
                    'email': 'campo de correo', 'search': 'campo de búsqueda'}.get(n.attrs.get('type', 'text'), 'campo de texto'))
            obligatorio = 'required' in n.attrs or n.attrs.get('aria-required') == 'true'
            guion.append(f'{tipo}: «{nombre_campo.strip() or "SIN NOMBRE"}»' + (', obligatorio' if obligatorio else '')
                         + (f'. Ayuda: {ayuda}' if ayuda else ''))
    if campos and not sin_nombre:
        anotar('Todos los campos de formulario tienen etiqueta', True, f'{len(campos)} campos')
    for ref, etiqueta in etiquetas.items():
        if ref not in ids and not oculto(etiqueta):
            anotar('Etiqueta <label for> que no apunta a ningún campo', False, f'for="{ref}" «{etiqueta.contenido()[:40]}»', en_contenido(etiqueta))
    usados = {i for n in nodos for a in ('aria-describedby', 'aria-labelledby', 'for') for i in n.attrs.get(a, '').split()}
    for rep in sorted(repetidos & usados):
        anotar('Id repetido y usado por una etiqueta o por ARIA', False, rep, en_contenido(ids[rep]))

    # Grupos de casillas u opciones (dos o más con el mismo nombre): necesitan un nombre de grupo.
    grupos = {}
    for n in campos:
        if n.attrs.get('type') in ('checkbox', 'radio'):
            grupos.setdefault(n.attrs.get('name', ''), []).append(n)
    for nombre_grupo, miembros in grupos.items():
        if len(miembros) > 1:
            ok = any((a.tag == 'fieldset' and any(h.tag == 'legend' for h in a.hijos))
                     or (a.attrs.get('role') in ('group', 'radiogroup') and (a.attrs.get('aria-label') or a.attrs.get('aria-labelledby')))
                     for a in miembros[0].ancestros())
            anotar('Grupo de casillas con nombre de grupo', ok, nombre_grupo, en_contenido(miembros[0]))

    # Botones y enlaces: con texto que diga qué hacen.
    for n in nodos:
        if oculto(n):
            continue
        es_boton = n.tag == 'button' or (n.tag == 'input' and n.attrs.get('type') in ('submit', 'button', 'reset'))
        if es_boton or (n.tag == 'a' and 'href' in n.attrs):
            texto = n.attrs.get('aria-label') or n.contenido() or n.attrs.get('value') or n.attrs.get('title') or ''
            if n.attrs.get('aria-labelledby'):
                texto = ' '.join(ids[i].contenido() for i in n.attrs['aria-labelledby'].split() if i in ids) or texto
            if not texto.strip():
                anotar('Botón o enlace sin texto', False, f'<{n.tag} {n.attrs.get("href", n.attrs.get("class", ""))[:60]}>', en_contenido(n))
            elif es_boton and en_contenido(n):
                guion.append(f'botón: «{texto.strip()}»')
    if not any(r[0] == 'Botón o enlace sin texto' for r in res):
        anotar('Todos los botones y enlaces tienen texto', True)

    # Desplegables de preguntas: cada <details> con su <summary>.
    for n in nodos:
        if n.tag == 'details' and not any(h.tag == 'summary' and h.contenido() for h in n.hijos):
            anotar('Bloque <details> sin título <summary>', False, n.contenido()[:50], en_contenido(n))
    # Mensajes de estado y de error: anunciados con role="alert" o role="status".
    for n in nodos:
        if 'cadus-aviso' in n.attrs.get('class', '').split() and n.tag == 'p' and en_contenido(n):
            anotar('Mensaje del formulario anunciado (role alert/status)', n.attrs.get('role') in ('alert', 'status'), n.contenido()[:60])
    return res, guion


def informar(nombre, res, guion):
    print(f'\n== {nombre}')
    for regla, ok, detalle, dentro in res:
        if ok:
            print('OK      ' + regla + (f'  [{detalle}]' if detalle else ''))
        elif dentro:
            fallos.append((nombre, regla, detalle))
            print('FALLO   ' + regla + (f'  [{detalle}]' if detalle else ''))
        else:
            avisos.append((nombre, regla, detalle))
            print('AVISO   (cabecera o pie, fuera del contenido) ' + regla + (f'  [{detalle}]' if detalle else ''))
    if guion:
        print('Lo que anuncia un lector de pantalla al recorrer el contenido con el tabulador:')
        for i, linea in enumerate(guion, 1):
            print(f'  {i}. {linea}')


def main():
    carpeta = None
    if '--guardar' in sys.argv:
        carpeta = Path(sys.argv[sys.argv.index('--guardar') + 1])
        carpeta.mkdir(parents=True, exist_ok=True)
    for nombre, ruta in PAGINAS:
        estado, html = pedir(ruta)
        if estado != 200:
            fallos.append((nombre, 'La página responde', f'HTTP {estado}'))
            print(f'\n== {nombre}\nFALLO   La página no responde  [HTTP {estado}]')
            continue
        if carpeta:
            (carpeta / (ruta.strip('/').replace('/', '__') + '.html')).write_text(html, encoding='utf-8')
        informar(nombre, *revisar(nombre, html))
    # Seguimiento con datos que no existen: el mensaje de respuesta debe anunciarse y recibir el foco (un intento del límite).
    ruta = '/atencion-al-estudiante/seguimiento-de-ticket/'
    _, html = pedir(ruta)
    nonce = re.search(r'name="cadus_seguimiento_nonce"[^>]*value="([^"]+)"', html)
    if nonce:
        _, html = pedir(ruta, {'cadus_seguimiento_enviar': '1', 'cadus_seguimiento_nonce': nonce.group(1),
                               'cadus_codigo': 'CAD-2026-00000', 'cadus_correo': 'nadie@alum.us.es'})
        if carpeta:
            (carpeta / 'atencion-al-estudiante__seguimiento-de-ticket__respuesta.html').write_text(html, encoding='utf-8')
        res, guion = revisar('Seguimiento: respuesta', html)
        foco = re.search(r'<div id="([^"]+_resultado)"[^>]*tabindex="-1"', html)
        res.append(('La respuesta del seguimiento recibe el foco (contenedor con tabindex="-1")', bool(foco), foco.group(1) if foco else '', True))
        res.append(('La respuesta del seguimiento se anuncia (role alert/status)', bool(re.search(r'role="(alert|status)"', html)), '', True))
        informar('Seguimiento de ticket: respuesta a una consulta', res, [])
    print(f'\n{len(fallos)} fallos en el contenido, {len(avisos)} avisos de cabecera o pie')
    return 1 if fallos else 0


if __name__ == '__main__':
    sys.exit(main())
