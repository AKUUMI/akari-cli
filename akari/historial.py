import sqlite3
import sys
import os
from datetime import datetime
from pathlib import Path

if sys.platform == "win32":
    BASE_DIR = Path(os.environ.get("APPDATA", Path.home())) / "akari"
else:
    BASE_DIR = Path.home() / ".config" / "akari"

DB_PATH = BASE_DIR / "history.db"

def get_connection():
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        c = conn.cursor()
        c.executescript("""
            CREATE TABLE IF NOT EXISTS historial (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                slug TEXT NOT NULL,
                fuente TEXT NOT NULL,
                episodio INTEGER NOT NULL,
                total_episodios INTEGER,
                idioma TEXT,
                fecha TEXT NOT NULL,
                portada TEXT,
                minuto INTEGER DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS favoritos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                slug TEXT NOT NULL,
                fuente TEXT NOT NULL,
                portada TEXT,
                fecha_agregado TEXT NOT NULL
            );
        """)
        try:
            c.execute("ALTER TABLE historial ADD COLUMN minuto INTEGER DEFAULT 0")
        except sqlite3.OperationalError:
            pass

def guardar_episodio(titulo, slug, fuente, episodio, total_episodios=None, idioma=None, portada=None, minuto=0):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM historial WHERE slug=? AND fuente=?", (slug, fuente))
        if c.fetchone():
            c.execute("""
                UPDATE historial SET episodio=?, total_episodios=?, idioma=?, fecha=?, portada=?, minuto=?
                WHERE slug=? AND fuente=?
            """, (episodio, total_episodios, idioma, datetime.now().isoformat(), portada, minuto, slug, fuente))
        else:
            c.execute("""
                INSERT INTO historial (titulo, slug, fuente, episodio, total_episodios, idioma, fecha, portada, minuto)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (titulo, slug, fuente, episodio, total_episodios, idioma, datetime.now().isoformat(), portada, minuto))

def obtener_historial(limite=10):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM historial ORDER BY fecha DESC LIMIT ?", (limite,))
        return [dict(r) for r in c.fetchall()]

def obtener_progreso(slug, fuente):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT episodio, total_episodios, minuto FROM historial WHERE slug=? AND fuente=?", (slug, fuente))
        row = c.fetchone()
        return dict(row) if row else None

def agregar_favorito(titulo, slug, fuente, portada=None):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM favoritos WHERE slug=? AND fuente=?", (slug, fuente))
        if not c.fetchone():
            c.execute("""
                INSERT INTO favoritos (titulo, slug, fuente, portada, fecha_agregado)
                VALUES (?, ?, ?, ?, ?)
            """, (titulo, slug, fuente, portada, datetime.now().isoformat()))
            return True
        return False

def obtener_favoritos():
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM favoritos ORDER BY fecha_agregado DESC")
        return [dict(r) for r in c.fetchall()]

def eliminar_favorito(slug, fuente):
    with get_connection() as conn:
        c = conn.cursor()
        c.execute("DELETE FROM favoritos WHERE slug=? AND fuente=?", (slug, fuente))