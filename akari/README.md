```
      ✦ · . ˚ ✦ · . ˚ ✦ · . ˚ ✦ · . ˚ ✦ · . ˚ ✦
     █████╗ ██╗  ██╗ █████╗ ██████╗ ██╗
    ██╔══██╗██║ ██╔╝██╔══██╗██╔══██╗██║
    ███████║█████╔╝ ███████║██████╔╝██║
    ██╔══██║██╔═██╗ ██╔══██║██╔══██╗██║
    ██║  ██║██║  ██╗██║  ██║██║  ██║██║
    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝
          ✧  ア カ リ  ✧  1.3.1
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
pip install -e . --break-system-packages
akari
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
akari buscar "attack on titan"
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
| termux (android) | ✅ requiere vlc |
| otras | debería funcionar |

---

## estado fuentes

| fuente | búsqueda | episodios | video |
|--------|----------|-----------|-------|
| jkanime | ✅ | ✅ | ✅ |

---

## roadmap

- [ ] más fuentes de anime en español
- [ ] explorar por género
- [ ] notificaciones de nuevos episodios
- [ ] `akari update` para actualizar automáticamente

---

## apoyar el proyecto

akari es y será siempre gratuito. si te gusta y quieres apoyar el desarrollo (café, ramen, etc.) puedes donar en ko-fi — es completamente voluntario y no da ninguna ventaja ni acceso especial.

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/)

---

## aviso legal

akari-cli es una herramienta open-source creada con fines educativos y de entretenimiento personal.

- este proyecto **no hostea ni distribuye** ningún contenido con derechos de autor
- solo actúa como cliente que accede a **fuentes públicas de terceros** disponibles en internet
- el uso depende de la disponibilidad y legalidad de dichas fuentes en tu país o región
- **no nos hacemos responsables** del contenido accedido, ni promovemos la infracción de derechos de autor
- recomendamos usar **servicios legales** como crunchyroll, netflix, hidive o amazon prime para apoyar a los creadores
- si eres titular de derechos y consideras que alguna fuente viola tus copyrights, contacta directamente al proveedor de la fuente — no a este repositorio

este proyecto es **gratuito, sin fines de lucro** y de uso personal/comunitario. cualquier donación vía ko-fi es voluntaria y solo para apoyar el desarrollo. uso bajo tu propio riesgo.

**legal notice (english)**

akari-cli is an open-source tool for personal and educational use. this project does **not host or distribute** any copyrighted content — it only accesses public third-party sources available on the internet. usage depends on the availability and legality of those sources in your region. we are **not responsible** for accessed content and do not encourage copyright infringement. we recommend using legal services like crunchyroll, netflix, etc. if you are a rights holder and believe a source infringes your copyrights, contact the source provider directly — not this repo. this project is free, non-profit, and for personal/community use. any ko-fi donations are voluntary and support development only. use at your own risk.

---

## créditos

inspirado en [ani-cli](https://github.com/pystardust/ani-cli) 🕊️

---

<p align="center">hecho con demasiado café y mucho amor 🖤</p>
