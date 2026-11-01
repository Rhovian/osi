#!/usr/bin/env python3
"""Inline local <script src="..."></script> tags so a page becomes one self-contained file.

    python3 src/inline.py src/journey.html journey.html
"""
import os, re, sys
src, out = sys.argv[1], sys.argv[2]
base = os.path.dirname(os.path.abspath(src))
page = open(src, encoding='utf-8').read()
def repl(m):
    path = os.path.join(base, m.group(1))
    code = open(path, encoding='utf-8').read().replace('</script', '<\\/script')
    return '<script>\n' + code + '\n</script>'
page = re.sub(r'<script\s+src="(?!https?:)([^"]+)"\s*>\s*</script>', repl, page)
open(out, 'w', encoding='utf-8').write(page)
print('wrote', out, len(page.encode()), 'bytes')
