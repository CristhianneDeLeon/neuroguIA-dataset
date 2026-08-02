#!/usr/bin/env python3
"""Valida los CSV canónicos de neuroguIA sin modificar su contenido."""

from __future__ import annotations

import csv
import json
import re
import sys
import uuid
from collections import Counter
from datetime import datetime
from pathlib import Path


BASE = Path(__file__).resolve().parent

EXPECTED_ROWS = {
    "01_app_meta.csv": 6,
    "02_ng_families.csv": 281,
    "03_ng_profiles.csv": 619,
    "04_ng_case_memory.csv": 6463,
    "05_conversation_messages_supplemental.csv": 47670,
    "06_ng_messages.csv": 47670,
    "07_ng_response_memory.csv": 465,
    "08_ng_routines.csv": 1468,
    "09_ng_user_context_memory.csv": 562,
    "10_ng_learned_patterns.csv": 1885,
    "11_ng_conversation_curation.csv": 6463,
    "12_research_participants.csv": 562,
    "13_research_prepost.csv": 562,
    "14_research_whoqol_items.csv": 562,
    "15_research_instruments.csv": 8,
    "16_research_instrument_items.csv": 92,
    "17_research_analysis_results.csv": 152,
    "18_research_provenance.csv": 20,
    "19_research_transformations.csv": 10,
}

PRIMARY_KEYS = {
    "01_app_meta.csv": ("meta_key",),
    "02_ng_families.csv": ("family_id",),
    "03_ng_profiles.csv": ("profile_id",),
    "04_ng_case_memory.csv": ("case_id",),
    "05_conversation_messages_supplemental.csv": ("message_id",),
    "07_ng_response_memory.csv": ("response_id",),
    "08_ng_routines.csv": ("routine_id",),
    "09_ng_user_context_memory.csv": ("scope_key",),
    "10_ng_learned_patterns.csv": ("pattern_id",),
    "11_ng_conversation_curation.csv": ("curation_id",),
    "12_research_participants.csv": ("participant_id",),
    "13_research_prepost.csv": ("participant_id",),
    "14_research_whoqol_items.csv": ("participant_id",),
    "15_research_instruments.csv": ("instrument_id",),
    "16_research_instrument_items.csv": ("instrument_id", "item_code"),
    "18_research_provenance.csv": ("source_file",),
    "19_research_transformations.csv": ("step_id",),
}

JSON_COLUMNS = {
    "01_app_meta.csv": {"meta_value"},
    "03_ng_profiles.csv": {
        "conditions", "strengths", "triggers", "early_signs",
        "helpful_strategies", "harmful_strategies", "sensory_needs",
        "emotional_needs",
    },
    "04_ng_case_memory.csv": {
        "secondary_states", "helps_patterns", "worsens_patterns", "tags",
    },
    "07_ng_response_memory.csv": {
        "conditions_signature", "response_structure_json", "avoid_rules",
        "must_include", "supporting_patterns", "tags",
    },
    "08_ng_routines.csv": {
        "steps", "short_version", "adjustments", "indicators",
    },
    "09_ng_user_context_memory.csv": {
        "conversation_preferences_json", "recurrent_topics_json",
        "recurrent_signals_json", "helpful_strategies_json",
        "helpful_routines_json", "summary_snapshot_json",
    },
    "10_ng_learned_patterns.csv": {"helps", "worsens"},
    "11_ng_conversation_curation.csv": {
        "candidate_targets_json", "input_summary_json",
        "secondary_states_json", "signal_summary_json",
        "response_structure_json", "metadata_json",
    },
    "14_research_whoqol_items.csv": {"payload"},
}

UUID_COLUMNS = {
    "02_ng_families.csv": {"family_id"},
    "03_ng_profiles.csv": {"profile_id", "family_id"},
    "04_ng_case_memory.csv": {"case_id", "family_id", "profile_id"},
    "05_conversation_messages_supplemental.csv": {
        "message_id", "case_id", "family_id", "profile_id",
    },
    "06_ng_messages.csv": {"profile_id", "family_id"},
    "07_ng_response_memory.csv": {
        "response_id", "family_id", "profile_id", "origin_case_id",
    },
    "08_ng_routines.csv": {
        "routine_id", "family_id", "profile_id", "source_case_id",
    },
    "09_ng_user_context_memory.csv": {
        "family_id", "profile_id", "source_case_id",
    },
    "10_ng_learned_patterns.csv": {"pattern_id", "family_id", "profile_id"},
    "11_ng_conversation_curation.csv": {
        "family_id", "profile_id", "source_case_id",
    },
}

BOOLEAN_COLUMNS = {
    "03_ng_profiles.csv": {"is_active"},
    "04_ng_case_memory.csv": {
        "applied_successfully", "followup_needed",
    },
    "07_ng_response_memory.csv": {"approved_for_reuse", "is_active"},
    "08_ng_routines.csv": {"is_active"},
    "11_ng_conversation_curation.csv": {
        "used_stub_fallback", "llm_enabled", "llm_approved",
    },
    "16_research_instrument_items.csv": {"reverse_scored"},
}

TIMESTAMP_COLUMNS = {
    "01_app_meta.csv": {"created_at", "updated_at"},
    "02_ng_families.csv": {"created_at", "updated_at"},
    "03_ng_profiles.csv": {"created_at", "updated_at"},
    "04_ng_case_memory.csv": {"created_at", "updated_at"},
    "05_conversation_messages_supplemental.csv": {"created_at"},
    "06_ng_messages.csv": {"created_at"},
    "07_ng_response_memory.csv": {"created_at", "updated_at"},
    "08_ng_routines.csv": {"created_at", "updated_at"},
    "09_ng_user_context_memory.csv": {"created_at", "updated_at"},
    "10_ng_learned_patterns.csv": {"last_seen", "created_at", "updated_at"},
    "11_ng_conversation_curation.csv": {"created_at", "updated_at"},
}


def load_csv(filename: str) -> list[dict[str, str]]:
    with (BASE / filename).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def is_timestamp(value: str) -> bool:
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def validate() -> tuple[list[str], list[str], dict[str, int]]:
    errors: list[str] = []
    warnings: list[str] = []
    data: dict[str, list[dict[str, str]]] = {}
    counts: dict[str, int] = {}

    for filename, expected in EXPECTED_ROWS.items():
        path = BASE / filename
        if not path.exists():
            errors.append(f"Falta el archivo {filename}.")
            continue
        try:
            rows = load_csv(filename)
        except Exception as exc:
            errors.append(f"No se pudo leer {filename}: {exc}")
            continue

        data[filename] = rows
        counts[filename] = len(rows)
        if len(rows) != expected:
            errors.append(
                f"{filename}: se esperaban {expected} filas y se encontraron {len(rows)}."
            )

        key_columns = PRIMARY_KEYS.get(filename)
        if key_columns:
            keys = [tuple(row.get(col, "") for col in key_columns) for row in rows]
            empty = sum(any(not part for part in key) for key in keys)
            duplicate_count = sum(n - 1 for n in Counter(keys).values() if n > 1)
            if empty:
                errors.append(f"{filename}: {empty} claves primarias incompletas.")
            if duplicate_count:
                errors.append(f"{filename}: {duplicate_count} claves primarias duplicadas.")

        for row_number, row in enumerate(rows, start=2):
            for column in JSON_COLUMNS.get(filename, set()):
                value = row.get(column, "")
                if not value:
                    continue
                try:
                    json.loads(value)
                except json.JSONDecodeError as exc:
                    errors.append(
                        f"{filename}:{row_number} JSON inválido en {column}: {exc.msg}."
                    )

            for column in UUID_COLUMNS.get(filename, set()):
                value = row.get(column, "")
                if not value:
                    continue
                try:
                    uuid.UUID(value)
                except ValueError:
                    errors.append(
                        f"{filename}:{row_number} UUID inválido en {column}."
                    )

            for column in BOOLEAN_COLUMNS.get(filename, set()):
                value = row.get(column, "")
                if value and value.lower() not in {"true", "false", "t", "f", "1", "0"}:
                    errors.append(
                        f"{filename}:{row_number} booleano inválido en {column}: {value!r}."
                    )

            for column in TIMESTAMP_COLUMNS.get(filename, set()):
                value = row.get(column, "")
                if value and not is_timestamp(value):
                    errors.append(
                        f"{filename}:{row_number} fecha inválida en {column}: {value!r}."
                    )

    if errors:
        return errors, warnings, counts

    families = {r["family_id"] for r in data["02_ng_families.csv"]}
    profiles = {r["profile_id"] for r in data["03_ng_profiles.csv"]}
    cases = {r["case_id"] for r in data["04_ng_case_memory.csv"]}
    participants = {r["participant_id"] for r in data["12_research_participants.csv"]}
    instruments = {r["instrument_id"] for r in data["15_research_instruments.csv"]}

    foreign_keys = [
        ("03_ng_profiles.csv", "family_id", families),
        ("04_ng_case_memory.csv", "family_id", families),
        ("04_ng_case_memory.csv", "profile_id", profiles),
        ("05_conversation_messages_supplemental.csv", "case_id", cases),
        ("05_conversation_messages_supplemental.csv", "family_id", families),
        ("05_conversation_messages_supplemental.csv", "profile_id", profiles),
        ("06_ng_messages.csv", "family_id", families),
        ("06_ng_messages.csv", "profile_id", profiles),
        ("07_ng_response_memory.csv", "family_id", families),
        ("07_ng_response_memory.csv", "profile_id", profiles),
        ("07_ng_response_memory.csv", "origin_case_id", cases),
        ("08_ng_routines.csv", "family_id", families),
        ("08_ng_routines.csv", "profile_id", profiles),
        ("08_ng_routines.csv", "source_case_id", cases),
        ("09_ng_user_context_memory.csv", "family_id", families),
        ("09_ng_user_context_memory.csv", "profile_id", profiles),
        ("09_ng_user_context_memory.csv", "source_case_id", cases),
        ("10_ng_learned_patterns.csv", "family_id", families),
        ("10_ng_learned_patterns.csv", "profile_id", profiles),
        ("11_ng_conversation_curation.csv", "family_id", families),
        ("11_ng_conversation_curation.csv", "profile_id", profiles),
        ("11_ng_conversation_curation.csv", "source_case_id", cases),
        ("13_research_prepost.csv", "participant_id", participants),
        ("16_research_instrument_items.csv", "instrument_id", instruments),
    ]

    for filename, column, parent_values in foreign_keys:
        missing = [
            row[column]
            for row in data[filename]
            if row.get(column) and row[column] not in parent_values
        ]
        if missing:
            errors.append(
                f"{filename}: {len(missing)} valores de {column} no tienen registro padre."
            )

    groups = Counter(r["group_type"] for r in data["12_research_participants.csv"])
    if groups != Counter({"Experimental": 281, "Control": 281}):
        errors.append(f"Distribución de grupos inesperada: {dict(groups)}.")

    speakers = Counter(
        r["speaker"] for r in data["05_conversation_messages_supplemental.csv"]
    )
    if set(speakers) - {"user", "assistant"}:
        errors.append(f"Valores de speaker no admitidos: {dict(speakers)}.")
    if speakers["user"] != 23835 or speakers["assistant"] != 23835:
        warnings.append(f"Distribución de speaker distinta de la esperada: {dict(speakers)}.")

    profile_rows = data["03_ng_profiles.csv"]
    profile_by_id = {row["profile_id"]: row for row in profile_rows}
    aliases = [row["alias"].strip().casefold() for row in profile_rows]
    if any(not alias for alias in aliases):
        errors.append("ng_profiles: existen alias vacíos.")
    duplicate_aliases = {
        alias: count for alias, count in Counter(aliases).items() if count > 1
    }
    if duplicate_aliases:
        errors.append(
            f"ng_profiles: alias repetidos sin distinguir mayúsculas: {duplicate_aliases}."
        )

    caregiver_aliases = [
        row["caregiver_alias"].strip().casefold()
        for row in data["02_ng_families.csv"]
    ]
    duplicate_caregivers = {
        alias: count
        for alias, count in Counter(caregiver_aliases).items()
        if count > 1
    }
    if duplicate_caregivers:
        errors.append(
            "ng_families: caregiver_alias repetidos sin distinguir "
            f"mayúsculas: {duplicate_caregivers}."
        )

    child_roles = {"adolescente", "hijo", "hija"}
    for row in profile_rows:
        if row["role"] in child_roles and not row["school_profile"].strip():
            errors.append(
                f"ng_profiles: el perfil infantil {row['profile_id']} "
                "no tiene school_profile."
            )

    for row in data["09_ng_user_context_memory.csv"]:
        valid_scope = (
            row["scope_type"] == "family" and not row["profile_id"].strip()
        ) or (
            row["scope_type"] == "profile" and bool(row["profile_id"].strip())
        )
        if not valid_scope:
            errors.append(
                f"ng_user_context_memory: alcance incoherente en {row['scope_key']}."
            )

    for row in data["13_research_prepost.csv"]:
        usage_fields = [
            row["reported_sessions"].strip(),
            row["reported_total_duration_min"].strip(),
            row["reported_mean_session_duration_min"].strip(),
        ]
        if row["group_type"] == "Experimental" and not all(usage_fields):
            errors.append(
                f"research_prepost: faltan métricas de uso para {row['participant_id']}."
            )
        if row["group_type"] == "Control" and any(usage_fields):
            errors.append(
                f"research_prepost: el control {row['participant_id']} "
                "no debe tener métricas de exposición."
            )

    item_counts = Counter(
        row["instrument_id"]
        for row in data["16_research_instrument_items.csv"]
    )
    for row in data["15_research_instruments.csv"]:
        expected_items = int(float(row["items_or_fields"]))
        if item_counts[row["instrument_id"]] != expected_items:
            errors.append(
                f"{row['instrument_id']}: se documentaron "
                f"{item_counts[row['instrument_id']]} campos y se declararon "
                f"{expected_items}."
            )

    placeholder_pattern = re.compile(
        r"(?<![\wÁÉÍÓÚÜÑáéíóúüñ])"
        r"(Iker|Mateo|Diego|Ximena|Valeria|Bruno|Santiago|Damián|"
        r"Camila|Renata|Gael|Samuel|Regina|Paula|Luna)"
        r"(?![\wÁÉÍÓÚÜÑáéíóúüñ])"
    )
    text_checks = {
        "04_ng_case_memory.csv": ["raw_input"],
        "05_conversation_messages_supplemental.csv": ["message_text"],
        "06_ng_messages.csv": ["message"],
        "11_ng_conversation_curation.csv": [
            "input_summary_json",
            "metadata_json",
        ],
    }
    for filename, fields in text_checks.items():
        for row in data[filename]:
            alias = profile_by_id[row["profile_id"]]["alias"]
            for field in fields:
                value = row[field]
                if placeholder_pattern.search(value) and alias not in value:
                    errors.append(
                        f"{filename}: mención nominal distinta al alias del "
                        f"perfil {row['profile_id']} en {field}."
                    )
                    break

    required_meta = {
        "schema_version",
        "created_by",
        "data_provenance",
        "canonical_source_policy",
        "profile_alias_policy",
        "null_semantics_policy",
    }
    meta_keys = {row["meta_key"] for row in data["01_app_meta.csv"]}
    if meta_keys != required_meta:
        errors.append(f"app_meta: claves inesperadas o faltantes: {sorted(meta_keys)}.")

    return errors, warnings, counts


def main() -> int:
    errors, warnings, counts = validate()

    print("VALIDACIÓN PREVIA DE CSV — neuroguIA")
    print("=" * 48)
    for filename in EXPECTED_ROWS:
        status = counts.get(filename, "NO LEÍDO")
        print(f"{filename}: {status}")

    print()
    if warnings:
        print("ADVERTENCIAS")
        for item in warnings:
            print(f"- {item}")
        print()

    if errors:
        print("RESULTADO: NO APTO PARA CARGA")
        for item in errors:
            print(f"- {item}")
        return 1

    print("RESULTADO: APTO PARA CARGA")
    print("- 19 archivos presentes.")
    print("- Conteos esperados confirmados.")
    print("- Claves primarias sin duplicados.")
    print("- Relaciones principales sin registros huérfanos.")
    print("- JSON, UUID, booleanos y fechas con formato válido.")
    print("- Alias de perfiles y cuidadores únicos.")
    print("- Menciones nominales alineadas por profile_id.")
    print("- Nulos no aplicables e instrumentos completos verificados.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
