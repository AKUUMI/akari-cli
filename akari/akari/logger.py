import json
from datetime import datetime
from pathlib import Path

LOG_PATH = Path.home() / ".config" / "akari" / "akari.log"

def _escribir(nivel, mensaje):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    entrada = {
        "fecha": datetime.now().isoformat(),
        "nivel": nivel,
        "mensaje": mensaje,
    }
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entrada, ensure_ascii=False) + "\n")

def info(msg):
    _escribir("INFO", msg)

def error(msg):
    _escribir("ERROR", msg)

def reproduccion(titulo, episodio, fuente, servidor):
    _escribir("REPRODUCCION", f"{titulo} ep.{episodio} | {fuente} | {servidor}")

def busqueda(query, resultados):
    _escribir("BUSQUEDA", f"'{query}' → {resultados} resultados")

def leer_log(limite=50):
    if not LOG_PATH.exists():
        return []
    entradas = []
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entradas.append(json.loads(line))
                except Exception:
                    pass
    return entradas[-limite:]
