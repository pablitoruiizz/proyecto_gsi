"""Auditoría Codex RN-03. Sesiones temporales en memoria; limpieza en finally."""
import concurrent.futures
import json
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
PHP = r'C:\Users\ruizv\OneDrive\Escritorio\UNI\GSI\apps proyecto\php\php.exe'
HELPER = Path(__file__).with_name('rn03_auditoria.php')
BASE = 'http://localhost/proyecto_gsi/cms-wordpress'
failures = []

def php(action, data=None):
    result = subprocess.run([PHP, str(HELPER), action], input=json.dumps(data or {}), capture_output=True, encoding='utf-8')
    if result.stderr:
        print('ERROR CLI:', result.stderr)
    if result.returncode:
        raise RuntimeError(result.stdout)
    return json.loads(result.stdout)

def check(label, ok, detail=''):
    print(('OK ' if ok else 'FALLO ') + label + (' — ' + detail if detail else ''), flush=True)
    if not ok:
        failures.append(label)

def request(path, auth=None, data=None):
    headers = {'Cookie': auth['cookie']} if auth else {}
    if auth and '/wp-json/' in path:
        headers['X-WP-Nonce'] = auth['nonce']
    req = urllib.request.Request(BASE + path, headers=headers,
        data=urllib.parse.urlencode(data).encode() if data else None)
    try:
        response = urllib.request.urlopen(req, timeout=45)
    except urllib.error.HTTPError as error:
        response = error
    with response:
        return response.status, response.read().decode('utf-8', 'replace'), response.headers

def main():
    state = {}
    try:
        state = php('fixture')
        for label, ok in state['checks'].items():
            check(label, ok)
        tid, attachment = state['id'], state['attachment']
        forbidden = ['RN03-CODEX-SECRETO', 'RN03-CODEX-ASUNTO', 'prueba@alum.us.es', state['code'], 'RN03-ADJUNTO']
        tasks = []
        direct = [f'/?p={tid}', f'/?post_type=cadus_ticket&p={tid}', f'/?p={tid}&preview=true',
                  f'/?attachment_id={tid}', f'/?attachment_id={attachment}', f'/?p={tid}&feed=rss2',
                  f'/?p={tid}&tb=1', f'/?page_id={tid}', '/?post_type=cadus_ticket', '/?cadus_ticket=no-existe']
        public = ['/?s=RN03-CODEX', '/?s=RN03-CODEX&post_type=cadus_ticket', '/?s=RN03-CODEX&post_type[]=cadus_ticket',
                  '/feed/', '/comments/feed/', '/?author=1', '/?year=2026&monthnum=10', '/sitemap_index.xml',
                  '/cadus_ticket-sitemap.xml', '/wp-sitemap.xml', '/wp-sitemap-posts-cadus_ticket-1.xml',
                  '/wp-json/wp/v2/types', '/wp-json/wp/v2/search?search=RN03-CODEX', '/wp-json/wp/v2/search?subtype=cadus_ticket',
                  '/wp-json/wp/v2/posts?search=RN03-CODEX', '/wp-json/wp/v2/cadus_ticket',
                  '/wp-json/wp/v2/media?parent=' + str(tid), '/wp-json/wp/v2/media/' + str(attachment),
                  '/wp-json/fluentform/v1/submissions?form_id=3', '/wp-json/fluentform/v1/report/form-stats',
                  '/wp-json/fluentform/v1/global-search?search=RN03-CODEX']
        for role, auth in [('anonimo', None), *state['auth'].items()]:
            if '--panel' not in sys.argv:
                for path in direct:
                    tasks.append((role, path, auth, 'direct'))
                for path in public:
                    tasks.append((role, path, auth, 'public'))
            if not (role.startswith('cadus_ejecutiva') or role == 'administrator'):
                tasks.append((role, f'/wp-admin/admin-ajax.php?action=get-attachment&id={attachment}', auth, 'ajax'))
            if auth:
                for path in ['/wp-admin/edit.php?post_type=cadus_ticket', f'/wp-admin/post.php?post={tid}&action=edit', '/wp-admin/index.php']:
                    tasks.append((role, path, auth, 'admin'))

        def test(task):
            role, path, auth, kind = task
            status, body, headers = request(path, auth)
            allowed = role.startswith('cadus_ejecutiva') or role == 'administrator'
            if kind == 'admin' and allowed:
                ok = status == 200
                if 'post.php?' in path:  # control positivo: la edición autorizada muestra el ticket
                    falta = [s for s in ['RN03-CODEX-SECRETO', state['code']] if s not in body]
                    ok = ok and not falta
                    if falta:
                        print('  falta en la edición autorizada:', falta)
                else:
                    ok = ok and not any(s in body for s in ['RN03-CODEX-SECRETO', 'RN03-CODEX-ASUNTO', 'prueba@alum.us.es'])
                    if 'edit.php' in path:
                        ok = ok and state['code'] in body
            else:
                # Un error de servidor no prueba nada: un 500 sin los textos no cuenta como correcto.
                ok = status < 500 and not any(s.lower() in body.lower() for s in forbidden)
                if kind == 'direct':
                    ok = ok and status in (403, 404)
                if kind == 'admin' and 'index.php' not in path:
                    ok = ok and status == 403
                if kind == 'ajax':  # get-attachment de un adjunto de ticket (revisión Codex)
                    ok = ok and status in (400, 403, 404)
            return role + ' ' + path, ok, 'HTTP ' + str(status)

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            for result in pool.map(test, tasks):
                check(*result)
        path = '/atencion-al-estudiante/seguimiento-de-ticket/'
        status, body, headers = request(path)
        check('GET seguimiento no-store', 'no-store' in headers.get('Cache-Control', ''))
        nonce = re.search(r'name="cadus_seguimiento_nonce"[^>]*value="([^"]+)"', body).group(1)
        status, body, headers = request(path, data={'cadus_seguimiento_enviar': '1', 'cadus_seguimiento_nonce': nonce,
                                                    'cadus_codigo': state['code'], 'cadus_correo': 'prueba@alum.us.es'})
        check('POST seguimiento nuevo código funciona', 'RN03-CODEX-ASUNTO' in body)
        check('POST seguimiento no expone correo ni texto original', 'prueba@alum.us.es' not in body and 'RN03-CODEX-SECRETO' not in body)
        check('POST seguimiento no-store', 'no-store' in headers.get('Cache-Control', ''))
        _, fresh, headers = request(path)
        check('GET posterior sin resultado privado ni caché', 'RN03-CODEX-ASUNTO' not in fresh and 'no-store' in headers.get('Cache-Control', ''))
        cache = Path('cms-wordpress/wp-content/cache/all/proyecto_gsi/cms-wordpress/atencion-al-estudiante/seguimiento-de-ticket/index.html')
        check('WP Fastest Cache no genera HTML de seguimiento', not cache.exists())
        status, body, _ = request('/wp-json/wp/v2/users')
        print('INFO /wp/v2/users HTTP', status, 'listado=' + str(status == 200 and 'slug' in body))
    finally:
        final = php('cleanup', state)
        check('Limpieza: cero tickets y entradas FF', final == {'tickets': 0, 'propios': 0, 'ff_entries': 0}, json.dumps(final))
    print('FALLOS:', len(failures))
    return bool(failures)

if __name__ == '__main__':
    sys.exit(main())
