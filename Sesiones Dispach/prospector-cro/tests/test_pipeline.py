import os

import pytest

from prospector.pipeline import guardar_estado, listar_pendientes, nueva_corrida


def test_nueva_corrida_crea_carpetas_y_state(tmp_path):
    lote_id = nueva_corrida("ecommerce", "Argentina", "11-50", base_dir=str(tmp_path))
    carpeta = tmp_path / lote_id
    assert (carpeta / "state.json").exists()
    assert (carpeta / "empresas").is_dir()
    assert (carpeta / "capturas").is_dir()


def test_guardar_estado_actualiza_el_paso_de_una_empresa(tmp_path):
    lote_id = nueva_corrida("ecommerce", "Argentina", "11-50", base_dir=str(tmp_path))
    guardar_estado(lote_id, "acme.example", "descubierta", base_dir=str(tmp_path))
    guardar_estado(lote_id, "acme.example", "auditada", base_dir=str(tmp_path))

    pendientes = listar_pendientes(lote_id, base_dir=str(tmp_path))
    assert "acme.example" in pendientes  # "auditada" no es el último paso todavía


def test_guardar_estado_paso_invalido_lanza_error(tmp_path):
    lote_id = nueva_corrida("ecommerce", "Argentina", "11-50", base_dir=str(tmp_path))
    with pytest.raises(ValueError):
        guardar_estado(lote_id, "acme.example", "paso_que_no_existe", base_dir=str(tmp_path))


def test_listar_pendientes_excluye_las_que_llegaron_al_ultimo_paso(tmp_path):
    lote_id = nueva_corrida("ecommerce", "Argentina", "11-50", base_dir=str(tmp_path))
    guardar_estado(lote_id, "acme.example", "con_borrador", base_dir=str(tmp_path))
    guardar_estado(lote_id, "otra.example", "puntuada", base_dir=str(tmp_path))

    pendientes = listar_pendientes(lote_id, base_dir=str(tmp_path))
    assert pendientes == ["otra.example"]


def test_lote_se_puede_retomar_leyendo_el_mismo_state(tmp_path):
    """Simula un corte a la mitad: se crea el lote, se guarda progreso parcial,
    y una 'nueva sesión' que solo conoce el lote_id puede seguir desde ahí."""
    lote_id = nueva_corrida("ecommerce", "Argentina", "11-50", base_dir=str(tmp_path))
    guardar_estado(lote_id, "acme.example", "auditada", base_dir=str(tmp_path))

    # "reinicio": nada en memoria, solo el lote_id y la carpeta en disco.
    pendientes_tras_reinicio = listar_pendientes(lote_id, base_dir=str(tmp_path))
    assert pendientes_tras_reinicio == ["acme.example"]
