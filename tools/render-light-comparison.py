#!/usr/bin/env python3
"""Render the dark/light comparison HTML into PR-ready PNG specimens."""

import argparse
from pathlib import Path

from playwright.sync_api import sync_playwright


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('comparison', type=Path)
    parser.add_argument('--chromium', default='/usr/bin/chromium')
    args = parser.parse_args()
    output = args.comparison.resolve()
    with sync_playwright() as runtime:
        browser = runtime.chromium.launch(executable_path=args.chromium, headless=True,
                                          args=['--no-sandbox'])
        page = browser.new_page(viewport={'width': 1700, 'height': 1100}, device_scale_factor=1)
        page.set_content((output / 'comparison.html').read_text(), wait_until='load')
        assert page.locator('.pair').count() == 5
        for index, name in enumerate(('python', 'rust', 'typescript', 'markdown')):
            page.locator(f'.syntax-{index}').screenshot(path=str(output / f'{name}.png'))
        page.locator('.ui-pair').screenshot(path=str(output / 'ui.png'))
        page.locator('.palettepair').screenshot(path=str(output / 'palette.png'))
        page.screenshot(path=str(output / 'comparison.png'), full_page=True)
        browser.close()
    print(f'Rendered six comparison specimens in {output}')


if __name__ == '__main__':
    main()
