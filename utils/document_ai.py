import pdfplumber
import aiohttp
import io

async def extract_financial_tables(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            content = await response.read()
            pdf_file = io.BytesIO(content)
            
            extracted_tables = []
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    table = page.extract_table()
                    if table:
                        extracted_tables.append(table)
            
            return extracted_tables # Returns structured list of rows/columns