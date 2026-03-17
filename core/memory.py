import os
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

class ResearchVault:
    def __init__(self):
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index_name = "aletheia-vault"
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Create index if it doesn't exist
        if self.index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=self.index_name,
                dimension=384, # Matches MiniLM dimension
                metric='cosine',
                spec=ServerlessSpec(cloud='aws', region='us-east-1')
            )
        self.index = self.pc.Index(self.index_name)

    def store_research(self, query, content):
        """Shreds and stores research into the vault."""
        vector = self.model.encode(content).tolist()
        self.index.upsert(vectors=[{
            "id": str(hash(content)), 
            "values": vector, 
            "metadata": {"query": query, "text": content[:500]} # Store snippet
        }])

    def recall_relevant_past(self, current_query):
        """Recalls past research related to the new query."""
        query_vector = self.model.encode(current_query).tolist()
        results = self.index.query(vector=query_vector, top_k=2, include_metadata=True)
        
        past_context = ""
        for match in results['matches']:
            past_context += f"\n[Past Research Context]: {match['metadata']['text']}...\n"
        return past_context