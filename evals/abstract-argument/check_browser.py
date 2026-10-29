"""Optional local Playwright checks; no writing-quality inference."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--chrome")
    args = parser.parse_args()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    views, errors, requests = [], [], []
    with sync_playwright() as playwright:
        options = {"executable_path": args.chrome} if args.chrome else {}
        browser = playwright.chromium.launch(headless=True, **options)
        try:
            for width in (1440, 960, 390, 320):
                page = browser.new_page(viewport={"width": width, "height": 960},
                                        reduced_motion="reduce")
                page.on("pageerror", lambda error: errors.append(str(error)))
                page.on("request", lambda req: requests.append(req.url)
                        if req.url.startswith(("https://", "http://")) else None)
                page.route("https://**/*", lambda route: route.abort())
                page.route("http://**/*", lambda route: route.abort())
                page.goto((ROOT / "comparison.html").as_uri())
                assert page.locator(".paper").count() == 5
                assert page.locator("article.version").count() == 15
                assert page.locator("details[open]").count() == 0
                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
                overflow = page.locator(".version, .paper, nav").evaluate_all(
                    "els => els.filter(e => e.scrollWidth > e.clientWidth + 1).length")
                assert overflow == 0, (width, overflow)
                for link in page.locator("nav a").all():
                    ident = link.get_attribute("href")[1:]
                    link.click()
                    page.wait_for_function("id => {const r = document.getElementById(id).getBoundingClientRect(); return r.top >= 0 && r.top < innerHeight}", arg=ident)
                details = page.locator(".english, .decisions")
                nested_toggles = 0
                for item in details.all():
                    item.locator(":scope > summary").click()
                    assert item.get_attribute("open") is not None
                    assert item.evaluate("e => e.scrollWidth <= e.clientWidth + 1")
                    for nested in item.locator("details").all():
                        nested.locator("summary").click()
                        assert nested.get_attribute("open") is not None
                        assert nested.evaluate("e => e.scrollWidth <= e.clientWidth + 1")
                        nested.locator("summary").click()
                        nested_toggles += 1
                    item.locator(":scope > summary").click()
                    assert item.get_attribute("open") is None
                page.evaluate("scrollTo(0, 0)")
                page.screenshot(path=str(output / f"comparison-{width}.png"), full_page=True)
                views.append({"width": width, "overflow": overflow, "anchors": 5,
                              "detail_toggles": details.count(), "nested_toggles": nested_toggles})
                page.close()
        finally:
            browser.close()
    assert not errors, errors
    assert not requests, requests
    report = {"scope": "Rendering, anchors, toggles and offline behavior only",
              "views": views, "errors": errors, "remote_requests": requests}
    (output / "browser.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report))


if __name__ == "__main__":
    main()
