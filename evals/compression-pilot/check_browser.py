"""Optional local Playwright check of the saved comparison, filters and layout."""
import argparse
import importlib.util
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("compression_pilot", ROOT / "pilot.py")
pilot = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(pilot)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--chrome", default="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    outputs = pilot.generations()
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=args.chrome, headless=True)
        for width, height in ((1680, 1080), (960, 1000), (390, 844)):
            page = browser.new_page(viewport={"width": width, "height": height})
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto((ROOT / "comparison.html").as_uri())
            assert page.locator("article").count() == 12
            for ident in sorted({key[0] for key in outputs}):
                for index, condition in enumerate(("initial", "prior", "compression", "editorial")):
                    assert page.locator(f"#{ident} .prose").nth(index).text_content() == outputs[ident, condition]["text"]
            assert not page.evaluate("document.documentElement.scrollWidth > innerWidth")
            page.select_option("#paper", "R03")
            page.select_option("#unit", "abstract")
            assert page.locator("article:visible").count() == 1
            page.select_option("#paper", "all")
            page.select_option("#unit", "all")
            assert page.locator("article:visible").count() == 12
            page.screenshot(path=str(args.output / f"comparison-{width}.png"))
            assert not errors, errors
            print(f"{width}x{height}: 48 exact passages, filters and overflow checks passed")
            page.close()
        browser.close()


if __name__ == "__main__":
    main()
