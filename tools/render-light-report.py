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
        assert page.locator('article').count() in (30, 32)
        assert page.locator('.sample').count() == 4
        page.screenshot(path=str(output / 'review.png'), full_page=True)
        page.locator('.grid').screenshot(path=str(output / 'palette.png'))
        page.locator('.samples').screenshot(path=str(output / 'syntax.png'))
        page.locator('.ui-grid').screenshot(path=str(output / 'ui.png'))
        value = page.locator('#surface option').filter(has_text='gray4 ·').get_attribute('value')
        page.locator('#surface').select_option(value=value)
        assert page.locator('article').first.evaluate(
            'element => getComputedStyle(element).backgroundColor') == 'rgb(' + ', '.join(str(int(value[i:i+2], 16)) for i in (1, 3, 5)) + ')'
        browser.close()
    print(f'Rendered and checked {output / "review.png"}')


if __name__ == '__main__':
    main()
