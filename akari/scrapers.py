import requests
from bs4 import BeautifulSoup
import re
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

GENEROS = [
    "accion", "aventura", "carreras", "ciencia-ficcion", "comedia",
    "demencia", "demonios", "deportes", "drama", "ecchi", "escolares",
    "espacial", "fantasia", "harem", "historico", "josei", "juegos",
    "magia", "mecha", "militar", "misterio", "musica", "parodia",
    "psicologico", "recuentos-de-la-vida", "romance", "samurai",
    "seinen", "shoujo", "shounen", "sobrenatural", "suspenso",
    "terror", "vampiros", "yaoi", "yuri",
]


def _extraer_json_balanceado(texto, patron_inicio, bracket="{"):
    cierre = "}" if bracket == "{" else "]"
    m = re.search(patron_inicio, texto)
    if not m:
        return None
    pos = m.end()
    while pos < len(texto) and texto[pos] != bracket:
        pos += 1
    if pos >= len(texto):
        return None

    nivel = 0
    start = pos
    en_string = False
    escape_next = False

    for i in range(pos, len(texto)):
        c = texto[i]
        if escape_next:
            escape_next = False
            continue
        if c == "\\" and en_string:
            escape_next = True
            continue
        if c == '"':
            en_string = not en_string
            continue
        if en_string:
            continue
        if c == bracket:
            nivel += 1
        elif c == cierre:
            nivel -= 1
            if nivel == 0:
                return texto[start:i + 1]
    return None


def jkanime_buscar(query):
    url = f"https://jkanime.net/buscar/{query.replace(' ', '_')}/"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        resultados = []
        for item in soup.select("div.anime__item"):
            titulo_tag = item.select_one("div.anime__item__text h5 a")
            img_tag = item.select_one("[data-setbg]")
            tipo_tag = item.select_one("div.anime__item__text ul li.anime")
            if titulo_tag:
                href = titulo_tag.get("href", "")
                slug = href.strip("/").split("/")[-1]
                img_url = img_tag.get("data-setbg") if img_tag else None
                resultados.append({
                    "titulo": titulo_tag.text.strip(),
                    "slug": slug,
                    "url": href if href.startswith("http") else f"https://jkanime.net/{slug}/",
                    "portada": img_url,
                    "tipo": tipo_tag.text.strip() if tipo_tag else "Anime",
                    "fuente": "JKAnime",
                })
        return resultados
    except Exception:
        return []


def jkanime_por_genero(genero, pagina=1):
    url = f"https://jkanime.net/genero/{genero}/page/{pagina}/"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        resultados = []
        for item in soup.select("div.anime__item"):
            titulo_tag = item.select_one("div.anime__item__text h5 a")
            img_tag = item.select_one("[data-setbg]")
            tipo_tag = item.select_one("div.anime__item__text ul li.anime")
            if titulo_tag:
                href = titulo_tag.get("href", "")
                slug = href.strip("/").split("/")[-1]
                resultados.append({
                    "titulo": titulo_tag.text.strip(),
                    "slug": slug,
                    "url": href if href.startswith("http") else f"https://jkanime.net/{slug}/",
                    "portada": img_tag.get("data-setbg") if img_tag else None,
                    "tipo": tipo_tag.text.strip() if tipo_tag else "Anime",
                    "fuente": "JKAnime",
                })
        return resultados
    except Exception:
        return []


def jkanime_info(slug):
    url = f"https://jkanime.net/{slug}/"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        sinopsis_tag = soup.select_one("div.anime__details__text p")
        sinopsis = sinopsis_tag.text.strip() if sinopsis_tag else None

        estado = None
        tipo = None
        anio = None
        generos = []

        for item in soup.select("div.anime__details__widget ul li"):
            texto = item.get_text(" ", strip=True)
            if "Estado:" in texto:
                estado = texto.replace("Estado:", "").strip()
            elif "Tipo:" in texto:
                tipo = texto.replace("Tipo:", "").strip()
            elif "Temporada:" in texto or "Año:" in texto:
                anio = texto.split(":")[-1].strip()

        for g in soup.select("div.anime__details__widget a[href*='/genero/']"):
            generos.append(g.text.strip())

        portada_tag = soup.select_one("div.anime__details__pic")
        portada = portada_tag.get("data-setbg") if portada_tag else None

        return {
            "sinopsis": sinopsis,
            "estado": estado,
            "tipo": tipo,
            "anio": anio,
            "generos": generos,
            "portada": portada,
        }
    except Exception:
        return {}


def jkanime_get_anime_id(slug):
    url = f"https://jkanime.net/{slug}/"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        for pattern in [r"ajax/episodes/(\d+)/", r"ajax/search_episode/(\d+)/"]:
            m = re.search(pattern, r.text)
            if m:
                return m.group(1)
        return None
    except Exception:
        return None


def jkanime_episodios(slug):
    anime_id = jkanime_get_anime_id(slug)
    if not anime_id:
        return []
    try:
        session = requests.Session()
        r = session.get(f"https://jkanime.net/{slug}/", headers=HEADERS, timeout=10)

        m = re.search(r'<meta name="csrf-token"\s+content="([^"]+)"', r.text)
        csrf_token = m.group(1) if m else ""

        episodios = []
        pag = 1
        while True:
            ajax_url = f"https://jkanime.net/ajax/episodes/{anime_id}/{pag}"
            resp = session.post(ajax_url, headers={
                **HEADERS,
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRF-TOKEN": csrf_token,
                "Referer": f"https://jkanime.net/{slug}/",
            }, timeout=10)

            data = resp.json()
            items = data.get("data", [])
            if not items:
                break
            for item in items:
                num = item.get("number")
                if num is not None:
                    episodios.append(int(num))
            if not data.get("next_page_url"):
                break
            pag += 1

        return sorted(set(episodios))
    except Exception:
        return []


def jkanime_extraer_stream(iframe_url):
    try:
        r = requests.get(iframe_url, headers={
            **HEADERS,
            "Referer": "https://jkanime.net/",
        }, timeout=10)
        m = re.search(r'(https?://[^\s"\'<>]+\.m3u8[^\s"\'<>]*)', r.text)
        if m:
            return m.group(1)
        m = re.search(r'file\s*:\s*["\'](\s*https?://[^"\']+)["\']', r.text)
        if m:
            return m.group(1).strip()
        return None
    except Exception:
        return None


def jkanime_get_video_url(slug, episodio):
    url = f"https://jkanime.net/{slug}/{episodio}/"
    try:
        r = requests.get(url, headers={
            **HEADERS,
            "Referer": "https://jkanime.net/",
            "Accept-Language": "es-MX,es;q=0.8",
        }, timeout=10)

        iframes = re.findall(
            r"video\[\d+\]\s*=\s*'<iframe[^>]+src=\"(https://jkanime\.net/jkplayer/[^\"]+)\"",
            r.text
        )

        nombres = ["JKPlayer 1", "JKPlayer 2", "JKPlayer 3", "JKPlayer 4"]
        servidores = []
        for i, src in enumerate(iframes):
            src = src.strip()
            if not src:
                continue
            stream_url = jkanime_extraer_stream(src)
            url_final = stream_url if stream_url else src
            servidores.append({
                "servidor": nombres[i] if i < len(nombres) else f"Servidor {i + 1}",
                "url": url_final,
                "idioma": "SUB Latino",
                "lang_key": "SUB",
                "es_stream": stream_url is not None,
            })
        return servidores
    except Exception:
        return []


FUENTES = {
    "JKAnime": {
        "buscar": jkanime_buscar,
        "episodios": jkanime_episodios,
        "video": jkanime_get_video_url,
    },
}


def buscar_en_todas(query):
    resultados = []
    for fuente in FUENTES.values():
        resultados += fuente["buscar"](query)
    return resultados


def obtener_episodios(slug, fuente):
    fn = FUENTES.get(fuente, {}).get("episodios", lambda s: [])
    return fn(slug)


def obtener_video(slug, episodio, fuente):
    fn = FUENTES.get(fuente, {}).get("video", lambda s, e: [])
    return fn(slug, episodio)
