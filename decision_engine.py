def make_decision(rule_errors, llm_decision):
    """
    Combines rule validation and LLM decision to make final decision.
    """
    if rule_errors:
        decision = "REJECTED"
    elif llm_decision and llm_decision.get("decision") == "APPROVE":
        decision = "APPROVED"
    else:
        decision = "NEEDS_REVIEW"
    
    return decision
