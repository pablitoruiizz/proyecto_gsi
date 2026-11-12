"""Sprint 3 · buzón: HU-17a (campo trampa y límite de envíos), HU-16b (búsqueda del panel) y E3-08 (aviso y datos mínimos).

Amplía la batería de privacidad RN-03. Sin navegador y solo con la biblioteca estándar.
Uso, desde la raíz del repositorio y con el sitio local arrancado:  python scripts/pruebas/sprint3_buzon.py
Crea un ticket, un centro y dos cuentas temporales, y lo borra todo al terminar (también si falla).
Si se interrumpe:  php scripts/pruebas/sprint3_buzon.php cleanup
"""
import json
import re
import sys
import urllib.parse
from pathlib import Path

import rn03_http as audit

audit.HELPER = Path(__file__).with_suffix('.php')
check, php, request = audit.check, audit.php, audit.request
SECRET, SUBJECT, NAME, EMAIL = 'S3-BUZON-SECRETO', 'S3-BUZON-ASUNTO', 'S3-BUZON-NOMBRE', 'prueba@alum.us.es'
PAGE = '/atencion-al-estudiante/buzon-de-consultas/'
LIST = '/wp-admin/edit.php?post_type=cadus_ticket'


def main():
    baseline = {}
    try:
        baseline = php('status')
        check('Inicio sin restos de una ejecución anterior', baseline['propios'] == 0 and baseline['usuarios_temporales'] == 0
              and baseline['centro_temporal'] == 0, json.dumps(baseline))
        state = php('fixture')
        for label, ok in state['checks'].items():
            check(label, ok)
        code, fid = state['code'], state['form_id']
        ejecutiva, delegado = state['auth']['cadus_ejecutiva'], state['auth']['cadus_delegado']

        print('-- HU-16b: búsqueda en el panel de tickets (por HTTP, con una cuenta de la Ejecutiva)')
        # WordPress repite en la página el término buscado, así que se comprueba el resto de datos del ticket.
        casos = [('asunto', SUBJECT, True), ('trozo del código', state['hex'], True), ('descripción', SECRET, False),
                 ('correo del estudiante', EMAIL, False), ('nombre del estudiante', NAME, False)]
        for label, term, found in casos:
            status, body, headers = request(LIST + '&s=' + urllib.parse.quote(term), ejecutiva)
            otros = [s for s in (SECRET, SUBJECT, NAME, EMAIL) if s != term]
            ok = status == 200 and (code in body) == found and not any(s in body for s in otros)
            check(f'Ejecutiva busca por {label}: ' + ('encuentra el ticket' if found else 'no devuelve nada'), ok, f'HTTP {status}')
            check(f'Búsqueda por {label}: respuesta no cacheable', 'no-store' in headers.get('Cache-Control', ''))
        status, body, _ = request(LIST + '&cadus_estado=abierto&s=' + SUBJECT, ejecutiva)
        check('Búsqueda combinada con el filtro de estado (abierto)', status == 200 and code in body, f'HTTP {status}')
        status, body, _ = request(LIST + '&cadus_estado=cerrado&s=' + SUBJECT, ejecutiva)
        check('Búsqueda combinada con el filtro de estado (cerrado) no lo devuelve', status == 200 and code not in body, f'HTTP {status}')
        status, body, _ = request(LIST, ejecutiva)
        check('El botón de búsqueda dice por qué se busca', 'Buscar por código o asunto' in body)
        status, body, _ = request(LIST + '&s=' + SUBJECT, delegado)
        check('Un delegado no puede buscar tickets', status == 403 and code not in body, f'HTTP {status}')
        status, body, _ = request('/?s=' + SUBJECT)
        check('La búsqueda pública no encuentra el ticket', status < 500 and code not in body and NAME not in body, f'HTTP {status}')
        status, body, _ = request(f'/wp-admin/post.php?post={state["id"]}&action=edit', ejecutiva)
        check('La ficha autorizada sí muestra los datos mínimos del estudiante',
              status == 200 and all(s in body for s in (NAME, EMAIL, 'Datos del estudiante')), f'HTTP {status}')

        print('-- HU-17a y E3-08: formulario del buzón por HTTP, como visitante anónimo')
        status, body, headers = request(PAGE)
        check('GET del buzón no cacheable', status == 200 and 'no-store' in headers.get('Cache-Control', ''), f'HTTP {status}')
        nonce_name = f'_fluentform_{fid}_fluentformnonce'
        honey_name = f'item_{fid}__fluent_sf'
        match = re.search(r'name="' + nonce_name + r'"[^>]*value="([^"]+)"', body)
        check('El formulario lleva nonce y campo trampa oculto', bool(match) and f'name="{honey_name}"' in body)
        check('El formulario pide nombre y apellidos y Facultad o Escuela', 'name="solicitante"' in body and 'name="centro"' in body)
        data = {'solicitante': NAME, 'email': EMAIL, 'centro': state['centro'], 'asunto': SUBJECT, 'tipo': 'Consulta',
                'descripcion': SECRET, 'consentimiento[]': 'acepto', nonce_name: match.group(1) if match else '', honey_name: ''}

        def submit(values):
            return request('/wp-admin/admin-ajax.php', data={'action': 'fluentform_submit', 'form_id': fid,
                           'data': urllib.parse.urlencode(values)})

        for label, field, value in [('sin nonce', nonce_name, ''), ('campo trampa relleno (robot)', honey_name, 'soy-un-robot'),
                                    ('campo trampa ausente', honey_name, None), ('sin nombre', 'solicitante', ''),
                                    ('centro inventado', 'centro', 'NO-EXISTE'), ('correo de otro dominio', 'email', 'prueba@example.com')]:
            invalid = dict(data)
            if value is None:
                del invalid[field]
            else:
                invalid[field] = value
            status, body, headers = submit(invalid)
            check('HTTP rechaza ' + label, status in (422, 423) and 'errors' in body, f'HTTP {status}')
            check('Error no cacheable: ' + label, 'no-store' in headers.get('Cache-Control', ''))
        check('Los rechazos no han creado tickets', php('status')['propios'] == 1)
        status, body, headers = submit(data)
        try:
            response = json.loads(body)
        except ValueError:
            response = {}
        nuevo = re.search(r'CAD-\d{4}-\d{5,20}-[A-F0-9]{32}', body)
        check('HTTP: un envío correcto crea el ticket y entrega el código', status == 200 and response.get('success') is True and nuevo is not None, f'HTTP {status}')
        check('HTTP: la confirmación no repite nombre, correo ni descripción', not any(s in body for s in (SECRET, NAME, EMAIL)))
        check('HTTP: la confirmación no es cacheable', 'no-store' in headers.get('Cache-Control', ''))
        counts = php('status')
        check('HTTP: un único ticket nuevo y ninguna copia en Fluent Forms', counts['propios'] == 2 and counts['ff_entries'] == baseline['ff_entries'], json.dumps(counts))
    finally:
        final = php('cleanup')
        check('Limpieza: sin tickets, cuentas ni centro de prueba', final['propios'] == 0 and final['usuarios_temporales'] == 0
              and final['centro_temporal'] == 0 and final['tickets'] == baseline.get('tickets', final['tickets']), json.dumps(final))
    print('FALLOS:', len(audit.failures))
    return bool(audit.failures)


if __name__ == '__main__':
    sys.exit(main())
