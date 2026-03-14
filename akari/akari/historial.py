import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path.home() / ".config" / "akari" / "history.db"

def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
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
    # Migrar DB antigua que no tenga columna minuto
    try:
        c.execute("ALTER TABLE historial ADD COLUMN minuto INTEGER DEFAULT 0")
        conn.commit()
    except Exception:
        pass
    conn.commit()
    conn.close()

def guardar_episodio(titulo, slug, fuente, episodio, total_episodios=None, idioma=None, portada=None, minuto=0):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id FROM historial WHERE slug=? AND fuente=?", (slug, fuente))
    row = c.fetchone()
    if row:
        c.execute("""
            UPDATE historial SET episodio=?, total_episodios=?, idioma=?, fecha=?, portada=?, minuto=?
            WHERE slug=? AND fuente=?
        """, (episodio, total_episodios, idioma, datetime.now().isoformat(), portada, minuto, slug, fuente))
    else:
        c.execute("""
            INSERT INTO historial (titulo, slug, fuente, episodio, total_episodios, idioma, fecha, portada, minuto)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (titulo, slug, fuente, episodio, total_episodios, idioma, datetime.now().isoformat(), portada, minuto))
    conn.commit()
    conn.close()

def obtener_historial(limite=10):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM historial ORDER BY fecha DESC LIMIT ?", (limite,))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def obtener_progreso(slug, fuente):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT episodio, total_episodios, minuto FROM historial WHERE slug=? AND fuente=?", (slug, fuente))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def agregar_favorito(titulo, slug, fuente, portada=None):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id FROM favoritos WHERE slug=? AND fuente=?", (slug, fuente))
    if not c.fetchone():
        c.execute("""
            INSERT INTO favoritos (titulo, slug, fuente, portada, fecha_agregado)
            VALUES (?, ?, ?, ?, ?)
        """, (titulo, slug, fuente, portada, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def obtener_favoritos():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM favoritos ORDER BY fecha_agregado DESC")
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def eliminar_favorito(slug, fuente):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM favoritos WHERE slug=? AND fuente=?", (slug, fuente))
    conn.commit()
    conn.close()
