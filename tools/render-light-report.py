#!/usr/bin/env python3
"""Render an iteration's self-contained HTML with Playwright and local Chromium."""

import argparse
from pathlib import Path

from playwright.sync_api import sync_playwright


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('iteration', type=Path)
    parser.add_argument('--chromium', default='/usr/bin/chromium')
    args = parser.parse_args()
    output = args.iteration.resolve()
    with sync_playwright() as runtime:
        browser = runtime.chromium.launch(executable_path=args.chromium, headless=True,
                                          args=['--no-sandbox'])
        page = browser.new_page(viewport={'width': 1600, 'height': 1100}, device_scale_factor=1)
        page.set_content((output / 'report.html').read_text(), wait_until='load')
        assert page.locator('article').count() == 30
        assert page.locator('.sample').count() == 4
        page.screenshot(path=str(output / 'review.png'), full_page=True)
        page.locator('.grid').screenshot(path=str(output / 'palette.png'))
        page.locator('.samples').screenshot(path=str(output / 'syntax.png'))
        page.locator('.ui-grid').screenshot(path=str(output / 'ui.png'))
        page.locator('#surface').select_option(label='gray4 · #DBCEB5')
        assert page.locator('article').first.evaluate(
            'element => getComputedStyle(element).backgroundColor') == 'rgb(219, 206, 181)'
        browser.close()
    print(f'Rendered and checked {output / "review.png"}')


if __name__ == '__main__':
    main()
