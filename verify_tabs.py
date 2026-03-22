import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        # Set a standard desktop viewport
        await page.set_viewport_size({"width": 1024, "height": 768})
        await page.goto("http://localhost:8080/index.html")

        # Wait for the main elements
        await page.wait_for_selector("#enc")

        # Screenshot Encrypt Tab (scroll down to stats)
        await page.evaluate("document.querySelector('.main-content').scrollTop = 300")
        await page.screenshot(path="verification/encrypt_stats.png")

        # Switch to Decrypt tab
        await page.click("#goDec")
        await page.wait_for_selector("#dec")

        # Screenshot Decrypt Tab
        await page.evaluate("document.querySelector('.main-content').scrollTop = 0")
        await page.screenshot(path="verification/decrypt_layout.png")

        await browser.close()

asyncio.run(main())
