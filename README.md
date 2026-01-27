# AI Lead Automation System

## 📋 Descripción del Problema

El sistema resuelve el problema de **validación automática y clasificación de leads legales** usando una combinación de:
- **Validación de reglas**: Asegura que los datos básicos sean válidos (nombre, email, descripción)
- **Validación con IA (LLM)**: Analiza la calidad y relevancia del lead
- **Decisión final automatizada**: Clasifica leads como APPROVED, REJECTED o NEEDS_REVIEW

Esto ahorra tiempo manual de revisión y proporciona decisiones consistentes basadas en criterios claros.

---

## 🏗️ Arquitectura

El sistema está compuesto por 5 módulos principales:

```
┌─────────────────────────────────────────┐
│         main.py (Orquestador)           │
│  - Carga leads                          │
│  - Coordina el flujo                    │
│  - Imprime y guarda resultados          │
└────────────┬────────────────────────────┘
             │
    ┌────────┼────────┬──────────────┐
    ▼        ▼        ▼              ▼
┌────────┐┌──────────────┐┌────────────────┐
│ rules  ││llm_validator ││decision_engine│
│ .py    ││.py           ││.py             │
└────────┘└──────────────┘└────────────────┘
    │
    └──────────────┬──────────────────────┐
                   ▼                      ▼
            ┌────────────┐         ┌─────────────────┐
            │ database.py│         │lead_results.json│
            │ (SQLite)   │         │(JSON backup)    │
            └────────────┘         └─────────────────┘
```

### Módulos

| Módulo | Responsabilidad |
|--------|-----------------|
| **main.py** | Orquestador principal, carga leads, coordina el procesamiento |
| **rules.py** | Validaciones de reglas (nombre, email, descripción) |
| **llm_validator.py** | Simulación de validación con LLM para evaluar calidad del lead |
| **decision_engine.py** | Toma decisión final combinando reglas y LLM |
| **database.py** | Persistencia en SQLite con lead_id, decision, timestamp, reason |
| **sample_leads.json** | Datos de prueba con ejemplos de leads válidos e inválidos |

---

## 🚀 Cómo Ejecutar

### Requisitos
- Python 3.7+
- No requiere dependencias externas (usa sqlite3 nativo)

### Pasos

1. **Clonar o acceder al repositorio**
```bash
cd ai-lead-automation
```

2. **Ejecutar el sistema**
```bash
python3 main.py
```

3. **Ver resultados**
   - En pantalla: Salida formateada de cada lead
   - En archivo: `lead_results.json` - Copia de seguridad JSON
   - En base de datos: `leads.db` - Registro persistente SQLite

### Datos de Prueba

Modifica `sample_leads.json` para agregar más leads:

```json
{
  "id": "lead_003",
  "name": "Jane Smith",
  "email": "jane@email.com",
  "phone": "+11234567890",
  "case_type": "personal injury",
  "description": "Car accident with multiple injuries, seeking legal representation"
}
```

---

## 📊 Ejemplo de Output

### Ejecución en Terminal
```
==================================================
AI Lead Automation System
==================================================

Database initialized: leads.db

Loaded 2 leads

--- Lead lead_001 ---
{
  "lead_id": "lead_001",
  "decision": "APPROVED",
  "rule_errors": [],
  "llm_reason": "Clear description and valid contact info"
}

--- Lead lead_002 ---
{
  "lead_id": "lead_002",
  "decision": "REJECTED",
  "rule_errors": [
    "Missing name",
    "Invalid email",
    "Description too short"
  ],
  "llm_reason": ""
}

Results saved to lead_results.json

==================================================
Decision Statistics:
  APPROVED: 1
  REJECTED: 1
==================================================
Processing complete!
==================================================
```

### Archivo `lead_results.json`
```json
[
  {
    "lead_id": "lead_001",
    "decision": "APPROVED",
    "rule_errors": [],
    "llm_reason": "Clear description and valid contact info"
  },
  {
    "lead_id": "lead_002",
    "decision": "REJECTED",
    "rule_errors": [
      "Missing name",
      "Invalid email",
      "Description too short"
    ],
    "llm_reason": ""
  }
]
```

### Base de Datos SQLite (`leads.db`)
```
lead_id   | decision | timestamp                    | reason
----------|----------|------------------------------|------------------------------------------
lead_001  | APPROVED | 2026-01-27T14:23:45.123456  | Clear description and valid contact info
lead_002  | REJECTED | 2026-01-27T14:23:45.234567  | Missing name, Invalid email, ...
```

---

## 🔄 Flujo de Procesamiento

```
Lead (JSON)
    ↓
1. Validar Reglas
    ├─ ¿Tiene nombre? ✓
    ├─ ¿Email válido? ✓
    └─ ¿Descripción suficiente? ✓
    ↓
2. ¿Hay errores de reglas?
    ├─ SÍ → REJECTED
    └─ NO → LLM Validator
        ↓
    3. Evaluar calidad con LLM
        ├─ Buena → APPROVE
        ├─ Aceptable → NEEDS_REVIEW
        └─ Mala → REJECT
        ↓
    4. Decision Engine
        └─ Decisión Final (APPROVED/NEEDS_REVIEW/REJECTED)
            ↓
        5. Guardar
            ├─ lead_results.json
            └─ leads.db (SQLite)
```

---

## 🛠️ Personalización

### Modificar Reglas de Validación
Editar `rules.py`:
```python
def validate_rules(lead):
    errors = []
    
    if not lead.get("name"):
        errors.append("Missing name")
    
    # Agregar más validaciones aquí
    
    return errors
```

### Conectar LLM Real
Reemplazar la simulación en `llm_validator.py` con API real:
```python
def get_llm_decision(lead):
    # Usar OpenAI, Anthropic, etc.
    response = client.messages.create(...)
    return parse_response(response)
```

### Consultar Base de Datos
```python
from database import get_all_leads, get_decision_stats

# Obtener todos los leads
leads = get_all_leads()

# Estadísticas
stats = get_decision_stats()
```

---

## 📈 Próximas Mejoras

- [ ] Integración con API real de LLM (OpenAI/Claude)
- [ ] Dashboard web para visualizar resultados
- [ ] Sistema de logging detallado
- [ ] Configuración externa (settings.json)
- [ ] Validaciones más complejas
- [ ] Manejo de errores mejorado
- [ ] Tests unitarios

---

## 📝 Licencia

Este proyecto es de uso interno para automatización de leads legales.

---

## 👤 Autor

Creado con ❤️ para automatizar la clasificación de leads legales.
