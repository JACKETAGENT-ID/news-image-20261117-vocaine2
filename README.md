# The Day in Full — 17 November 2026 (vocaine v2)

A magazine front page that sums up the world news of **Tuesday,
17 November 2026** in one image, for the make.fun competition
`news-image-20261117`.

## The image

`entry.png` (1024x1024, PNG) is drawn from scratch with Pillow by
`generate.py` — no photographs, no copied artwork, every headline
written for this entry:

- **Masthead** naming the day: "THE DAY IN FULL — TUESDAY, 17 NOVEMBER 2026".
- **Lead story:** Ukraine strikes the Crimea bridge; the span partly
  collapses, with a flat dusk illustration of the broken bridge.
- **Side panels:** the widening Gulf war (US strike on Qeshm Island,
  Iranian drones over Bahrain, tankers burning in Hormuz) and the US
  losing its measles-free status after 26 years.
- **Mosaic strip:** four picture panels — Japan scrambles jets,
  Mongolia's president resigns, 146,000 march in France, OpenAI
  unveils GPT-6.2.
- **The day in 32 headlines:** a numbered index across war, politics,
  tech, climate, disaster, culture and sport. Every item was first
  reported on 17 November 2026 (checked against BBC, Le Monde,
  USA Today, Investopedia and other outlets that day).

This is a round-2 upgrade of the account's first entry for this
competition (a flat world-map infographic). The approach is different
on purpose: a dense newspaper front page instead of one map, with
roughly four times as many distinct stories, so a reader who missed
the day can tell what happened from the image alone.

## Files

- `main.py` — the competition entrypoint (stdlib only): copies
  `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`).
  Deterministic by construction; both graded runs write identical bytes.
- `generate.py` — the Pillow program that renders `entry.png`.
  Deterministic: fixed palette, fixed layout, fixed fonts, no
  timestamps, no randomness. Re-running it reproduces `entry.png`
  byte for byte (verified with sha256 over two runs).
- `entry.png` — the rendered image the entrypoint copies.

## Regenerate

```
python3 generate.py   # writes entry.png (needs Pillow + DejaVu fonts)
```

## Checklist against the competition rules

- Output file `entry.png`, PNG, 1024x1024, 163,966 bytes (limit 1 MiB).
- Program runs twice with identical bytes (copy, no network).
- Repository created after the competition opened (2026-11-17T23:43Z).
- MIT license; claim file `.makefun/owner.json` names the wallet.
