# Srcery Light: rationale, comparisons and measured results

Srcery Light adds an opt-in parchment palette with `#FCE8C3` as its background,
using the canonical Srcery hue families and the existing Vim theme's semantic
relationships. The resulting candidate meets a 4.5:1 target for every audited
text pair and a 3:1 target for every audited non-text indicator/decorative pair
in both the GUI palette and the fixed 256-color fallback. It remains a visual
review candidate; passing contrast checks does not establish that every reader
will prefer its appearance or that arbitrary plugins meet the same targets.

## Scope and provenance

The source of color definitions is `srcery-palette/palette.json`, at input commit
`1176afc74f23dc4ff7c4f3bb116ea327b006f4bb`. The initial reference implementation
is `srcery-vim/colors/srcery.vim`, at input commit
`ae584b8320c6e74bd37ca908e45026163c086628`. The original palette, its existing
package exports, and the original dark colorscheme remain unchanged.

Both iteration directories record SHA-256 hashes of those input files. They
contain the generated palette and Vim theme, measured color pairs, resolved
highlight attributes from both editors, syntax specimens, and readable reports.
This preserves the first attempt and its failures instead of retaining only
the successful result. The generated Vim test palette is a snapshot, not a
second authoritative source; the canonical generator updates it alongside
the theme. The colorscheme itself has no JSON or Python runtime dependency.

The dark comparison is captured from the actual unmodified Vim implementation,
rather than a reconstructed approximation of it. This matters because there
are small differences between that implementation and the canonical palette:
for example, its hard-black default is `#121212`, whereas the canonical entry
is `#0E0D0C`. The light palette always derives its entries from the canonical
source. The comparison does not silently correct the existing dark implementation.

## Direct comparison examples

Every pair uses the same source fixture, font settings and Vim syntax engine.
The left side is the current dark theme; the right side is light iteration 02.
These images are HTML syntax specimens rendered from actual headless Vim
syntax IDs and resolved attributes. They are not screenshots of a running
editor, and no Tree-sitter parser was installed. Neovim's resolved dark and
light highlight data are also retained.

### Python

![Current dark and proposed light Python](comparison/python.png)

### Rust

![Current dark and proposed light Rust](comparison/rust.png)

### TypeScript

![Current dark and proposed light TypeScript](comparison/typescript.png)

### Markdown

![Current dark and proposed light Markdown](comparison/markdown.png)

### UI, selection, search and diffs

![Current dark and proposed light UI](comparison/ui.png)

The selection rows retain inverse highlighting. A selected keyword and a
selected string can therefore have different backgrounds, because the syntax
foreground becomes the selected cell's background. This is the original
relationship, not a new selection design. Keeping it avoids a broad highlight
redesign, though the visual result deserves review in an actual editing session.

### Hue families

![Canonical dark accents and adapted light accents](comparison/palette.png)

## Why swapping only the background is insufficient

Contrast is symmetric for a given pair, but changing the background changes
the pair. Srcery's bright colors were chosen for a nearly black background;
placing the same RGB accents on parchment loses substantial contrast.
The following measurements use actual resolved groups from the unchanged dark
implementation, with the middle column substituting only the background:

| Group / entry | Dark text on `#121110` | Unchanged dark text on `#FCE8C3` | Adjusted light text on `#FCE8C3` |
|---|---:|---:|---:|
| Function / yellow | 10.77 | 1.46 | 5.90 |
| String / bright_green | 8.61 | 1.82 | 6.60 |
| Identifier and Type / bright_blue | 7.46 | 2.10 | 6.60 |
| Constant / bright_magenta | 6.45 | 2.43 | 6.60 |
| PreProc / cyan | 6.93 | 2.26 | 5.94 |
| Keyword / red | 4.59 | 3.42 | 5.92 |
| Comment / bright_black | 4.85 | 3.23 | 5.91 |
| Decorator / bright_orange | 7.83 | 2.00 | 6.63 |
| Define / orange | 6.19 | 2.54 | 5.90 |
| Special / blue | 4.08 | 3.84 | 5.89 |

The dark theme is a reference for identity and relationships, not a claim of
uniform AA text contrast. For example, its blue Special text measures 4.08:1
on the main dark background, and its current error-text pairing measures
3.42:1. This change does not alter either dark behavior.

## Color-generation decisions

### Preserve accent hue and saturation before changing syntax semantics

Each chromatic accent starts from canonical RGB, converts to HSL, and keeps
its hue and saturation while varying only lightness. Canonical RGB is used
because the stored HSL metadata is rounded. For each fixed hue/saturation,
the generator searches for the highest quantized lightness satisfying the
required contrast against the modeled backgrounds, bounded by the original
accent's lightness. Forty-eight binary-search steps are used; final acceptance
uses the rounded eight-bit RGB values actually written to the theme.

This is a constrained, reproducible lightness adjustment. It is not a global
perceptual optimization or proof that HSL hue preservation preserves perceived
hue perfectly. RGB rounding produces less than one degree of HSL hue drift
across the fifteen chromatic accent entries tested. A future comparison in
OKLCH could evaluate perceptual alternatives, but replacing the color model
now would add another design change without resolving a measured failure in
this candidate.

### Reuse the requested parchment and existing role relationships

Canonical bright white, `#FCE8C3`, becomes the light background in the `black`
role. Canonical black, `#121110`, becomes ordinary dark text in the
`bright_white` role. Names are retained to preserve the existing mapping from
palette entries to highlight groups. They describe inherited roles here rather
than literal perceptual brightness. Primary text/background contrast is 15.69:1.

The warm comment hue is retained through `bright_black`, now `#635649`.
The ordinary white/text-muted role becomes `#685633`. These are deliberately
warm browns rather than neutral grays, following the canonical palette.

### Retain distinct bright accent roles on light backgrounds

Ordinary accents are generated against a 4.55:1 internal target; strong/bright
accent variants use 5.10:1. The required text threshold is still 4.5:1.
The 0.05 margin accommodates a small numerical margin above that threshold;
checking rounded RGB ensures it is not lost during serialization. The extra
0.60 for bright accents is a design parameter chosen to keep those roles
visibly separate after adapting to light surfaces, not a WCAG requirement.
On a light background, stronger variants are darker rather than literally
brighter. Their relative visual weight and distinctness require human review.

### Adapt neutral and diff backgrounds as surfaces

Gray1 through gray5 retain their canonical warm hues and use canonical white's
saturation. Their lightness steps down from the parchment reference by 0.023
per step. Dark green/red/blue become light tints at HSL lightness 0.88; dim green
uses 0.85. The hard-black role becomes a slightly lighter parchment, using
canonical bright-white hue/saturation with lightness increased by 0.025.

These constants are documented design choices, not measured optima. They
produce ordered, warm surfaces and distinct diff tints while keeping the
existing foreground/background relationships. The foreground solver then
checks readability against the modeled light surfaces. Surface colors alone
have no text contrast requirement; that requirement applies when a foreground
is paired with a surface. NonText/gray6 is generated for a 3.05:1 internal
indicator target rather than being forced into the ordinary text target.

## Contrast method and audit coverage

The calculation uses the WCAG sRGB transfer function. For a normalized channel
`c`, linearization is `c / 12.92` when `c <= 0.04045`, and
`((c + 0.055) / 1.055) ** 2.4` otherwise. Relative luminance is
`0.2126 R + 0.7152 G + 0.0722 B`. Contrast is
`(L_lighter + 0.05) / (L_darker + 0.05)`.

Targets are 4.5:1 for ordinary-sized text and 3:1 for non-text indicators and
decorations. Bold text is not granted a reduced target merely because its
highlight group enables bold. Ratios are compared before display rounding.
Reference checks include black/white at 21:1, identical white at 1:1, green on
black at 15.304:1, and the adjacent `#767676`/`#777777` boundary on white.

The palette solver models black, gray1–gray4, dark red, dark green, dark blue,
and dim green as relevant light backgrounds. Dark blue is a conservative
palette-surface check even though the current Vim highlight calls do not use
it as a default background. Group-level checks use the actual highlights
resolved by each editor, including linked groups, inherited Normal foregrounds,
inverse attributes, and colored decorations. The syntax foreground matrix
covers cursor-line/code backgrounds, popup surfaces, selections, search
highlights and diffs. Scrollbar thumbs are compared with their track, and
whitespace markers with the adjacent surface; they are painted cells rather
than text.

The iteration-02 report contains 2,974 pair records across both editors and
both color modes: 1,495 GUI records and 1,479 cterm records. Counts include
repeated colors through links, contexts and editors; they are not 2,974 unique
colors or independently different cases. The GUI count is larger because it
also includes special decoration colors. Raw records retain each editor's
result, while the human report collapses identical findings.

## Iterations and minimal necessary exceptions

Iteration 01 generates the palette and preserves every direct highlight
relationship. It validates in both editors and passes the ordinary syntax
foreground matrix, but reveals seven distinct GUI group failures. Those seven
appear as eleven records when Vim and Neovim results are both counted, because
several groups exist only in Neovim. Its unconstrained nearest-xterm fallback
has 257 failing records, or 136 distinct group/context/color combinations.
Repeated failures mostly come from just three shared fallback color entries.

Iteration 02 keeps every RGB color from iteration 01. It applies the seven
necessary foreground-only corrections below and constrains the xterm choice.
There is no broad recoloring of syntax families or replacement of language links.

| Group(s) | Initial unchanged light mapping | Initial GUI ratio | Minimal correction | Corrected GUI ratio |
|---|---|---:|---|---:|
| Error, ErrorMsg | Dark bright_white text on dark red | 2.65 | Use parchment `black` as foreground; retain red background | 5.92 |
| PmenuBorder, FloatBorder | Light gray3 on parchment | 1.25 | Use brown `bright_black`; retain gray3 for selection surfaces | 5.91 |
| TermCursorNC | Light gray1 on parchment | 1.11 | Use `bright_black` for the inactive cursor | 5.91 |
| NvimPagerFG_black_BG_, bold variant | Parchment black-role text on parchment | 1.00 | Use dark `bright_white` for pager foreground | 15.69 |

The error conflict cannot be solved by changing `bright_white` globally:
ordinary text needs it dark on parchment, while error text needs it light on
red. The foreground exception resolves that shared-role conflict without
creating another color. The border conflict similarly cannot be solved by
darkening gray3 globally without changing selection and diff surfaces. These
are reasons tied to specific measured failures, rather than discretionary
syntax redesign.

There are 168 direct `s:HL` definitions in the source. Exactly seven change
palette arguments; 161 retain the same arguments. All 232 explicit `hi! link`
lines are retained byte-for-byte, including language, Tree-sitter, diagnostic
and plugin links. Inverse and emphasis arguments are retained. The namespace
and palette values change, and hard-coded rainbow defaults are derived from
the new entries instead of retaining dark RGB literals.

## Fixed 256-color fallback

ANSI slots 0–15 are user-configurable, so they cannot support a portable numeric
contrast assertion. The light theme's cterm attributes use fixed slots 16–255.
The embedded Vim/Neovim terminal palette still exports sixteen colors in the
original order; cterm approximation indices are separate from those ANSI slots.
`canonical_index` retains the original palette metadata, while `index` records
the chosen fixed fallback.

Iteration 01 chooses the nearest RGB approximation. Iteration 02 chooses the
nearest RGB approximation among entries meeting the background contrast target.
Only three indices change: yellow 94 → 58, orange 94 → 88, and bright_orange
94 → 58. No GUI hex value changes. The limited cube requires a visible fidelity
tradeoff: slot 94 is `#875F00`, slot 58 is `#5F5F00`, and slot 88 is `#870000`.
The orange fallback therefore becomes redder, and several base/bright families
collapse to the same fallback. This is not full preservation of GUI hue identity
in 256 colors. Prefer `termguicolors` for the reviewed RGB palette.

## Final measured result

| Metric | GUI colors | Fixed 256-color approximation |
|---|---:|---:|
| Lowest audited text ratio | 4.5519 | 4.5554 |
| Limiting text case | Label on gray4 | Decorator on gray3 |
| Lowest audited indicator ratio | 3.9709 | 3.3723 |
| Limiting indicator case | NonText on main background | NonText on main background |
| Below-target recorded pairs | 0 | 0 |

The palette-only indicator matrix additionally checks gray6 against all modeled
surfaces; its worst GUI ratio is approximately 3.07:1. That is different from
the group-level indicator minimum because the actual NonText definition uses
the main background. Ordinary accent/main-background ratios are approximately
5.89–5.94:1; bright accents are approximately 6.60–6.64:1. The higher main ratio
is a consequence of solving against the darker relevant surfaces, not an
extra WCAG requirement for the main background.

## Validation and reproducibility

Validation passed in Vim 9.1 and Neovim 0.10.4, plus Vint. The standalone Vim
repository test now checks loading with and without `termguicolors`, direct
foreground palette mappings including Neovim-only definitions, language and
diagnostic links, dark/light switching, emphasis options, a custom red override,
float backgrounds, terminal ANSI exports and four syntax fixtures. Its expected
palette snapshot is local, so CI does not need another repository checkout.
The existing Vim lint workflow also runs these headless tests.

The canonical repository's three test cases check WCAG reference values and
the 4.5 threshold, reproduce the generated candidate, check the companion Vim
output/snapshot when that checkout is present, inspect both color modes/editors
in the saved audit, and verify accent hue drift. Browser rendering checks the
expected specimen counts and produces side-by-side PNGs. The palette reports
also check the interactive background selector.

Run from adjacent checkouts with Python 3, Vim and Neovim available:

```sh
python3 srcery-palette/tools/test-light.py
python3 srcery-vim/tests/run-light.py
python3 srcery-palette/tools/generate-light.py --iteration 03 --fix-ui --fix-cterm
python3 srcery-palette/tools/compare-light.py --iteration 03
```

Generation records a new palette, palette contrast, generated Vim theme,
headless editor validation, resolved-group audit, and visual HTML/Markdown
reports. Existing iteration snapshots are not overwritten. PNG rendering is
optional and requires Playwright and Chromium; HTML generation and contrast
checks need neither a browser nor network access. The companion renderer scripts
create the saved palette and comparison PNGs.

## Boundaries and decisions still requiring visual judgment

The measured pass applies to the enumerated default pairs, not arbitrary
terminal/editor rendering. Custom colors, plugin-provided backgrounds, actual
Tree-sitter parsers and user changes need additional checks. The separate
srcery airline, lightline, clap and lualine themes still read dark globals and
are not light implementations in this change.

Gray5 is exported but not used by the current direct Vim highlight calls and
is not included in the ordinary syntax-background guarantee. For example,
white-role text on gray5 measures 4.39:1. Any future status-line integration
using that pair must minimally lighten that surface or darken its foreground,
then rerun the contrast and visual review. This limitation is stated explicitly
rather than extending the zero-failure claim to unmodeled integrations.

The `g:srcery_light_*` namespace isolates palette defaults and theme options
from the dark theme. Some third-party rainbow settings remain global and can
retain prior defaults. Embedded terminal colors are also active-theme state,
not independently isolated state. Terminal programs assuming black is always
a dark text foreground may need different role choices after the black/bright
white reversal.

Contrast cannot measure whether function yellow remains subjectively yellow
enough, whether the warm neutral ramp feels balanced, whether bright/base
variants feel distinct enough, or whether inverse selections are pleasant.
Those are the main visual review questions. No further adjustment is required
to fix a measured failure among the currently audited default pairs. If visual
review changes any colors or mapping, repeat the full iteration cycle rather
than relying on these recorded results.
