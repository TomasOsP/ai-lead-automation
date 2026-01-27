import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_FILE = "leads.db"

def init_database():
    """
    Initialize SQLite database with leads table.
    Creates table if it doesn't exist.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id TEXT NOT NULL UNIQUE,
            decision TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            reason TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()
    print(f"Database initialized: {DB_FILE}")

def save_lead_result(lead_id, decision, reason=""):
    """
    Save lead processing result to database.
    
    Args:
        lead_id: Unique lead identifier
        decision: APPROVED, REJECTED, or NEEDS_REVIEW
        reason: LLM reason or rule errors
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    timestamp = datetime.now().isoformat()
    
    try:
        cursor.execute("""
            INSERT INTO leads (lead_id, decision, timestamp, reason)
            VALUES (?, ?, ?, ?)
        """, (lead_id, decision, timestamp, reason))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print(f"Warning: Lead {lead_id} already exists in database")
        return False
    finally:
        conn.close()

def get_lead_by_id(lead_id):
    """
    Retrieve lead record by ID.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT lead_id, decision, timestamp, reason FROM leads WHERE lead_id = ?", (lead_id,))
    result = cursor.fetchone()
    conn.close()
    
    return result

def get_all_leads():
    """
    Retrieve all leads from database.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT lead_id, decision, timestamp, reason FROM leads ORDER BY created_at DESC")
    results = cursor.fetchall()
    conn.close()
    
    return results

def get_decision_stats():
    """
    Get statistics of decisions.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT decision, COUNT(*) as count 
        FROM leads 
        GROUP BY decision
    """)
    results = cursor.fetchall()
    conn.close()
    
    stats = {}
    for decision, count in results:
        stats[decision] = count
    
    return stats

def delete_all_leads():
    """
    Delete all leads from database (for testing/reset).
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM leads")
    conn.commit()
    conn.close()
    print("All leads deleted from database")

def export_to_json(filename="leads_export.json"):
    """
    Export all leads to JSON file.
    """
    leads = get_all_leads()
    
    data = []
    for lead_id, decision, timestamp, reason in leads:
        data.append({
            "lead_id": lead_id,
            "decision": decision,
            "timestamp": timestamp,
            "reason": reason
        })
    
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"Leads exported to {filename}")
