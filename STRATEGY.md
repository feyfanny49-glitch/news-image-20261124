# Strategy — news-image-20261124

## Exact deliverable

One image, written by a standard-library-only program to `/output/entry.png` on
every run. The image must sum up the world news of **Tuesday, 24 November 2026**
(events that happened, or were first reported, on that day in any time zone).
The repository root carries the entrypoint; the finished PNG is shipped in the
repository and the entrypoint copies its bytes to the output directory. Two
runs must produce byte-identical output. No network is available at run time.

Entrypoint: `main.ts` (Node 22, standard library only). Locally,
`MAKEFUN_OUTPUT_DIR=out` stands in for `/output`.

## Scoring and judge criteria

The gate gives a binary Valid column: whole PNG or JPEG, named `entry.png`,
at most 1 MiB (1,048,576 bytes) and at most 1024x1024 pixels, with every PNG
chunk and its CRC intact through IEND. Invalid entries never reach the judge.

The judge is `z-ai/glm-5.3-flash`. It sees an image but has no news feed and is
**not told which day** the contest covers. It compares two entries at a time,
in both orders, and picks the one that better sums up its day's news. Its
criteria, in the exact order given in the rules:

1. **One day's news, and names that day.** Specific, recognisable events of the
   day plus the date it sums up. An image that names no day, shows no news, is
   about a day before 13 November 2026, or presents older events as that day's
   news loses. => Put the date huge and make every story a real 24 Nov item.
2. **Selection and breadth.** The day's most consequential stories across
   regions and fields, not one country or one beat. => Cover US tech/markets,
   global climate, Middle East, Europe/war, East Asia, and world sport.
3. **It reads.** A viewer who missed the day can tell what happened from the
   image alone; each story clear from its picture and short label; nothing
   self-contradictory or false. => One pictogram plus one bold headline and one
   short, faithful sub-line per story.
4. **Faithful.** Report what happened, without hype or speculation as fact.
   => Only claims supported by the cited roundups; no predictions.
5. **Craft.** One clear composition, cleanly rendered, legible at about 300 px
   across, no smears, artefacts or garbled text. => Flat-colour vector-style
   PIL drawing at 1024x1024, heavy weight, few colours, generous spacing.

Ranking is a Bradley-Terry win rate from the judge's pairwise verdicts; entries
in the playoff rank above those that are not. At most 10 submissions per day
and 20 total; the last valid submission before the deadline is final. Exact
rate ties break by playoff results, then smaller file size, then earlier
receipt. Never byte-identical to a house or reference image.

## Hard caps

- Image: PNG or JPEG, <= 1,048,576 bytes, <= 1024x1024 pixels; whole file with
  valid chunk CRCs and IEND.
- Runtime: no network, 1 CPU, 512 MB RAM, 64 processes, 60 seconds per run,
  standard library only, two runs with identical bytes.
- Submission: OSI-approved license (MIT already committed by `init`), created
  at or after the opening, transcripts required.
- Text constraints for this entry: spell out every digit in words and never
  use the euro glyph, so the image stays legible and font-safe.

## Concrete plan to maximise the score

1. Research the real news of 24 November 2026 with web search/extract and keep
   only claims corroborated by multiple roundups. Never invent a fact. Sources
   used: Reuters world news summary (devdiscourse, updated 24 Nov 2026 05:24
   IST), The Straits Times "While You Were Sleeping, 24 Nov 2026", Yonhap's 24
   Nov newspaper headlines, SBS World 24 Nov, and the BBC 24 Nov archive.
2. Select six consequential, mutually independent stories with geographic and
   topical breadth (see below). Each is a real item first reported on or by
   24 November 2026.
3. Render once, at build time, with Pillow in `tools/render_image.py`. Draw a
   flat-colour editorial board: a huge spelled-out date header, then six rows
   with a distinct simple pictogram, a short bold headline and a short
   sub-line. Save optimised PNG; no metadata, no random seeds, deterministic.
4. Ship the finished `entry.png`. `main.ts` only copies those bytes. Verify the
   copy locally and verify byte equality across two runs.
5. Validate the PNG structurally (signature, IHDR, every chunk CRC, IEND,
   dimensions, byte cap) and print bytes, dimensions and sha256.
6. Keep the `init` freshness commit and the LICENSE commit untouched; commit
   all work afterwards; do not submit or upload.

## The six stories on the image

| # | Bold headline | Sub-line | Region / field | Reported |
|---|---|---|---|---|
| one | JENSEN HUANG RETURNS | Nvidia reinstates its CEO as shares soar | US / technology, markets | 23-24 Nov |
| two | CLIMATE TALKS COLLAPSE | No deal after two weeks of talks | Global / climate | 23-24 Nov |
| three | IRAN FACES US BLOCKADE | Tehran vows to counter it | Middle East / geopolitics | 23-24 Nov |
| four | UKRAINE SINKS RUSSIAN SHIP | Sea drone strike off Libya | Europe / war | 23-24 Nov |
| five | KOREA NAMES WOMAN SPY CHIEF | First woman to lead spy agency | East Asia / politics | 24 Nov |
| six | FIFA NAMES WORLD CUP HOSTS | United States and Britain win rights | World / sport | 23-24 Nov |

All numerals on the image are written out: the date is
`TWENTY-FOUR NOVEMBER` / `TWO THOUSAND TWENTY-SIX`; no euro glyph appears.
Pictograms are hand-coded geometric primitives (chip, cracked globe, ship
behind a blockade bar, drone and sinking hull, government building with star,
trophy and ball), so no copied artwork is used.
