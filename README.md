```
      ✦ · . ˚ ✦ · . ˚ ✦ · . ˚ ✦ · . ˚ ✦ · . ˚ ✦
     █████╗ ██╗  ██╗ █████╗ ██████╗ ██╗
    ██╔══██╗██║ ██╔╝██╔══██╗██╔══██╗██║
    ███████║█████╔╝ ███████║██████╔╝██║
    ██╔══██║██╔═██╗ ██╔══██║██╔══██╗██║
    ██║  ██║██║  ██╗██║  ██║██║  ██║██║
    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝
          ✧  ア カ リ  ✧  1.2.1
      ✦ · . ˚ ✦ · . ˚ ✦ · . ˚ ✦ · . ˚ ✦ · . ˚ ✦
```

cliente de anime en español para terminal — inspirado en ani-cli 🕊️

---

## qué es esto

akari es un cliente de anime para terminal hecho en python. busca, selecciona y reproduce anime directo desde la terminal sin abrir el navegador. actualmente usa jkanime como fuente porque tiene streams m3u8 directos que funcionan bien con mpv.

el nombre es por alguien especial.

---

## requisitos

- python 3.8+
- mpv
- yt-dlp

```bash
# arch / endeavouros / manjaro
sudo pacman -S mpv yt-dlp python

# ubuntu / debian / mint
sudo apt install mpv python3 python3-pip
pip install yt-dlp

# fedora
sudo dnf install mpv python3 python3-pip
pip install yt-dlp

# cualquier distro
pip install requests beautifulsoup4 rich click lxml
```

---

## instalación

```bash
git clone https://github.com/AKUUMI/akari-cli
cd akari-cli
python3 -m akari.main
```

---

## uso

```
[b] buscar anime
[c] continuar viendo
[f] favoritos
[h] historial
[q] salir
```

también puedes buscar directo:

```bash
python3 -m akari.main buscar "attack on titan"
```

---

## compatibilidad

funciona en cualquier distro de linux con python 3.8+ y mpv instalado.

| distro | estado |
|--------|--------|
| arch / endeavouros / manjaro | ✅ |
| ubuntu / debian / mint | ✅ |
| fedora | ✅ |
| opensuse | ✅ |
| otras | debería funcionar |

---

## estado fuentes

| fuente | búsqueda | episodios | video |
|--------|----------|-----------|-------|
| jkanime | ✅ | ✅ | ✅ |

---

## roadmap

- [ ] soporte termux / android
- [ ] más fuentes
- [ ] notificaciones de nuevos episodios

---

## créditos

inspirado en [ani-cli](https://github.com/pystardust/ani-cli) 🕊️

---

<p align="center">hecho con demasiado café y mucho amor 🖤</p>
