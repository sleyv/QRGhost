import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch()

        # Emulate a mobile device (iPhone 13 size)
        context = await browser.new_context(
            viewport={'width': 390, 'height': 844},
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1'
        )
        page = await context.new_page()

        # Open the local file directly
        await page.goto("file:///app/public/index.html")
        await page.wait_for_timeout(1000)

        # 1. Take a screenshot of the top half (to see the tabs)
        await page.screenshot(path="/app/verification/mobile_top.png")

        # 2. Take a screenshot of the bottom half (to see the footer)
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(500)
        await page.screenshot(path="/app/verification/mobile_bottom.png")

        print("Mobile verification screenshots generated.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
