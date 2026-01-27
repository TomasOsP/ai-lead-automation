import json
import llm_validator
import decision_engine
import rules
import database
from datetime import datetime

def process_lead(lead):
    """
    Complete lead processing pipeline:
    1. Validate against rules
    2. Call LLM validator if no rule errors
    3. Make final decision
    4. Return structured result
    """
    # Step 1: Validate lead against rules
    rule_errors = rules.validate_rules(lead)
    
    # Step 2: Get LLM decision if no rule errors
    llm_decision = None
    llm_reason = ""
    if not rule_errors:
        llm_decision = llm_validator.get_llm_decision(lead)
        llm_reason = llm_decision.get("reason", "")
    
    # Step 3: Make final decision
    final_decision = decision_engine.make_decision(rule_errors, llm_decision)
    
    # Step 4: Build result
    result = {
        "lead_id": lead.get("id"),
        "decision": final_decision,
        "rule_errors": rule_errors,
        "llm_reason": llm_reason
    }
    
    return result

def load_leads(filename="sample_leads.json"):
    """
    Load leads from JSON file.
    """
    try:
        with open(filename, "r") as f:
            leads = json.load(f)
        return leads
    except FileNotFoundError:
        print(f"Error: {filename} not found")
        return []

def save_results(results, filename="lead_results.json"):
    """
    Save processing results to JSON file.
    """
    with open(filename, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {filename}")

def main():
    """
    Main execution pipeline.
    """
    print("=" * 50)
    print("AI Lead Automation System")
    print("=" * 50)
    
    # Initialize database
    database.init_database()
    
    # Load leads
    leads = load_leads()
    if not leads:
        print("No leads to process")
        return
    
    print(f"\nLoaded {len(leads)} leads")
    
    # Process all leads
    results = []
    for lead in leads:
        result = process_lead(lead)
        results.append(result)
        
        # Print result
        print(f"\n--- Lead {result['lead_id']} ---")
        print(json.dumps(result, indent=2))
        
        # Save to database
        reason = result.get("llm_reason") or ", ".join(result.get("rule_errors", []))
        database.save_lead_result(result["lead_id"], result["decision"], reason)
    
    # Save results to JSON
    save_results(results)
    
    # Show database statistics
    stats = database.get_decision_stats()
    print("\n" + "=" * 50)
    print("Decision Statistics:")
    for decision, count in stats.items():
        print(f"  {decision}: {count}")
    print("=" * 50)
    print("Processing complete!")
    print("=" * 50)

if __name__ == "__main__":
    main()
