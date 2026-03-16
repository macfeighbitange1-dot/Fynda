import os
from mistralai.client import Mistral  # Explicitly import from .client
from dotenv import load_dotenv

load_dotenv()

class ResearchProcessor:
    def __init__(self):
        api_key = os.getenv("MISTRAL_API_KEY")
        # Initialize with the new v2 signature
        self.client = Mistral(api_key=api_key)
        self.model = "mistral-large-latest"

    def extract_claims(self, query: str, context: str):
        safe_context = context[:12000] 

        prompt = f"""
        [SYSTEM]
        You are a Deep Research Intelligence Agent.
        
        [QUERY]
        {query}
        
        [CONTEXT]
        {safe_context}
        
        [TASK]
        Extract 3-5 'Atomic Claims' (specific, verifiable technical facts) from the context.
        Include a Confidence Level (0-1.0) for each.
        
        Format:
        - [Fact] (Confidence: X.X)
        """
        
        try:
            # The v2 method is .chat.complete()
            response = self.client.chat.complete(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Processing Error: {str(e)}"