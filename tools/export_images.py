"""Export project photos (full 1600px + 720px thumbs) into images/p/<slug>/.
Usage: python3 -I tools/export_images.py <site_dir> <dropbox_2026_dir> <pkg_dir>"""
import csv, json, os, subprocess, sys
site, d26, pkg = sys.argv[1:4]
sys.path.insert(0, os.path.join(site, 'tools'))
from projects import PROJECTS
idx = json.load(open(os.path.join(d26, 'idx.json')))
assets = {r['id'].split('-')[1]: r for r in csv.DictReader(open(os.path.join(pkg, 'raw', 'asset-manifest.csv')))}

def src26(proj, i):
    items = [x for x in idx if x[0].split('/')[0] == proj]
    return os.path.join(d26, 'raw', items[i][0])
def srcpkg(aid):
    return os.path.join(pkg, 'web', assets[aid]['web_ready_path'])
def sips(src, dst, size, q):
    subprocess.run(['sips', '-s', 'format', 'jpeg', '-s', 'formatOptions', str(q), '-Z', str(size), src, '--out', dst], capture_output=True)
    return os.path.exists(dst)

manifest = {}
for p in PROJECTS:
    out = os.path.join(site, 'images', 'p', p['slug']); os.makedirs(out, exist_ok=True)
    if p['src'][0] == '26':
        proj = p['src'][1]
        if p['photos'] == 'all':
            n = len([x for x in idx if x[0].split('/')[0] == proj and '/BEFORE' not in x[0].upper()])
            items = [i for i, x in enumerate([x for x in idx if x[0].split('/')[0] == proj]) if '/BEFORE' not in x[0].upper()][:p.get('max', 10)]
        else:
            items = p['photos']
        srcs = [src26(proj, i) for i in items]
        extra = {k: src26(proj, p[k]) for k in ('before', 'after') if k in p}
    else:
        srcs = [srcpkg(a) for a in p['photos']]
        extra = {}
        if 'before_asset' in p: extra = {'before': srcpkg(p['before_asset']), 'after': srcpkg(p['after_asset'])}
        if 'composite' in p: extra['composite'] = srcpkg(p['composite'])
        for n, a in enumerate(p.get('stages', []), 1): extra[f'stage-{n}'] = srcpkg(a)
    files = []
    for n, s in enumerate(srcs, 1):
        f = f'{n:02d}'
        ok = sips(s, os.path.join(out, f + '.jpg'), 1600, 72) and sips(s, os.path.join(out, f + '-t.jpg'), 720, 66)
        if ok:
            w, h = [int(v) for v in subprocess.run(['sips', '-g', 'pixelWidth', '-g', 'pixelHeight', os.path.join(out, f + '-t.jpg')], capture_output=True, text=True).stdout.split()[-3::2]]
            files.append({'f': f, 'w': w, 'h': h})
    for k, s in extra.items():
        sips(s, os.path.join(out, k + '.jpg'), 1600, 72)
    manifest[p['slug']] = {'photos': files, 'extra': sorted(extra)}
    print(p['slug'], len(files), sorted(extra))
json.dump(manifest, open(os.path.join(site, 'tools', 'image-manifest.json'), 'w'), indent=1)
