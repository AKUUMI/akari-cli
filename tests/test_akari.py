import pytest
from akari.historial import init_db, guardar_episodio, obtener_historial, obtener_progreso
from akari.player import detectar_reproductor
import tempfile
import os

# ── Historial ─────────────────────────────────────────────────────────────────

def test_init_db(tmp_path, monkeypatch):
    db_path = tmp_path / "history.db"
    monkeypatch.setattr("akari.historial.DB_PATH", db_path)
    init_db()
    assert db_path.exists()

def test_guardar_y_obtener(tmp_path, monkeypatch):
    db_path = tmp_path / "history.db"
    monkeypatch.setattr("akari.historial.DB_PATH", db_path)
    init_db()
    guardar_episodio("Naruto", "naruto", "AnimeFLV", 5, 220, "SUB Latino")
    hist = obtener_historial()
    assert len(hist) == 1
    assert hist[0]["titulo"] == "Naruto"
    assert hist[0]["episodio"] == 5

def test_progreso(tmp_path, monkeypatch):
    db_path = tmp_path / "history.db"
    monkeypatch.setattr("akari.historial.DB_PATH", db_path)
    init_db()
    guardar_episodio("Bleach", "bleach", "JKAnime", 12, 366)
    progreso = obtener_progreso("bleach", "JKAnime")
    assert progreso is not None
    assert progreso["episodio"] == 12

# ── Player ────────────────────────────────────────────────────────────────────

def test_detectar_reproductor_retorna_string_o_none():
    result = detectar_reproductor()
    assert result is None or isinstance(result, str)
