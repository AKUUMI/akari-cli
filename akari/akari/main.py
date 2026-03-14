import subprocess
import click
import sys
import threading

from akari.banner import show_banner
from akari.ui import (
    console, separador, seleccionar_anime, mostrar_info_anime,
    seleccionar_episodio, mostrar_historial, mostrar_favoritos,
    menu_principal, spinner, cuenta_regresiva_autoplay,
    seleccionar_genero_catalogo, mostrar_catalogo_genero,
    C_LAVANDA, C_ROSA, C_DORADO, C_VERDE, C_GRIS
)
from akari.scrapers import (
    buscar_en_todas, obtener_episodios, obtener_video, jkanime_info
)
from akari.catalogo import CATALOGO, GENEROS_CATALOGO
from akari.historial import (
    init_db, guardar_episodio, obtener_historial,
    obtener_progreso, obtener_favoritos, agregar_favorito
)
from akari.logger import info, error, reproduccion, busqueda
from akari.player import (
    reproducir, reproducir_y_verificar, detectar_reproductor,
    es_termux, mostrar_portada_ascii
)

init_db()


def flujo_busqueda():
    query = console.input(f"[{C_LAVANDA}]  ✧ Buscar anime: [/]").strip()
    if not query:
        return

    with spinner("Buscando en JKAnime"):
        resultados = buscar_en_todas(query)

    busqueda(query, len(resultados))
    if not resultados:
        console.print(f"\n[{C_ROSA}]  🕊️  Sin resultados para '{query}'[/]\n")
        return

    anime = seleccionar_anime(resultados)
    flujo_ver_anime(anime)



def flujo_ver_anime(anime):
    separador()
    console.print(f"\n[{C_DORADO}]  ✦ {anime['titulo']}[/]  [{C_LAVANDA}]({anime['fuente']})[/]\n")

    # Mostrar portada ASCII si chafa está instalado
    if anime.get("portada"):
        mostrar_portada_ascii(anime["portada"])

    # Info del anime
    with spinner("Cargando info"):
        info = jkanime_info(anime["slug"])
    mostrar_info_anime(info, anime["titulo"])

    with spinner("Cargando episodios"):
        episodios = obtener_episodios(anime["slug"], anime["fuente"])

    if not episodios:
        console.print(f"[{C_ROSA}]  No se pudieron obtener los episodios.[/]\n")
        return

    progreso = obtener_progreso(anime["slug"], anime["fuente"])
    ep = seleccionar_episodio(episodios, anime["titulo"], progreso)

    while ep is not None:
        ep = _loop_episodio(anime, ep, episodios)


def _loop_episodio(anime, ep, episodios):
    with console.status(f"[{C_LAVANDA}]  ✦ Obteniendo servidores (ep. {ep})...[/]"):
        servidores = obtener_video(anime["slug"], ep, anime["fuente"])

    if not servidores:
        console.print(f"[{C_ROSA}]  No se pudo obtener el video.[/]\n")
        return None

    player = detectar_reproductor() if not es_termux() else "vlc"
    if not player and not es_termux():
        console.print(f"[{C_ROSA}]  ⚠️  mpv o vlc no encontrado. Instala mpv.[/]")
        console.print(f"[{C_LAVANDA}]  URL directa: {servidores[0]['url']}[/]")
        console.print(f"[{C_GRIS}]  mpv \"{servidores[0]['url']}\" --referrer=\"https://jkanime.net/\"[/]")
        return None

    referer = "https://jkanime.net/"

    progreso = obtener_progreso(anime["slug"], anime["fuente"])
    desde_segundo = 0
    if progreso and progreso.get("episodio") == ep and progreso.get("minuto", 0) > 30:
        minuto_guardado = progreso["minuto"]
        mins = minuto_guardado // 60
        segs = minuto_guardado % 60
        resp = console.input(
            f"[{C_LAVANDA}]  ¿Continuar desde {mins}:{segs:02d}? [S/n]: [/]"
        ).strip().lower()
        if resp != "n":
            desde_segundo = minuto_guardado

    url_reproducida = None
    minuto_final = 0
    for s in servidores:
        console.print(f"[{C_GRIS}]  ▶ Probando {s['servidor']}...[/]", end="\r")
        ok, url_final, pos, termino_solo = reproducir_y_verificar(
            s["url"],
            titulo=anime["titulo"],
            episodio=ep,
            player=player,
            referer=referer,
            desde_segundo=desde_segundo,
        )
        console.print(" " * 55, end="\r")
        if ok and url_final:
            url_reproducida = url_final
            minuto_final = pos
            reproduccion(anime["titulo"], ep, anime["fuente"], s["servidor"])
            break

    if not url_reproducida:
        console.print(f"[{C_ROSA}]  No se pudo reproducir con ningún servidor disponible.[/]")
        if servidores:
            console.print(f"[{C_LAVANDA}]  URL directa: {servidores[0]['url']}[/]")
            console.print(f"[{C_GRIS}]  mpv \"{servidores[0]['url']}\" --referrer=\"https://jkanime.net/\"[/]\n")
        return None

    guardar_episodio(
        titulo=anime["titulo"],
        slug=anime["slug"],
        fuente=anime["fuente"],
        episodio=ep,
        total_episodios=max(episodios) if episodios else None,
        portada=anime.get("portada"),
        minuto=minuto_final,
    )

    tiene_siguiente = (ep + 1) in episodios

    # Autoplay solo si mpv terminó el video solo (no si el usuario cerró)
    if tiene_siguiente and termino_solo:
        cancelado = [False]

        def esperar_input():
            try:
                input()
                cancelado[0] = True
            except Exception:
                pass

        t = threading.Thread(target=esperar_input, daemon=True)
        t.start()

        console.print(f"\n[{C_GRIS}]  Siguiente episodio en 5s... (Enter para cancelar)[/]", end="\r")
        for i in range(5, 0, -1):
            if cancelado[0]:
                break
            console.print(f"[{C_GRIS}]  Siguiente episodio en {i}s... (Enter para cancelar)[/]", end="\r")
            t.join(timeout=1)

        console.print(" " * 60, end="\r")

        if not cancelado[0]:
            return ep + 1

    # Menú post-reproducción
    while True:
        separador()
        partes = []
        if tiene_siguiente:
            partes.append(f"[{C_DORADO}][n][/] Siguiente")
        partes.append(f"[{C_DORADO}][r][/] Repetir")
        partes.append(f"[{C_DORADO}][f][/] Favoritos")
        partes.append(f"[{C_DORADO}][u][/] Abrir en navegador")
        partes.append(f"[{C_DORADO}][q][/] Menú")
        console.print(f"\n[{C_LAVANDA}]  ¿Qué deseas hacer?[/]")
        console.print("  " + "   ".join(partes))

        accion = console.input(f"[{C_LAVANDA}]  ✧ Opción: [/]").strip().lower()

        if accion == "n" and tiene_siguiente:
            return ep + 1

        elif accion == "r":
            reproducir(
                url_reproducida,
                titulo=anime["titulo"],
                episodio=ep,
                player=player,
                referer=referer,
            )

        elif accion == "f":
            agregado = agregar_favorito(
                anime["titulo"], anime["slug"], anime["fuente"], anime.get("portada")
            )
            if agregado:
                console.print(f"[{C_VERDE}]  ✦ Agregado a favoritos 🕊️[/]")
            else:
                console.print(f"[{C_GRIS}]  Ya está en favoritos.[/]")

        elif accion == "u":
            subprocess.run(["xdg-open", url_reproducida], stderr=subprocess.DEVNULL)
            console.print(f"[{C_VERDE}]  ✦ Abriendo en navegador...[/]")
            return None

        else:
            return None


def flujo_catalogo():
    genero = seleccionar_genero_catalogo(GENEROS_CATALOGO)
    animes = CATALOGO[genero]

    POR_PAGINA = 5
    pagina = 1
    total_paginas = (len(animes) + POR_PAGINA - 1) // POR_PAGINA

    # Enriquecer con portadas de JKAnime
    with spinner(f"Cargando {genero}"):
        for anime in animes:
            if not anime.get("portada"):
                from akari.scrapers import jkanime_info
                info = jkanime_info(anime["slug"])
                if info.get("portada"):
                    anime["portada"] = info["portada"]

    while True:
        inicio = (pagina - 1) * POR_PAGINA
        fin = inicio + POR_PAGINA
        pagina_animes = animes[inicio:fin]

        mostrar_catalogo_genero(pagina_animes, genero, pagina, total_paginas)

        accion = console.input(f"[{C_LAVANDA}]  ✧ Opción: [/]").strip().lower()

        if accion == "n" and pagina < total_paginas:
            pagina += 1
        elif accion == "p" and pagina > 1:
            pagina -= 1
        elif accion == "q":
            return
        else:
            try:
                idx = int(accion) - 1
                if 0 <= idx < len(pagina_animes):
                    anime = pagina_animes[idx]
                    flujo_ver_anime({
                        "titulo": anime["titulo"],
                        "slug": anime["slug"],
                        "fuente": "JKAnime",
                        "portada": anime.get("portada"),
                        "tipo": "Anime",
                    })
                    return
            except ValueError:
                pass


def flujo_continuar(historial):
    mostrar_historial(historial)
    eleccion = console.input(
        f"[{C_LAVANDA}]  ✧ Elige número (o Enter para volver): [/]"
    ).strip()
    if not eleccion:
        return
    try:
        idx = int(eleccion) - 1
        if 0 <= idx < len(historial):
            item = historial[idx]
            anime = {
                "titulo": item["titulo"],
                "slug": item["slug"],
                "fuente": item["fuente"],
                "portada": item.get("portada"),
                "tipo": "Anime",
            }
            flujo_ver_anime(anime)
    except (ValueError, IndexError):
        pass


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    show_banner(console)
    separador()

    if ctx.invoked_subcommand is None:
        historial = obtener_historial(5)
        while True:
            opcion = menu_principal(tiene_historial=bool(historial))

            if opcion == "b":
                flujo_busqueda()

            elif opcion == "g":
                flujo_catalogo()

            elif opcion == "c":
                flujo_continuar(historial)
                historial = obtener_historial(5)

            elif opcion == "f":
                favs = obtener_favoritos()
                mostrar_favoritos(favs)
                console.input(f"[{C_LAVANDA}]  Presiona Enter para volver...[/]")

            elif opcion == "h":
                hist = obtener_historial(20)
                mostrar_historial(hist)
                console.input(f"[{C_LAVANDA}]  Presiona Enter para volver...[/]")

            elif opcion == "q":
                console.print(f"\n[{C_LAVANDA}]  ✦ ¡Hasta pronto! 🕊️[/]\n")
                separador()
                info("sesion terminada")
                subprocess.run(["clear"])
                sys.exit(0)


@cli.command()
@click.argument("query", nargs=-1)
def buscar(query):
    q = " ".join(query)
    if not q:
        console.print(f"[{C_ROSA}]  Especifica qué anime buscar.[/]")
        return
    with spinner("Buscando"):
        resultados = buscar_en_todas(q)
    if resultados:
        anime = seleccionar_anime(resultados)
        flujo_ver_anime(anime)
    else:
        console.print(f"[{C_ROSA}]  Sin resultados para '{q}'[/]")


@cli.command()
def historial():
    show_banner(console)
    hist = obtener_historial(20)
    mostrar_historial(hist)


@cli.command()
def favoritos():
    show_banner(console)
    favs = obtener_favoritos()
    mostrar_favoritos(favs)


if __name__ == "__main__":
    cli()
