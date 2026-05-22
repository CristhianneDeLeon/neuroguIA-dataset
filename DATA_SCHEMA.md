# neuroguIA Dataset – Data Schema

## Overview

The neuroguIA dataset follows a hybrid relational architecture designed for:
- conversational AI,
- contextual memory persistence,
- longitudinal interaction analysis,
- and NLP experimentation.

The structure was optimized for PostgreSQL/Supabase environments.

---

# Core Relational Structure

```text
families
   │
   ├── profiles
   │      │
   │      ├── ng_case_memory
   │      ├── response_memory
   │      ├── routines
   │      ├── user_context_memory
   │      └── conversation_messages_supplemental