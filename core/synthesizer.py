import os
from mistralai.client import Mistral

class ResearchSynthesizer:
    def __init__(self):
        self.client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

    def check_for_gaps(self, reports):
        """
        Phase 4: Agentic Audit
        Analyzes reports for missing data or contradictions before synthesis.
        """
        combined_data = "\n\n".join(reports)
        prompt = f"""
        [DATA]
        {combined_data}
        
        [TASK]
        1. Identify major technical contradictions or missing metrics.
        2. If insufficient, generate ONE highly specific search query to resolve it.
        3. If solid, return only: NONE.
        
        Format:
        QUERY: [The specific search query]
        """
        try:
            response = self.client.chat.complete(
                model="mistral-large-latest",
                messages=[{"role": "user", "content": prompt}]
            )
            content = response.choices[0].message.content
            return content.split("QUERY:")[1].strip().strip('"') if "QUERY:" in content else None
        except:
            return None

    def synthesize(self, query, all_reports):
        """Phase 3: Initial Synthesis"""
        combined_text = "\n".join(all_reports)
        prompt = f"""
        [ROLE] Senior Research Lead.
        [QUERY] {query}
        [RAW DATA] {combined_text}
        [TASK] Provide an 'Executive Synthesis' in Markdown covering Consensus, Contradictions, and Technical Verdict.
        """
        try:
            response = self.client.chat.complete(
                model="mistral-large-latest",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Synthesis Error: {str(e)}"

    def criticize(self, query, report):
        """
        Phase 6: The Devil's Advocate Protocol
        Acts as a skeptical reviewer to find flaws or gaps in the synthesis.
        """
        prompt = f"""
        [ROLE] 
        You are a Skeptical Red-Team Analyst. Your job is to find flaws in this research.
        
        [QUERY]
        {query}
        
        [REPORT TO REVIEW]
        {report}
        
        [CRITIQUE CRITERIA]
        1. Accuracy: Are the technical claims too broad or potentially outdated?
        2. Depth: Is there 'AI fluff' that lacks hard data?
        3. Logic: Does the 'Technical Verdict' actually follow from the data provided?
        
        Return a list of 'REQUIRED AMENDMENTS'. If the report is flawless, return 'APPROVED'.
        """
        try:
            response = self.client.chat.complete(
                model="mistral-large-latest",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Critique Error: {str(e)}"

    def refine(self, query, original_report, critique):
        """
        Phase 6: Final Refinement
        Rewrites the report by merging the draft with the critical feedback.
        """
        prompt = f"""
        [ROLE] Senior Technical Editor (Top 0.1% Genius Output).
        
        [TASK]
        Rewrite the draft report based on the Critique. Address all 'Required Amendments'.
        Ensure the tone is objective, precise, and high-density.
        
        [QUERY] {query}
        [DRAFT] {original_report}
        [CRITIQUE] {critique}
        """
        try:
            response = self.client.chat.complete(
                model="mistral-large-latest",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Refinement Error: {str(e)}"