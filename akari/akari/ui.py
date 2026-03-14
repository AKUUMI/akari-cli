from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.columns import Columns
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.align import Align
from rich import box
import time

console = Console()

C_LAVANDA  = "color(183)"
C_ROSA     = "color(219)"
C_DORADO   = "color(220)"
C_BLANCO   = "bold white"
C_GRIS     = "color(245)"
C_VERDE    = "color(157)"
C_AZUL     = "color(153)"


def separador():
    console.print(f"[{C_LAVANDA}]  ✦ · . ˚ ✦ · . ˚ ✦ · . ˚ ✦ · . ˚ ✦ · . ˚ ✦[/]", justify="center")


def mostrar_resultados(resultados):
    if not resultados:
        console.print(f"\n[{C_ROSA}]  🕊️  No se encontraron resultados...[/]\n")
        return

    table = Table(
        box=box.ROUNDED,
        border_style=C_LAVANDA,
        header_style=f"bold {C_DORADO}",
        show_lines=True,
        expand=False,
    )
    table.add_column("#", style=C_GRIS, justify="right", width=3)
    table.add_column("Título", style=C_BLANCO, min_width=30)
    table.add_column("Fuente", style=C_AZUL, width=12)
    table.add_column("Tipo", style=C_ROSA, width=10)

    for i, r in enumerate(resultados, 1):
        table.add_row(str(i), r["titulo"], r["fuente"], r.get("tipo", "Anime"))

    console.print()
    console.print(Align.center(table))
    console.print()


def seleccionar_anime(resultados):
    mostrar_resultados(resultados)
    while True:
        eleccion = Prompt.ask(f"[{C_LAVANDA}]  ✧ Elige un número[/]", default="1")
        try:
            idx = int(eleccion) - 1
            if 0 <= idx < len(resultados):
                return resultados[idx]
        except ValueError:
            pass
        console.print(f"[{C_ROSA}]  Por favor elige un número válido[/]")


def mostrar_info_anime(info, titulo):
    if not info:
        return

    console.print()
    partes = Text()

    if info.get("sinopsis"):
        sin = info["sinopsis"]
        if len(sin) > 280:
            sin = sin[:280] + "…"
        partes.append(sin + "\n\n", style=C_GRIS)

    meta = []
    if info.get("estado"):
        meta.append(f"Estado: {info['estado']}")
    if info.get("tipo"):
        meta.append(f"Tipo: {info['tipo']}")
    if info.get("anio"):
        meta.append(f"Año: {info['anio']}")
    if meta:
        partes.append("  ".join(meta) + "\n", style=C_AZUL)

    if info.get("generos"):
        partes.append("\n" + "  ".join(info["generos"]), style=C_ROSA)

    panel = Panel(
        partes,
        title=f"[{C_DORADO}]✦ {titulo}[/]",
        border_style=C_LAVANDA,
        padding=(1, 2),
    )
    console.print(Align.center(panel))
    console.print()


def seleccionar_idioma():
    console.print()
    panel = Panel(
        Text.assemble(
            ("  1  ", f"bold {C_DORADO}"), ("Subtítulos en Español Latino\n", C_BLANCO),
            ("  2  ", f"bold {C_DORADO}"), ("Subtítulos en Español de España\n", C_BLANCO),
            ("  3  ", f"bold {C_DORADO}"), ("Doblaje en Español Latino\n", C_BLANCO),
            ("  4  ", f"bold {C_DORADO}"), ("Doblaje en Español de España", C_BLANCO),
        ),
        title=f"[{C_LAVANDA}]🕊️  Elige tu idioma[/]",
        border_style=C_LAVANDA,
        padding=(1, 4),
    )
    console.print(Align.center(panel))
    console.print()

    opciones = {
        "1": ("SUB", "Latino"),
        "2": ("SUB", "España"),
        "3": ("DUB", "Latino"),
        "4": ("DUB", "España"),
    }
    while True:
        eleccion = Prompt.ask(f"[{C_LAVANDA}]  ✧ Opción[/]", default="1")
        if eleccion in opciones:
            tipo, region = opciones[eleccion]
            console.print(f"\n[{C_VERDE}]  ✦ Seleccionado: {tipo} — Español {region}[/]\n")
            return tipo, region
        console.print(f"[{C_ROSA}]  Opción inválida, elige 1-4[/]")


def seleccionar_episodio(episodios, anime_titulo, progreso_anterior=None):
    console.print()

    panel_text = Text()
    panel_text.append("  Total de episodios: ", style=C_GRIS)
    panel_text.append(f"{len(episodios)}\n", style=f"bold {C_DORADO}")
    if progreso_anterior:
        panel_text.append("  Último visto: ", style=C_GRIS)
        panel_text.append(f"Episodio {progreso_anterior['episodio']}", style=f"bold {C_VERDE}")
        minuto = progreso_anterior.get("minuto", 0)
        if minuto > 30:
            mins = minuto // 60
            segs = minuto % 60
            panel_text.append(f"  (min {mins}:{segs:02d})", style=C_GRIS)

    panel = Panel(
        panel_text,
        title=f"[{C_LAVANDA}]📺  {anime_titulo}[/]",
        border_style=C_LAVANDA,
        padding=(0, 2),
    )
    console.print(Align.center(panel))
    console.print()

    default_ep = str(progreso_anterior["episodio"]) if progreso_anterior else "1"
    while True:
        eleccion = Prompt.ask(f"[{C_LAVANDA}]  ✧ Número de episodio[/]", default=default_ep)
        try:
            ep = int(eleccion)
            if ep in episodios:
                return ep
        except ValueError:
            pass
        console.print(f"[{C_ROSA}]  Episodio inválido. Rango: 1–{max(episodios)}[/]")


def cuenta_regresiva_autoplay(segundos=5):
    console.print()
    for i in range(segundos, 0, -1):
        console.print(
            f"[{C_GRIS}]  Siguiente episodio en {i}s... (Enter para cancelar)[/]",
            end="\r"
        )
        time.sleep(1)
    console.print(" " * 55, end="\r")
    return True


def mostrar_historial(historial):
    if not historial:
        console.print(f"\n[{C_ROSA}]  🕊️  Tu historial está vacío...[/]\n")
        return

    console.print()
    separador()
    console.print(f"[{C_DORADO}]  ✦ Continuar viendo[/]\n")

    table = Table(
        box=box.SIMPLE_HEAVY,
        border_style=C_LAVANDA,
        header_style=f"bold {C_DORADO}",
        show_lines=False,
    )
    table.add_column("#", style=C_GRIS, width=3, justify="right")
    table.add_column("Título", style=C_BLANCO, min_width=28)
    table.add_column("Episodio", style=C_ROSA, width=10, justify="center")
    table.add_column("Progreso", style=C_VERDE, width=10, justify="center")
    table.add_column("Fuente", style=C_AZUL, width=12)

    for i, item in enumerate(historial, 1):
        total = f"/{item['total_episodios']}" if item.get("total_episodios") else ""
        minuto = item.get("minuto", 0)
        if minuto > 30:
            mins = minuto // 60
            segs = minuto % 60
            prog_str = f"min {mins}:{segs:02d}"
        else:
            prog_str = "—"
        table.add_row(
            str(i),
            item["titulo"],
            f"Ep. {item['episodio']}{total}",
            prog_str,
            item["fuente"],
        )

    console.print(Align.center(table))
    console.print()


def mostrar_favoritos(favoritos):
    if not favoritos:
        console.print(f"\n[{C_ROSA}]  🕊️  No tienes favoritos aún...[/]\n")
        return

    console.print()
    separador()
    console.print(f"[{C_DORADO}]  ✦ Tus favoritos[/]\n")

    table = Table(
        box=box.SIMPLE_HEAVY,
        border_style=C_LAVANDA,
        header_style=f"bold {C_DORADO}",
        show_lines=False,
    )
    table.add_column("#", style=C_GRIS, width=3, justify="right")
    table.add_column("Título", style=C_BLANCO, min_width=28)
    table.add_column("Fuente", style=C_AZUL, width=12)
    table.add_column("Agregado", style=C_GRIS, width=12)

    for i, fav in enumerate(favoritos, 1):
        fecha = fav["fecha_agregado"][:10] if fav.get("fecha_agregado") else "—"
        table.add_row(str(i), fav["titulo"], fav["fuente"], fecha)

    console.print(Align.center(table))
    console.print()


def seleccionar_genero(generos):
    console.print()
    table = Table(
        box=box.SIMPLE,
        border_style=C_LAVANDA,
        header_style=f"bold {C_DORADO}",
        show_lines=False,
    )
    table.add_column("#", style=C_GRIS, width=4, justify="right")
    table.add_column("Género", style=C_ROSA, min_width=20)
    table.add_column("#", style=C_GRIS, width=4, justify="right")
    table.add_column("Género", style=C_ROSA, min_width=20)

    mitad = (len(generos) + 1) // 2
    izq = generos[:mitad]
    der = generos[mitad:]

    for i, g in enumerate(izq):
        j = i + mitad
        der_num = str(j + 1) if j < len(generos) else ""
        der_nom = der[i].replace("-", " ").title() if i < len(der) else ""
        table.add_row(str(i + 1), g.replace("-", " ").title(), der_num, der_nom)

    console.print(Align.center(table))
    console.print()

    while True:
        eleccion = Prompt.ask(f"[{C_LAVANDA}]  ✧ Elige un género[/]", default="1")
        try:
            idx = int(eleccion) - 1
            if 0 <= idx < len(generos):
                return generos[idx]
        except ValueError:
            pass
        console.print(f"[{C_ROSA}]  Número inválido[/]")


def spinner(mensaje="Buscando"):
    return Progress(
        SpinnerColumn(style=C_LAVANDA),
        TextColumn(f"[{C_ROSA}]{mensaje}...[/]"),
        transient=True,
    )


def barra_carga(mensaje="Cargando"):
    return Progress(
        SpinnerColumn(style=C_LAVANDA),
        TextColumn(f"[{C_ROSA}]{mensaje}[/]"),
        BarColumn(bar_width=30, style=C_LAVANDA, complete_style=C_DORADO),
        transient=True,
    )


def menu_principal(tiene_historial=False):
    console.print()
    opciones = []

    if tiene_historial:
        opciones.append(("c", "Continuar viendo", C_VERDE))

    opciones += [
        ("b", "Buscar anime", C_DORADO),
        ("g", "Explorar por género", C_ROSA),
        ("f", "Favoritos", C_LAVANDA),
        ("h", "Historial completo", C_AZUL),
        ("q", "Salir", C_GRIS),
    ]

    text = Text()
    for key, label, color in opciones:
        text.append(f"  [{key}]  ", style=f"bold {C_DORADO}")
        text.append(f"{label}\n", style=color)

    panel = Panel(
        text,
        title=f"[{C_LAVANDA}]✦ Menú principal ✦[/]",
        border_style=C_LAVANDA,
        padding=(1, 4),
    )
    console.print(Align.center(panel))
    console.print()

    keys = [o[0] for o in opciones]
    while True:
        eleccion = Prompt.ask(
            f"[{C_LAVANDA}]  ✧ Elige una opción[/]",
            choices=keys,
            show_choices=False,
        )
        return eleccion


def mostrar_catalogo_genero(animes, genero, pagina, total_paginas):
    import shutil
    from akari.player import mostrar_portada_ascii

    console.print()
    separador()
    console.print(f"[{C_DORADO}]  ✦ {genero.upper()}[/]  [{C_GRIS}]página {pagina}/{total_paginas}[/]\n")

    for i, anime in enumerate(animes, 1):
        console.print(f"[{C_DORADO}]  {i}.[/] [{C_BLANCO}]{anime['titulo']}[/]")
        if anime.get("portada") and shutil.which("chafa"):
            mostrar_portada_ascii(anime["portada"])

    console.print()
    nav = []
    if pagina > 1:
        nav.append(f"[{C_DORADO}][p][/] anterior")
    if pagina < total_paginas:
        nav.append(f"[{C_DORADO}][n][/] siguiente")
    nav.append(f"[{C_DORADO}][número][/] elegir")
    nav.append(f"[{C_DORADO}][q][/] volver")
    console.print("  " + "   ".join(nav))
    console.print()


def seleccionar_genero_catalogo(generos):
    console.print()
    separador()
    console.print(f"[{C_DORADO}]  ✦ Explorar por género[/]\n")

    table = Table(
        box=box.SIMPLE,
        border_style=C_LAVANDA,
        show_lines=False,
        show_header=False,
    )
    table.add_column("#", style=C_GRIS, width=4, justify="right")
    table.add_column("Género", style=C_ROSA, min_width=20)
    table.add_column("#", style=C_GRIS, width=4, justify="right")
    table.add_column("Género", style=C_ROSA, min_width=20)

    mitad = (len(generos) + 1) // 2
    izq = generos[:mitad]
    der = generos[mitad:]

    for i, g in enumerate(izq):
        j = i + mitad
        der_num = str(j + 1) if j < len(generos) else ""
        der_nom = der[i].title() if i < len(der) else ""
        table.add_row(str(i + 1), g.title(), der_num, der_nom)

    console.print(Align.center(table))
    console.print()

    while True:
        eleccion = Prompt.ask(f"[{C_LAVANDA}]  ✧ Elige un género[/]", default="1")
        try:
            idx = int(eleccion) - 1
            if 0 <= idx < len(generos):
                return generos[idx]
        except ValueError:
            pass
        console.print(f"[{C_ROSA}]  Número inválido[/]")
