"""RN-03/HU-12: servicio FF, HTTP anónimo/REST y panel, sin navegador. Limpieza en finally."""
import concurrent.futures
import json
import re
import sys
import urllib.parse
from pathlib import Path

import rn03_http as audit

audit.HELPER = Path(__file__).with_suffix('.php')
check, php, request = audit.check, audit.php, audit.request
SECRET = 'RN03-MEDIACION-SECRETO'
NAME = 'RN03-MEDIACION-SOLICITANTE'
PAGE = '/atencion-al-estudiante/mediacion-estudiantil/'


def main():
    state = {}
    try:
        baseline = php('status')
        check('Inicio limpio', all(value == 0 for value in baseline.values()), json.dumps(baseline))
        for label, ok in php('fallos')['checks'].items():
            check(label, ok)
        php('cache')
        state = php('fixture')
        for label, ok in state['checks'].items():
            check(label, ok)
        tid, attachment = state['id'], state['attachment']
        forbidden = [SECRET, NAME, 'prueba@alum.us.es', state['code'], 'RN03-MEDIACION-ADJUNTO']
        direct = [f'/?p={tid}', f'/?post_type=cadus_mediacion&p={tid}', f'/?p={tid}&preview=true',
                  f'/?attachment_id={attachment}', f'/?p={tid}&feed=rss2', f'/?p={tid}&tb=1',
                  f'/?page_id={tid}', '/?post_type=cadus_mediacion', '/?cadus_mediacion=',
                  '/?cadus_mediacion=no-existe', '/?post_type[]=cadus_mediacion',
                  f'/?post_type=any&p={tid}']
        public = ['/?s=RN03-MEDIACION', '/?s=RN03-MEDIACION&post_type=cadus_mediacion',
                  '/feed/', '/comments/feed/', '/?author=1', '/sitemap_index.xml',
                  '/cadus_mediacion-sitemap.xml', '/wp-sitemap.xml', '/wp-sitemap-posts-cadus_mediacion-1.xml',
                  '/wp-json/wp/v2/types', '/wp-json/wp/v2/search?search=RN03-MEDIACION',
                  '/wp-json/wp/v2/search?subtype=cadus_mediacion', '/wp-json/wp/v2/posts?search=RN03-MEDIACION',
                  '/wp-json/wp/v2/cadus_mediacion', f'/wp-json/wp/v2/cadus_mediacion/{tid}',
                  f'/wp-json/wp/v2/media?parent={tid}', f'/wp-json/wp/v2/media/{attachment}',
                  f'/wp-json/wp/v2/media/{attachment}?context=edit',
                  f'/wp-json/fluentform/v1/submissions?form_id={state["form_id"]}',
                  '/wp-json/fluentform/v1/global-search?search=RN03-MEDIACION']
        tasks = []
        for role, auth in [('anonimo', None), *state['auth'].items()]:
            for path in direct:
                tasks.append((role, path, auth, 'direct'))
            for path in public:
                tasks.append((role, path, auth, 'public'))
            if auth:
                for path in ['/wp-admin/edit.php?post_type=cadus_mediacion',
                             f'/wp-admin/post.php?post={tid}&action=edit', '/wp-admin/index.php']:
                    tasks.append((role, path, auth, 'admin'))

        def test(task):
            role, path, auth, kind = task
            status, body, headers = request(path, auth)
            allowed = role.startswith('cadus_ejecutiva') or role == 'administrator'
            if kind == 'admin' and allowed:
                ok = status == 200
                if 'post.php?' in path:
                    ok = ok and all(s in body for s in [SECRET, NAME, 'prueba@alum.us.es', state['code']])
                else:
                    ok = ok and not any(s in body for s in [SECRET, NAME, 'prueba@alum.us.es'])
                    if 'edit.php?' in path:
                        ok = ok and state['code'] in body and 'action=edit' in body
                if 'index.php' not in path:
                    ok = ok and 'no-store' in headers.get('Cache-Control', '')
            else:
                ok = not any(s.lower() in body.lower() for s in forbidden)
                if kind == 'direct':
                    ok = ok and status in (403, 404)
                if kind == 'admin' and 'index.php' not in path:
                    ok = ok and status == 403
                if path.endswith('/wp/v2/types'):
                    ok = ok and 'cadus_mediacion' not in body
                if f'/wp/v2/media/{attachment}' in path:
                    ok = ok and status in (401, 403, 404)
            return role + ' ' + path, ok, 'HTTP ' + str(status)

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            for result in pool.map(test, tasks):
                check(*result)

        status, body, headers = request(PAGE)
        check('GET formulario no-store', status == 200 and 'no-store' in headers.get('Cache-Control', ''))
        fid = state['form_id']
        nonce_name = f'_fluentform_{fid}_fluentformnonce'
        nonce = re.search(r'name="' + nonce_name + r'"[^>]*value="([^"]+)"', body).group(1)
        honey_name = f'item_{fid}__fluent_sf'
        check('Honeypot presente en HTML', f'name="{honey_name}"' in body)
        data = {'email': 'prueba@alum.us.es', 'solicitante': NAME, 'descripcion': SECRET,
                'centro': state['centro'], 'consentimiento[]': 'acepto', nonce_name: nonce, honey_name: ''}
        # El AJAX de FF llama al mismo SubmissionHandlerService probado en CLI.
        def submit(values):
            return request('/wp-admin/admin-ajax.php', data={'action': 'fluentform_submit', 'form_id': fid,
                           'data': urllib.parse.urlencode(values)})

        for label, field, value in [('sin nonce', nonce_name, ''), ('dominio ajeno', 'email', 'prueba@example.com'),
                                    ('centro inventado', 'centro', 'NO-EXISTE'), ('honeypot lleno', honey_name, 'bot'),
                                    ('honeypot ausente', honey_name, None)]:
            invalid = dict(data)
            if value is None:
                del invalid[field]
            else:
                invalid[field] = value
            status, body, headers = submit(invalid)
            check('HTTP rechaza ' + label, status in (422, 423) and 'errors' in body, f'HTTP {status}')
            check('Error no-store ' + label, 'no-store' in headers.get('Cache-Control', ''))
        status, body, headers = submit(data)
        response = json.loads(body)
        code = re.search(r'MED-\d{4}-\d{5,20}-[A-F0-9]{32}', body)
        check('HTTP envío anónimo crea referencia', status == 200 and response.get('success') is True and code is not None, f'HTTP {status}')
        check('HTTP confirmación sin nombre, correo ni conflicto', not any(s in body for s in [SECRET, NAME, 'prueba@alum.us.es']))
        check('HTTP confirmación no-store', 'no-store' in headers.get('Cache-Control', ''))
        status, fresh, headers = request(PAGE)
        check('GET posterior sin resultado privado, no-store', status == 200 and 'no-store' in headers.get('Cache-Control', '')
              and state['code'] not in fresh and (not code or code.group() not in fresh) and SECRET not in fresh)
        cache = Path('cms-wordpress/wp-content/cache/all/proyecto_gsi/cms-wordpress/atencion-al-estudiante/mediacion-estudiantil/index.html')
        check('WP Fastest Cache no regenera HTML de mediación', not cache.exists())
        counts = php('status')
        check('HTTP creó una única solicitud adicional y ninguna entrada FF', counts['solicitudes'] == 2
              and counts['ff_entries'] == counts['ff_details'] == counts['ff_meta'] == 0, json.dumps(counts))
    finally:
        final = php('cleanup')
        check('Limpieza: cero solicitudes/tickets/entradas/detalles/metas/cuentas temporales',
              all(value == 0 for value in final.values()), json.dumps(final))
    print('FALLOS:', len(audit.failures))
    return bool(audit.failures)


if __name__ == '__main__':
    sys.exit(main())
