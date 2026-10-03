# Srcery Light — iteration 05

Revision candidate. Syntax families and links are preserved. Dedicated canonical UI surfaces separate Error/PmenuSel backgrounds from contrast-adjusted syntax foregrounds. PmenuSel uses an explicit pair; other inverse attributes are retained.

Background: `#FCE8C3`. Text target: 4.5:1 (WCAG AA); indicators/decorations: 3:1.

Accent hue and saturation are derived from canonical RGB, varying HSL lightness only. Strong variants use a darker contrast target. Warm neutrals and diff surfaces are role adaptations. Hex quantization can cause small hue drift.

Both editors loaded the theme, checked palette mappings, switched dark → light → dark, exercised options and overrides, and parsed Python, Rust, TypeScript and Markdown fixtures.

GUI failures: 0; xterm fallback failures: 0. All ratios are evaluated unrounded. GUI and fixed 256-color results are separate.

## Palette

| Entry | Canonical | Light | Role | Main BG | Worst relevant BG |
|---|---|---|---|---:|---:|
| black | #121110 | #FCE8C3 | surface | 1.00 | 1.00 |
| red | #EF2F27 | #B7140E | text | 5.60 | 4.89 |
| green | #519F50 | #346533 | text | 5.72 | 5.00 |
| yellow | #FBB829 | #724F02 | text | 6.16 | 5.39 |
| blue | #2C78BF | #235F98 | text | 5.53 | 4.83 |
| magenta | #E02C6D | #B21A51 | text | 5.53 | 4.83 |
| cyan | #0AAEB3 | #066366 | text | 5.85 | 5.12 |
| white | #C5B088 | #675532 | text | 5.98 | 5.22 |
| bright_black | #917E6B | #67594C | text | 5.62 | 4.91 |
| bright_red | #F75341 | #961406 | text | 7.28 | 6.36 |
| bright_green | #98BC37 | #3F4E17 | text | 7.55 | 6.60 |
| bright_yellow | #FED06E | #5D3F01 | text | 8.03 | 7.01 |
| bright_blue | #68A8E4 | #164B7D | text | 7.48 | 6.53 |
| bright_magenta | #FF5C8F | #980030 | text | 7.35 | 6.42 |
| bright_cyan | #2BE4D0 | #0A4F48 | text | 7.85 | 6.86 |
| bright_white | #FCE8C3 | #121110 | text | 15.69 | 13.71 |
| dark_green | #294229 | #E6EFE6 | surface | 1.02 | 1.00 |
| dark_red | #4F2321 | #F3E3E2 | surface | 1.03 | 1.00 |
| dark_blue | #1E5181 | #DEEBF7 | surface | 1.01 | 1.00 |
| dim_green | #2E5C2E | #E4F1E4 | surface | 1.03 | 1.00 |
| orange | #FF5F00 | #9D3A00 | text | 5.75 | 5.02 |
| bright_orange | #FF8700 | #703C00 | text | 7.48 | 6.54 |
| teal | #008080 | #005555 | text | 7.19 | 6.28 |
| gray1 | #1C1B19 | #E9E1D2 | surface | 1.08 | 1.00 |
| gray2 | #262522 | #E7E1CE | surface | 1.09 | 1.00 |
| gray3 | #312F2C | #E6DBCB | surface | 1.14 | 1.00 |
| gray4 | #3B3935 | #E4DBC8 | surface | 1.14 | 1.00 |
| gray5 | #45433E | #E3DAC5 | surface | 1.16 | 1.01 |
| gray6 | #504D47 | #807B72 | indicator | 3.50 | 3.06 |
| hard_black | #0E0D0C | #FDEDCF | surface | 1.04 | 1.01 |
| error_red | #EF2F27 | #EF2F27 | surface | 3.42 | 2.99 |
| selection_green | #98BC37 | #98BC37 | surface | 1.82 | 1.59 |

## Mapping adjustments

Eight UI/error definitions differ from the dark reference. Error/ErrorMsg use canonical red surfaces and dark text; PmenuSel uses canonical bright green and dark text without inverse; border/cursor/pager fixes are retained. Syntax color families and links are unchanged.

## Below-target pairs and minimal recommendations

| Mode | Group / context | Foreground | Background | Ratio / target | Recommendation |
|---|---|---|---|---|---|
| — | No audited pairs below target | — | — | — | No further contrast adjustment recommended. |

## Scope and limits

Surface colors have no text target until used with a foreground. ANSI slots are exported in their existing order, but black is now a light surface; arbitrary terminal applications can require separate role choices. Plugin-specific custom colors are outside the default audit.

Syntax overlays use the inherited foreground, including reverse. Indicator pairs are measured against Normal; actual plugin/terminal rendering can supply other backgrounds. This is a pairwise contrast audit, not a claim of complete WCAG conformance.

Implementation visual review completed; user appearance review remains open. See metadata.json for the exact corrections applied in this iteration.

## Canonical UI colors

Error/ErrorMsg use exact canonical red `#EF2F27` with dark text. PmenuSel uses exact canonical bright green `#98BC37` with dark text and no inverse attribute. This is an explicit new popup selection design, not the unchanged dark theme's default popup. Syntax foregrounds retain their existing families.
