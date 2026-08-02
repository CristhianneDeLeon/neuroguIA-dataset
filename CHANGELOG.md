# Changelog

All notable changes to the **neuroguIA Dataset** project will be documented in this file.

The format is inspired by:
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/)

This project follows a research-oriented versioning strategy focused on
traceability, reproducibility, academic preservation, and responsible data use.

---

# [2.0.0] - 2026-08-01

## ?? Consolidated Research Dataset Release

Final consolidated release of the neuroguIA research dataset used for
academic consultation, reproducibility, auditing, preservation, and
scientific visualization.

This release reorganizes the repository around the complete research
workflow, from instruments and operational data to statistical analysis,
dashboard resources, and methodological documentation.

---

## ? Added

### ?? Consolidated Repository Structure

Added the final research-oriented repository architecture:

- `01_INSTRUMENTOS_Y_FUENTES/`
- `02_SUPABASE/`
- `03_ANALISIS/`
- `04_DASHBOARD/`
- `05_DOCUMENTACION/`

---

### ?? Research Instruments and Sources

Added the instruments and canonical methodological sources used in the study:

- informed consent documentation,
- sociodemographic instrument,
- DASS-21 adapted instrument,
- perceived social support scale,
- technological utility scale,
- neuroguIA pretest instrument,
- neuroguIA posttest instrument,
- pretest-posttest evaluation workbook,
- consolidated master input dataset,
- and WHOQOL-BREF reference workbook.

---

### ??? Supabase Dataset and Migration Resources

Added a complete and ordered Supabase migration package including:

- database diagnostic scripts,
- schema creation scripts,
- import-ready relational CSV files,
- validation scripts,
- dashboard analytical views,
- Row Level Security configuration,
- recovery and verification scripts,
- research participant records,
- research instrument items,
- provenance records,
- and transformation metadata.

The migration workflow includes the ordered loading of 19 CSV files.

---

### ?? Reproducible Research Analysis

Added reproducible analytical outputs for:

- pretest-posttest results,
- psychometric indicators,
- effect sizes,
- ANCOVA results,
- categorical distributions,
- emotional-state distributions,
- weekly and time-band distributions,
- NLP performance metrics,
- confusion matrices,
- relational integrity,
- participant summaries,
- session summaries,
- WHOQOL-BREF dimensions,
- and operational usage analysis.

---

### ?? Scientific Dashboard Resources

Added consolidated resources used by the neuroguIA scientific dashboard:

- dashboard KPI tables,
- conversational category summaries,
- pretest-posttest dashboard data,
- emotional-state summaries,
- time-band distributions,
- weekly distributions,
- and WHOQOL-BREF visual summaries.

---

### ?? Documentation and Traceability

Added documentation for:

- data provenance,
- data dictionary,
- transformation records,
- data-source fingerprints,
- SHA-256 integrity manifests,
- Supabase validation,
- instrument interpretation criteria,
- quality controls,
- and canonical source identification.

---

## ?? Changed

### ?? Repository Architecture

Replaced the previous folder organization with a consolidated structure
aligned with the complete research lifecycle.

Previous structure:

- `00_documentacion/`
- `01_supabase_core/`
- `02_mensajes_conversacionales/`
- `03_validacion/`
- `04_backups/`
- `05_exports_produccion/`

Current structure:

- `01_INSTRUMENTOS_Y_FUENTES/`
- `02_SUPABASE/`
- `03_ANALISIS/`
- `04_DASHBOARD/`
- `05_DOCUMENTACION/`

---

### ?? Main Documentation

Updated `README.md` to identify:

- canonical data sources,
- import-ready Supabase files,
- analytical resources,
- dashboard resources,
- quality-control documentation,
- and the methodological interpretation file for the research instruments.

---

### ?? Citation Metadata

Updated `CITATION.cff` to:

- version `2.0.0`,
- release date `2026-08-01`,
- current repository metadata,
- author identification,
- and academic citation information.

---

## ?? Consolidated Dataset Statistics

| Metric | Value |
|---|---:|
| Research participants | 562 |
| Families / experimental units | 281 |
| Profile aliases | 619 |
| Conversational sessions | 6,463 |
| Conversational messages | 47,670 |
| Learned patterns | 1,885 |
| Stored responses | 465 |
| User contextual memory records | 562 |
| Routines | 1,468 |
| NLP classified records | 1,020 |
| NLP categories | 9 |

---

## ?? Research Components

This release supports research and reproducibility in:

- Conversational Artificial Intelligence
- Natural Language Processing
- Hybrid AI architectures
- Contextual memory systems
- Socioemotional support technologies
- Neurodivergent caregiving contexts
- Longitudinal conversational analytics
- Psychometric evaluation
- Human-centered AI
- Scientific dashboard development

---

## ?? Security and Privacy

This release implements:

- anonymized research identifiers,
- exclusion of passwords and credentials,
- exclusion of local backups and temporary files,
- separation of operational records from the analytical corpus,
- integrity verification through SHA-256 manifests,
- documented provenance,
- methodological traceability,
- and privacy-oriented publication controls.

No Streamlit secrets, Supabase credentials, database connection strings,
or internal Git backup bundles are included in the public repository.

---

## ? Validation

The consolidated package was validated for:

- repository structure,
- canonical source availability,
- CSV loading order,
- relational consistency,
- profile and participant counts,
- session and message counts,
- UTF-8 compatibility,
- absence of publication secrets,
- Git synchronization,
- and reproducible dashboard inputs.

---

## ?? Important Notes

- This dataset is intended for academic and research purposes.
- The system is non-clinical.
- Published records use anonymized or controlled identifiers.
- Operational and analytical values may follow different documented definitions.
- Canonical sources and transformation rules are identified in the repository documentation.

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
