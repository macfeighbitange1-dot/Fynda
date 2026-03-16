import click
import asyncio
import os
from core.search import ResearchSearch
from utils.scraper import scrape_content
from core.processor import ResearchProcessor
from core.synthesizer import ResearchSynthesizer

async def process_source(res, query, processor):
    """Worker function to scrape and analyze a single source."""
    url = res['url']
    click.secho(f" [+] Extracting & Analyzing: {url}", fg='green')
    
    content = await scrape_content(url)
    
    if "Error" in content:
        return f"\nSOURCE: {url}\n[!] Failed to retrieve content."

    claims = processor.extract_claims(query, content)
    return f"\nSOURCE: {url}\n{claims}"

@click.command()
@click.argument('query')
@click.option('--depth', default=1, help='Recursive depth')
def run_research(query, depth):
    """Aletheia: Deep Research Engine (Devil's Advocate Edition)"""
    
    if not os.getenv("TAVILY_API_KEY") or not os.getenv("MISTRAL_API_KEY"):
        click.secho("[!] Error: TAVILY_API_KEY or MISTRAL_API_KEY missing in .env", fg='red', bold=True)
        return

    click.secho(f"\n[*] RESEARCH IDENTITY: {query.upper()}", fg='cyan', bold=True)
    click.echo("[*] Status: Querying live web...")

    search_engine = ResearchSearch()
    processor = ResearchProcessor()
    synthesizer = ResearchSynthesizer()
    
    results = search_engine.execute_search(query)
    click.echo(f"[*] Found {len(results)} primary sources. Starting Parallel Cognitive Analysis...")

    async def main_loop():
        # --- ROUND 1: Initial Research ---
        tasks = [process_source(res, query, processor) for res in results]
        reports = await asyncio.gather(*tasks)
        
        # --- AGENTIC AUDIT: Round 2 Check ---
        click.echo("\n" + "═"*60)
        click.secho(" AGENTIC AUDIT: ANALYZING DATA CONSISTENCY ", fg='yellow', bold=True)
        click.echo("═"*60)
        
        gap_query = synthesizer.check_for_gaps(reports)
        
        if gap_query and "NONE" not in gap_query.upper():
            click.secho(f"[!] CONTRADICTION DETECTED. Launching Targeted Round 2:", fg='magenta', bold=True)
            click.secho(f" [Query]: {gap_query}", fg='magenta')
            
            new_results = search_engine.execute_search(gap_query)
            new_tasks = [process_source(res, gap_query, processor) for res in new_results[:2]]
            new_reports = await asyncio.gather(*new_tasks)
            reports.extend(new_reports)
        else:
            click.secho("[*] Data Integrity Confirmed. Proceeding to Synthesis.", fg='green')

        # --- PHASE 3: DRAFT SYNTHESIS ---
        click.echo("\n" + "═"*60)
        click.secho(" GENERATING INITIAL DRAFT SYNTHESIS ", fg='white', bg='blue', bold=True)
        click.echo("═"*60)
        draft_report = synthesizer.synthesize(query, reports)

        # --- PHASE 6: DEVIL'S ADVOCATE PROTOCOL ---
        click.echo("\n" + "═"*60)
        click.secho(" DEVIL'S ADVOCATE: RUNNING RED-TEAM AUDIT ", fg='red', bold=True)
        click.echo("═"*60)
        
        critique = synthesizer.criticize(query, draft_report)
        
        if "APPROVED" in critique.upper() and len(critique) < 25:
            click.secho("[*] Critique Passed: No structural amendments required.", fg='green')
            final_report = draft_report
        else:
            click.secho("[!] Critique Identified Weaknesses. Refining for Extreme Accuracy...", fg='yellow')
            # Extract the core of the critique for user transparency
            preview = critique[:200].replace("\n", " ") + "..."
            click.echo(f" [Critique Focus]: {preview}")
            
            # Final Polish
            final_report = synthesizer.refine(query, draft_report, critique)

        # --- FINAL OUTPUT & EXPORT ---
        click.echo("\n" + "═"*60)
        click.secho(" FINAL PEER-REVIEWED EXECUTIVE REPORT ", fg='white', bg='green', bold=True)
        click.echo("═"*60)
        click.echo(final_report)
        
        report_filename = "research_report.md"
        with open(report_filename, "w", encoding="utf-8") as f:
            f.write(f"# Research Identity: {query}\n\n")
            f.write(final_report)
            
        click.echo("\n" + "═"*60)
        click.secho(f" SUCCESS: Comprehensive Report saved to {report_filename} ", fg='white', bg='green', bold=True)

    asyncio.run(main_loop())

if __name__ == '__main__':
    run_research()