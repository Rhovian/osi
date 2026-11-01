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
