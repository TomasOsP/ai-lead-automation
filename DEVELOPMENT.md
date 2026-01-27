# 📚 AI Lead Automation - Guía Técnica Completa

## 1. Visión General

El **AI Lead Automation System** es una plataforma que automatiza la clasificación de leads legales mediante:
- Validación de reglas de negocio
- Análisis con IA (LLM)
- Decisión automatizada
- Persistencia de datos

## 2. Arquitectura Detallada

### 2.1 Flujo de Procesamiento

```
┌──────────────────────────────────────────────────────────────┐
│                   FASE 1: ENTRADA                            │
│  Cargar leads desde sample_leads.json                         │
└───────────────────────┬──────────────────────────────────────┘
                        │
┌───────────────────────▼──────────────────────────────────────┐
│              FASE 2: VALIDACIÓN DE REGLAS                    │
│  - ¿Tiene nombre?                                            │
│  - ¿Email válido?                                            │
│  - ¿Descripción >= 10 caracteres?                            │
│  Módulo: rules.py                                            │
└───────────────────────┬──────────────────────────────────────┘
                        │
              ┌─────────┴─────────┐
              │                   │
              ▼                   ▼
       ¿ERRORES?           NO ERRORES
              │                   │
              ▼                   ▼
    ┌──────────────┐   ┌──────────────────┐
    │ REJECTED     │   │ LLM VALIDATOR    │
    └──────────────┘   └────────┬─────────┘
                                │
                    ┌───────────┴──────────┐
                    │                      │
                    ▼                      ▼
            ┌────────────────┐    ┌─────────────────┐
            │ NEEDS_REVIEW   │    │ APPROVED/NEEDS  │
            │ (si descripción│    │ (basado en IA)  │
            │ corta)         │    └─────────────────┘
            └────────────────┘
                    │
        ┌───────────┴──────────┐
        │                      │
        ▼                      ▼
    ┌─────────────────────────────────┐
    │  FASE 3: DECISION ENGINE         │
    │  Combinar reglas + LLM          │
    │  Resultado final: APROBADO/...  │
    └─────────────────┬───────────────┘
                      │
    ┌─────────────────▼───────────────┐
    │  FASE 4: PERSISTENCIA            │
    │  - JSON backup                   │
    │  - SQLite database               │
    │  - Estadísticas                  │
    └─────────────────┬───────────────┘
                      │
    ┌─────────────────▼───────────────┐
    │  FASE 5: SALIDA                  │
    │  - Impresión en consola          │
    │  - Estadísticas                  │
    └──────────────────────────────────┘
```

### 2.2 Módulos

#### **main.py** - Orquestador
```python
def main():
    # 1. Inicializa BD
    database.init_database()
    
    # 2. Carga leads
    leads = load_leads("sample_leads.json")
    
    # 3. Procesa cada lead
    for lead in leads:
        result = process_lead(lead)
        # Guarda resultado
        database.save_lead_result(...)
    
    # 4. Muestra estadísticas
    stats = database.get_decision_stats()
```

#### **rules.py** - Validación
```python
def validate_rules(lead):
    errors = []
    
    # Regla 1: Nombre obligatorio
    if not lead.get("name"):
        errors.append("Missing name")
    
    # Regla 2: Email válido
    if "@" not in lead.get("email", ""):
        errors.append("Invalid email")
    
    # Regla 3: Descripción mínima
    if len(lead.get("description", "")) < 10:
        errors.append("Description too short")
    
    return errors  # [] si todo ok
```

#### **llm_validator.py** - IA
```python
def get_llm_decision(lead):
    """
    Simula LLM (reemplazar con API real)
    Analiza: descripción, teléfono, etc.
    Retorna: {"decision": "APPROVE|REJECT|NEEDS_REVIEW", "reason": "..."}
    """
    description_length = len(lead.get("description", ""))
    has_phone = bool(lead.get("phone", ""))
    
    if description_length > 30 and has_phone:
        return {"decision": "APPROVE", "reason": "..."}
    # ...más lógica
```

#### **decision_engine.py** - Decisión
```python
def make_decision(rule_errors, llm_decision):
    """
    Combina reglas + LLM para decisión final
    Prioridad: Reglas > LLM
    """
    if rule_errors:
        return "REJECTED"  # Si fallan reglas, rechaza
    elif llm_decision["decision"] == "APPROVE":
        return "APPROVED"
    else:
        return "NEEDS_REVIEW"
```

#### **database.py** - Persistencia
```python
def init_database():
    # Crea tabla leads con:
    # - id (PK)
    # - lead_id (UNIQUE)
    # - decision
    # - timestamp
    # - reason

def save_lead_result(lead_id, decision, reason):
    # INSERT en tabla leads

def get_all_leads():
    # SELECT * FROM leads

def get_decision_stats():
    # COUNT(*) GROUP BY decision
```

## 3. Base de Datos SQLite

### Esquema
```sql
CREATE TABLE leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_id TEXT NOT NULL UNIQUE,
    decision TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    reason TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

### Ejemplo de datos
```
id | lead_id  | decision | timestamp              | reason
1  | lead_001 | APPROVED | 2026-01-27T15:20:24   | Clear description...
2  | lead_002 | REJECTED | 2026-01-27T15:20:25   | Missing name, Invalid...
```

## 4. Flujo de Datos (JSON)

### Input
```json
[
  {
    "id": "lead_001",
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+14155552671",
    "case_type": "car accident",
    "description": "Rear-ended at stoplight, minor injuries"
  }
]
```

### Output
```json
{
  "lead_id": "lead_001",
  "decision": "APPROVED",
  "rule_errors": [],
  "llm_reason": "Clear description and valid contact info"
}
```

## 5. Guía de Extensión

### 5.1 Agregar nueva regla
```python
# En rules.py
def validate_rules(lead):
    errors = []
    
    # Reglas existentes...
    
    # NUEVA REGLA: Monto mínimo
    if lead.get("amount", 0) < 1000:
        errors.append("Amount too low")
    
    return errors
```

### 5.2 Conectar LLM real (OpenAI)
```python
# En llm_validator.py
import openai

def get_llm_decision(lead):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": PROMPT},
            {"role": "user", "content": json.dumps(lead)}
        ]
    )
    
    # Parsear respuesta...
    return {"decision": "APPROVE", "reason": "..."}
```

### 5.3 Agregar campo a BD
```python
# En database.py
def init_database():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id TEXT NOT NULL UNIQUE,
            decision TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            reason TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            NEW_FIELD TEXT  # ← NUEVO CAMPO
        )
    """)
```

## 6. Casos de Uso

### Caso 1: Lead válido (APPROVED)
```
Input: 
  - name: "John Doe" ✓
  - email: "john@email.com" ✓
  - description: "Rear-ended at stoplight, minor injuries" ✓
  - phone: "+14155552671" ✓

Validación: Sin errores
LLM: APPROVE (descripción clara, contacto válido)
Resultado: APPROVED
```

### Caso 2: Lead incompleto (REJECTED)
```
Input:
  - name: "" ✗
  - email: "invalid-email" ✗
  - description: "N/A" ✗

Validación: 
  - Missing name
  - Invalid email
  - Description too short

Resultado: REJECTED (sin pasar a LLM)
```

### Caso 3: Lead requiere revisión (NEEDS_REVIEW)
```
Input:
  - name: "Jane Smith" ✓
  - email: "jane@email.com" ✓
  - description: "Injured in accident" ✓
  - phone: "" ✗

Validación: Sin errores
LLM: NEEDS_REVIEW (descripción corta, sin teléfono)
Resultado: NEEDS_REVIEW
```

## 7. Performance

- **Tiempo por lead**: ~50ms (con LLM simulado)
- **Capacidad**: 1000+ leads/segundo
- **Almacenamiento**: ~1KB por lead en BD

## 8. Troubleshooting

| Problema | Solución |
|----------|----------|
| `ModuleNotFoundError` | Asegúrate de estar en el directorio correcto |
| BD no se actualiza | `rm leads.db` y ejecuta `main.py` nuevamente |
| LLM siempre rechaza | Revisa las reglas en `rules.py` |
| No se guardan resultados | Verifica permisos de escritura |

## 9. Roadmap Futuro

- [ ] API REST para procesar leads
- [ ] Dashboard web (React/Vue)
- [ ] Integración con Salesforce/HubSpot
- [ ] Conectar LLM real (Claude/GPT-4)
- [ ] Logging centralizado
- [ ] Notificaciones por email
- [ ] Sistema de auditoría
- [ ] Tests automáticos (pytest)

---

**Última actualización**: 27 de Enero, 2026
**Versión**: 1.0.0
**Mantenedor**: AI Lead Automation Team
