# core/router.py

def route_query(query: str):
    """
    Determines if the research requires the Sovereign (Kenyan) Node 
    or the General Web Node.
    """
    # Expanded 2026-specific Kenyan high-intent keywords
    kenyan_silo_keywords = [
        "kenya", "nairobi", "westlands", "nse", "sacco", "kra", "cbk", 
        "etims", "shif", "nssf", "kesonia", "hustle fund", "magistrate", 
        "gazette", "m-pesa", "equity bank", "kcb", "safaricom"
    ]
    
    query_lower = query.lower()
    
    # Check if any keyword exists as a standalone word to avoid false positives
    is_kenyan = any(f" {word} " in f" {query_lower} " for word in kenyan_silo_keywords)
    
    if is_kenyan:
        return "SOVEREIGN_NODE"
    
    return "GENERAL_WEB"