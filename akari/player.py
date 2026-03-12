import subprocess
import shutil
import sys
import re
import os


def detectar_reproductor():
    for player in ["mpv", "vlc", "cvlc"]:
        if shutil.which(player):
            return player
    return None


def es_termux():
    return "com.termux" in os.environ.get("PREFIX", "")


def _segundos_a_str(seg):
    m = seg // 60
    s = seg % 60
    return f"{m:02d}:{s:02d}"


def reproducir_termux(url, referer=None):
    cmd = [
        "am", "start",
        "-n", "org.videolan.vlc/org.videolan.vlc.gui.video.VideoPlayerActivity",
        "-d", url,
    ]
    try:
        subprocess.run(cmd, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False


def reproducir(url, titulo="Akari", episodio=1, player=None, referer=None, desde_segundo=0):
    if es_termux():
        reproducir_termux(url, referer)
        return

    if player is None:
        player = detectar_reproductor()
    if player is None:
        print("[akari] Error: no se encontró mpv ni vlc instalado.")
        sys.exit(1)

    titulo_completo = f"{titulo} — Episodio {episodio}"

    if "mpv" in player:
        cmd = ["mpv", url,
               f"--title={titulo_completo}",
               f"--force-media-title={titulo_completo}",
               "--save-position-on-quit"]
        if referer:
            cmd.append(f"--referrer={referer}")
        if desde_segundo > 0:
            cmd.append(f"--start={_segundos_a_str(desde_segundo)}")
    elif "vlc" in player or "cvlc" in player:
        cmd = [player, url, f"--meta-title={titulo_completo}"]
        if desde_segundo > 0:
            cmd += ["--start-time", str(desde_segundo)]
    else:
        cmd = [player, url]

    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        pass
    except FileNotFoundError:
        print(f"[akari] Error: '{player}' no encontrado.")
        sys.exit(1)


def reproducir_y_verificar(url, titulo="Akari", episodio=1, player=None, referer=None, desde_segundo=0):
    if es_termux():
        ok = reproducir_termux(url, referer)
        return ok, url if ok else None, 0

    if player is None:
        player = detectar_reproductor()
    if player is None:
        return False, None, 0

    if not url or url.startswith("data:") or len(url) > 2000:
        return False, None, 0

    titulo_completo = f"{titulo} — Episodio {episodio}"

    url_final = url
    es_directo = ".m3u8" in url or "okcdn.ru" in url or "/cdn" in url
    if not es_directo and shutil.which("yt-dlp"):
        try:
            cmd = ["yt-dlp", "--get-url", "--no-warnings", "-q", url]
            if referer:
                cmd += ["--add-header", f"Referer:{referer}"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
            if result.returncode == 0 and result.stdout.strip():
                extracted = result.stdout.strip().split("\n")[0]
                if extracted and not extracted.startswith("data:") and len(extracted) < 2000:
                    url_final = extracted
                else:
                    return False, None, 0
            else:
                return False, None, 0
        except Exception:
            return False, None, 0

    minuto_final = 0

    if "mpv" in player:
        cmd = ["mpv", url_final,
               f"--title={titulo_completo}",
               f"--force-media-title={titulo_completo}",
               "--save-position-on-quit",
               "--term-playing-msg=POSICION:${=playback-time}"]
        if referer:
            cmd.append(f"--referrer={referer}")
        if desde_segundo > 0:
            cmd.append(f"--start={_segundos_a_str(desde_segundo)}")
    else:
        cmd = [player, url_final]
        if desde_segundo > 0 and "vlc" in player:
            cmd += ["--start-time", str(desde_segundo)]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        ok = result.returncode == 0
        if ok and result.stdout:
            matches = re.findall(r'POSICION:(\d+(?:\.\d+)?)', result.stdout)
            if matches:
                minuto_final = int(float(matches[-1]))
        return ok, url_final if ok else None, minuto_final
    except KeyboardInterrupt:
        return True, url_final, minuto_final
    except Exception:
        return False, None, 0


def mostrar_portada_ascii(url_imagen):
    if not shutil.which("chafa"):
        return
    try:
        import urllib.request
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            urllib.request.urlretrieve(url_imagen, f.name)
            subprocess.run(
                ["chafa", "--size=20x28", f.name],
                stderr=subprocess.DEVNULL
            )
    except Exception:
        pass
