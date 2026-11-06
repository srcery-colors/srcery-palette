#!/usr/bin/env python3
"""Capture Neovim's actual built-in popup/error UI grid for both themes."""
import argparse
import json
import os
from pathlib import Path
import selectors
import shutil
import subprocess
import time

import msgpack
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]


def capture(theme, vim_root):
    env = dict(os.environ)
    env.pop('VIMRUNTIME', None)
    process = subprocess.Popen([shutil.which('nvim'), '--embed', '-u', 'NONE', '-i', 'NONE', '-n'],
                               env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ)
    unpacker = msgpack.Unpacker(raw=False)
    replies = {}
    grids = {}
    attributes = {}
    default = {}
    request_id = 0

    def events(message):
        if message[0] == 1:
            replies[message[1]] = message[2:]
            return
        if message[0] != 2 or message[1] != 'redraw':
            return
        for event in message[2]:
            name = event[0]
            for args in event[1:]:
                if name == 'grid_resize':
                    grid, width, height = args
                    grids[grid] = [[[' ', 0] for _ in range(width)] for _ in range(height)]
                elif name == 'grid_clear':
                    grid = args[0]
                    grids[grid] = [[[' ', 0] for _ in row] for row in grids[grid]]
                elif name == 'hl_attr_define':
                    attributes[args[0]] = args[1]
                elif name == 'default_colors_set':
                    default.update(foreground=args[0], background=args[1])
                elif name == 'grid_line':
                    grid, row, col, cells, *_ = args
                    attr = 0
                    for cell in cells:
                        text = cell[0]
                        if len(cell) > 1:
                            attr = cell[1]
                        repeat = cell[2] if len(cell) > 2 else 1
                        for _ in range(repeat):
                            grids[grid][row][col] = [text, attr]
                            col += 1

    def pump(timeout):
        if selector.select(timeout):
            chunk = os.read(process.stdout.fileno(), 65536)
            if not chunk:
                raise RuntimeError('Neovim closed its UI stream')
            unpacker.feed(chunk)
            for message in unpacker:
                events(message)

    def rpc(method, parameters):
        nonlocal request_id
        request_id += 1
        ident = request_id
        process.stdin.write(msgpack.packb([0, ident, method, parameters], use_bin_type=True))
        process.stdin.flush()
        deadline = time.monotonic() + 10
        while ident not in replies:
            if time.monotonic() > deadline:
                raise RuntimeError(f'Neovim RPC timeout: {method}')
            pump(.05)
        error, result = replies.pop(ident)
        if error:
            raise RuntimeError(str(error))
        return result

    try:
        rpc('nvim_ui_attach', [72, 15, {'rgb': True, 'ext_linegrid': True, 'ext_popupmenu': False}])
        for command in [f'set runtimepath^={vim_root}', 'set termguicolors', 'syntax on',
                        f'colorscheme {theme}', 'set laststatus=2 noshowmode',
                        'set completeopt=menuone,noinsert', 'set filetype=javascript']:
            rpc('nvim_command', [command])
        rpc('nvim_buf_set_lines', [0, 0, -1, True, [
            '// Native Neovim popup and Error group, identical source',
            'const color = "Srcery";',
            'ERROR: canonical Srcery red',
            '',
            '']])
        rpc('nvim_command', ['syntax match SrceryUIError /ERROR: canonical Srcery red/'])
        rpc('nvim_command', ['highlight link SrceryUIError Error'])
        rpc('nvim_input', ['Gicol'])
        deadline = time.monotonic() + 1
        while time.monotonic() < deadline:
            pump(.03)
            if rpc('nvim_eval', ['mode()']) == 'i':
                break
        rpc('nvim_command', ["call complete(1, ['color', 'column', 'colorize'])"])
        rpc('nvim_command', ['redraw!'])
        deadline = time.monotonic() + .25
        while time.monotonic() < deadline:
            pump(.02)
        return {'theme': theme, 'grid': grids[1], 'attributes': attributes, 'default': default,
                'method': 'actual Neovim ext_linegrid, native complete(), no syntax-color popup simulation'}
    finally:
        process.terminate()
        process.communicate(timeout=5)
        selector.close()


def render(data, label):
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 17)
    header_font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 18)
    width, height = 11, 24
    grid = data['grid']
    canvas = Image.new('RGB', (len(grid[0]) * width + 24, len(grid) * height + 62), '#e9e5dd')
    draw = ImageDraw.Draw(canvas)
    draw.text((12, 8), label, font=header_font, fill='#121110')
    for row, cells in enumerate(grid):
        for col, (text, attr) in enumerate(cells):
            style = data['attributes'].get(attr, data['attributes'].get(str(attr), {}))
            fg = style.get('foreground', data['default']['foreground'])
            bg = style.get('background', data['default']['background'])
            if style.get('reverse'):
                fg, bg = bg, fg
            x, y = 12 + col * width, 44 + row * height
            draw.rectangle((x, y, x + width, y + height), fill=f'#{bg:06x}')
            draw.text((x, y), text, font=font, fill=f'#{fg:06x}')
            if style.get('underline'):
                draw.line((x, y + 21, x + width, y + 21), fill=f'#{fg:06x}', width=1)
    return canvas


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--vim-root', type=Path, default=ROOT.parent / 'srcery-vim')
    parser.add_argument('--output', type=Path, default=ROOT / 'light/comparison')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    pictures = []
    for theme, label in [('srcery', 'Current dark: native popup and Error'),
                         ('srcery-light', 'Light: canonical UI colors')]:
        data = capture(theme, args.vim_root.resolve())
        def actual_colors(cell):
            attributes = data['attributes'].get(cell[1], {})
            foreground = attributes.get('foreground', data['default']['foreground'])
            background = attributes.get('background', data['default']['background'])
            return (background, foreground) if attributes.get('reverse') else (foreground, background)
        error_row = next(row for row in data['grid'] if ''.join(c[0] for c in row).startswith('ERROR:'))
        assert actual_colors(error_row[0])[1] == 0xEF2F27
        selected = next(row for row in data['grid'] if ''.join(c[0] for c in row).strip() == 'color')
        if theme == 'srcery-light':
            assert actual_colors(error_row[0])[0] == 0x121110
            assert actual_colors(selected[0]) == (0x121110, 0x98BC37)
            assert data['attributes'][selected[0][1]].get('underline')
        (args.output / f'native-{theme}.json').write_text(json.dumps(data, indent=2) + '\n')
        pictures.append(render(data, label))
    combined = Image.new('RGB', (pictures[0].width + pictures[1].width + 16,
                                 max(p.height for p in pictures)), '#e9e5dd')
    combined.paste(pictures[0], (0, 0))
    combined.paste(pictures[1], (pictures[0].width + 16, 0))
    combined.save(args.output / 'native-popup.png')
    print(args.output / 'native-popup.png')


if __name__ == '__main__':
    main()
