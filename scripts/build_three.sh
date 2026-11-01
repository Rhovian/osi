#!/bin/sh
# Rebuild src/vendor/three.min.js with only the parts of three.js the journey uses (about 25% smaller than the full
# build). Run this only when the page starts using a part of three.js that is not in NAMES. Needs Node and npm.
set -e
REPO="$(cd "$(dirname "$0")/.." && pwd)"
NAMES="BoxGeometry BufferGeometry CanvasTexture CatmullRomCurve3 Color ConeGeometry CylinderGeometry DataTexture
DirectionalLight DoubleSide EdgesGeometry Group HemisphereLight Line LineBasicMaterial LineSegments Mesh
MeshBasicMaterial MeshToonMaterial NearestFilter PCFSoftShadowMap PerspectiveCamera PlaneGeometry RedFormat Scene
SphereGeometry Spherical Sprite SpriteMaterial SRGBColorSpace TorusGeometry TubeGeometry Vector3 WebGLRenderer"
WORK="$(mktemp -d)"; cd "$WORK"
npm init -y >/dev/null
npm install --silent --no-audit --no-fund three@0.158.0 esbuild@0.24.0
echo "export { $(echo $NAMES | sed 's/ /, /g') } from 'three';" > entry.js
./node_modules/.bin/esbuild entry.js --bundle --minify --format=iife --global-name=THREE --target=es2020 --legal-comments=none --outfile=three.js
{ printf '/* three.js r158, MIT License, Copyright 2010-2023 three.js authors (https://threejs.org). Only the parts this page uses: see scripts/build_three.sh. */\n'; cat three.js; } > "$REPO/src/vendor/three.min.js"
rm -rf "$WORK"
echo "wrote src/vendor/three.min.js ($(wc -c < "$REPO/src/vendor/three.min.js") bytes)"
