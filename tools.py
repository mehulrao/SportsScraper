import asyncio
from smolagents import Tool
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

# Create a persistent global event loop and set it
global_loop = asyncio.new_event_loop()
asyncio.set_event_loop(global_loop)

async def init_browser_page():
    playwright = await async_playwright().start()
    browser = await playwright.firefox.launch(headless=True)
    page = await browser.new_page()
    return page

# Initialize the global_page using the persistent loop
global_page = global_loop.run_until_complete(init_browser_page())

# Utility function to run async tasks using the persistent loop
def run_async(coro):
    return global_loop.run_until_complete(coro)

class NavigateTool(Tool):
    name = "navigate_browser"
    description = "Navigate to a URL using the web browser."
    inputs = {
        "url": {
            "type": "string",
            "description": "The URL to navigate to."
        }
    }
    output_type = "string"

    def forward(self, url: str) -> str:
        run_async(global_page.goto(url))
        return global_page.url

class NavigateBackTool(Tool):
    name = "previous_page"
    description = "Navigate back to the previous page."
    inputs = {}
    output_type = "string"

    def forward(self) -> str:
        run_async(global_page.wait_for_load_state("load"))
        run_async(global_page.go_back())
        return global_page.url

class ClickTool(Tool):
    name = "click_element"
    description = "Click on an element specified by CSS selector."
    inputs = {
        "selector": {
            "type": "string",
            "description": "CSS selector of the element to click."
        }
    }
    output_type = "string"

    def forward(self, selector: str) -> str:
        run_async(global_page.wait_for_selector(selector))
        run_async(global_page.click(selector))
        return f"Clicked element {selector}"

class ExtractTextTool(Tool):
    name = "extract_text"
    description = "Extract text from the current web page using BeautifulSoup."
    inputs = {}
    output_type = "string"

    def forward(self) -> str:
        # Wait for the body element to ensure page has loaded
        run_async(global_page.wait_for_selector("body", timeout=10000))
        html = run_async(global_page.content())
        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text(separator="\n")

class ExtractHyperlinksTool(Tool):
    name = "extract_hyperlinks"
    description = "Extract all hyperlinks from the current web page using BeautifulSoup."
    inputs = {}
    output_type = "object"

    def forward(self) -> list:
        run_async(global_page.wait_for_load_state("load"))
        html = run_async(global_page.content())
        soup = BeautifulSoup(html, "html.parser")
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        return links

class GetElementsTool(Tool):
    name = "get_elements"
    description = "Select elements by CSS selector and return their inner text."
    inputs = {
        "selector": {
            "type": "string",
            "description": "CSS selector to find elements."
        }
    }
    output_type = "object"

    def forward(self, selector: str) -> list:
        run_async(global_page.wait_for_load_state("load"))
        async def get_texts():
            elems = await global_page.query_selector_all(selector)
            return [await e.inner_text() for e in elems]
        return run_async(get_texts())

class CurrentPageTool(Tool):
    name = "current_page"
    description = "Get the current page URL."
    inputs = {}
    output_type = "string"

    def forward(self) -> str:
        return global_page.url

