from __future__ import annotations

import asyncio
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]
CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        return


async def exercise(page, url: str) -> dict[str, object]:
    await page.goto(url, wait_until="networkidle")
    await page.locator('.choice[data-correct="true"]').click()
    code = """def select_confident_anzsic_suggestions(
    about_page_texts,
    industry_classifier,
    minimum_confidence=0.82,
):
    probabilities_by_page = industry_classifier.predict_proba(
        about_page_texts
    )
    return [
        about_text
        for about_text, probabilities in zip(
            about_page_texts,
            probabilities_by_page,
        )
        if max(probabilities) >= minimum_confidence
    ]
"""
    await page.locator("#refactor-editor").fill(code)
    await page.locator("#check-refactor").click()
    await page.locator("#refactor-editor").evaluate("element => { element.scrollTop = 0; element.scrollLeft = 0; }")
    return {
        "title": await page.title(),
        "h1": await page.locator("h1").inner_text(),
        "quiz": await page.locator(".question .feedback").inner_text(),
        "refactor": await page.locator("#refactor-feedback").inner_text(),
        "passed_checks": await page.locator("#refactor-checklist li.pass").count(),
        "scroll_width": await page.evaluate("document.documentElement.scrollWidth"),
        "client_width": await page.evaluate("document.documentElement.clientWidth"),
    }


async def exercise_promises(page, url: str) -> dict[str, object]:
    await page.goto(url, wait_until="networkidle")
    await page.locator('.choice[data-correct="true"]').click()
    for option in await page.locator('.promise-option[data-promise="true"]').all():
        await option.click()
    await page.locator("#check-promises").click()
    success_feedback = await page.locator("#promise-feedback").inner_text()

    await page.reload(wait_until="networkidle")
    persisted_selections = await page.locator(".promise-option.selected").count()
    persisted_score = await page.evaluate(
        "JSON.parse(localStorage.getItem('teach:0002-read-contracts-before-bodies') || '{}').promiseScore"
    )
    await page.locator("#check-promises").click()

    return {
        "title": await page.title(),
        "h1": await page.locator("h1").inner_text(),
        "quiz": await page.locator(".question .feedback").inner_text(),
        "promises": success_feedback,
        "persisted_selections": persisted_selections,
        "persisted_score": persisted_score,
        "scroll_width": await page.evaluate("document.documentElement.scrollWidth"),
        "client_width": await page.evaluate("document.documentElement.clientWidth"),
    }


async def run_browser_checks(base_url: str) -> None:
    async with async_playwright() as playwright:
        launch_args = {"headless": True}
        if CHROME.exists():
            launch_args["executable_path"] = str(CHROME)
        browser = await playwright.chromium.launch(**launch_args)
        all_errors: list[str] = []
        for name, viewport in (("desktop", {"width": 1200, "height": 900}), ("mobile", {"width": 390, "height": 844})):
            context = await browser.new_context(viewport=viewport)
            page = await context.new_page()
            page.on("console", lambda message: all_errors.append(f"console:{message.type}:{message.text}") if message.type == "error" else None)
            page.on("pageerror", lambda error: all_errors.append(f"pageerror:{error}"))
            await page.goto(base_url, wait_until="networkidle")
            home = {
                "title": await page.title(),
                "h1": await page.locator("h1").inner_text(),
                "modules": await page.locator(".module-card").count(),
                "scroll_width": await page.evaluate("document.documentElement.scrollWidth"),
                "client_width": await page.evaluate("document.documentElement.clientWidth"),
            }
            if home["title"] != "Software Fundamentals" or home["modules"] != 6:
                raise AssertionError(f"{name} course home is incomplete: {home}")
            if home["scroll_width"] != home["client_width"]:
                raise AssertionError(f"{name} course home has horizontal overflow: {home}")
            home_screenshot = ROOT / "artifacts" / f"course-home-{name}.png"
            home_screenshot.parent.mkdir(parents=True, exist_ok=True)
            await page.screenshot(path=str(home_screenshot), full_page=True)
            print(f"home_{name}={home}")
            print(f"screenshot={home_screenshot}")

            result = await exercise(page, f"{base_url}lessons/0001-names-are-architecture.html")
            if result["scroll_width"] != result["client_width"]:
                raise AssertionError(f"{name} has horizontal overflow: {result}")
            if result["passed_checks"] != 5:
                raise AssertionError(f"{name} refactor feedback failed: {result}")
            screenshot = ROOT / "artifacts" / f"lesson-0001-{name}.png"
            screenshot.parent.mkdir(parents=True, exist_ok=True)
            await page.screenshot(path=str(screenshot), full_page=True)
            print(f"{name}={result}")
            print(f"screenshot={screenshot}")

            promise_result = await exercise_promises(
                page,
                f"{base_url}lessons/0002-read-contracts-before-bodies.html",
            )
            if promise_result["scroll_width"] != promise_result["client_width"]:
                raise AssertionError(f"{name} Lesson 0002 has horizontal overflow: {promise_result}")
            if promise_result["persisted_selections"] != 3 or promise_result["persisted_score"] != 5:
                raise AssertionError(f"{name} Lesson 0002 persistence failed: {promise_result}")
            if not str(promise_result["promises"]).startswith("5/5"):
                raise AssertionError(f"{name} Lesson 0002 promise feedback failed: {promise_result}")
            if not str(promise_result["quiz"]).startswith("Correct."):
                raise AssertionError(f"{name} Lesson 0002 quiz persistence failed: {promise_result}")
            promise_screenshot = ROOT / "artifacts" / f"lesson-0002-{name}.png"
            await page.screenshot(path=str(promise_screenshot), full_page=True)
            print(f"promises_{name}={promise_result}")
            print(f"screenshot={promise_screenshot}")
            await context.close()
        await browser.close()
        if all_errors:
            raise AssertionError("Browser errors: " + " | ".join(all_errors))
        print("browser_errors=0")


def main() -> None:
    handler = partial(QuietHandler, directory=str(ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    port = server.server_address[1]
    url = f"http://127.0.0.1:{port}/"
    try:
        asyncio.run(run_browser_checks(url))
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


if __name__ == "__main__":
    main()
