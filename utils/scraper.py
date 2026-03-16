from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

async def scrape_content(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        try:
            await page.goto(url, wait_until="networkidle", timeout=60000)
            html = await page.content()
            soup = BeautifulSoup(html, 'html.parser')
            
            # Remove script and style elements
            for script_or_style in soup(["script", "style", "nav", "footer", "header"]):
                script_or_style.decompose()

            # Get text and clean up whitespace
            text = soup.get_text(separator=' ')
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            clean_text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return clean_text
        except Exception as e:
            return f"Error: {str(e)}"
        finally:
            await browser.close()