"""Orquestación y estado del lote (spec sección 3; plan.md sección 5, resumibilidad)."""

import json
import os
import uuid
from datetime import datetime, timezone

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

# Orden de pasos por empresa dentro de un lote. El último paso es el de corte.
PASOS = ["descubierta", "auditada", "puntuada", "con_propuesta", "con_borrador"]


def nueva_corrida(mercado: str, pais: str, tamano: str, base_dir: str | None = None) -> str:
    """Crea `data/<lote-id>/` con su `state.json` y devuelve el lote_id."""
    base_dir = base_dir or DATA_DIR
    lote_id = f"{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"
    carpeta = os.path.join(base_dir, lote_id)
    os.makedirs(os.path.join(carpeta, "empresas"), exist_ok=True)
    os.makedirs(os.path.join(carpeta, "capturas"), exist_ok=True)

    estado = {
        "lote_id": lote_id,
        "parametros": {"mercado": mercado, "pais": pais, "tamano": tamano},
        "creado": datetime.now(timezone.utc).isoformat(),
        "empresas": {},  # dominio -> paso actual (uno de PASOS)
    }
    _guardar_state(lote_id, estado, base_dir)
    return lote_id


def guardar_estado(lote_id: str, dominio: str, paso: str, base_dir: str | None = None) -> None:
    """Registra en qué paso quedó una empresa del lote, para poder retomar si se corta."""
    if paso not in PASOS:
        raise ValueError(f"Paso desconocido: {paso!r}. Debe ser uno de {PASOS}.")
    estado = _cargar_state(lote_id, base_dir)
    estado["empresas"][dominio] = paso
    _guardar_state(lote_id, estado, base_dir)


def listar_pendientes(lote_id: str, base_dir: str | None = None) -> list[str]:
    """Dominios del lote que todavía no llegaron al último paso (`con_borrador`)."""
    estado = _cargar_state(lote_id, base_dir)
    ultimo_paso = PASOS[-1]
    return [dominio for dominio, paso in estado["empresas"].items() if paso != ultimo_paso]


def _ruta_carpeta(lote_id: str, base_dir: str | None = None) -> str:
    return os.path.join(base_dir or DATA_DIR, lote_id)


def _ruta_state(lote_id: str, base_dir: str | None = None) -> str:
    return os.path.join(_ruta_carpeta(lote_id, base_dir), "state.json")


def _cargar_state(lote_id: str, base_dir: str | None = None) -> dict:
    with open(_ruta_state(lote_id, base_dir), "r", encoding="utf-8") as f:
        return json.load(f)


def _guardar_state(lote_id: str, estado: dict, base_dir: str | None = None) -> None:
    with open(_ruta_state(lote_id, base_dir), "w", encoding="utf-8") as f:
        json.dump(estado, f, ensure_ascii=False, indent=2)
