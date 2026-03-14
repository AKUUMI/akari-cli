# ✦ Instalación en Arch Linux

## 1. Dependencias

```bash
sudo pacman -S mpv python python-pip python-virtualenv git
```

Opcionales pero recomendados:
```bash
# yt-dlp: para mejor extracción de streams (como ani-cli)
sudo pacman -S yt-dlp

# ffmpeg: para procesamiento de video
sudo pacman -S ffmpeg
```

---

## 2. Clonar el proyecto

```bash
git clone https://github.com/tu-usuario/akari-cli
cd akari-cli
```

---

## 3. Entorno virtual (importante en Arch)

Arch usa **PEP 668** — no puedes instalar paquetes pip directamente en el sistema sin romper cosas. Usa siempre un venv:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

---

## 4. Ejecutar Akari

```bash
# Asegúrate de tener el venv activo
source .venv/bin/activate

akari                          # modo interactivo
akari buscar "death note"      # búsqueda directa
akari historial                # ver historial
```

---

## 5. Atajo permanente (opcional)

Para no tener que activar el venv cada vez, agrega esto a tu `~/.bashrc` o `~/.zshrc`:

```bash
alias akari="$HOME/akari-cli/.venv/bin/akari"
```

Luego:
```bash
source ~/.bashrc   # o source ~/.zshrc
akari              # funciona desde cualquier lugar ✦
```

---

## 6. AUR (futuro)

Cuando el proyecto esté estable, se publicará en el AUR para poder instalarlo con:

```bash
yay -S akari-cli
# o
paru -S akari-cli
```

---

## Solución de problemas

| Problema | Solución |
|----------|----------|
| `externally-managed-environment` | Usa el venv como se indica arriba |
| `mpv: command not found` | `sudo pacman -S mpv` |
| `ModuleNotFoundError: rich` | Activa el venv: `source .venv/bin/activate` |
| Video no reproduce | Verifica que mpv funcione: `mpv --version` |
