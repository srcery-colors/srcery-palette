# Srcery Light — iteration 01

Review-only candidate. No commits. Syntax mappings and inverse attributes are preserved.

Background: `#FCE8C3`. Text target: 4.5:1 (WCAG AA); indicators/decorations: 3:1.

Accent hue and saturation are derived from canonical RGB, varying HSL lightness only. Strong variants use a darker contrast target. Warm neutrals and diff surfaces are role adaptations. Hex quantization can cause small hue drift.

Both editors loaded the theme, checked palette mappings, switched dark → light → dark, exercised options and overrides, and parsed Python, Rust, TypeScript and Markdown fixtures.

GUI failures: 7; xterm fallback failures: 136. All ratios are evaluated unrounded. GUI and fixed 256-color results are separate.

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

## Mapping adjustments

None; pure mapping-preserving candidate.

## Below-target pairs and minimal recommendations

| Mode | Group / context | Foreground | Background | Ratio / target | Recommendation |
|---|---|---|---|---|---|
| cterm | NvimPagerFG_black_BG_ / own background | #FFD7AF | #FFD7AF | 1.00 / 4.5 | Use bright_white (#121110) for black pager text. |
| cterm | NvimPagerFG_black_BG__bold / own background | #FFD7AF | #FFD7AF | 1.00 / 4.5 | Use bright_white (#121110) for black pager text. |
| cterm | TermCursorNC / own background | #DADADA | #FFD7AF | 1.04 / 3.0 | Use bright_black (#635649) for this indicator; keep the light surface. |
| cterm | FloatBorder / own background | #D7D7AF | #FFD7AF | 1.10 / 3.0 | Use bright_black (#635649) for this indicator; keep the light surface. |
| cterm | PmenuBorder / own background | #D7D7AF | #FFD7AF | 1.10 / 3.0 | Use bright_black (#635649) for this indicator; keep the light surface. |
| cterm | Error / own background | #121212 | #AF0000 | 2.52 / 4.5 | Use black (#FCE8C3) as this group's foreground; keep its red background. |
| cterm | ErrorMsg / own background | #121212 | #AF0000 | 2.52 / 4.5 | Use black (#FCE8C3) as this group's foreground; keep its red background. |
| cterm | Decorator / CurSearch | #875F00 | #D7D7AF | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Decorator / IncSearch | #875F00 | #D7D7AF | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Decorator / PmenuSel | #D7D7AF | #875F00 | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Decorator / Visual | #D7D7AF | #875F00 | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Decorator / gray3 | #875F00 | #D7D7AF | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Decorator / gray4 | #875F00 | #D7D7AF | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Define / CurSearch | #875F00 | #D7D7AF | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Define / IncSearch | #875F00 | #D7D7AF | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Define / PmenuSel | #D7D7AF | #875F00 | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Define / Visual | #D7D7AF | #875F00 | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Define / gray3 | #875F00 | #D7D7AF | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Define / gray4 | #875F00 | #D7D7AF | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Function / CurSearch | #875F00 | #D7D7AF | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Function / IncSearch | #875F00 | #D7D7AF | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Function / PmenuSel | #D7D7AF | #875F00 | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Function / Visual | #D7D7AF | #875F00 | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Function / gray3 | #875F00 | #D7D7AF | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Function / gray4 | #875F00 | #D7D7AF | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Repeat / CurSearch | #875F00 | #D7D7AF | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Repeat / IncSearch | #875F00 | #D7D7AF | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Repeat / PmenuSel | #D7D7AF | #875F00 | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Repeat / Visual | #D7D7AF | #875F00 | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Repeat / gray3 | #875F00 | #D7D7AF | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Repeat / gray4 | #875F00 | #D7D7AF | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | SpecialChar / CurSearch | #875F00 | #D7D7AF | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | SpecialChar / IncSearch | #875F00 | #D7D7AF | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | SpecialChar / PmenuSel | #D7D7AF | #875F00 | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | SpecialChar / Visual | #D7D7AF | #875F00 | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | SpecialChar / gray3 | #875F00 | #D7D7AF | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | SpecialChar / gray4 | #875F00 | #D7D7AF | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Todo / CurSearch | #875F00 | #D7D7AF | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Todo / IncSearch | #875F00 | #D7D7AF | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Todo / PmenuSel | #D7D7AF | #875F00 | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Todo / Visual | #D7D7AF | #875F00 | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Todo / gray3 | #875F00 | #D7D7AF | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Todo / gray4 | #875F00 | #D7D7AF | 3.88 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Decorator / dim_green | #875F00 | #D7D7D7 | 3.98 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Decorator / gray2 | #875F00 | #D7D7D7 | 3.98 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Define / dim_green | #875F00 | #D7D7D7 | 3.98 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Define / gray2 | #875F00 | #D7D7D7 | 3.98 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Function / dim_green | #875F00 | #D7D7D7 | 3.98 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Function / gray2 | #875F00 | #D7D7D7 | 3.98 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Repeat / dim_green | #875F00 | #D7D7D7 | 3.98 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Repeat / gray2 | #875F00 | #D7D7D7 | 3.98 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | SpecialChar / dim_green | #875F00 | #D7D7D7 | 3.98 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | SpecialChar / gray2 | #875F00 | #D7D7D7 | 3.98 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Todo / dim_green | #875F00 | #D7D7D7 | 3.98 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Todo / gray2 | #875F00 | #D7D7D7 | 3.98 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | @markup.heading.2.markdown / own background | #875F00 | #DADADA | 4.10 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Decorator / dark_green | #875F00 | #DADADA | 4.10 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Decorator / gray1 | #875F00 | #DADADA | 4.10 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Define / dark_green | #875F00 | #DADADA | 4.10 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Define / gray1 | #875F00 | #DADADA | 4.10 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Function / dark_green | #875F00 | #DADADA | 4.10 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Function / gray1 | #875F00 | #DADADA | 4.10 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Repeat / dark_green | #875F00 | #DADADA | 4.10 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Repeat / gray1 | #875F00 | #DADADA | 4.10 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | SpecialChar / dark_green | #875F00 | #DADADA | 4.10 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | SpecialChar / gray1 | #875F00 | #DADADA | 4.10 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | SrceryH2 / own background | #875F00 | #DADADA | 4.10 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Todo / dark_green | #875F00 | #DADADA | 4.10 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Todo / gray1 | #875F00 | #DADADA | 4.10 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | htmlH2 / own background | #875F00 | #DADADA | 4.10 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | markdownH2 / own background | #875F00 | #DADADA | 4.10 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Decorator / dark_blue | #875F00 | #D7D7FF | 4.11 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Define / dark_blue | #875F00 | #D7D7FF | 4.11 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Function / dark_blue | #875F00 | #D7D7FF | 4.11 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Repeat / dark_blue | #875F00 | #D7D7FF | 4.11 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | SpecialChar / dark_blue | #875F00 | #D7D7FF | 4.11 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Todo / dark_blue | #875F00 | #D7D7FF | 4.11 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | @attribute / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | @constructor / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | @function.builtin / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | @keyword.directive.define / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | @keyword.repeat / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | @string.escape / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | @string.regex / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | @tag.attribute / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Annotation / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | CmpItemKindFunction / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Cursor / own background | #FFD7AF | #875F00 | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | CursorLineNr / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Decorator / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Define / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Function / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | GitGutterChange / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | GitGutterChangeDelete / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Macro / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | ModeMsg / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | MoreMsg / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | NERDTreeExecFile / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | NvimPagerFG_yellow_BG_ / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | NvimPagerFG_yellow_BG__bold / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Question / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Repeat / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | SpecialChar / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | SpecialKey / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Todo / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | diffFile / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | diffNewFile / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | goBuiltins / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | healthWarning / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | htmlArg / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | htmlSpecialChar / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | iCursor / own background | #FFD7AF | #875F00 | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | jsFuncCall / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | jsRegexpString / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | lCursor / own background | #FFD7AF | #875F00 | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | luaFunc / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | moonFunction / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | pythonEscape / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | rubyKeywordAsMethod / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | rubyLocalVariableOrMethod / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | rubyRegexp / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | sassFunctionName / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | sassInclude / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | sassMixinName / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | sassMixing / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | vCursor / own background | #FFD7AF | #875F00 | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | vimFunc / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | vimFunction / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | vimUserFunc / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | xmlAttrib / own background | #875F00 | #FFD7AF | 4.25 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Decorator / dark_red | #875F00 | #FFD7D7 | 4.35 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Define / dark_red | #875F00 | #FFD7D7 | 4.35 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Function / dark_red | #875F00 | #FFD7D7 | 4.35 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Repeat / dark_red | #875F00 | #FFD7D7 | 4.35 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | SpecialChar / dark_red | #875F00 | #FFD7D7 | 4.35 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| cterm | Todo / dark_red | #875F00 | #FFD7D7 | 4.35 / 4.5 | Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair. |
| gui | NvimPagerFG_black_BG_ / own background | #FCE8C3 | #FCE8C3 | 1.00 / 4.5 | Use bright_white (#121110) for black pager text. |
| gui | NvimPagerFG_black_BG__bold / own background | #FCE8C3 | #FCE8C3 | 1.00 / 4.5 | Use bright_white (#121110) for black pager text. |
| gui | TermCursorNC / own background | #E7DECD | #FCE8C3 | 1.11 / 3.0 | Use bright_black (#635649) for this indicator; keep the light surface. |
| gui | FloatBorder / own background | #DFD1BD | #FCE8C3 | 1.25 / 3.0 | Use bright_black (#635649) for this indicator; keep the light surface. |
| gui | PmenuBorder / own background | #DFD1BD | #FCE8C3 | 1.25 / 3.0 | Use bright_black (#635649) for this indicator; keep the light surface. |
| gui | Error / own background | #121110 | #B0140D | 2.65 / 4.5 | Use black (#FCE8C3) as this group's foreground; keep its red background. |
| gui | ErrorMsg / own background | #121110 | #B0140D | 2.65 / 4.5 | Use black (#FCE8C3) as this group's foreground; keep its red background. |

## Scope and limits

Surface colors have no text target until used with a foreground. ANSI slots are exported in their existing order, but black is now a light surface; arbitrary terminal applications can require separate role choices. Plugin-specific custom colors are outside the default audit.

Syntax overlays use the inherited foreground, including reverse. Indicator pairs are measured against Normal; actual plugin/terminal rendering can supply other backgrounds. This is a pairwise contrast audit, not a claim of complete WCAG conformance.

Visual review is pending. See metadata.json for the exact corrections applied in this iteration.
