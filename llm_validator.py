import json

PROMPT = """
You are a QA system for legal leads.

Given the following lead data:
{lead}

Decide if this lead should be APPROVED, REJECTED, or NEEDS_REVIEW.
Explain briefly why.
Return your answer in JSON with fields:
- decision
- reason
"""

def get_llm_decision(lead):
    """
    Simulates LLM validation of lead quality.
    In production, this would call an actual LLM API (OpenAI, Claude, etc.)
    """
    # Simulated LLM response based on lead quality
    description = lead.get("description", "").lower()
    phone = lead.get("phone", "")
    
    # Simple heuristics for demo
    if len(description) > 30 and phone and len(phone) > 5:
        reason = "Clear description and valid contact info"
        return {
            "decision": "APPROVE",
            "reason": reason
        }
    elif len(description) > 10:
        reason = "Adequate description but limited contact details"
        return {
            "decision": "NEEDS_REVIEW",
            "reason": reason
        }
    else:
        reason = "Insufficient information provided"
        return {
            "decision": "REJECT",
            "reason": reason
        }
