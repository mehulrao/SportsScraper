import asyncio
from playwright.async_api import async_playwright

async def init_async_browser():
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(headless=False)
    page = await browser.new_page()
    return page

# Expose the browser/page for other modules
async_browser = asyncio.run(init_async_browser())
