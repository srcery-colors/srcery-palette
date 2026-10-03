#!/usr/bin/env python3
"""Capture the unchanged Vim dark theme and compare it with a light iteration."""

import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('generate_light', ROOT / 'tools/generate-light.py')
light = importlib.util.module_from_spec(spec)
spec.loader.exec_module(light)


def attributes(group, groups, foreground=None, overlay=None):
    group = dict(group)
    if foreground is not None:
        group['guifg'] = foreground
    if overlay is not None:
        group['guibg'] = overlay['guibg']
        group['guireverse'] = overlay['guireverse']
    fg, bg = light.effective(group, groups)
    style = f'color:{fg};background:{bg};'
    if group['guibold']:
        style += 'font-weight:bold;'
    if group['guiitalic']:
        style += 'font-style:italic;'
    if group['guiunderline']:
        style += 'text-decoration:underline;'
    return style


def specimen(data, index):
    groups = data['groups']
    sample = data['samples'][index]
    rows = []
    for row in sample['lines']:
        rows.append(''.join(f'<span title="{light.html.escape(token["group"])}" '
                            f'style="{attributes(groups[token["group"]], groups)}">'
                            f'{light.html.escape(token["text"])}</span>' for token in row))
    normal_fg, normal_bg = light.effective(groups['Normal'], groups)
    return f'<section style="color:{normal_fg};background:{normal_bg}"><h3>{sample["name"]}</h3><pre>' + '\n'.join(rows) + '</pre></section>'


def ui_specimen(data):
    groups = data['groups']
    fg, bg = light.effective(groups['Normal'], groups)
    rows = []
    tokens = [('Keyword', 'const '), ('Identifier', 'color'), ('Operator', ' = '),
              ('String', '"parchment"'), ('Delimiter', '; '), ('Comment', '// Srcery')]
    for name in ('Normal', 'CursorLine', 'Pmenu', 'PmenuSel', 'Visual', 'CurSearch',
                 'DiffAdd', 'DiffDelete', 'DiffChange', 'DiffText'):
        overlay = groups[name]
        spans = []
        # PmenuSel is an explicit/default completion row, not a syntax overlay.
        if name == 'PmenuSel':
            rows.append(f'<div class="ui-row"><b>{name}</b><code style="{attributes(overlay, groups)}">'
                        'selected_completion_item</code></div>')
            continue
        for group_name, text in tokens:
            group = groups[group_name]
            spans.append(f'<span style="{attributes(group, groups, overlay=overlay)}">{light.html.escape(text)}</span>')
        rows.append(f'<div class="ui-row"><b>{name}</b><code>' + ''.join(spans) + '</code></div>')
    for name in ('Error', 'ErrorMsg', 'PmenuBorder', 'FloatBorder', 'StatusLine'):
        group = groups[name]
        fg0, bg0 = light.effective(group, groups)
        rows.append(f'<div class="ui-row"><b>{name}</b><code style="{attributes(group, groups)}">'
                    f'Aa 0123 — {light.contrast(fg0, bg0):.2f}:1</code></div>')
    return f'<section style="color:{fg};background:{bg}"><h3>Identical tokens and UI contexts</h3>' + ''.join(rows) + '</section>'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--iteration', default=json.loads((ROOT / 'light/latest.json').read_text())['iteration'])
    parser.add_argument('--vim-root', type=Path, default=ROOT.parent / 'srcery-vim')
    parser.add_argument('--output', type=Path, default=ROOT / 'light/comparison')
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    iteration = ROOT / 'light/iterations' / args.iteration
    data = {}
    for editor in ('vim', 'nvim'):
        binary = shutil.which(editor)
        if not binary:
            raise RuntimeError(f'{editor} is required')
        env = {**os.environ, 'SRCERY_LIGHT_ROOT': str(args.vim_root.resolve()),
               'SRCERY_LIGHT_GROUPS': str((iteration / 'groups.json').resolve()),
               'SRCERY_LIGHT_DUMP': str(output / f'{editor}-dark.json')}
        if editor == 'nvim':
            env.pop('VIMRUNTIME', None)
        command = [binary, '-Nu', 'NONE', '-i', 'NONE', '-n']
        command += ['--headless'] if editor == 'nvim' else ['-es']
        command += ['-S', str(args.vim_root.resolve() / 'tests/dark.vim')]
        result = subprocess.run(command, env=env, text=True, capture_output=True, timeout=40)
        (output / f'{editor}-dark.log').write_text(result.stdout + result.stderr)
        if result.returncode:
            raise RuntimeError(f'{editor} dark capture failed; inspect {output}')
        data[editor] = json.loads((output / f'{editor}-dark.json').read_text())
    dark = data['vim']
    current = json.loads((iteration / 'vim-highlights.json').read_text())
    palette = json.loads((iteration / 'palette.json').read_text())
    canonical = json.loads((ROOT / 'palette.json').read_text())
    metrics = []
    for name in light.SYNTAX:
        fg0, bg0 = light.effective(dark['groups'][name], dark['groups'])
        fg1, bg1 = light.effective(current['groups'][name], current['groups'])
        metrics.append({'group': name, 'dark_fg': fg0, 'dark_bg': bg0,
                        'dark_contrast': light.contrast(fg0, bg0), 'light_fg': fg1,
                        'light_bg': bg1, 'light_contrast': light.contrast(fg1, bg1),
                        'unchanged_accent_on_light': light.contrast(fg0, bg1)})
    light.dump_json(output / 'syntax-contrast.json', metrics)
    light.dump_json(output / 'metadata.json', {
        'dark_source_sha256': light.hashlib.sha256((args.vim_root / 'colors/srcery.vim').read_bytes()).hexdigest(),
        'light_iteration': args.iteration, 'method': 'headless editor syntax IDs, identical source fixtures',
        'tree_sitter_parser': False, 'visual_review': 'pending'})
    content = '''<!doctype html><html lang="en"><meta charset="utf-8"><title>Srcery dark and light comparison</title>
<style>*{box-sizing:border-box}body{margin:0;padding:28px;background:#e9e5dd;color:#121110;font:16px/1.5 system-ui}h1{margin:0;font-size:34px}h2{margin:28px 0 12px}.labels,.pair{display:grid;grid-template-columns:1fr 1fr;gap:16px}.labels{font-size:20px;font-weight:bold;padding:10px 0}.pair{margin-bottom:16px}section{padding:18px;min-width:0}h3{margin:0 0 16px;font:17px system-ui}pre,code{font:14px/1.55 monospace}pre{white-space:pre;margin:0;overflow:auto}.ui-row{margin:8px 0;display:grid;grid-template-columns:115px 1fr;gap:10px}.ui-row b{font:13px monospace}code{padding:4px}table{border-collapse:collapse;width:100%;font:13px monospace}th,td{text-align:left;padding:8px;border-bottom:1px solid #aaa}.chips{display:flex;gap:8px}.chip{padding:8px 12px}.palettepair{display:grid;grid-template-columns:1fr 1fr;gap:16px}.swatches{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;padding:18px}.swatch{padding:10px;min-height:54px}.swatch small{display:block;font:12px monospace}@media(max-width:1000px){.pair,.labels,.palettepair{grid-template-columns:1fr}}
</style><h1>Srcery dark → Srcery Light</h1><p>Same source, font, syntax engine and group relationships. Left: unchanged srcery.vim. Right: light iteration ''' + args.iteration + '''. These are HTML specimens rendered from actual Vim syntax IDs, not editor screenshots.</p>
<div class="labels"><div>Current dark · #121110</div><div>Proposed light · #FCE8C3</div></div>'''
    content += '<p>PmenuSel below is a completion row using its resolved pair, not inherited syntax colors. The optional native-popup.png captures Neovim\'s actual built-in popup grid.</p>'
    for index in range(4):
        content += f'<div class="pair syntax-{index}">' + specimen(dark, index) + specimen(current, index) + '</div>'
    content += '<h2>Inherited foregrounds, selections, search and diff backgrounds</h2><div class="pair ui-pair">' + ui_specimen(dark) + ui_specimen(current) + '</div>'
    content += '<h2>Canonical hue families on their own backgrounds</h2><div class="palettepair">'
    accents = ('red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'orange', 'bright_orange',
               'bright_red', 'bright_green', 'bright_yellow', 'bright_blue', 'bright_magenta',
               'bright_cyan', 'white', 'bright_black', 'teal')
    for source, bg in ((canonical, '#121110'), (palette, '#FCE8C3')):
        content += f'<div class="swatches" style="background:{bg}">'
        for name in accents:
            value = source[name]['hex']
            content += f'<div class="swatch" style="color:{value}"><div style="height:48px;background:{value};margin-bottom:8px"></div>{name}<small>{value} · {light.contrast(value, bg):.2f}:1</small></div>'
        content += '</div>'
    content += '</div><h2>Contrast: current dark, unchanged dark accent on parchment, adjusted light</h2><p>The unchanged-accent column isolates why changing only the background would leave several syntax families below the 4.5:1 text target.</p><table><tr><th>Group</th><th>Current dark FG</th><th>Dark ratio</th><th>Unchanged accent on light</th><th>Light FG</th><th>Light ratio</th></tr>'
    for row in metrics:
        content += '<tr>' + ''.join(f'<td>{value}</td>' for value in (row['group'], row['dark_fg'],
                         f"{row['dark_contrast']:.2f}", f"{row['unchanged_accent_on_light']:.2f}",
                         row['light_fg'], f"{row['light_contrast']:.2f}")) + '</tr>'
    content += '</table></html>'
    (output / 'comparison.html').write_text(content)
    previous_path = ROOT / 'light/iterations/04/palette.json'
    if previous_path.exists():
        previous = json.loads(previous_path.read_text())
        revision = '<!doctype html><meta charset="utf-8"><style>body{font:16px system-ui;background:#e9e5dd;padding:24px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:16px}.grid{background:#FCE8C3;display:grid;grid-template-columns:repeat(4,1fr);gap:12px;padding:20px}.chip{height:55px;margin-bottom:8px}small{display:block;font:12px monospace}</style><h1>Light revision: same #FCE8C3 background</h1><div class="pair">'
        for source, label in ((previous, 'Previous light · 04'), (palette, 'Revised light · ' + args.iteration)):
            revision += '<section><h2>' + label + '</h2><div class="grid">'
            for name in accents:
                value = source[name]['hex']
                revision += f'<div style="color:{value}"><div class="chip" style="background:{value}"></div>{name}<small>{value}</small></div>'
            revision += '</div></section>'
        (output / 'revision.html').write_text(revision + '</div>')
    md = ['# Dark/light comparison', '', 'Left: current `srcery.vim`; right: light iteration ' + args.iteration + '.', '',
          'Identical source fixtures, Vim syntax IDs and font settings. Neovim dark capture is also retained. '
          'These are rendered syntax specimens, not editor screenshots or Tree-sitter parser runs.', '',
          '![Previous and revised light palette](revision.png)', '',
          '![Actual Neovim native popup and error UI grid](native-popup.png)', '',
          'The native popup image is rendered from Neovim ext_linegrid events after calling complete(). '
          'Error red is identical on both sides. The light selected popup uses exact canonical bright green; '
          'that is a new explicit selection choice rather than the unchanged dark default.', '',
          '![Python](python.png)', '', '![Rust](rust.png)', '', '![TypeScript](typescript.png)', '',
          '![Markdown](markdown.png)', '', '![UI](ui.png)', '', '![Palette](palette.png)', '',
          '| Group | Current dark FG | Dark ratio | Unchanged accent on parchment | Light FG | Light ratio |',
          '|---|---|---:|---:|---|---:|']
    for row in metrics:
        md.append(f"| {row['group']} | {row['dark_fg']} | {row['dark_contrast']:.2f} | "
                  f"{row['unchanged_accent_on_light']:.2f} | {row['light_fg']} | {row['light_contrast']:.2f} |")
    (output / 'comparison.md').write_text('\n'.join(md) + '\n')
    print(output / 'comparison.html')


if __name__ == '__main__':
    main()
