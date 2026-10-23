"""Inspección de marcado público con curl, sin escribir en WordPress ni sus ajustes."""
import json
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parents[2]
PHP = ROOT.parent.parent / 'apps proyecto/php/php.exe'
BASE = 'http://localhost/proyecto_gsi/cms-wordpress/'
inventory = r'''<?php
$_SERVER['HTTP_HOST'] = 'localhost';
require 'cms-wordpress/wp-load.php';
$urls = [];
foreach (get_posts(['post_type' => ['page', 'post', 'cadus_acta', 'cadus_delegacion'],
    'post_status' => 'publish', 'has_password' => false, 'numberposts' => -1]) as $post) {
    $urls[] = ['url' => get_permalink($post), 'tipo' => $post->post_type];
}
echo json_encode($urls);
'''
result = subprocess.run([str(PHP)], input=inventory, cwd=ROOT, capture_output=True, encoding='utf-8', check=True)
urls = json.loads(result.stdout)
urls += [{'url': BASE + path, 'tipo': kind} for path, kind in [
    ('actas/', 'archivo'), ('delegaciones-centro/', 'archivo'), ('?s=CADUS', 'busqueda'),
    ('codex-interior-no-existe-404/', '404'), ('events/', 'eventos'),
    ('noticias/?q=codex-sin-resultados-908127', 'vacio'), ('actas-y-normativa/?tipo=normativa', 'filtro'),
    ('actas-y-normativa/?tipo%5B%5D=acta', 'entrada-array'),
    ('wp-admin/', 'admin'), ('feed/', 'feed'), ('?feed=rss2&post_type=page', 'feed'),
    ('wp-json/wp/v2/pages?per_page=100', 'rest'), ('wp-json/wp/v2/posts', 'rest')]]
folder = Path(tempfile.mkdtemp(prefix='cadus-interiores-'))
rows = []
seen = set()
for entry in urls:
    url, kind = entry['url'], entry['tipo']
    if url in seen:
        continue
    seen.add(url)
    file = folder / f'{len(rows):02d}.html'
    response = subprocess.run(['curl.exe', '-sS', '-L', '--max-time', '45', '-o', str(file),
        '-w', '%{http_code}', url], capture_output=True, encoding='utf-8', check=True)
    raw = file.read_text(encoding='utf-8', errors='replace')
    soup = BeautifulSoup(raw, 'html.parser')
    ids = Counter(node['id'] for node in soup.select('[id]'))
    row = dict(url=url, tipo=kind, status=int(response.stdout),
        h1=[h.get_text(' ', strip=True) for h in soup.select('h1')],
        main=len(soup.select('main')), pie=len(soup.select('.cadus-seccion--contacto')),
        pie_en_datos='cadus-seccion--contacto' in raw if kind in ['feed', 'rest', 'admin'] else None,
        hero=len(soup.select('.hero-section')), migas=len(soup.select('.ct-breadcrumbs')),
        salto=[a.get('href') for a in soup.select('a.skip-link')],
        ids_duplicados=[key for key, count in ids.items() if count > 1],
        titulos_vacios=len([h for h in soup.select('h1,h2,h3,h4,h5,h6') if not h.get_text(strip=True)]),
        archivo=str(file))
    rows.append(row)
    print(f"{row['status']} h1={len(row['h1'])} main={row['main']} pie={row['pie']} hero={row['hero']} {url}", flush=True)
output = Path(__file__).with_name('interiores_http_resultados.json')
output.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Evidencia: {output}\nHTML temporal: {folder}')
