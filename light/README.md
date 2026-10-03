# Srcery Light development candidate

This candidate is proposed for visual review. No package release or deployment
has been made. The companion Vim implementation is reviewed separately.

The canonical input is `../palette.json`; the Vim reference is the adjacent
`srcery-vim/colors/srcery.vim` checkout. Neither original has been modified.
The proposed palette is `../palette-light.json`, with opt-in CSS variables in
`../srcery-light.css` and a standalone `srcery-vim/colors/srcery-light.vim` theme.
These additions do not change the package's existing dark exports.

## Review

- [Iteration 01](iterations/01/report.html): preserve all highlight mappings.
  Its audit identifies errors, faint borders/inactive cursors, invisible pager
  text, and insufficient contrast in some nearest xterm approximations.
- [Iteration 02](iterations/02/report.html): retain all RGB colors, apply seven
  necessary foreground corrections, and select xterm approximations meeting
  the target. No audited GUI or fixed 256-color pair is below its target.
- [Current palette image](iterations/02/palette.png),
  [syntax specimens](iterations/02/syntax.png), and
  [UI specimens](iterations/02/ui.png).
- [Detailed analysis](ANALYSIS.md) and [current dark/light comparisons](comparison/comparison.md).
- Each iteration also contains `report.md`, `contrast.json`,
  `palette-contrast.json`, input hashes in `metadata.json`, a palette/theme
  snapshot, and Vim/Neovim resolved highlight data and validation logs.

The HTML reports are self-contained. The background selector previews text on
the actual neutral/diff surfaces. Syntax specimens come from headless Vim's
resolved syntax IDs. Both editors validate the same fixtures; the report does
not claim to be a screenshot of a running editor or Tree-sitter parser.

## Method and targets

`#FCE8C3`, canonical bright white, becomes the light background (`black` role).
Canonical black becomes the primary text (`bright_white` role). All other
accent hues and saturations are derived from canonical **RGB**, rather than
its rounded HSL metadata. Only their HSL lightness changes. Eight-bit RGB
rounding causes less than one degree of hue drift for chromatic accents.
Bright accents use a darker contrast target to remain distinct on light
surfaces. Comments retain the canonical warm brown hue.

Gray surfaces retain their canonical warm hues and use canonical white's
saturation, stepping down in lightness from the parchment background. Dark
red/green/blue and dim green become light diff tints of their canonical hues
and saturations. These are role adaptations rather than accent redesigns.

WCAG relative luminance uses the sRGB transfer function and the 0.04045
breakpoint. Text requires 4.5:1; borders, non-text indicators, and decorations
require 3:1. Ratios are compared before display rounding. The audit covers
main, cursor-line, code-block, popup, selection, search, and diff backgrounds,
including inherited foregrounds and reverse attributes. Scrollbar thumbs and
whitespace markers are evaluated as painted indicators, rather than text.

Iteration 02 changes only these foreground relationships:

| Groups | Original entry | Light entry | Reason |
|---|---|---|---|
| Error, ErrorMsg | bright_white | black | Parchment text on a dark red background |
| PmenuBorder, FloatBorder | gray3 | bright_black | A readable border without darkening the selection surface |
| TermCursorNC | gray1 | bright_black | Visible inactive cursor |
| NvimPagerFG_black_BG_, NvimPagerFG_black_BG__bold | black | bright_white | Dark pager text on parchment |

All language links, syntax families, and inverse attributes are copied from
the reference. Rainbow plugin defaults use generated entries instead of
hard-coded dark colors. Custom plugin colors and separate airline, lightline,
clap, and lualine integrations are outside this initial reference.

Fixed cterm approximations use slots 16–255, avoiding user-defined ANSI slots.
They receive a separate contrast audit. Embedded terminal ANSI colors retain
their existing slot order, including the role reversal of black/bright white;
arbitrary terminal applications can need other role choices. Enable
`termguicolors` for the exact reviewed colors. This pairwise audit does not
establish complete WCAG conformance.

## Try it

With the `srcery-vim` checkout on your runtimepath:

```vim
set termguicolors
colorscheme srcery-light
```

Overrides and options use `g:srcery_light_*`, isolated from `g:srcery_*`, so
switching between themes does not contaminate either set of defaults. Set an
override before loading the theme; overrides require a fresh contrast audit.

## Reproduce an iteration

In this workspace, activate the existing toolchain first:

```sh
source /workspace/.srcery-setup/env.sh
python3 /workspace/srcery-palette/tools/generate-light.py --iteration 03 --fix-ui --fix-cterm
vint --stat /workspace/srcery-vim/colors/srcery-light.vim /workspace/srcery-vim/tests/light.vim
python3 /workspace/srcery-palette/tools/render-light-report.py /workspace/srcery-palette/light/iterations/03
python3 /workspace/srcery-palette/tools/compare-light.py --iteration 03
python3 /workspace/srcery-palette/tools/render-light-comparison.py /workspace/srcery-palette/light/comparison
```

The generator requires Python 3, Vim and Neovim. It first generates the palette
and measures palette contrast, writes the Vim theme, runs both headless editor
validations, audits their resolved groups, then produces the visual HTML and
Markdown reports. Omit both fix flags to reproduce the initial attempt.
Use a new iteration name every time; existing snapshots are never overwritten.

The optional PNG renderer requires Playwright and Chromium (available in this
workspace). Local Chromium needs sandbox socket permission here, even though
the report contains no remote assets. The HTML and all contrast checks are
generated without a browser or network access.

Validation covers direct palette mappings, diagnostic and language links,
dark/light switching, emphasis options, an RGB override, float backgrounds,
terminal ANSI exports, and Python/Rust/TypeScript/Markdown syntax fixtures.

For self-contained tests, run `python3 tools/test-light.py` in this repository
and `python3 tests/run-light.py` in srcery-vim. The latter needs no sibling
checkout and is included in the Vim CI workflow.

Review the palette, syntax and UI artifacts before any commit. Further visual
adjustments should repeat the full generation, contrast, editor validation,
and reporting cycle.
