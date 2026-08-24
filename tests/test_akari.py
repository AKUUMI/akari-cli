import pytest
from akari.historial import init_db, guardar_episodio, obtener_historial, obtener_progreso
from akari.player import detectar_reproductor, reproducir_y_verificar
from akari.scrapers import buscar_en_todas, _episodios_desde_javascript, _videos_desde_javascript

# ── Historial ─────────────────────────────────────────────────────────────────

def test_init_db(tmp_path, monkeypatch):
    db_path = tmp_path / "history.db"

    monkeypatch.setattr("akari.historial.BASE_DIR", tmp_path)
    monkeypatch.setattr("akari.historial.DB_PATH", db_path)
    
    init_db()
    assert db_path.exists(), "La base de datos no se creó correctamente."

def test_guardar_y_obtener(tmp_path, monkeypatch):
    db_path = tmp_path / "history.db"
    monkeypatch.setattr("akari.historial.BASE_DIR", tmp_path)
    monkeypatch.setattr("akari.historial.DB_PATH", db_path)
    
    init_db()
    
    guardar_episodio("Naruto", "naruto", "AnimeFLV", 5, 220, "SUB Latino", portada=None, minuto=320)
    
    hist = obtener_historial()
    assert len(hist) == 1
    assert hist[0]["titulo"] == "Naruto"
    assert hist[0]["episodio"] == 5
    assert hist[0]["minuto"] == 320, "¡No estás guardando el minuto de reproducción, baka!"

def test_progreso(tmp_path, monkeypatch):
    db_path = tmp_path / "history.db"
    monkeypatch.setattr("akari.historial.BASE_DIR", tmp_path)
    monkeypatch.setattr("akari.historial.DB_PATH", db_path)
    
    init_db()
    guardar_episodio("Bleach", "bleach", "JKAnime", 12, 366, minuto=850)
    
    progreso = obtener_progreso("bleach", "JKAnime")
    assert progreso is not None
    assert progreso["episodio"] == 12
    assert progreso["minuto"] == 850

# ── Player ────────────────────────────────────────────────────────────────────

def test_detectar_reproductor_retorna_string_o_none():
    result = detectar_reproductor()
    assert result is None or isinstance(result, str)

def test_reproducir_devuelve_cuatro_valores_si_falla_ytdlp(monkeypatch):
    monkeypatch.setattr("akari.player.detectar_reproductor", lambda: "mpv")
    monkeypatch.setattr("akari.player.shutil.which", lambda _: "yt-dlp")
    monkeypatch.setattr("akari.player.subprocess.run", lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError()))

    result = reproducir_y_verificar("https://example.com/embed/1")

    assert result == (False, None, 0, False)

def test_busqueda_filtra_navegacion_y_duplicados(monkeypatch):
    resultados = [
        {"titulo": "Notificaciones", "slug": "notificaciones", "fuente": "Prueba"},
        {"titulo": "Naruto", "slug": "naruto", "fuente": "Prueba"},
        {"titulo": "Naruto duplicado", "slug": "naruto", "fuente": "Prueba"},
    ]
    monkeypatch.setattr(
        "akari.scrapers.FUENTES",
        {"Prueba": {"buscar": lambda _: resultados}},
    )

    result = buscar_en_todas("naruto")

    assert [item["titulo"] for item in result] == ["Naruto"]

def test_episodios_desde_javascript_admite_listas_simples_y_pares():
    simples = "var episodes = [3,2,2,1];"
    pares = "var episodes = [[3,30],[2,20],[1,10]];"

    assert _episodios_desde_javascript(simples) == [1, 2, 3]
    assert _episodios_desde_javascript(pares) == [1, 2, 3]

def test_videos_desde_javascript_admite_objetos_y_listas():
    objeto = 'var videos = {"SUB":[{"title":"Uno","code":"https://example.com"}]};'
    lista = 'var videos = [["Uno","https://example.com",0,0]];'

    assert _videos_desde_javascript(objeto)["SUB"][0]["title"] == "Uno"
    assert _videos_desde_javascript(lista)[0][0] == "Uno"
