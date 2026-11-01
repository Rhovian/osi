#!/usr/bin/env python3
"""Build the static site into dist/ (no dependencies beyond Python 3).

    python3 scripts/build_site.py

dist/index.html     landing page
dist/journey.html   The Network Journey (src/journey.html with three.js inlined)
dist/osi.html       the OSI colorfigure (src/osi.html built with the colorfigures script)

Used by Netlify (netlify.toml), Vercel (vercel.json) and GitHub Pages (.github/workflows/pages.yml).
"""
import os, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, 'dist')

def run(*args):
    subprocess.run([sys.executable, *args], cwd=ROOT, check=True)

shutil.rmtree(DIST, ignore_errors=True)
os.makedirs(DIST)
run('src/inline.py', 'src/journey.html', 'dist/journey.html')
run('.claude/skills/colorfigures/scripts/build.py', 'src/osi.html', 'dist/osi.html')
shutil.copy(os.path.join(ROOT, 'src', 'index.html'), os.path.join(DIST, 'index.html'))

for name in ('index.html', 'journey.html', 'osi.html'):
    page = open(os.path.join(DIST, name), encoding='utf-8').read()
    assert page.lstrip().lower().startswith('<!doctype html>'), name
    assert '<script src=' not in page, f'{name} still loads an external script'
print('built', ', '.join(sorted(os.listdir(DIST))), 'into dist/')
