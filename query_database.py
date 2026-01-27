#!/usr/bin/env python3
"""
Ejemplo de uso del módulo database para consultar resultados.
"""

import database
from datetime import datetime

def main():
    print("\n" + "=" * 60)
    print("AI Lead Automation - Database Query Examples")
    print("=" * 60)
    
    # Ejemplo 1: Obtener todos los leads
    print("\n1. TODOS LOS LEADS:")
    print("-" * 60)
    leads = database.get_all_leads()
    for lead_id, decision, timestamp, reason in leads:
        print(f"  Lead ID: {lead_id}")
        print(f"  Decision: {decision}")
        print(f"  Timestamp: {timestamp}")
        print(f"  Reason: {reason}")
        print()
    
    # Ejemplo 2: Estadísticas de decisiones
    print("2. ESTADÍSTICAS:")
    print("-" * 60)
    stats = database.get_decision_stats()
    total = sum(stats.values())
    for decision, count in stats.items():
        percentage = (count / total * 100) if total > 0 else 0
        print(f"  {decision}: {count} ({percentage:.1f}%)")
    print(f"  TOTAL: {total}")
    
    # Ejemplo 3: Buscar lead específico
    print("\n3. BUSCAR LEAD ESPECÍFICO:")
    print("-" * 60)
    lead_id = "lead_001"
    result = database.get_lead_by_id(lead_id)
    if result:
        lead_id, decision, timestamp, reason = result
        print(f"  Lead: {lead_id}")
        print(f"  Decision: {decision}")
        print(f"  Timestamp: {timestamp}")
        print(f"  Reason: {reason}")
    else:
        print(f"  Lead {lead_id} not found")
    
    # Ejemplo 4: Exportar a JSON
    print("\n4. EXPORTAR RESULTADOS:")
    print("-" * 60)
    database.export_to_json("leads_export_example.json")
    print("  ✓ Exportado a leads_export_example.json")
    
    print("\n" + "=" * 60)
    print("¡Consultas completadas!")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
