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
- [Current palette image](iterations/05/palette.png),
  [syntax specimens](iterations/05/syntax.png), and
  [UI specimens](iterations/05/ui.png).
- [Iteration 03](iterations/03/report.html): retain the thirty RGB entries and add
  exact canonical error-red and popup-green surface roles, with explicit dark text.
  Its original text audit passes, but a subsequent selection-state check finds
  the green fill only 1.59:1 against the menu.
- [Iteration 04](iterations/04/report.html): retain all RGB values and add a dark
  selection underline. The expanded state-cue audit passes, along with text and
  indicator checks. [Native popup/error capture](comparison/native-popup.png).
- [Iteration 05](iterations/05/report.html): retain the main background and exact UI
  fills, widen accent lightness spacing, lighten secondary surfaces, and expand
  the overview to large solid swatches. All audited pairs pass.
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

Iteration 02 records the initial foreground-only corrections:

| Groups | Original entry | Light entry | Reason |
|---|---|---|---|
| Error, ErrorMsg | bright_white | black | Parchment text on a dark red background |
| PmenuBorder, FloatBorder | gray3 | bright_black | A readable border without darkening the selection surface |
| TermCursorNC | gray1 | bright_black | Visible inactive cursor |
| NvimPagerFG_black_BG_, NvimPagerFG_black_BG__bold | black | bright_white | Dark pager text on parchment |

Iteration 03 keeps all language links and syntax families. It uses canonical
red and bright green for dedicated Error/PmenuSel backgrounds, with dark text;
PmenuSel removes inverse; iteration 04 adds a high-contrast underline. Other inverse attributes remain as in the reference.
The green popup is an explicit new choice, not the unchanged dark default. Rainbow plugin defaults use generated entries instead of
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
python3 /workspace/srcery-palette/tools/generate-light.py --iteration 06 --fix-ui --fix-cterm --canonical-ui --selection-underline --separated
vint --stat /workspace/srcery-vim/colors/srcery-light.vim /workspace/srcery-vim/tests/light.vim
python3 /workspace/srcery-palette/tools/render-light-report.py /workspace/srcery-palette/light/iterations/06
python3 /workspace/srcery-palette/tools/compare-light.py --iteration 06
python3 /workspace/srcery-palette/tools/render-light-comparison.py /workspace/srcery-palette/light/comparison
```

The generator requires Python 3, Vim and Neovim. It first generates the palette
and measures palette contrast, writes the Vim theme, runs both headless editor
validations, audits their resolved groups, then produces the visual HTML and
Markdown reports. Omit the fix flags and canonical-ui flag to reproduce the initial attempt.
Use a new iteration name every time; existing snapshots are never overwritten.

The optional PNG renderers require Playwright and Chromium. Native UI capture
requires msgpack and Pillow. Use a Python environment containing these optional
packages; the workspace editor toolchain Python does not include all of them. Local Chromium needs sandbox socket permission here, even though
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
