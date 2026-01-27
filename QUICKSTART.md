# 🚀 QUICK START GUIDE

## Estructura del Proyecto

```
ai-lead-automation/
├── main.py              # 🎯 Punto de entrada - ejecuta todo
├── rules.py             # ✓ Validación de reglas
├── llm_validator.py     # 🤖 Validador LLM simulado
├── decision_engine.py   # ⚙️ Motor de decisión
├── database.py          # 💾 Persistencia SQLite
├── query_database.py    # 📊 Consultar resultados
├── sample_leads.json    # 📋 Datos de prueba
├── README.md            # 📖 Documentación completa
├── .gitignore           # 🚫 Archivos ignorados
└── QUICKSTART.md        # 👈 Este archivo
```

## ⚡ Ejecución Rápida

```bash
# 1. Procesar leads (carga, valida, decide, guarda)
python3 main.py

# 2. Consultar resultados de la BD
python3 query_database.py

# 3. Ver documentación completa
cat README.md
```

## 📂 Archivos de Salida

- `lead_results.json` - Resultados en formato JSON
- `leads.db` - Base de datos SQLite
- `leads_export_example.json` - Exportación de ejemplo

## 🔄 Flujo de Datos

```
sample_leads.json
       ↓
   main.py
       ├→ rules.validate_rules()
       ├→ llm_validator.get_llm_decision()
       ├→ decision_engine.make_decision()
       └→ database.save_lead_result()
       ↓
├─ lead_results.json (JSON backup)
├─ leads.db (SQLite persistent)
└─ Console output (formateado)
```

## 📊 Estructura de Datos

### Input (sample_leads.json)
```json
{
  "id": "lead_001",
  "name": "John Doe",
  "email": "john@email.com",
  "phone": "+14155552671",
  "case_type": "car accident",
  "description": "Rear-ended at stoplight, minor injuries"
}
```

### Output (lead_results.json / leads.db)
```json
{
  "lead_id": "lead_001",
  "decision": "APPROVED",
  "rule_errors": [],
  "llm_reason": "Clear description and valid contact info"
}
```

## 🛠️ Personalización

### Agregar nuevas reglas
Edita `rules.py` y agrega validaciones en `validate_rules()`

### Conectar LLM real
Reemplaza la simulación en `llm_validator.get_llm_decision()` con:
- OpenAI API
- Claude API
- Cualquier otro LLM

### Consultar la BD
```python
from database import get_all_leads, get_decision_stats

leads = get_all_leads()
stats = get_decision_stats()
```

## 📈 Decisiones Posibles

| Decisión | Significado |
|----------|------------|
| APPROVED | Lead válido y de buena calidad |
| REJECTED | Lead inválido (fallan reglas) |
| NEEDS_REVIEW | Lead requiere revisión manual |

## 🐛 Troubleshooting

**Error: "No module named 'database'"**
- Asegúrate de estar en el directorio correcto

**La BD no se actualiza**
- Ejecuta: `rm leads.db` y luego `python3 main.py`

**No se guardan resultados**
- Verifica permisos de escritura en el directorio

---

Para más información, ver [README.md](README.md)
