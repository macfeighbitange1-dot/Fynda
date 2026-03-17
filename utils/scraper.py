import aiohttp
import io
import pdfplumber
from bs4 import BeautifulSoup
import html2text

async def scrape_content(url):
    """
    Genius-Level Hybrid Scraper: 
    Detects PDFs for Financial Table Extraction vs. standard HTML scraping.
    Optimized for Render's memory limits.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=20) as response:
                if response.status != 200:
                    return f"Error: Received status {response.status}"
                
                # --- PDF BRANCH: Financial Intelligence Extraction ---
                content_type = response.headers.get('Content-Type', '').lower()
                if 'application/pdf' in content_type or url.lower().endswith('.pdf'):
                    pdf_data = await response.read()
                    with pdfplumber.open(io.BytesIO(pdf_data)) as pdf:
                        # Extract first 5 pages to balance depth vs. Render RAM
                        extracted_intel = []
                        for page in pdf.pages[:5]:
                            # Extract Tables (The 0.1% move for Financial Auditing)
                            tables = page.extract_tables()
                            if tables:
                                for table in tables:
                                    extracted_intel.append(f"\n[FINANCIAL TABLE DATA]:\n{str(table)}\n")
                            
                            # Extract Text
                            text = page.extract_text()
                            if text:
                                extracted_intel.append(text)
                        
                        return "\n".join(extracted_intel)

                # --- HTML BRANCH: Standard Web Scraping ---
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Remove noise
                for noise in soup(["script", "style", "nav", "footer", "header", "aside"]):
                    noise.decompose()
                
                # Convert to high-density Markdown
                h = html2text.HTML2Text()
                h.ignore_links = False
                h.bypass_tables = False # Crucial for keeping HTML tables intact
                h.ignore_images = True
                
                markdown_text = h.handle(str(soup))
                
                # Cleanup whitespace
                lines = (line.strip() for line in markdown_text.splitlines())
                return '\n'.join(line for line in lines if line)
                
    except Exception as e:
        return f"Intelligence Extraction Error: {str(e)}"