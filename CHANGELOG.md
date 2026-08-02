# Changelog

Todas las versiones relevantes del dataset de investigación neuroguIA
se documentan en este archivo.

El proyecto utiliza un esquema de versionado orientado a investigación,
reproducibilidad y preservación académica.

---

## [2.0.0] - 2026-08-01

### Consolidación final del dataset de investigación neuroguIA

Esta versión reúne el paquete público consolidado utilizado para consulta,
reproducibilidad, auditoría y preservación académica.

### Contenido incorporado

- Instrumentos y fuentes metodológicas del estudio.
- Datos estructurados y archivos de importación para Supabase.
- Resultados estadísticos, psicométricos y conversacionales.
- Recursos utilizados por el dashboard científico.
- Diccionario de datos, criterios instrumentales y documentación técnica.
- Scripts de creación, carga, validación, seguridad y recuperación.
- Manifiestos de integridad, procedencia y trazabilidad.
- Conjunto consolidado de 562 participantes, 6,463 sesiones y 47,670 mensajes.

### Organización del repositorio

- `01_INSTRUMENTOS_Y_FUENTES`
- `02_SUPABASE`
- `03_ANALISIS`
- `04_DASHBOARD`
- `05_DOCUMENTACION`

### Seguridad y privacidad

- Datos anonimizados para investigación.
- Exclusión de credenciales, secretos y respaldos internos.
- Conservación de trazabilidad metodológica.
- Validación de archivos destinados a publicación.

---

All notable changes to the **neuroguIA Dataset** project will be documented in this file.

The format is inspired by:
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/)

This project follows a research-oriented versioning strategy.

---

# [1.0.0] - 2026-05-21

## 🎉 Initial Public Research Dataset Release

First structured release of the neuroguIA hybrid conversational AI dataset for neurodivergent socioemotional support research.

---

## ✨ Added

### 📂 Repository Structure

Added organized repository architecture:

- `00_documentacion/`
- `01_supabase_core/`
- `02_mensajes_conversacionales/`
- `03_validacion/`
- `04_backups/`
- `05_exports_produccion/`

---

### 🗄️ Relational Dataset

Added core relational CSV datasets:

- `families.csv`
- `profiles.csv`
- `ng_case_memory.csv`
- `learned_patterns.csv`
- `response_memory.csv`
- `routines.csv`
- `user_context_memory.csv`

---

### 💬 Conversational Datasets

Added conversational and supplemental datasets:

- `conversation_curation.csv`
- `conversation_messages_supplemental.csv`
- `conversation_messages_supplemental_clean.csv`
- `ng_messages_import_from_supplemental.csv`

---

### 📊 Validation Resources

Added validation and analytical resources:

- `category_distribution.csv`
- `state_distribution.csv`
- `validation_report_conversation_messages.csv`

---

### 🧠 Hybrid Conversational Architecture

Integrated hybrid conversational system components:

- TF-IDF classification
- Semantic embeddings
- Contextual memory
- Conversational state analysis
- Longitudinal tracking
- Controlled generative AI
- Hybrid routing logic

---

### 🗄️ PostgreSQL / Supabase Integration

Added:

- relational schema compatibility,
- import-ready CSV structures,
- Supabase-compatible organization,
- and relational workflow documentation.

---

### 🔒 Ethical and Privacy Improvements

Implemented:

- anonymized conversational aliases,
- diversified caregiver names,
- removal of repeated identities,
- contextual anonymization,
- and ethical research-oriented protections.

---

### 📚 Documentation

Added:

- `README.md`
- `VARIABLE_DICTIONARY.md`
- `DATA_SCHEMA.md`
- `CITATION.cff`
- `LICENSE`
- `IMPORT_ORDER.txt`
- `README_IMPORTACION.md`
- `requirements.txt`
- `schema_supabase.sql`

---

### 🖼️ Research Diagrams

Added 4K UHD research diagrams:

- Hybrid architecture
- Relational schema
- Conversational flow
- Dataset statistics

---

## 📊 Dataset Statistics

| Metric | Value |
|---|---|
| Families | 281 |
| Profiles | 619 |
| Conversational Sessions | 6,463 |
| Supplemental Messages | 47,670 |
| Learned Patterns | 1,885 |
| Stored Responses | 465 |
| Routines | 1,468 |
| Emotional States | 9 |
| Conversational Categories | 7 |

---

## 🔬 Research Scope

This release supports research in:

- Conversational AI
- NLP
- Emotional computing
- Hybrid AI architectures
- Neurodivergent support systems
- Longitudinal conversational analytics
- Contextual memory systems

---

## ⚠️ Important Notes

- This dataset is intended exclusively for academic and research purposes.
- The system is non-clinical.
- No real personal identities are included.
- All conversational data was anonymized and diversified.

---

# [Future Releases]

## Planned Features

- Multilingual conversational datasets
- Expanded emotional trajectory tracking
- Reinforcement learning integration
- Real-time conversational analytics
- Additional validation pipelines
- Multimodal contextual memory
- Advanced semantic retrieval experiments

---