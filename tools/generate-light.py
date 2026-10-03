#!/usr/bin/env python3
"""Generate the review-only light palette and Vim reference from canonical inputs.

Requires Python 3. Run after activating the workspace editor toolchain.
Every run records an iteration, validates both editors, and emits contrast/visual reports.
"""

import argparse
import colorsys
import hashlib
import html
import json
import os
from pathlib import Path
import re
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
TEXT_BACKGROUNDS = ('black', 'gray1', 'gray2', 'gray3', 'gray4',
                    'dark_red', 'dark_green', 'dark_blue', 'dim_green')
SURFACES = {'black', 'hard_black', 'gray1', 'gray2', 'gray3', 'gray4',
            'gray5', 'dark_red', 'dark_green', 'dark_blue', 'dim_green'}
SYNTAX = ('Boolean Character Comment Conditional Constant Decorator Define Delimiter '
          'Exception Float Function Identifier Include Keyword Label Member Number '
          'Operator PreCondit PreProc Repeat Special SpecialChar SpecialComment '
          'Statement StorageClass String Structure Tag Todo Type Typedef Variable').split()
UI_FIXES = {'Error': 'black', 'ErrorMsg': 'black', 'PmenuBorder': 'bright_black',
            'FloatBorder': 'bright_black', 'TermCursorNC': 'bright_black',
            'NvimPagerFG_black_BG_': 'bright_white', 'NvimPagerFG_black_BG__bold': 'bright_white'}


def rgb(value):
    return tuple(int(value[i:i + 2], 16) / 255 for i in (1, 3, 5))


def hex_color(channels):
    return '#' + ''.join(f'{round(c * 255):02X}' for c in channels)


def hls(value):
    return colorsys.rgb_to_hls(*rgb(value))


def luminance(value):
    linear = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4
              for c in rgb(value)]
    return sum(c * w for c, w in zip(linear, (.2126, .7152, .0722)))


def contrast(a, b):
    a, b = sorted((luminance(a), luminance(b)))
    return (b + .05) / (a + .05)


def darkest_needed(value, backgrounds, target, upper=None):
    """Highest quantized HSL lightness meeting target; hue/saturation stay fixed."""
    hue, light, saturation = hls(value)
    lo, hi = 0., light if upper is None else upper
    for _ in range(48):
        mid = (lo + hi) / 2
        candidate = hex_color(colorsys.hls_to_rgb(hue, mid, saturation))
        if min(contrast(candidate, bg) for bg in backgrounds) >= target:
            lo = mid
        else:
            hi = mid
    return hex_color(colorsys.hls_to_rgb(hue, lo, saturation))


def xterm_palette():
    cube = (0, 95, 135, 175, 215, 255)
    result = {16 + 36 * r + 6 * g + b: hex_color((rv / 255, gv / 255, bv / 255))
              for r, rv in enumerate(cube) for g, gv in enumerate(cube)
              for b, bv in enumerate(cube)}
    result.update({232 + i: hex_color(((8 + i * 10) / 255,) * 3) for i in range(24)})
    return result


XTERM = xterm_palette()


def nearest_xterm(value):
    # Avoid configurable ANSI slots 0..15. The fallback has its own contrast audit.
    return min(XTERM, key=lambda i: sum((a - b) ** 2 for a, b in zip(rgb(value), rgb(XTERM[i]))))


def generate_palette(canonical, target, fix_cterm=False):
    background = canonical['bright_white']['hex']
    hue, light, saturation = hls(background)
    colors = {'black': background, 'bright_white': canonical['black']['hex'],
              'hard_black': hex_color(colorsys.hls_to_rgb(hue, min(1, light + .025), saturation))}
    # Preserve warm gray hues; use the canonical white's saturation for parchment surfaces.
    for i in range(1, 6):
        hue = hls(canonical[f'gray{i}']['hex'])[0]
        colors[f'gray{i}'] = hex_color(colorsys.hls_to_rgb(
            hue, light - i * .023, hls(canonical['white']['hex'])[2]))
    for name, lightness in (('dark_red', .88), ('dark_green', .88),
                            ('dark_blue', .88), ('dim_green', .85)):
        hue, _, saturation = hls(canonical[name]['hex'])
        colors[name] = hex_color(colorsys.hls_to_rgb(hue, lightness, saturation))
    backgrounds = [colors[n] for n in TEXT_BACKGROUNDS]
    for name, entry in canonical.items():
        if name in colors:
            continue
        # Strong variants are darker on light surfaces, retaining separate terminal roles.
        goal = 3.05 if name == 'gray6' else target + (.60 if name.startswith('bright_')
                                                     and name != 'bright_black' else .05)
        colors[name] = darkest_needed(entry['hex'], backgrounds, goal,
                                      upper=.9 if name == 'gray6' else None)
    result = {}
    for name, entry in canonical.items():
        hue, light, saturation = hls(colors[name])
        result[name] = {**entry, 'hex': colors[name],
                        'rgb': [round(c * 255) for c in rgb(colors[name])],
                        'hsl': [round(hue * 360, 2), f'{saturation * 100:.2f}%', f'{light * 100:.2f}%'],
                        'index': nearest_xterm(colors[name]),
                        'canonical_index': entry['index'],
                        'css': entry['css'].replace('--srcery-palette-', '--srcery-light-'),
                        'var': entry['var'].replace('g:srcery_', 'g:srcery_light_')}
    if fix_cterm:
        backgrounds = [XTERM[result[n]['index']] for n in TEXT_BACKGROUNDS]
        for name, entry in result.items():
            if name in SURFACES:
                continue
            goal = 3.05 if name == 'gray6' else target + .05
            candidates = [i for i, value in XTERM.items()
                          if min(contrast(value, bg) for bg in backgrounds) >= goal]
            entry['index'] = min(candidates, key=lambda i: sum(
                (a - b) ** 2 for a, b in zip(rgb(entry['hex']), rgb(XTERM[i]))))
    return result


def generate_vim(source, palette, fix_ui=False):
    # Copy the implementation so existing syntax/UI relationships survive unchanged.
    result = source.replace("'srcery.vim' -- Dark Ritual", "'srcery-light.vim' -- Light Ritual")
    result = result.replace('set background=dark', 'set background=light')
    result = result.replace("g:colors_name='srcery'", "g:colors_name='srcery-light'")
    result = result.replace('g:srcery_', 'g:srcery_light_')
    result = result.replace('" Colors\n', '" Generated by srcery-palette/tools/generate-light.py; review before committing.\n" Colors\n')
    for name, entry in palette.items():
        pattern = rf"(let g:srcery_light_{name}=)'[^']+'"
        result = re.sub(pattern, lambda m: m[1] + "'" + entry['hex'] + "'", result)
        result = re.sub(rf'(let g:srcery_light_{name}_cterm=)\d+',
                        lambda m: m[1] + str(entry['index']), result)
        # Base colors also use fixed xterm fallbacks, independent of terminal ANSI settings.
        result = re.sub(rf'(let s:{name}\s*= \[g:srcery_light_{name},\s*)\d+(\])',
                        lambda m: m[1] + str(entry['index']) + m[2], result)
    result = result.replace('g:srcery_light_background_cterm=0',
                            f"g:srcery_light_background_cterm={palette['black']['index']}")
    # Hard-coded rainbow plugin defaults must also come from the canonical palette.
    result = re.sub(r"\['blue',\s*'#2C78BF'\], \['202',\s*'#FF5F00'\],\n"
                    r"\s*\\ \['red',\s*'#EF2F27'\], \['magenta',\s*'#E02C6D'\]",
                    "[string(s:blue[1]), s:blue[0]], [string(s:orange[1]), s:orange[0]],\n"
                    "      \\ [string(s:red[1]), s:red[0]], [string(s:magenta[1]), s:magenta[0]]",
                    result)
    result = re.sub(r"let g:rainbow_guifgs = .*", "let g:rainbow_guifgs = [s:magenta[0], s:red[0], s:orange[0], s:blue[0]]", result)
    result = re.sub(r"let g:rainbow_ctermfgs = .*", "let g:rainbow_ctermfgs = [string(s:magenta[1]), string(s:red[1]), string(s:orange[1]), string(s:blue[1])]", result)
    if fix_ui:
        for group, color in UI_FIXES.items():
            result = re.sub(rf"(call s:HL\('{re.escape(group)}',\s*)s:\w+",
                            lambda m: m[1] + 's:' + color, result)
    return result


def dump_json(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')


def editor_validation(vim_root, output, names, fix_ui=False):
    names_file = output / 'groups.json'
    dump_json(names_file, sorted(names))
    results = {}
    for editor in ('vim', 'nvim'):
        binary = shutil.which(editor)
        if not binary:
            raise RuntimeError(f'{editor} is required; activate/install the editor toolchain')
        destination = output / f'{editor}-highlights.json'
        env = {**os.environ, 'SRCERY_LIGHT_ROOT': str(vim_root),
               'SRCERY_LIGHT_GROUPS': str(names_file), 'SRCERY_LIGHT_DUMP': str(destination),
               'SRCERY_LIGHT_PALETTE': str(output / 'palette.json')}
        env['SRCERY_LIGHT_UI_FIXES'] = json.dumps(UI_FIXES if fix_ui else {})
        # Workspace VIMRUNTIME belongs to Vim; Neovim needs its own runtime.
        if editor == 'nvim':
            env.pop('VIMRUNTIME', None)
        args = [binary, '-Nu', 'NONE', '-i', 'NONE', '-n']
        args += ['--headless'] if editor == 'nvim' else ['-es']
        args += ['-S', str(vim_root / 'tests/light.vim')]
        completed = subprocess.run(args, env=env, capture_output=True, text=True, timeout=40)
        (output / f'{editor}.log').write_text(completed.stdout + completed.stderr)
        if completed.returncode:
            raise RuntimeError(f'{editor} validation failed; see {output / (editor + ".log")}')
        results[editor] = json.loads(destination.read_text())
    return results


def effective(group, groups, cterm=False, background=None):
    normal = groups['Normal']
    key = 'cterm' if cterm else 'gui'
    def color(value, fallback):
        value = value or fallback
        return XTERM[int(value)] if cterm else value.upper()
    fg = color(group[key + 'fg'], normal[key + 'fg'])
    bg = color(group[key + 'bg'], background or normal[key + 'bg'])
    if group[key + 'reverse']:
        fg, bg = bg, fg
    return fg, bg


def audit(palette, editor_data, target):
    colors = {n: e['hex'] for n, e in palette.items()}
    matrix = []
    for name, entry in palette.items():
        role = 'surface' if name in SURFACES else ('indicator' if name == 'gray6' else 'text')
        goal = None if role == 'surface' else 3. if role == 'indicator' else target
        matrix.append({'name': name, 'role': role, 'hex': entry['hex'], 'target': goal,
                       'contrasts': {bg: contrast(entry['hex'], colors[bg]) for bg in TEXT_BACKGROUNDS}})
    pairs = []
    indicators = {'VertSplit', 'WinSeparator', 'PmenuBorder', 'FloatBorder', 'NonText', 'TermCursorNC'}
    for editor, data in editor_data.items():
        groups = data['groups']
        for mode in ('gui', 'cterm'):
            for name, group in groups.items():
                if not any(group[mode + a] for a in ('fg', 'bg', 'sp')):
                    continue  # links with no definition and emphasis-only groups inherit syntax
                fg, bg = effective(group, groups, cterm=mode == 'cterm')
                # These highlights paint empty cells, not text: compare the indicator
                # background to its adjacent surface rather than inherited Normal text.
                if name in ('PmenuSbar', 'PmenuThumb', 'ExtraWhitespace'):
                    if name == 'PmenuSbar':
                        continue  # the track is decorative; thumb/track is audited below
                    track = groups['PmenuSbar'] if name == 'PmenuThumb' else groups['Normal']
                    _, adjacent = effective(track, groups, cterm=mode == 'cterm')
                    pairs.append({'editor': editor, 'mode': mode, 'group': name,
                                  'context': 'adjacent surface', 'fg': bg, 'bg': adjacent,
                                  'ratio': contrast(bg, adjacent), 'target': 3.})
                    continue
                goal = 3. if name in indicators or 'Underline' in name or name.startswith('Spell') else target
                pairs.append({'editor': editor, 'mode': mode, 'group': name, 'context': 'own background',
                              'fg': fg, 'bg': bg, 'ratio': contrast(fg, bg), 'target': goal})
                if mode == 'gui' and group['guisp']:
                    pairs.append({'editor': editor, 'mode': mode, 'group': name, 'context': 'decoration',
                                  'fg': group['guisp'].upper(), 'bg': bg,
                                  'ratio': contrast(group['guisp'], bg), 'target': 3.})
            # Syntax still applies on cursor lines, color columns, diffs, and code blocks.
            for name in SYNTAX:
                for surface in TEXT_BACKGROUNDS[1:]:
                    bg = colors[surface] if mode == 'gui' else str(palette[surface]['index'])
                    fg, bg = effective(groups[name], groups, mode == 'cterm', bg)
                    pairs.append({'editor': editor, 'mode': mode, 'group': name,
                                  'context': surface, 'fg': fg, 'bg': bg,
                                  'ratio': contrast(fg, bg), 'target': target})
            # Inverse overlays exchange the inherited syntax foreground and overlay background.
            for overlay in ('Visual', 'PmenuSel', 'CurSearch', 'IncSearch'):
                for name in SYNTAX:
                    group = {**groups[overlay], mode + 'fg': groups[name][mode + 'fg']}
                    fg, bg = effective(group, groups, mode == 'cterm')
                    pairs.append({'editor': editor, 'mode': mode, 'group': name,
                                  'context': overlay, 'fg': fg, 'bg': bg,
                                  'ratio': contrast(fg, bg), 'target': target})
    return {'targets': {'text': target, 'indicator': 3.}, 'palette': matrix,
            'pairs': pairs, 'failures': [p for p in pairs if p['ratio'] < p['target']]}


def recommendation(pair, palette):
    name = pair['group']
    if name in ('Error', 'ErrorMsg'):
        return f"Use black ({palette['black']['hex']}) as this group's foreground; keep its red background."
    if name in ('PmenuBorder', 'FloatBorder', 'TermCursorNC'):
        return f"Use bright_black ({palette['bright_black']['hex']}) for this indicator; keep the light surface."
    if name.startswith('NvimPagerFG_black'):
        return f"Use bright_white ({palette['bright_white']['hex']}) for black pager text."
    if pair['mode'] == 'cterm':
        return 'Use termguicolors for the reviewed palette, or choose a darker xterm foreground for this pair.'
    value = darkest_needed(pair['fg'], [pair['bg']], pair['target'] + .01, upper=hls(pair['fg'])[1])
    return f'Darken foreground to {value} while retaining hue/saturation; recheck other uses before applying.'


def reports(output, canonical, palette, data, audit_result, metadata):
    failures = audit_result['failures']
    # Collapse equivalent Vim/Neovim findings for a manageable report; raw JSON retains every pair.
    unique = {(p['mode'], p['group'], p['context'], p['fg'], p['bg']): p for p in failures}
    mapping_note = ('Syntax mappings and inverse attributes are preserved.' if not metadata['ui_fixes'] else
                    'Syntax families, links and inverse attributes are preserved, with necessary '
                    'foreground corrections for shared error/UI roles recorded below.')
    md = ['# Srcery Light — iteration ' + metadata['iteration'], '',
          'Review-only candidate. No commits. ' + mapping_note, '',
          f"Background: `#FCE8C3`. Text target: {audit_result['targets']['text']}:1 (WCAG AA); indicators/decorations: 3:1.", '',
          'Accent hue and saturation are derived from canonical RGB, varying HSL lightness only. '
          'Strong variants use a darker contrast target. Warm neutrals and diff surfaces are role adaptations. '
          'Hex quantization can cause small hue drift.', '',
          'Both editors loaded the theme, checked palette mappings, switched dark → light → dark, '
          'exercised options and overrides, and parsed Python, Rust, TypeScript and Markdown fixtures.', '',
          f"GUI failures: {sum(p['mode'] == 'gui' for p in unique.values())}; "
          f"xterm fallback failures: {sum(p['mode'] == 'cterm' for p in unique.values())}. "
          'All ratios are evaluated unrounded. GUI and fixed 256-color results are separate.', '',
          '## Palette', '', '| Entry | Canonical | Light | Role | Main BG | Worst relevant BG |',
          '|---|---|---|---|---:|---:|']
    cards = []
    for row in audit_result['palette']:
        name = row['name']
        minimum = min(row['contrasts'].values())
        goal = row['target']
        verdict = 'SURFACE' if goal is None else 'PASS' if minimum >= goal else 'BELOW TARGET'
        md.append(f"| {name} | {canonical[name]['hex']} | {row['hex']} | {row['role']} | "
                  f"{row['contrasts']['black']:.2f} | {minimum:.2f} |")
        h0, _, s0 = hls(canonical[name]['hex'])
        h1, _, s1 = hls(row['hex'])
        delta = abs((h1 - h0) * 360 + 180) % 360 - 180
        sample_style = (f"color:{palette['bright_white']['hex']};background:{row['hex']}"
                        if row['role'] == 'surface' else f"color:{row['hex']}")
        cards.append(f'<article><div class="swatches"><i style="background:{canonical[name]["hex"]}"></i>'
                     f'<i style="background:{row["hex"]}"></i></div><b>{name}</b>'
                     f'<code>{canonical[name]["hex"]} → {row["hex"]}</code>'
                     f'<p style="{sample_style}">Aa function(42) # comment</p>'
                     f'<small>{row["role"]} · main {row["contrasts"]["black"]:.2f}:1 · worst {minimum:.2f}:1</small>'
                     f'<small>Hue drift {abs(delta):.2f}° · saturation {s0 * 100:.1f}% → {s1 * 100:.1f}% · {verdict}</small></article>')
    md += ['', '## Mapping adjustments', '',
           'None; pure mapping-preserving candidate.' if not metadata['ui_fixes'] else
           'Seven foreground-only corrections for conflicting roles. No syntax color families '
           'or links changed. Error/ErrorMsg use light text on red; borders and the inactive cursor '
           'use bright_black; black pager text uses bright_white.', '',
           '## Below-target pairs and minimal recommendations', '',
           '| Mode | Group / context | Foreground | Background | Ratio / target | Recommendation |',
           '|---|---|---|---|---|---|']
    fail_rows = []
    for p in sorted(unique.values(), key=lambda p: (p['mode'], p['ratio'], p['group'], p['context'])):
        rec = recommendation(p, palette)
        md.append(f"| {p['mode']} | {p['group']} / {p['context']} | {p['fg']} | {p['bg']} | "
                  f"{p['ratio']:.2f} / {p['target']:.1f} | {rec} |")
        fail_rows.append('<tr>' + ''.join(f'<td>{html.escape(str(v))}</td>' for v in
                         (p['mode'], p['group'] + ' / ' + p['context'], p['fg'], p['bg'],
                          f"{p['ratio']:.2f} / {p['target']:.1f}", rec)) + '</tr>')
    if not unique:
        md.append('| — | No audited pairs below target | — | — | — | No further contrast adjustment recommended. |')
        fail_rows.append('<tr><td colspan="6">No audited GUI or fixed xterm pairs below target. No further contrast adjustment recommended.</td></tr>')
    md += ['', '## Scope and limits', '',
           'Surface colors have no text target until used with a foreground. ANSI slots are exported '
           'in their existing order, but black is now a light surface; arbitrary terminal applications '
           'can require separate role choices. Plugin-specific custom colors are outside the default audit.', '',
           'Syntax overlays use the inherited foreground, including reverse. Indicator pairs are measured '
           'against Normal; actual plugin/terminal rendering can supply other backgrounds. This is a '
           'pairwise contrast audit, not a claim of complete WCAG conformance.', '',
           'Visual review is pending. See metadata.json for the exact corrections applied in this iteration.', '']
    (output / 'report.md').write_text('\n'.join(md))
    groups = data['vim']['groups']
    syntax = []
    for sample in data['vim']['samples']:
        lines = []
        for line in sample['lines'][:26]:
            spans = []
            for token in line:
                g = groups.get(token['group'], groups['Normal'])
                fg, bg = effective(g, groups)
                style = f'color:{fg};background:{bg};'
                if g['guibold']: style += 'font-weight:bold;'
                if g['guiitalic']: style += 'font-style:italic;'
                spans.append(f'<span title="{html.escape(token["group"])}" style="{style}">{html.escape(token["text"])}</span>')
            lines.append(''.join(spans))
        syntax.append(f'<section class="sample"><h3>{html.escape(sample["name"])}</h3><pre>' + '\n'.join(lines) + '</pre></section>')
    ui = []
    for name in ('Normal', 'Comment', 'String', 'Function', 'Keyword', 'Type', 'Error',
                 'ErrorMsg', 'Visual', 'Pmenu', 'PmenuSel', 'CurSearch', 'DiffAdd', 'DiffDelete',
                 'DiffChange', 'DiffText', 'StatusLine', 'PmenuBorder'):
        fg, bg = effective(groups[name], groups)
        ui.append(f'<div class="ui" style="color:{fg};background:{bg}">{name} · Aa 0123 · {contrast(fg, bg):.2f}:1</div>')
    content = '''<!doctype html><html lang="en"><meta charset="utf-8"><title>Srcery Light palette review</title>
<style>*{box-sizing:border-box}body{margin:0;padding:36px;background:#FCE8C3;color:#121110;font:16px/1.5 system-ui}h1{font-size:40px;margin:0}h2{margin-top:32px}p{max-width:1000px}code,pre{font-family:monospace}code,small{display:block}small{font-size:12px}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}article{border:1px solid #917E6B;padding:14px;min-width:0}.swatches{display:flex;height:44px;margin-bottom:8px}.swatches i{width:50%}article p{margin:12px 0;font:18px monospace}.samples{display:grid;grid-template-columns:1fr 1fr;gap:18px}.sample{border:1px solid #917E6B;padding:16px;overflow:auto}pre{font-size:14px;line-height:1.55}.ui-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.ui{padding:12px;font:14px monospace}table{border-collapse:collapse;width:100%;font-size:13px}th,td{text-align:left;padding:8px;border-bottom:1px solid #917E6B}button,select{font:inherit;padding:6px;margin-right:10px}.failures{overflow:auto}@media(max-width:850px){.grid,.samples{grid-template-columns:1fr 1fr}.ui-grid{grid-template-columns:1fr}}
</style><h1>Srcery Light</h1>'''
    content += f'<p>Iteration {metadata["iteration"]} · background #FCE8C3 · visual review pending · no commits</p>'
    content += '<p>Canonical swatch on the left, light candidate on the right. Hue and saturation stay fixed for accents; lightness changes for contrast. Text ≥ 4.5:1; non-text indicators ≥ 3:1.</p>'
    content += '<label>Swatch text background: <select id="surface">' + ''.join(
        f'<option value="{palette[n]["hex"]}">{n} · {palette[n]["hex"]}</option>' for n in TEXT_BACKGROUNDS) + '</select></label>'
    content += '<h2>Canonical → light</h2><div class="grid">' + ''.join(cards) + '</div>'
    content += '<h2>Actual Vim syntax</h2><p>Rendered from headless Vim syntax IDs. Hover a token to see its resolved group. Neovim syntax and mappings are validated separately.</p><div class="samples">' + ''.join(syntax) + '</div>'
    content += '<h2>UI and overlay samples</h2><div class="ui-grid">' + ''.join(ui) + '</div>'
    note = 'Seven necessary foreground corrections resolve shared UI/error roles. Syntax families and links are preserved.' if metadata['ui_fixes'] else 'The pure mapping-preserving candidate exposes shared-role conflicts; minimal adjustments are listed below.'
    content += '<h2>Below-target pairs</h2><p>' + note + ' GUI and fixed xterm results are audited separately. Enable termguicolors to see the exact reviewed hues.</p><div class="failures"><table><thead><tr><th>Mode</th><th>Group / context</th><th>FG</th><th>BG</th><th>Ratio / target</th><th>Minimal adjustment</th></tr></thead><tbody>' + ''.join(fail_rows) + '</tbody></table></div>'
    content += '<script>document.querySelector("#surface").onchange=e=>{document.querySelectorAll("article").forEach(a=>a.style.background=e.target.value)}</script></html>'
    (output / 'report.html').write_text(content)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--iteration', required=True, help='New immutable review snapshot name, e.g. 01')
    parser.add_argument('--vim-root', type=Path, default=ROOT.parent / 'srcery-vim')
    parser.add_argument('--target', type=float, default=4.5)
    parser.add_argument('--fix-ui', action='store_true', help='Apply audited minimal shared-role foreground corrections')
    parser.add_argument('--fix-cterm', action='store_true', help='Constrain xterm approximations to the contrast target')
    args = parser.parse_args()
    if not re.fullmatch(r'[a-zA-Z0-9_-]+', args.iteration):
        parser.error('iteration must be a simple directory name')
    output = ROOT / 'light/iterations' / args.iteration
    if output.exists():
        parser.error(f'{output} already exists; choose a new iteration to retain history')
    output.mkdir(parents=True)
    canonical_path = ROOT / 'palette.json'
    source_path = args.vim_root / 'colors/srcery.vim'
    canonical = json.loads(canonical_path.read_text())
    source = source_path.read_text()
    palette = generate_palette(canonical, args.target, args.fix_cterm)
    dump_json(ROOT / 'palette-light.json', palette)
    dump_json(output / 'palette.json', palette)
    theme = generate_vim(source, palette, args.fix_ui)
    (args.vim_root / 'colors/srcery-light.vim').write_text(theme)
    dump_json(args.vim_root / 'tests/light-palette.json', palette)
    (output / 'srcery-light.vim').write_text(theme)
    css = ':root {\n' + ''.join(f'  {e["css"]}: {e["hex"]};\n' for e in palette.values()) + '}\n'
    (ROOT / 'srcery-light.css').write_text(css)
    metadata = {'iteration': args.iteration, 'background': '#FCE8C3', 'target': args.target,
                'canonical_sha256': hashlib.sha256(canonical_path.read_bytes()).hexdigest(),
                'vim_source_sha256': hashlib.sha256(source_path.read_bytes()).hexdigest(),
                'visual_review': 'pending', 'syntax_remapping': False,
                'ui_fixes': UI_FIXES if args.fix_ui else {}, 'cterm_constrained': args.fix_cterm}
    dump_json(output / 'metadata.json', metadata)
    # Measure the palette before editor execution, then audit the resolved editor groups.
    dump_json(output / 'palette-contrast.json', audit(palette, {}, args.target)['palette'])
    names = set(re.findall(r"call s:HL\('([^']+)'", source))
    for pair in re.findall(r'^\s*hi! link (\S+) (\S+)', source, re.M):
        names.update(pair)
    data = editor_validation(args.vim_root, output, names, args.fix_ui)
    result = audit(palette, data, args.target)
    dump_json(output / 'contrast.json', result)
    reports(output, canonical, palette, data, result, metadata)
    print(f'Generated {output / "report.html"}')
    print(f'GUI below-target pairs: {sum(p["mode"] == "gui" for p in result["failures"])}')
    print(f'xterm below-target pairs: {sum(p["mode"] == "cterm" for p in result["failures"])}')


if __name__ == '__main__':
    main()
