// Record The Network Journey as a GIF, frame by frame on a virtual clock (smooth however slowly the browser renders).
//   python3 scripts/build_site.py && node scripts/record_gif.js        ->  docs/journey.gif
// Needs Node with Playwright (and its Chromium) and ffmpeg on the PATH.
const { chromium } = require('playwright');
const fs = require('fs'), os = require('os'), path = require('path'), { execFileSync } = require('child_process');
const ROOT = path.join(__dirname, '..'), file = path.join(ROOT, 'dist', 'index.html'), out = fs.mkdtempSync(path.join(os.tmpdir(), 'journey-frames-'));
(async () => {
  const b = await chromium.launch({ args:['--use-angle=swiftshader','--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport:{ width:1040, height:650 }, deviceScaleFactor:1 });
  await p.addInitScript(() => { let t = 0, q = []; performance.now = () => t; window.requestAnimationFrame = cb => { q.push(cb); return q.length; };
    window.__vt = ms => { t += ms; const cbs = q; q = []; cbs.forEach(cb => cb(t)); }; });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + file);
  await p.addStyleTag({ content:'.app{grid-template-columns:minmax(0,1fr)!important}#panel{display:none!important}#loader{display:none!important}header,#rail{grid-column:1!important}' });
  await p.evaluate(() => window.dispatchEvent(new Event('resize')));
  await p.waitForTimeout(400); await p.evaluate(() => window.__vt(16));
  let n = 0;
  const rec = async (seconds, step, sub = 1) => { for (let t = 0; t < seconds*1000; t += step*sub){ await p.evaluate(([s, k]) => { for (let i = 0; i < k; i++) window.__vt(s); }, [step, sub]); await p.screenshot({ path:`${out}/f${String(n++).padStart(4, '0')}.png` }); } };
  await rec(2.6, 125);                                                    // overview with the route line
  for (let i = 0; i < 18; i++){ await p.keyboard.press('ArrowRight'); await rec(2.5, 125); }   // laptop 7..1, network, server 1..7
  await p.keyboard.press('ArrowRight'); await rec(22.5, 104, 2);            // the reply, faster
  await rec(2.6, 125);                                                    // hold on the finished page
  await b.close();
  if (errs.length) throw new Error(errs.join(' | '));
  const gif = path.join(ROOT, 'docs', 'journey.gif'); fs.mkdirSync(path.dirname(gif), { recursive:true });
  execFileSync('ffmpeg', ['-loglevel', 'error', '-y', '-framerate', '12', '-i', path.join(out, 'f%04d.png'), '-filter_complex',
    'scale=680:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128:stats_mode=diff[p];[b][p]paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle', '-loop', '0', gif]);
  fs.rmSync(out, { recursive:true, force:true });
  console.log(`wrote ${path.relative(ROOT, gif)} from ${n} frames (${(fs.statSync(gif).size/1048576).toFixed(1)} MB)`); })();
