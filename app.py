import streamlit as st
import asyncio
import os
from core.search import ResearchSearch
from core.processor import ResearchProcessor
from core.synthesizer import ResearchSynthesizer
from utils.scraper import scrape_content
from fpdf import FPDF

# Page Config
st.set_page_config(page_title="Aletheia AI", page_icon="🔍", layout="wide")

# Initialize Agents
search_engine = ResearchSearch()
processor = ResearchProcessor()
synthesizer = ResearchSynthesizer()

def export_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Simple multi-line text handling for PDF
    pdf.multi_cell(0, 10, txt=text.encode('latin-1', 'replace').decode('latin-1'))
    return pdf.output(dest='S').encode('latin-1')

# Sidebar for Config
with st.sidebar:
    st.title("⚙️ Research Settings")
    depth = st.slider("Recursive Depth", 1, 3, 1)
    st.info("Phase 6 Devil's Advocate Protocol is ACTIVE.")

# Main UI
st.title("🔍 Aletheia: Deep Research Engine")
query = st.text_input("Enter your research identity (e.g., 'Next-gen SLM benchmarks 2026'):")

if st.button("Launch Research Agent"):
    if query:
        async def run_gui_research():
            log_area = st.empty()
            
            # --- ROUND 1 ---
            log_area.status("🌐 Querying live web...")
            results = search_engine.execute_search(query)
            
            reports = []
            progress_bar = st.progress(0)
            for i, res in enumerate(results):
                log_area.write(f"Analyzing: {res['url']}")
                content = await scrape_content(res['url'])
                claims = processor.extract_claims(query, content)
                reports.append(f"SOURCE: {res['url']}\n{claims}")
                progress_bar.progress((i + 1) / len(results))

            # --- AGENTIC AUDIT ---
            log_area.status("⚖️ Auditing data consistency...")
            gap_query = synthesizer.check_for_gaps(reports)
            
            if gap_query and "NONE" not in gap_query.upper():
                st.warning(f"Contradiction found. Round 2 Search: {gap_query}")
                new_results = search_engine.execute_search(gap_query)
                for res in new_results[:2]:
                    content = await scrape_content(res['url'])
                    reports.append(processor.extract_claims(gap_query, content))

            # --- CRITIQUE & REFINE (PHASE 6) ---
            log_area.status("🛡️ Running Red-Team Critique...")
            draft = synthesizer.synthesize(query, reports)
            critique = synthesizer.criticize(query, draft)
            
            log_area.status("✨ Finalizing Executive Synthesis...")
            final_report = synthesizer.refine(query, draft, critique)
            
            st.session_state['final_report'] = final_report
            st.success("Research Complete!")

        asyncio.run(run_gui_research())

# Display Result
if 'final_report' in st.session_state:
    st.markdown("---")
    st.header("📋 Final Executive Report")
    st.markdown(st.session_state['final_report'])
    
    # One-Click PDF Export
    pdf_bytes = export_pdf(st.session_state['final_report'])
    st.download_button(
        label="📥 Download Report as PDF",
        data=pdf_bytes,
        file_name="research_report.pdf",
        mime="application/pdf"
    )