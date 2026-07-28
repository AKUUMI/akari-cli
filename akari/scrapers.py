import requests
import re
import json
import concurrent.futures

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept-Language": "es-MX,es;q=0.9,en;q=0.8",
}

URL_JKANIME = "https://jkanime.net"
URL_ANIMEFLV = "https://www4.animeflv.net"
URL_TIOANIME = "https://tioanime.com"
URL_ANIMEFENIX = "https://animefenix.tv"
URL_ANIMEID = "https://www.animeid.tv"
URL_MONOSCHINOS = "https://monoschinos2.com"

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

def _safe_get(url, extra_headers=None, timeout=15):
    try:
        h = {**HEADERS}
        if extra_headers:
            h.update(extra_headers)
        r = requests.get(url, headers=h, timeout=timeout)
        r.raise_for_status()
        return r
    except Exception:
        return None

def _slugify(texto):
    return re.sub(r'[^\w\s-]', '', texto).strip().replace(' ', '-').lower()

def jkanime_buscar(query):
    from urllib.parse import quote
    url = f"{URL_JKANIME}/buscar/{quote(query.strip())}"
    r = _safe_get(url)
    if not r:
        return []
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, "html.parser")
        ignorar = {
            "directorio", "horario", "comunidad", "top", "estrenos",
            "aplicacion", "historial", "guardado", "dash", "buscar",
            "categoria", "genero", "temporada", "usuario", "salir",
        }
        vistos = set()
        resultados = []
        for a in soup.select(f'a[href^="{URL_JKANIME}/"], a[href^="/"]'):
            href = a.get("href", "")
            if href.startswith("/"):
                href = URL_JKANIME + href
            m = re.match(rf'^{re.escape(URL_JKANIME)}/([a-z0-9][a-z0-9\-]*)/?$', href)
            if not m:
                continue
            slug = m.group(1)
            if slug in ignorar or slug in vistos:
                continue
            titulo = a.get_text(strip=True)
            if not titulo:
                continue
            vistos.add(slug)
            img_tag = a.select_one("img") or (a.parent.select_one("img") if a.parent else None)
            portada = None
            if img_tag:
                portada = img_tag.get("src") or img_tag.get("data-src")
            resultados.append({
                "titulo": titulo,
                "slug": slug,
                "url": f"{URL_JKANIME}/{slug}/",
                "portada": portada,
                "tipo": "Anime",
                "fuente": "JKAnime",
            })
        return resultados
    except Exception:
        return []

def jkanime_por_genero(genero, pagina=1):
    url = f"{URL_JKANIME}/genero/{genero}/page/{pagina}/"
    r = _safe_get(url)
    if not r:
        return []
    try:
        from bs4 import BeautifulSoup
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
                    "url": href if href.startswith("http") else f"{URL_JKANIME}/{slug}/",
                    "portada": img_tag.get("data-setbg") if img_tag else None,
                    "tipo": tipo_tag.text.strip() if tipo_tag else "Anime",
                    "fuente": "JKAnime",
                })
        return resultados
    except Exception:
        return []

def jkanime_info(slug):
    url = f"{URL_JKANIME}/{slug}/"
    r = _safe_get(url)
    if not r:
        return {}
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, "html.parser")
        texto = soup.get_text(" ", strip=True)

        def campo(nombre):
            m = re.search(
                rf'{nombre}:\s*([^:]+?)(?=\s+(?:Tipo|Generos|Studios|Temporada|Idiomas|Episodios|Duracion|Emitido|Estado|Calidad):|$)',
                texto,
            )
            return m.group(1).strip() if m else None

        tipo = campo("Tipo")
        estado = campo("Estado")
        anio = campo("Temporada")

        ep_m = re.search(r'Episodios:\s*(\d+)', texto)
        episodios_totales = int(ep_m.group(1)) if ep_m else None

        generos = [g.get_text(strip=True) for g in soup.select('a[href*="/genero/"]')]

        sinopsis = None
        meta = soup.select_one('meta[name="description"]')
        if meta and meta.get("content"):
            sinopsis = meta.get("content").strip()

        img_tag = soup.select_one('img[src*="/animes/image/"]')
        portada = img_tag.get("src") if img_tag else None

        return {
            "sinopsis": sinopsis,
            "estado": estado,
            "tipo": tipo,
            "anio": anio,
            "generos": generos,
            "portada": portada,
            "episodios_totales": episodios_totales,
        }
    except Exception:
        return {}

def jkanime_get_anime_id(slug):
    url = f"{URL_JKANIME}/{slug}/"
    r = _safe_get(url)
    if not r:
        return None
    try:
        for pattern in [r"ajax/episodes/(\d+)/", r"ajax/search_episode/(\d+)/"]:
            m = re.search(pattern, r.text)
            if m:
                return m.group(1)
        return None
    except Exception:
        return None

def jkanime_episodios(slug):
    """Devuelve la lista de números de episodio disponibles (1..N),
    igual que el resto de fuentes. Antes esta función devolvía por error
    una URL de stream en vez de la lista de episodios."""
    url = f"{URL_JKANIME}/{slug}/"
    r = _safe_get(url)
    if not r:
        return []
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, "html.parser")
        texto = soup.get_text(" ", strip=True)
        m = re.search(r'Episodios:\s*(\d+)', texto)
        if not m:
            # fallback: contar links de tipo /slug/N/
            nums = set()
            for a in soup.select(f'a[href*="/{slug}/"]'):
                href = a.get("href", "")
                m2 = re.search(rf'/{re.escape(slug)}/(\d+)/?$', href)
                if m2:
                    nums.add(int(m2.group(1)))
            return sorted(nums)
        total = int(m.group(1))
        return list(range(1, total + 1))
    except Exception:
        return []

def jkanime_extraer_stream(url_iframe):
    r = _safe_get(url_iframe, extra_headers={"Referer": f"{URL_JKANIME}/"})
    if not r:
        return None
    try:
        m = re.search(r'["\'](https?://[^"\']+\.m3u8[^"\']*)["\']', r.text)
        if m:
            return m.group(1)
        m = re.search(r'["\']?file["\']?\s*[:=]\s*["\'](https?://[^"\']+)["\']', r.text)
        if m:
            return m.group(1)
        return None
    except Exception:
        return None

def jkanime_get_video_url(slug, episodio):
    url = f"{URL_JKANIME}/{slug}/{episodio}/"
    r = _safe_get(url, extra_headers={
        "Referer": f"{URL_JKANIME}/",
        "Accept-Language": "es-MX,es;q=0.8",
    })
    if not r:
        return []
    try:
        iframes = re.findall(
            r"video\[\d+\]\s*=\s*'[^']*src=\"(https://jkanime\.net/jkplayer/[^\"]+)\"",
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

def animeflv_buscar(query):
    url = f"{URL_ANIMEFLV}/browse?q={query.replace(' ', '+')}"
    r = _safe_get(url)
    if not r:
        return []
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, "html.parser")
        resultados = []
        for item in soup.select("ul.ListAnimes li"):
            title_tag = item.select_one("h3.Title")
            img_tag = item.select_one("img")
            link_tag = item.select_one("a")
            type_tag = item.select_one("span.Type")
            if title_tag and link_tag:
                href = link_tag.get("href", "")
                slug = href.strip("/").split("/")[-1] if href else ""
                resultados.append({
                    "titulo": title_tag.text.strip(),
                    "slug": slug,
                    "url": f"{URL_ANIMEFLV}{href}" if href.startswith("/") else href,
                    "portada": img_tag.get("src") if img_tag else None,
                    "tipo": type_tag.text.strip() if type_tag else "Anime",
                    "fuente": "AnimeFLV",
                })
        return resultados
    except Exception:
        return []

def animeflv_info(slug):
    url = f"{URL_ANIMEFLV}/anime/{slug}"
    r = _safe_get(url)
    if not r:
        return {}
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, "html.parser")
        sinopsis_tag = soup.select_one("div.Description p")
        sinopsis = sinopsis_tag.text.strip() if sinopsis_tag else None
        estado = None
        tipo = None
        generos = []
        for item in soup.select("nav.NvCnAB span"):
            texto = item.text.strip()
            if texto in ["En emisión", "Finalizado", "Próximamente"]:
                estado = texto
            elif texto in ["Anime", "OVA", "Especial", "Película"]:
                tipo = texto
        for g in soup.select("nav.NvCnAB a[href*='/browse?genre=']"):
            generos.append(g.text.strip())
        portada_tag = soup.select_one("figure img")
        portada = portada_tag.get("src") if portada_tag else None
        return {
            "sinopsis": sinopsis,
            "estado": estado,
            "tipo": tipo,
            "anio": None,
            "generos": generos,
            "portada": portada,
        }
    except Exception:
        return {}

def animeflv_episodios(slug):
    url = f"{URL_ANIMEFLV}/anime/{slug}"
    r = _safe_get(url)
    if not r:
        return []
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, "html.parser")
        episodios = []
        for ep in soup.select("ul.ListCaps li a"):
            ep_num = ep.get("href", "").split("-")[-1]
            if ep_num.isdigit():
                episodios.append(int(ep_num))
        return sorted(set(episodios)) if episodios else []
    except Exception:
        return []

def animeflv_get_video_url(slug, episodio):
    url = f"{URL_ANIMEFLV}/ver/{slug}-{episodio}"
    r = _safe_get(url, extra_headers={"Referer": f"{URL_ANIMEFLV}/"})
    if not r:
        return []
    try:
        servidores = []
        server_matches = re.findall(
            r'<button[^>]*data-server="([^"]*)"[^>]*>([^<]*)</button>',
            r.text
        )
        for server_url, server_name in server_matches:
            if server_url:
                servidores.append({
                    "servidor": server_name.strip() or "Servidor",
                    "url": server_url,
                    "idioma": "SUB Latino",
                    "lang_key": "SUB",
                    "es_stream": ".m3u8" in server_url,
                })
        scripts = re.findall(r'<script[^>]*>(.*?)</script>', r.text, re.DOTALL)
        for script in scripts:
            embeds = re.findall(r'["\'](https?://[^"\']+(?:embed|player|stream)[^"\']*)["\']', script)
            for embed in embeds:
                if not any(s["url"] == embed for s in servidores):
                    servidores.append({
                        "servidor": "Embed",
                        "url": embed,
                        "idioma": "SUB Latino",
                        "lang_key": "SUB",
                        "es_stream": ".m3u8" in embed,
                    })
        return servidores
    except Exception:
        return []

def tioanime_buscar(query):
    url = f"{URL_TIOANIME}/directorio?q={query.replace(' ', '+')}"
    r = _safe_get(url)
    if not r:
        return []
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, "html.parser")
        resultados = []
        for item in soup.select("article.anime"):
            title_tag = item.select_one("h3.title")
            img_tag = item.select_one("img")
            link_tag = item.select_one("a")
            type_tag = item.select_one("span.type")
            if title_tag and link_tag:
                href = link_tag.get("href", "")
                slug = href.strip("/").split("/")[-1] if href else ""
                resultados.append({
                    "titulo": title_tag.text.strip(),
                    "slug": slug,
                    "url": f"{URL_TIOANIME}{href}" if href.startswith("/") else href,
                    "portada": img_tag.get("src") if img_tag else None,
                    "tipo": type_tag.text.strip() if type_tag else "Anime",
                    "fuente": "TioAnime",
                })
        return resultados
    except Exception:
        return []

def tioanime_info(slug):
    url = f"{URL_TIOANIME}/anime/{slug}"
    r = _safe_get(url)
    if not r:
        return {}
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, "html.parser")
        sinopsis_tag = soup.select_one("p.sinopsis")
        sinopsis = sinopsis_tag.text.strip() if sinopsis_tag else None
        estado = None
        tipo = None
        generos = []
        for item in soup.select("span.status"):
            texto = item.text.strip()
            if texto in ["En emisión", "Finalizado"]:
                estado = texto
        for item in soup.select("span.type"):
            texto = item.text.strip()
            if texto:
                tipo = texto
        for g in soup.select("a[href*='/directorio?genero=']"):
            generos.append(g.text.strip())
        portada_tag = soup.select_one("img.anime-img")
        portada = portada_tag.get("src") if portada_tag else None
        return {
            "sinopsis": sinopsis,
            "estado": estado,
            "tipo": tipo,
            "anio": None,
            "generos": generos,
            "portada": portada,
        }
    except Exception:
        return {}

def tioanime_episodios(slug):
    url = f"{URL_TIOANIME}/anime/{slug}"
    r = _safe_get(url)
    if not r:
        return []
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, "html.parser")
        episodios = []
        for ep in soup.select("ul.episodes li a"):
            ep_num = ep.get("href", "").split("-")[-1]
            if ep_num.isdigit():
                episodios.append(int(ep_num))
        return sorted(set(episodios)) if episodios else []
    except Exception:
        return []

def tioanime_get_video_url(slug, episodio):
    url = f"{URL_TIOANIME}/ver/{slug}-{episodio}"
    r = _safe_get(url, extra_headers={"Referer": f"{URL_TIOANIME}/"})
    if not r:
        return []
    try:
        servidores = []
        iframe_matches = re.findall(
            r'<iframe[^>]*src=["\']([^"\']+)["\'][^>]*>',
            r.text
        )
        for i, iframe_url in enumerate(iframe_matches):
            servidores.append({
                "servidor": f"Servidor {i + 1}",
                "url": iframe_url,
                "idioma": "SUB Latino",
                "lang_key": "SUB",
                "es_stream": ".m3u8" in iframe_url,
            })
        scripts = re.findall(r'<script[^>]*>(.*?)</script>', r.text, re.DOTALL)
        for script in scripts:
            urls = re.findall(r'["\'](https?://[^"\']+(?:stream|video|player)[^"\']*)["\']', script)
            for url in urls:
                if not any(s["url"] == url for s in servidores):
                    servidores.append({
                        "servidor": "Stream",
                        "url": url,
                        "idioma": "SUB Latino",
                        "lang_key": "SUB",
                        "es_stream": ".m3u8" in url,
                    })
        return servidores
    except Exception:
        return []

def animefenix_buscar(query):
    url = f"{URL_ANIMEFENIX}/animes?q={query.replace(' ', '+')}"
    r = _safe_get(url)
    if not r:
        return []
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, "html.parser")
        resultados = []
        for item in soup.select("article.serie-card"):
            title_tag = item.select_one("h3.serie-title a, h2 a")
            img_tag = item.select_one("img")
            link_tag = item.select_one("a")
            if title_tag and link_tag:
                href = link_tag.get("href", "")
                slug = href.strip("/").split("/")[-1] if href else ""
                resultados.append({
                    "titulo": title_tag.text.strip(),
                    "slug": slug,
                    "url": href if href.startswith("http") else f"{URL_ANIMEFENIX}{href}",
                    "portada": img_tag.get("src") if img_tag else None,
                    "tipo": "Anime",
                    "fuente": "AnimeFenix",
                })
        return resultados
    except Exception:
        return []

def animefenix_info(slug):
    url = f"{URL_ANIMEFENIX}/anime/{slug}"
    r = _safe_get(url)
    if not r:
        return {}
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, "html.parser")
        sinopsis_tag = soup.select_one("div.sinopsis p, div.description p")
        sinopsis = sinopsis_tag.text.strip() if sinopsis_tag else None
        estado = None
        tipo = None
        generos = []
        for item in soup.select("span.status, div.status"):
            texto = item.text.strip()
            if texto in ["En emisión", "Finalizado", "Emisión"]:
                estado = texto
        for g in soup.select("a[href*='/genero/'], a[href*='/genre/']"):
            generos.append(g.text.strip())
        portada_tag = soup.select_one("figure.poster img, div.poster img")
        portada = portada_tag.get("src") if portada_tag else None
        return {
            "sinopsis": sinopsis,
            "estado": estado,
            "tipo": tipo,
            "anio": None,
            "generos": generos,
            "portada": portada,
        }
    except Exception:
        return {}

def animefenix_episodios(slug):
    url = f"{URL_ANIMEFENIX}/anime/{slug}"
    r = _safe_get(url)
    if not r:
        return []
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, "html.parser")
        episodios = []
        for ep in soup.select("ul.episode-list li a, div.episodes a"):
            ep_num = ep.get_text(strip=True)
            if ep_num.isdigit():
                episodios.append(int(ep_num))
            else:
                m = re.search(r'(\d+)', ep_num)
                if m:
                    episodios.append(int(m.group(1)))
        return sorted(set(episodios)) if episodios else []
    except Exception:
        return []

def animefenix_get_video_url(slug, episodio):
    url = f"{URL_ANIMEFENIX}/ver/{slug}-{episodio}"
    r = _safe_get(url, extra_headers={"Referer": f"{URL_ANIMEFENIX}/"})
    if not r:
        return []
    try:
        servidores = []
        iframe_matches = re.findall(
            r'<iframe[^>]*src=["\']([^"\']+)["\'][^>]*>',
            r.text
        )
        for i, iframe_url in enumerate(iframe_matches):
            servidores.append({
                "servidor": f"Servidor {i + 1}",
                "url": iframe_url,
                "idioma": "SUB/DUB Latino",
                "lang_key": "MIX",
                "es_stream": ".m3u8" in iframe_url,
            })
        server_matches = re.findall(
            r'data-url=["\']([^"\']+)["\'][^>]*>([^<]*)</(?:button|a)>',
            r.text
        )
        for server_url, server_name in server_matches:
            if server_url and not any(s["url"] == server_url for s in servidores):
                servidores.append({
                    "servidor": server_name.strip() or "Servidor",
                    "url": server_url,
                    "idioma": "SUB/DUB Latino",
                    "lang_key": "MIX",
                    "es_stream": ".m3u8" in server_url,
                })
        scripts = re.findall(r'<script[^>]*>(.*?)</script>', r.text, re.DOTALL)
        for script in scripts:
            urls = re.findall(r'["\'](https?://[^"\']+(?:stream|video|player|embed)[^"\']*)["\']', script)
            for url in urls:
                if not any(s["url"] == url for s in servidores):
                    servidores.append({
                        "servidor": "Stream",
                        "url": url,
                        "idioma": "SUB/DUB Latino",
                        "lang_key": "MIX",
                        "es_stream": ".m3u8" in url,
                    })
        return servidores
    except Exception:
        return []

def animeid_buscar(query):
    url = f"{URL_ANIMEID}/buscar?q={query.replace(' ', '+')}"
    r = _safe_get(url)
    if not r:
        return []
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, "html.parser")
        resultados = []
        for item in soup.select("div.anime-item, article.anime"):
            title_tag = item.select_one("h3 a, h2 a, .title a")
            img_tag = item.select_one("img")
            link_tag = item.select_one("a")
            if title_tag and link_tag:
                href = link_tag.get("href", "")
                slug = href.strip("/").split("/")[-1] if href else ""
                resultados.append({
                    "titulo": title_tag.text.strip(),
                    "slug": slug,
                    "url": href if href.startswith("http") else f"{URL_ANIMEID}{href}",
                    "portada": img_tag.get("src") if img_tag else None,
                    "tipo": "Anime",
                    "fuente": "AnimeID",
                })
        return resultados
    except Exception:
        return []

def animeid_info(slug):
    url = f"{URL_ANIMEID}/anime/{slug}"
    r = _safe_get(url)
    if not r:
        return {}
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, "html.parser")
        sinopsis_tag = soup.select_one("div.sinopsis p, div.synopsis p")
        sinopsis = sinopsis_tag.text.strip() if sinopsis_tag else None
        estado = None
        generos = []
        for item in soup.select("span.status, div.status"):
            texto = item.text.strip()
            if texto in ["En emisión", "Finalizado"]:
                estado = texto
        for g in soup.select("a[href*='/genero/']"):
            generos.append(g.text.strip())
        portada_tag = soup.select_one("img.poster, div.poster img")
        portada = portada_tag.get("src") if portada_tag else None
        return {
            "sinopsis": sinopsis,
            "estado": estado,
            "tipo": None,
            "anio": None,
            "generos": generos,
            "portada": portada,
        }
    except Exception:
        return {}

def animeid_episodios(slug):
    url = f"{URL_ANIMEID}/anime/{slug}"
    r = _safe_get(url)
    if not r:
        return []
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, "html.parser")
        episodios = []
        for ep in soup.select("ul.episode-list li a, div.episode a"):
            ep_num = ep.get_text(strip=True)
            if ep_num.isdigit():
                episodios.append(int(ep_num))
            else:
                m = re.search(r'(\d+)', ep_num)
                if m:
                    episodios.append(int(m.group(1)))
        return sorted(set(episodios)) if episodios else []
    except Exception:
        return []

def animeid_get_video_url(slug, episodio):
    url = f"{URL_ANIMEID}/ver/{slug}-{episodio}"
    r = _safe_get(url, extra_headers={"Referer": f"{URL_ANIMEID}/"})
    if not r:
        return []
    try:
        servidores = []
        iframe_matches = re.findall(
            r'<iframe[^>]*src=["\']([^"\']+)["\'][^>]*>',
            r.text
        )
        for i, iframe_url in enumerate(iframe_matches):
            servidores.append({
                "servidor": f"Servidor {i + 1}",
                "url": iframe_url,
                "idioma": "SUB/DUB Latino",
                "lang_key": "MIX",
                "es_stream": ".m3u8" in iframe_url,
            })
        server_matches = re.findall(
            r'data-src=["\']([^"\']+)["\'][^>]*>([^<]*)</(?:button|a)>',
            r.text
        )
        for server_url, server_name in server_matches:
            if server_url and not any(s["url"] == server_url for s in servidores):
                servidores.append({
                    "servidor": server_name.strip() or "Servidor",
                    "url": server_url,
                    "idioma": "SUB/DUB Latino",
                    "lang_key": "MIX",
                    "es_stream": ".m3u8" in server_url,
                })
        scripts = re.findall(r'<script[^>]*>(.*?)</script>', r.text, re.DOTALL)
        for script in scripts:
            urls = re.findall(r'["\'](https?://[^"\']+(?:stream|video|player|embed)[^"\']*)["\']', script)
            for url in urls:
                if not any(s["url"] == url for s in servidores):
                    servidores.append({
                        "servidor": "Stream",
                        "url": url,
                        "idioma": "SUB/DUB Latino",
                        "lang_key": "MIX",
                        "es_stream": ".m3u8" in url,
                    })
        return servidores
    except Exception:
        return []

def monoschinos_buscar(query):
    url = f"{URL_MONOSCHINOS}/buscar?q={query.replace(' ', '+')}"
    r = _safe_get(url)
    if not r:
        return []
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, "html.parser")
        resultados = []
        for item in soup.select("div.anime-item, article.anime, div.serie"):
            title_tag = item.select_one("h3 a, h2 a, .title")
            img_tag = item.select_one("img")
            link_tag = item.select_one("a")
            if title_tag and link_tag:
                href = link_tag.get("href", "")
                slug = href.strip("/").split("/")[-1] if href else ""
                resultados.append({
                    "titulo": title_tag.text.strip(),
                    "slug": slug,
                    "url": href if href.startswith("http") else f"{URL_MONOSCHINOS}{href}",
                    "portada": img_tag.get("src") if img_tag else None,
                    "tipo": "Anime",
                    "fuente": "MonosChinos",
                })
        return resultados
    except Exception:
        return []

def monoschinos_info(slug):
    url = f"{URL_MONOSCHINOS}/anime/{slug}"
    r = _safe_get(url)
    if not r:
        return {}
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, "html.parser")
        sinopsis_tag = soup.select_one("div.sinopsis p, div.description p")
        sinopsis = sinopsis_tag.text.strip() if sinopsis_tag else None
        estado = None
        generos = []
        for item in soup.select("span.status, div.status"):
            texto = item.text.strip()
            if texto in ["En emisión", "Finalizado"]:
                estado = texto
        for g in soup.select("a[href*='/genero/']"):
            generos.append(g.text.strip())
        portada_tag = soup.select_one("img.poster, div.poster img")
        portada = portada_tag.get("src") if portada_tag else None
        return {
            "sinopsis": sinopsis,
            "estado": estado,
            "tipo": None,
            "anio": None,
            "generos": generos,
            "portada": portada,
        }
    except Exception:
        return {}

def monoschinos_episodios(slug):
    url = f"{URL_MONOSCHINOS}/anime/{slug}"
    r = _safe_get(url)
    if not r:
        return []
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, "html.parser")
        episodios = []
        for ep in soup.select("ul.episode-list li a, div.episode a"):
            ep_num = ep.get_text(strip=True)
            if ep_num.isdigit():
                episodios.append(int(ep_num))
            else:
                m = re.search(r'(\d+)', ep_num)
                if m:
                    episodios.append(int(m.group(1)))
        return sorted(set(episodios)) if episodios else []
    except Exception:
        return []

def monoschinos_get_video_url(slug, episodio):
    url = f"{URL_MONOSCHINOS}/ver/{slug}-{episodio}"
    r = _safe_get(url, extra_headers={"Referer": f"{URL_MONOSCHINOS}/"})
    if not r:
        return []
    try:
        servidores = []
        iframe_matches = re.findall(
            r'<iframe[^>]*src=["\']([^"\']+)["\'][^>]*>',
            r.text
        )
        for i, iframe_url in enumerate(iframe_matches):
            servidores.append({
                "servidor": f"Servidor {i + 1}",
                "url": iframe_url,
                "idioma": "DUB Latino",
                "lang_key": "DUB",
                "es_stream": ".m3u8" in iframe_url,
            })
        server_matches = re.findall(
            r'data-url=["\']([^"\']+)["\'][^>]*>([^<]*)</(?:button|a)>',
            r.text
        )
        for server_url, server_name in server_matches:
            if server_url and not any(s["url"] == server_url for s in servidores):
                servidores.append({
                    "servidor": server_name.strip() or "Servidor",
                    "url": server_url,
                    "idioma": "DUB Latino",
                    "lang_key": "DUB",
                    "es_stream": ".m3u8" in server_url,
                })
        scripts = re.findall(r'<script[^>]*>(.*?)</script>', r.text, re.DOTALL)
        for script in scripts:
            urls = re.findall(r'["\'](https?://[^"\']+(?:stream|video|player|embed)[^"\']*)["\']', script)
            for url in urls:
                if not any(s["url"] == url for s in servidores):
                    servidores.append({
                        "servidor": "Stream",
                        "url": url,
                        "idioma": "DUB Latino",
                        "lang_key": "DUB",
                        "es_stream": ".m3u8" in url,
                    })
        return servidores
    except Exception:
        return []

FUENTES = {
    "JKAnime": {
        "buscar": jkanime_buscar,
        "episodios": jkanime_episodios,
        "video": jkanime_get_video_url,
        "info": jkanime_info,
    },
    "AnimeFLV": {
        "buscar": animeflv_buscar,
        "episodios": animeflv_episodios,
        "video": animeflv_get_video_url,
        "info": animeflv_info,
    },
    "TioAnime": {
        "buscar": tioanime_buscar,
        "episodios": tioanime_episodios,
        "video": tioanime_get_video_url,
        "info": tioanime_info,
    },
    "AnimeFenix": {
        "buscar": animefenix_buscar,
        "episodios": animefenix_episodios,
        "video": animefenix_get_video_url,
        "info": animefenix_info,
    },
    "AnimeID": {
        "buscar": animeid_buscar,
        "episodios": animeid_episodios,
        "video": animeid_get_video_url,
        "info": animeid_info,
    },
    "MonosChinos": {
        "buscar": monoschinos_buscar,
        "episodios": monoschinos_episodios,
        "video": monoschinos_get_video_url,
        "info": monoschinos_info,
    },
}

def buscar_en_todas(query):
    resultados = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(FUENTES)) as executor:
        futuros = {executor.submit(fuente["buscar"], query): nombre for nombre, fuente in FUENTES.items()}
        for futuro in concurrent.futures.as_completed(futuros):
            try:
                res = futuro.result()
                if res:
                    resultados.extend(res)
            except Exception:
                pass
    return resultados

def obtener_episodios(slug, fuente):
    fn = FUENTES.get(fuente, {}).get("episodios", lambda s: [])
    return fn(slug)

def obtener_video(slug, episodio, fuente):
    fn = FUENTES.get(fuente, {}).get("video", lambda s, e: [])
    return fn(slug, episodio)

def obtener_info(slug, fuente):
    fn = FUENTES.get(fuente, {}).get("info", lambda s: {})
    return fn(slug)