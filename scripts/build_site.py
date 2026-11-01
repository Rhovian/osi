#!/usr/bin/env python3
"""Build the site into dist/ (Python 3 only, nothing to install).

    python3 scripts/build_site.py

dist/index.html                    The Network Journey (src/index.html)
dist/assets/three-<hash>.min.js    three.js, named by its content so it can be cached for a year

Used by Netlify (netlify.toml), Vercel (vercel.json) and GitHub Pages (.github/workflows/pages.yml).
"""
import hashlib, os, re, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC, DIST = os.path.join(ROOT, 'src'), os.path.join(ROOT, 'dist')

shutil.rmtree(DIST, ignore_errors=True)
os.makedirs(os.path.join(DIST, 'assets'))

page = open(os.path.join(SRC, 'index.html'), encoding='utf-8').read()
three = open(os.path.join(SRC, 'vendor', 'three.min.js'), 'rb').read()
asset = f"assets/three-{hashlib.sha256(three).hexdigest()[:10]}.min.js"
open(os.path.join(DIST, asset), 'wb').write(three)

page, n = re.subn(r'<script src="vendor/three\.min\.js"></script>', f'<script src="{asset}"></script>', page)
assert n == 1, 'expected one <script src="vendor/three.min.js"> in src/index.html'
assert not re.search(r'<script src="(?!assets/)', page), 'src/index.html loads a script this build does not copy'
open(os.path.join(DIST, 'index.html'), 'w', encoding='utf-8').write(page)

for path in ('index.html', asset):
    print(f"dist/{path:40s} {os.path.getsize(os.path.join(DIST, path)) / 1024:6.0f} KB")
