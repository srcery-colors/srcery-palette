# Srcery Light: revision 05, rationale and measured results

Revision 05 retains `#FCE8C3`, gives regular and bright foregrounds more lightness separation, preserves the exact canonical red and green UI surfaces, and replaces the small text-only hue overview with large filled swatches. The reference remains the unchanged dark `srcery.vim`; the source of color identity remains `srcery-palette/palette.json`. All 232 explicit highlight links and all syntax palette relationships are preserved. Eight UI/error definitions differ from the dark reference.

This revision addresses two distinct observations: Error and PmenuSel previously reused contrast-adjusted foreground colors as fills, changing their appearance; the hue-family overview also made regular/bright colors difficult to distinguish. Exact surface roles address the first observation. A wider accent lightness distribution and larger specimens address the second. Passing the contrast audit supports readability of the recorded pairs; it does not establish a subjective preference or universal visual distinguishability.

## Comparisons with the current dark implementation

The following examples use identical source fixtures, fonts and Vim syntax IDs. Left is current dark; right is revision 05. These are HTML specimens from resolved editor attributes, not screenshots of a running editor. The separate popup capture is rendered from actual Neovim `ext_linegrid` events with its native completion popup enabled.

![Hue families: current dark and revision 05](comparison/palette.png)

![Previous light candidate and revision 05](comparison/revision.png)

![Native Neovim completion popup and Error](comparison/native-popup.png)

![Python](comparison/python.png)

![Rust](comparison/rust.png)

![TypeScript](comparison/typescript.png)

![Markdown](comparison/markdown.png)

![UI, selection, search and diff contexts](comparison/ui.png)

## Why the background remains unchanged

The background has relative luminance 0.8235, versus 1.0000 for white. It is bright, but changing it does not independently solve collapsed foreground spacing. The previous solver selected every regular accent at almost the same worst-background contrast, and every bright accent at a second closely spaced threshold. This compressed their luminance differences even where canonical source colors differed substantially.

Darkening the background while holding accents constant lowers the contrast of dark text. Restoring the same target would require further foreground darkening. That can work as a separate visual direction, but it is not evidence that a darker background would improve this candidate. This revision holds the requested parchment background fixed to isolate the accent and secondary-surface changes. No monitor measurements, ambient-light experiment or subjective reader study was performed, so there is no fact-based basis to claim that the background is universally too bright or comfortable.

## Hue identity and the revised generation rule

Canonical RGB is authoritative. The generator recomputes HSL from those channels rather than relying on rounded HSL metadata. For chromatic foregrounds it holds HSL hue and saturation fixed and changes lightness only, using binary search and checking the resulting eight-bit hex color. The hue constraint test verifies less than one degree of circular hue drift after quantization. HSL hue preservation is a reproducible technical constraint; it is not a claim that a darker yellow has the same perceived appearance as a bright yellow.

The new ordinary accent contrast goal is `target + 0.05 + 1.5 × canonical relative luminance`. Bright accent roles receive an additional `1.4`. Teal also receives `1.4` to retain its deeper role relative to cyan. Gray6 keeps its separate 3.05 indicator goal. The solver finds the highest HSL lightness meeting that goal on every modeled syntax background, with canonical lightness as its upper bound.

These coefficients are explicit design choices, not WCAG requirements or values uniquely dictated by the source. They provide modest source-dependent spacing, a stronger distinction for bright roles on a light background, and headroom above the minimum. The canonical bright roles become deeper rather than lighter on parchment. This preserves separate semantic roles and hue identity, while changing the direction of their lightness hierarchy. The original identical-threshold strategy remains reproducible through the generator's flags and historical snapshots.

Secondary neutral surfaces now step down by `0.009` HSL lightness per entry rather than `0.023`. Diff tints use lightness `0.92` instead of `0.88`/`0.85`, with their canonical hues and saturations retained. This reduces the amount of foreground darkening demanded by darker overlays while retaining warm neutral and tinted background roles. The main background itself is unchanged. The surface modifications are palette changes, not language highlighting redesigns.

| Accent | Canonical | Previous light 04 | Revised light 05 | Contrast on parchment |
|---|---|---|---|---:|
| red | #EF2F27 | #B0140D | #B7140E | 5.5995 |
| green | #519F50 | #326332 | #346533 | 5.7179 |
| yellow | #FBB829 | #775102 | #724F02 | 6.1627 |
| blue | #2C78BF | #215B90 | #235F98 | 5.5253 |
| magenta | #E02C6D | #AA194E | #B21A51 | 5.5292 |
| cyan | #0AAEB3 | #066265 | #066366 | 5.8538 |
| orange | #FF5F00 | #9A3900 | #9D3A00 | 5.7488 |
| bright_red | #F75341 | #A11607 | #961406 | 7.2806 |
| bright_green | #98BC37 | #47571A | #3F4E17 | 7.5513 |
| bright_yellow | #FED06E | #6D4A01 | #5D3F01 | 8.0252 |
| bright_blue | #68A8E4 | #19538A | #164B7D | 7.4763 |
| bright_magenta | #FF5C8F | #A50033 | #980030 | 7.3472 |
| bright_cyan | #2BE4D0 | #0C5B53 | #0A4F48 | 7.8520 |
| bright_orange | #FF8700 | #7C4200 | #703C00 | 7.4808 |
| teal | #008080 | #006363 | #005555 | 7.1875 |

## Measured accent separation

The table below measures contrast between two foreground colors, rather than their contrast against the background. It is useful evidence of increased luminance spacing. There is no 3:1 or 4.5:1 requirement for arbitrary syntax colors to contrast against each other, and these values are not a color-difference metric or proof of accessibility for color-vision deficiencies.

| Pair | Previous 04 | Revised 05 |
|---|---:|---:|
| red / bright_red | 1.1210 | 1.3002 |
| green / bright_green | 1.1210 | 1.3206 |
| yellow / bright_yellow | 1.1262 | 1.3022 |
| blue / bright_blue | 1.1203 | 1.3531 |
| magenta / bright_magenta | 1.1173 | 1.3288 |
| cyan / bright_cyan | 1.1160 | 1.3414 |
| orange / bright_orange | 1.1225 | 1.3013 |
| cyan / teal | 1.0075 | 1.2278 |

The overview now uses large solid swatches as well as labeled text and hex values. This removes the small glyph area as a confounding factor during palette review. The previous/revised light image uses the same parchment background and grid, allowing the adjustment to be judged independently of the dark comparison. All primary, syntax and UI images were regenerated for the current palette.

## Exact canonical Error and PmenuSel surfaces

`error_red` copies canonical `red` exactly: `#EF2F27`. Error and ErrorMsg use canonical black `#121110` as their foreground. Their truecolor contrast is 4.5861:1. A contrast-adjusted syntax red can therefore remain a readable foreground without also changing the prominent Error fill. The dedicated `g:srcery_light_error_red` override exposes that distinction explicitly.

`selection_green` copies canonical `bright_green` exactly: `#98BC37`. PmenuSel uses `#121110` text at 8.6076:1, without inverse. This is a new explicit popup choice. The existing dark default popup selection is neutral cream, so the report does not describe green as an unchanged default mapping. The native capture shows the actual popup generated by `complete()`, rather than applying PmenuSel to unrelated syntax tokens.

The green fill against the unselected menu is only 1.6757:1 and does not independently reach the 3:1 state-cue target. A dark underline provides a selection-specific cue at 8.6076:1 against the fill. Its attributes and capture are validated. Removing underline or customizing these colors requires a new audit; the fill by itself remains a documented low-contrast relationship.

These surface entries are deliberate exceptions to ordinary syntax foreground adaptation. Exporting canonical red as syntax text on parchment would produce only 3.4214:1. Keeping exact UI fills and adapted text roles separate avoids a conflict between hue appearance and the stated foreground contrast target.

## Highlight relationships and necessary exceptions

The generated Vim implementation copies the current reference, changes palette values and namespaces, and preserves language links. There are 168 direct highlight calls: 160 retain their palette arguments and eight UI/error calls change. All 232 explicit links remain verbatim. Syntax families such as keywords, strings, functions and types keep their original entry assignments.

| Groups | Adjustment | Reason |
|---|---|---|
| Error, ErrorMsg | Dark text on dedicated canonical red | Preserve the red fill while meeting text contrast |
| PmenuSel | Dark text on dedicated canonical bright green, no inverse, underline | Keep exact green and provide a strong state cue |
| PmenuBorder, FloatBorder | bright_black foreground | Original gray3 is a light surface in this variant |
| TermCursorNC | bright_black foreground | Original gray1 is too faint for the inactive cursor |
| NvimPagerFG_black_BG_, NvimPagerFG_black_BG__bold | bright_white foreground | The black role now represents the light background |

Other inverse attributes are retained. Rainbow defaults use generated entries instead of hard-coded dark hex values. This does not constitute complete third-party plugin state isolation: global rainbow settings may keep existing user defaults. Separate airline, lightline, clap and lualine integrations are outside this initial reference.

## WCAG calculations, audit coverage and current failures

For each sRGB channel, the calculation uses `c / 12.92` for `c ≤ 0.04045`, otherwise `((c + 0.055) / 1.055)^2.4`. Relative luminance is `0.2126R + 0.7152G + 0.0722B`. Contrast is `(lighter + 0.05) / (darker + 0.05)`. Ratios are compared before display rounding. Reference tests cover black/white 21:1, identical colors 1:1, green on black, and colors immediately around the 4.5 threshold.

There are **2,978 recorded editor/context/mode pairs**, including both Vim and Neovim, truecolor and fixed xterm modes. Every text pair reaches 4.5:1; every audited indicator, decoration or state cue reaches 3:1. There are **zero below-target audited pairs**. Repeated editor/mode/context records are not 2,978 unique color combinations.

| Mode | Target | Minimum | Group / context | Pair |
|---|---:|---:|---|---|
| gui | 4.5 | 4.5861 | ErrorMsg / own background | #121110 on #EF2F27 |
| gui | 3 | 3.4981 | NonText / own background | #807B72 on #FCE8C3 |
| cterm | 4.5 | 4.6714 | Decorator / gray4 | #5F5F00 on #D7D7D7 |
| cterm | 3 | 3.3723 | NonText / own background | #767676 on #FFD7AF |

The audit resolves inherited Normal foregrounds/backgrounds and reverse attributes. It covers syntax on the main, gray1–gray4 and diff surfaces, plus Visual, selected popup, search and UI contexts. The selected popup's explicit foreground is respected rather than incorrectly inheriting syntax color. Scrollbar thumbs and whitespace markers are evaluated as painted indicators. Underlines and undercurls are checked as decorations against their relevant surfaces.

Surface entries have no text contrast requirement by themselves. The exported `gray5` is not part of the modeled ordinary syntax-background guarantee. Arbitrary integrations or custom terminal programs are not covered simply because they use a palette entry. The green selection fill alone is the specifically identified below-target relationship; the recommended minimal adjustment is the included underline. No additional color changes are recommended to resolve the current audited pairs.

## Fixed 256-color behavior

The fallback selects slots 16–255, avoiding user-configurable ANSI slots 0–15. Text approximations are selected from candidates that meet the contrast goal across modeled fallback backgrounds, then minimized by RGB distance. GUI and fallback measurements are separate because a visually similar terminal approximation can have materially different contrast.

The 256-color cube has much less hue resolution. Several distinct GUI colors may map to the same slot. The wider truecolor spacing therefore does not imply equal fallback differentiation, and exact canonical Error/PmenuSel fills apply only to truecolor. Enable `termguicolors` for the reviewed RGB identity. Embedded terminal ANSI exports retain their existing ordering, including the black/bright-white role reversal; applications that assume black is always a dark foreground may need separate treatment.

## Iteration history and reproducibility

1. **01:** preserve highlight mappings first. The audit exposed shared-role errors and faint indicators, plus nearest-xterm failures. The failures and minimal recommendations remain recorded.
2. **02:** keep the RGB palette, correct seven foreground definitions, constrain xterm choices. The recorded default audit passes.
3. **03:** introduce exact canonical red/green surface roles. Text checks pass, but the expanded selection-state check identifies four editor/mode cue failures; the supplementary findings remain recorded.
4. **04:** add the dark popup underline. The expanded audit passes, but accent spacing remains compressed.
5. **05:** retain those UI fixes; widen accent spacing and lighten secondary backgrounds. Regenerate the palette, contrast matrices, Vim implementation, headless captures, reports and comparison assets. The expanded audit again passes.

Canonical input hashes are recorded in every iteration. `palette.json` and `colors/srcery.vim` remain unchanged. The original input commits are `1176afc74f23dc4ff7c4f3bb116ea327b006f4bb` and `ae584b8320c6e74bd37ca908e45026163c086628`. The generator snapshots the theme and test palette; neither is a second canonical source.

For a subsequent iteration from adjacent checkouts:

```sh
python3 srcery-palette/tools/generate-light.py --iteration 06 --fix-ui --fix-cterm --canonical-ui --selection-underline --separated
python3 srcery-palette/tools/test-light.py
python3 srcery-vim/tests/run-light.py
python3 srcery-palette/tools/compare-light.py --iteration 06
python3 srcery-palette/tools/render-light-report.py srcery-palette/light/iterations/06
python3 srcery-palette/tools/render-light-comparison.py srcery-palette/light/comparison
python3 srcery-palette/tools/capture-native-ui.py
```

Generation and contrast checks use standard-library Python plus Vim and Neovim. PNG rendering additionally requires Playwright/Chromium; native-grid rendering requires msgpack/Pillow. The standalone colorscheme requires none of these at runtime. Existing iteration directories are not overwritten.

## Validation and visual review

Both headless editors load the theme, check GUI/cterm mappings, switch dark/light/dark, exercise options and color overrides, verify terminal exports and parse Python, Rust, TypeScript and Markdown fixtures. The three Python tests pass for reference WCAG calculations, deterministic palette/theme generation and the recorded audit/hue constraints. Vint passes the generated theme and Vim test scripts. Browser rendering checks specimen counts and the interactive surface selector. Native popup capture asserts the actual RGB fills, text and underline.

The rendered palette overview, Python specimen and native popup/Error capture were visually inspected before committing this revision. Large swatches make the base/deeper roles easier to compare, and Error/PmenuSel visibly use their canonical fills. This is an implementation visual review, not an assertion of final user approval. The linked PRs remain drafts for appearance review.

No universal comfort, color-vision accessibility or whole-editor WCAG conformance claim is made. Contrast evidence applies to the recorded default pairs. Custom colors, backgrounds, actual Tree-sitter parsers and third-party integrations require separate verification. The remaining judgment is whether the deeper bright roles, ochre yellows and warm parchment meet the intended Srcery Light appearance.
