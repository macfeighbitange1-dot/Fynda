import aiohttp
from bs4 import BeautifulSoup
import html2text

async def scrape_content(url):
    """
    Hybrid Scraper: Efficiently handles content extraction 
    without requiring heavy browser binaries on Render.
    Optimized for memory-constrained environments.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            # Setting a 15-second timeout to ensure the agent doesn't hang
            async with session.get(url, headers=headers, timeout=15) as response:
                if response.status != 200:
                    return f"Error: Received status {response.status}"
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Remove non-content noise to save tokens and processing power
                for noise in soup(["script", "style", "nav", "footer", "header", "aside"]):
                    noise.decompose()
                
                # Convert to clean Markdown for the Synthesizer
                h = html2text.HTML2Text()
                h.ignore_links = False
                h.bypass_tables = False
                h.ignore_images = True
                
                # Extract and clean text
                markdown_text = h.handle(str(soup))
                
                # Final cleanup of excessive whitespace
                lines = (line.strip() for line in markdown_text.splitlines())
                clean_text = '\n'.join(line for line in lines if line)
                
                return clean_text
                
    except Exception as e:
        return f"Scraping Error: {str(e)}"