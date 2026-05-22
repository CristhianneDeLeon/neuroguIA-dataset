# neuroguIA Dataset – Variable Dictionary

## General Description

This document describes the primary variables included in the neuroguIA longitudinal conversational dataset used for socioemotional interaction analysis in neurodivergent support contexts.

The dataset was designed for:
- conversational AI experimentation,
- longitudinal behavioral analysis,
- emotional state detection,
- contextual memory modeling,
- and educational/research reproducibility.

---

# 01. families.csv

| Variable | Type | Description |
|---|---|---|
| family_id | UUID/Text | Unique identifier for each family unit |
| unit_type | Text | Type of support unit (family, individual, caregiver group) |
| caregiver_alias | Text | Anonymized caregiver identifier |
| context_notes | Text | General contextual observations |
| support_network | Text | Description of support environment |
| environment_type | Text | Household or environmental condition |
| created_at | Timestamp | Record creation date |
| updated_at | Timestamp | Record last update |

---

# 02. profiles.csv

| Variable | Type | Description |
|---|---|---|
| profile_id | UUID/Text | Unique participant profile identifier |
| family_id | UUID/Text | Related family identifier |
| profile_alias | Text | Anonymized participant alias |
| neurotype | Text | Neurodivergent profile category |
| age_range | Text | Estimated age range |
| support_level | Text | Functional support level |
| communication_style | Text | Communication characteristics |
| sensory_profile | Text | Sensory regulation profile |
| created_at | Timestamp | Creation date |
| updated_at | Timestamp | Last modification date |

---

# 03. ng_case_memory.csv

| Variable | Type | Description |
|---|---|---|
| case_id | UUID/Text | Conversational memory case identifier |
| family_id | UUID/Text | Linked family identifier |
| profile_id | UUID/Text | Linked participant profile |
| detected_category | Text | Main detected conversational category |
| detected_stage | Text | Conversation stage classification |
| primary_state | Text | Main emotional state |
| secondary_states | JSON/Text | Additional emotional states |
| emotional_intensity | Float | Estimated emotional intensity |
| caregiver_capacity | Float | Estimated caregiver functional capacity |
| suggested_strategy | Text | Recommended intervention strategy |
| suggested_microaction | Text | Suggested micro-support action |
| response_mode | Text | Conversational response style |
| created_at | Timestamp | Memory creation timestamp |

---

# 04. learned_patterns.csv

| Variable | Type | Description |
|---|---|---|
| pattern_id | UUID/Text | Learned interaction pattern identifier |
| category | Text | Pattern category |
| trigger_context | Text | Contextual trigger detected |
| response_effectiveness | Float | Estimated response effectiveness |
| reinforcement_score | Float | Adaptive learning reinforcement score |
| created_at | Timestamp | Pattern registration date |

---

# 05. response_memory.csv

| Variable | Type | Description |
|---|---|---|
| response_id | UUID/Text | Stored response identifier |
| response_text | Text | Generated or curated response |
| reuse_score | Float | Reusability confidence score |
| category | Text | Associated category |
| validation_status | Text | Validation state |
| created_at | Timestamp | Response creation timestamp |

---

# 06. routines.csv

| Variable | Type | Description |
|---|---|---|
| routine_id | UUID/Text | Routine identifier |
| profile_id | UUID/Text | Linked profile |
| routine_type | Text | Type of routine |
| routine_goal | Text | Intended support objective |
| sensory_support | Text | Sensory regulation assistance |
| executive_support | Text | Executive function assistance |
| created_at | Timestamp | Creation date |

---

# 07. user_context_memory.csv

| Variable | Type | Description |
|---|---|---|
| context_id | UUID/Text | Context memory identifier |
| profile_id | UUID/Text | Linked profile |
| memory_summary | Text | Condensed contextual memory |
| relevance_score | Float | Importance estimation |
| retrieval_frequency | Integer | Retrieval count |
| created_at | Timestamp | Creation date |

---

# 08. conversation_curation.csv

| Variable | Type | Description |
|---|---|---|
| conversation_id | UUID/Text | Curated conversation identifier |
| category | Text | Main conversational category |
| validation_score | Float | Validation confidence |
| reviewed_flag | Boolean | Human-reviewed flag |
| created_at | Timestamp | Registration timestamp |

---

# 09. conversation_messages_supplemental.csv

| Variable | Type | Description |
|---|---|---|
| message_id | UUID/Text | Message identifier |
| profile_id | UUID/Text | Linked participant profile |
| sender_type | Text | User/system sender type |
| message_text | Text | Conversational message |
| detected_intent | Text | NLP-detected intent |
| detected_state | Text | Emotional state |
| semantic_score | Float | Semantic similarity score |
| created_at | Timestamp | Message timestamp |

---

# Validation Files

## category_distribution.csv
Distribution of conversational categories detected across the dataset.

## state_distribution.csv
Distribution of emotional states and conversational conditions.

## validation_report_conversation_messages.csv
Validation report for conversational message integrity and preprocessing consistency.