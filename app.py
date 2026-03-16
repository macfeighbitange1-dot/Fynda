import streamlit as st
import asyncio
import os
from core.search import ResearchSearch
from core.processor import ResearchProcessor
from core.synthesizer import ResearchSynthesizer
from core.memory import ResearchVault
from utils.scraper import scrape_content
from fpdf import FPDF

# Initialize Knowledge Vault and Agents
vault = ResearchVault()
search_engine = ResearchSearch()
processor = ResearchProcessor()
synthesizer = ResearchSynthesizer()

# --- Phase 7: Genius-Level UI Configuration ---
st.set_page_config(page_title="Aletheia AI | Research Lab", page_icon="🔬", layout="wide")

# Inject Custom Addictive Dark Theme CSS
st.markdown("""
    <style>
        .stApp { background-color: #121212; color: #E0E0E0; font-family: 'Inter', sans-serif; }
        [data-testid="stSidebar"] { background-color: #1E1E1E; border-right: 1px solid #333333; }
        h1, h2, h3 { color: #FFFFFF !important; font-weight: 700; letter-spacing: -0.5px; }
        div[data-baseweb="input"] { background-color: #2D2D2D !important; border-radius: 8px !important; border: 1px solid #444444 !important; }
        input { color: #FFFFFF !important; }
        .stButton>button {
            background-color: #008080 !important;
            color: white !important;
            border-radius: 8px !important;
            border: none !important;
            padding: 10px 24px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #00A3A3 !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 163, 163, 0.3);
        }
        .stWarning { background-color: #332B00 !important; color: #FFD700 !important; border-left: 5px solid #FFD700 !important; border-radius: 4px; }
        .stSuccess { background-color: #002B1A !important; color: #00cf91 !important; border-left: 5px solid #00cf91 !important; }
        .critique-box { background-color: #2B0000; color: #FF4B4B; padding: 15px; border-radius: 8px; border: 1px solid #FF4B4B; margin: 10px 0; }
        .log-text { color: #A0A0A0; font-family: 'Courier New', monospace; font-size: 0.9rem; }
    </style>
""", unsafe_allow_html=True)

def export_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    clean_text = text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, txt=clean_text)
    return bytes(pdf.output())

# Sidebar for Config
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=60)
    st.title("Aletheia Lab")
    st.markdown("---")
    depth = st.slider("Recursive Depth", 1, 3, 1)
    st.info("Vault Memory & Red Team Critique are ACTIVE.")

# Main UI
st.title("🔬 Aletheia: Advanced Research Lab")
st.markdown("Enter your research identity. The system will autonomously recall, search, verify, and synthesize intelligence.")

query = st.text_input("", placeholder="e.g., 'Quantitative analysis of SLM performance vs LLM on ARM devices'")
status_container = st.container()

if st.button("Initialize Agentic Research"):
    if query:
        async def run_gui_research():
            with status_container:
                st.markdown("### 📡 Live Research Feed")
                log_area = st.empty()
                progress_bar = st.progress(0)
                
                # --- VAULT RECALL ---
                log_area.markdown("<p class='log-text'>🧠 Consulting the Knowledge Vault...</p>", unsafe_allow_html=True)
                past_knowledge = vault.recall_relevant_past(query)
                reports = []
                if past_knowledge:
                    st.info(f"💡 Found relevant past research in the Vault.")
                    reports.append(past_knowledge)
                
                # --- ROUND 1 ---
                log_area.markdown("<p class='log-text'>🌐 Round 1: Querying live web...</p>", unsafe_allow_html=True)
                results = search_engine.execute_search(query)
                
                for i, res in enumerate(results):
                    log_area.markdown(f"<p class='log-text'>[+] Analyzing: {res['url'][:60]}...</p>", unsafe_allow_html=True)
                    content = await scrape_content(res['url'])
                    claims = processor.extract_claims(query, content)
                    reports.append(f"SOURCE: {res['url']}\n{claims}")
                    progress_bar.progress((i + 1) / len(results))

                # --- PHASE 4: AGENTIC AUDIT ---
                log_area.markdown("<p class='log-text'>⚖️ Running Agentic Audit (Phase 4)...</p>", unsafe_allow_html=True)
                gap_query = synthesizer.check_for_gaps(reports)
                
                if gap_query and "NONE" not in gap_query.upper():
                    st.warning(f"⚠️ Contradiction Detected! Launching Round 2: '{gap_query}'")
                    new_results = search_engine.execute_search(gap_query)
                    for res in new_results[:2]:
                        content = await scrape_content(res['url'])
                        reports.append(processor.extract_claims(gap_query, content))

                # --- PHASE 3 & 6: SYNTHESIS & CRITIQUE ---
                log_area.markdown("<p class='log-text'>✨ Generating Executive Synthesis...</p>", unsafe_allow_html=True)
                draft = synthesizer.synthesize(query, reports)

                log_area.markdown("<p class='log-text'>🛡️ Running Red-Team Critique...</p>", unsafe_allow_html=True)
                critique = synthesizer.criticize(query, draft)
                
                if "APPROVED" not in critique.upper():
                    st.markdown(f"<div class='critique-box'>{critique}</div>", unsafe_allow_html=True)
                    final_report = synthesizer.refine(query, draft, critique)
                else:
                    final_report = draft
                
                # --- VAULT STORAGE ---
                log_area.markdown("<p class='log-text'>💾 Archiving intelligence to Knowledge Vault...</p>", unsafe_allow_html=True)
                vault.store_research(query, final_report)
                
                st.session_state['final_report'] = final_report
                st.success("🎉 Research Protocol Complete!")

        asyncio.run(run_gui_research())

if 'final_report' in st.session_state:
    st.markdown("---")
    st.header("📋 Final Intelligence Report")
    st.markdown(st.session_state['final_report'])
    
    pdf_bytes = export_pdf(st.session_state['final_report'])
    st.download_button(label="📥 Download PDF", data=pdf_bytes, file_name="aletheia_report.pdf", mime="application/pdf")