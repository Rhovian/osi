# OSI Model — Colorfigure

An interactive, hand-inked isometric figure of the **OSI 7-layer network model**, built with the
[Colorfigures](https://april-zhu.com/colorfigures) skill (MIT, April Zhu). The skill is vendored at
`.claude/skills/colorfigures/` — read its `SKILL.md`, `assets/core.js`, and all three `assets/examples/*.html`
before writing anything.

Inspiration: [@0xMovez's interactive electronics boards](https://x.com/0xMovez/status/2112940162103615783) — learn by
building part-by-part and **breaking things on purpose** (reversed caps pop, chips smoke). Same spirit here, for networking.

## Task (for Claude)

Use the colorfigures skill to build `osi.html` (single self-contained file via `scripts/build.py`).
The skill targets physical machines, so the abstract model must be made **a physical machine**:

### The object
- A desk board (like `lamp.html`) with **two 7-storey towers**: *Sender* (left) and *Receiver* (right).
- Each floor = one layer, each its own colour band, labelled on the side:
  7 Application · 6 Presentation · 5 Session · 4 Transport · 3 Network · 2 Data Link · 1 Physical.
- Floor 1 of each tower is a NIC with an RJ45 port; a real **Ethernet cable** runs between them
  (optionally via a small **switch** and **router** box mid-board, so L2/L3 devices have a physical home).
- Must look right from every side, back and underside included (skill's *Truth first* / *Verify* rules).

### Main interaction: "Send"
A letter (the data) enters at L7 of the Sender and travels **down**, each floor wrapping it — visible encapsulation:
- L7–L5: data (HTTP request) → L6 gets a padlock/encoding stamp (TLS) → L5 session tag
- L4: wrapped in a **segment** envelope with port numbers (TCP)
- L3: **packet** envelope with src/dst IP
- L2: **frame** envelope with MAC header + FCS trailer
- L1: becomes **bits** — blinking pulses travelling along the cable

Then up the Receiver tower, each floor **unwrapping** its own envelope. Router strips/rewrites the L2 frame but
keeps the L3 packet (shows why MAC changes per hop and IP doesn't).

### See-through
Each floor reveals its working parts, labelled & lighting up while active: browser/app (L7), cipher wheel (L6),
session handshake (L5), TCP sequence counter + ACK return (L4), routing table (L3), MAC table / switch ports (L2),
PHY transceiver + twisted pairs (L1).

### Break it on purpose (buttons)
- **Unplug cable** — L1: bits stop, link light dies.
- **Corrupt bits** — L2: FCS check fails, frame dropped at receiver, ✗ stamp.
- **Wrong IP** — L3: router has no route, packet bounced back (ICMP unreachable).
- **Drop a segment** — L4: TCP timeout, retransmit, ACK.
- **Toggle TCP/UDP** — L4: UDP just fires, no ACKs, losses stay lost.
- **Bad certificate** — L6: padlock breaks, receiver refuses.

### Extras (if budget allows)
- Step mode (advance one layer at a time) alongside the full Send animation.
- Hover a floor → tooltip: layer name, PDU name, example protocols, real devices.

## Done when
- `osi.html` opens standalone in a browser, no external requests.
- Verified from all sides with headless Chrome per the skill's *Verify* section.
- Short note in this readme listing what each button does.

## Buttons (what each one does)

Open `osi.html` in a browser (single file, no network). Source: `src/osi.html` + `src/core.js`; rebuild with
`python3 .claude/skills/colorfigures/scripts/build.py src/osi.html osi.html`.

- **Send** — the letter (GET /) rides the Sender's lift down L7→L1; each floor adds its header block in its own colour
  (TLS → session tag → TCP/UDP → IP → MAC + FCS), then it leaves as blinking bits on the cable, through the switch
  (reads MAC) and router (strips the frame, keeps the IP packet, builds a new frame: SRC MAC changes aa:01 → cc:07),
  and climbs the Receiver's lift L1→L7 with each floor removing its own block. With TCP a green ACK runs back and the
  sender's L4 lamp lights. The top-right panel shows the current PDU, SRC MAC and DST IP.
- **Step** — same journey one layer/hop at a time, with a one-line note per step. Press Send to finish at full speed.
- **Unplug cable** — the plug lies loose on the board, the link LED goes dark; the frame stops at L1 (✗).
- **Corrupt bits** — noise flips a bit on the last cable (red pulse); the receiver's L2 FCS check fails and the frame
  is dropped (✗). TCP times out and retransmits; UDP leaves it lost.
- **Wrong IP** — destination becomes 10.9.9.9; the router has no route, its screen says so, and a red ICMP
  "unreachable" travels back to the sender's L3.
- **Drop a segment** — the router's queue is full and drops it. TCP: the sender's L4 timer runs out (amber), it
  retransmits and gets an ACK. UDP: just lost.
- **Use UDP** — toggles TCP/UDP: smaller L4 header block, no sequence numbers, no ACK, no retransmits.
- **Bad certificate** — at the receiver's L6 the padlock springs open (see-through) and the request is refused (✗).
- **See-through** — the tower cases fade; each floor's parts show and light up while working: browser (L7), cipher
  wheel + padlock (L6), handshake sliders (L5), sequence counter, retransmit timer and ACK tube (L4), routing table +
  IP stamp (L3), MAC table + MAC/FCS chips (L2), PHY transceiver, magnetics, RJ45 and twisted pairs (L1); plus the
  switch ASIC/MAC table and router CPU/routing table. **Labels** names them.
- Fault toggles stay on (button shown dark) until pressed again. Hover a floor for a tooltip (layer, PDU, protocols,
  real devices). Drag to turn the board all the way round; pinch / ctrl-scroll to zoom.

## The Network Journey (`journey.html`)

A step-by-step journey that follows one request (`GET /` from a laptop at 10.0.0.20 to `wiki.lan` at 10.0.1.7) down
the laptop's seven layers, across a cable, a switch, a router and a second cable, up the server's seven layers, and
back again as the reply, ending with the page drawn on the laptop (20 stops). One control: Next / Back (arrow keys, or click a stop on the route map). Each stop shows a plain-language
summary, an "in everyday terms" postal analogy, the steps that happen, the real bytes at that point (click a header block, point at a field to find it in
the hex), who does the work in real systems, and one "Try it":

| Stop | Try it |
|---|---|
| Laptop 7 Application | edit the path; byte counts and checksums change all the way through |
| Laptop 6 Presentation | peek at the decrypted bytes, encrypt again |
| Laptop 5 Session | replay the TLS handshake |
| Laptop 4 Transport | switch TCP / UDP (carries through the rest of the trip) |
| Laptop 3 Network | pick a destination: local delivery or the default gateway |
| Laptop 2 Data link | clear the ARP cache and ask again |
| Laptop 1 Physical | unplug the cable |
| Cable | add a burst of noise (a flipped bit) |
| Switch | forget the MAC table (flooding) |
| Router | pick a destination: which routing-table row wins |
| Server 2 Data link | flip one bit: the recomputed CRC-32 no longer matches the FCS |
| Server 4 Transport | lose the segment: TCP retransmits, UDP doesn't |
| Server 6 Presentation | tamper with one byte: TLS tag check fails |
| Server 7 Application | start again |
| The reply | play the reply again: down the server, back across the network, up the laptop |

In 3D, a small tag pops up each time a layer adds (`+ TCP 20 B`), removes (`- ETH`) or changes (`TTL 63`, `new FCS`) a
header; the overview traces the whole route; the cable stop draws the four twisted pairs and why twisting cancels noise.

All bytes are computed: the TLS record lengths, the TCP/UDP checksum, the IP header checksum (recomputed when the
router changes the TTL from 64 to 63), the Ethernet FCS (CRC-32), and the new MAC addresses on the second hop.

Single file, works offline: `src/journey.html` (stops are plain data in `CONTENT`) + three.js r158 (MIT,
`src/vendor/`). Rebuild with `python3 src/inline.py src/journey.html journey.html`.
