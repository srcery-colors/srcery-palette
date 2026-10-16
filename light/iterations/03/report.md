# Srcery Light — iteration 03

Review-only candidate. No commits. Syntax families and links are preserved. Dedicated canonical UI surfaces separate Error/PmenuSel backgrounds from contrast-adjusted syntax foregrounds. PmenuSel uses an explicit pair; other inverse attributes are retained.

Background: `#FCE8C3`. Text target: 4.5:1 (WCAG AA); indicators/decorations: 3:1.

Accent hue and saturation are derived from canonical RGB, varying HSL lightness only. Strong variants use a darker contrast target. Warm neutrals and diff surfaces are role adaptations. Hex quantization can cause small hue drift.

Both editors loaded the theme, checked palette mappings, switched dark → light → dark, exercised options and overrides, and parsed Python, Rust, TypeScript and Markdown fixtures.

GUI failures: 0; xterm fallback failures: 0. All ratios are evaluated unrounded. GUI and fixed 256-color results are separate.

## Palette

| Entry | Canonical | Light | Role | Main BG | Worst relevant BG |
|---|---|---|---|---:|---:|
| black | #121110 | #FCE8C3 | surface | 1.00 | 1.00 |
| red | #EF2F27 | #B0140D | text | 5.92 | 4.58 |
| green | #519F50 | #326332 | text | 5.89 | 4.55 |
| yellow | #FBB829 | #775102 | text | 5.90 | 4.56 |
| blue | #2C78BF | #215B90 | text | 5.89 | 4.56 |
| magenta | #E02C6D | #AA194E | text | 5.91 | 4.57 |
| cyan | #0AAEB3 | #066265 | text | 5.94 | 4.59 |
| white | #C5B088 | #685633 | text | 5.89 | 4.55 |
| bright_black | #917E6B | #635649 | text | 5.91 | 4.57 |
| bright_red | #F75341 | #A11607 | text | 6.63 | 5.13 |
| bright_green | #98BC37 | #47571A | text | 6.60 | 5.10 |
| bright_yellow | #FED06E | #6D4A01 | text | 6.64 | 5.14 |
| bright_blue | #68A8E4 | #19538A | text | 6.60 | 5.11 |
| bright_magenta | #FF5C8F | #A50033 | text | 6.60 | 5.10 |
| bright_cyan | #2BE4D0 | #0C5B53 | text | 6.62 | 5.12 |
| bright_white | #FCE8C3 | #121110 | text | 15.69 | 12.13 |
| dark_green | #294229 | #D9E8D9 | surface | 1.06 | 1.00 |
| dark_red | #4F2321 | #EDD5D4 | surface | 1.16 | 1.00 |
| dark_blue | #1E5181 | #CDE1F3 | surface | 1.12 | 1.00 |
| dim_green | #2E5C2E | #CCE5CC | surface | 1.12 | 1.00 |
| orange | #FF5F00 | #9A3900 | text | 5.90 | 4.56 |
| bright_orange | #FF8700 | #7C4200 | text | 6.63 | 5.12 |
| teal | #008080 | #006363 | text | 5.89 | 4.56 |
| gray1 | #1C1B19 | #E7DECD | surface | 1.11 | 1.00 |
| gray2 | #262522 | #E3DBC5 | surface | 1.15 | 1.00 |
| gray3 | #312F2C | #DFD1BD | surface | 1.25 | 1.00 |
| gray4 | #3B3935 | #DBCEB5 | surface | 1.29 | 1.00 |
| gray5 | #45433E | #D7CBAD | surface | 1.34 | 1.04 |
| gray6 | #504D47 | #77726A | indicator | 3.97 | 3.07 |
| hard_black | #0E0D0C | #FDEDCF | surface | 1.04 | 1.04 |
| error_red | #EF2F27 | #EF2F27 | surface | 3.42 | 2.65 |
| selection_green | #98BC37 | #98BC37 | surface | 1.82 | 1.41 |

## Mapping adjustments

Eight UI/error definitions differ from the dark reference. Error/ErrorMsg use canonical red surfaces and dark text; PmenuSel uses canonical bright green and dark text without inverse; border/cursor/pager fixes are retained. Syntax color families and links are unchanged.

## Below-target pairs and minimal recommendations

| Mode | Group / context | Foreground | Background | Ratio / target | Recommendation |
|---|---|---|---|---|---|
| — | No audited pairs below target | — | — | — | No further contrast adjustment recommended. |

## Scope and limits

Surface colors have no text target until used with a foreground. ANSI slots are exported in their existing order, but black is now a light surface; arbitrary terminal applications can require separate role choices. Plugin-specific custom colors are outside the default audit.

Syntax overlays use the inherited foreground, including reverse. Indicator pairs are measured against Normal; actual plugin/terminal rendering can supply other backgrounds. This is a pairwise contrast audit, not a claim of complete WCAG conformance.

Visual review is pending. See metadata.json for the exact corrections applied in this iteration.

## Canonical UI colors

Error/ErrorMsg use exact canonical red `#EF2F27` with dark text. PmenuSel uses exact canonical bright green `#98BC37` with dark text and no inverse attribute. This is an explicit new popup selection design, not the unchanged dark theme's default popup. Syntax foregrounds retain their existing families.

## Additional selection-state finding

The original audit above did not include selection fill versus the unselected menu.
The expanded audit finds that pair below the 3:1 state target: 1.5866:1 in GUI.
See `selection-state-findings.json` for both editors and modes. Keep the exact
canonical green and add a dark underline, as iteration 04 does; it has 8.6076:1
contrast against the fill.
