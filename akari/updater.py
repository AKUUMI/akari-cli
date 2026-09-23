import os
from pathlib import Path
import shutil
import subprocess
import sys

import click


def actualizar():
    raiz = Path(__file__).resolve().parent.parent
    if not (raiz / ".git").exists() or not (raiz / "setup.py").is_file():
        raise click.ClickException("Esta instalación no está vinculada a un repositorio. Instala con git clone y python -m pip install -e . desde su carpeta.")
    git = shutil.which("git")
    if not git:
        raise click.ClickException("Git no está instalado o no está disponible en PATH.")
    entorno = dict(os.environ, GIT_TERMINAL_PROMPT="0", GIT_MERGE_AUTOEDIT="no")

    def ejecutar(*args):
        try:
            resultado = subprocess.run(
                [git, *args], cwd=raiz, env=entorno,
                capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120,
            )
        except subprocess.TimeoutExpired:
            raise click.ClickException("Git agotó el tiempo de espera. Comprueba tu conexión y vuelve a ejecutar akari update.")
        except OSError as exc:
            raise click.ClickException(f"No se pudo ejecutar Git: {exc}")
        if resultado.returncode:
            detalle = resultado.stderr.strip() or resultado.stdout.strip()
            raise click.ClickException(f"No se pudo actualizar: {detalle}")
        return resultado.stdout.strip()

    if Path(ejecutar("rev-parse", "--show-toplevel")).resolve() != raiz:
        raise click.ClickException("No se pudo identificar el repositorio de esta instalación.")
    if ejecutar("branch", "--show-current") != "main":
        raise click.ClickException("La instalación debe estar en main. No se cambiará de rama automáticamente.")
    if ejecutar("status", "--porcelain", "--untracked-files=no"):
        raise click.ClickException("Hay cambios locales sin guardar. Guarda tus cambios antes de ejecutar akari update; no se sobrescribió ningún archivo.")
    anterior = ejecutar("rev-parse", "HEAD")
    click.echo("Buscando actualizaciones de origin/main...")
    ejecutar("fetch", "origin", "main")
    remoto = ejecutar("rev-parse", "FETCH_HEAD")
    base = ejecutar("merge-base", "HEAD", remoto)
    if base != anterior:
        raise click.ClickException("main contiene commits locales que no están en origin/main. No se modificó tu rama.")
    ejecutar("merge", "--ff-only", remoto)
    click.echo("Actualizando la instalación y sus dependencias...")
    try:
        resultado = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "-e", str(raiz)],
            cwd=raiz, timeout=600,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise click.ClickException(f"El repositorio está actualizado, pero la instalación no terminó: {exc}. Vuelve a ejecutar akari update.")
    if resultado.returncode:
        raise click.ClickException("El repositorio está actualizado, pero pip falló. Vuelve a ejecutar akari update para completar la instalación.")
    if anterior == remoto:
        click.echo("Ya tienes la última versión de main. Instalación verificada.")
    else:
        click.echo(f"Akari actualizado: {anterior[:7]} → {remoto[:7]}.")
    click.echo("Abre akari de nuevo para usar la versión actualizada.")
