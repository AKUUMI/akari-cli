```
      ✧･ﾟ: *✧･ﾟ:*  ♡ (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧  ♡  *:･ﾟ✧*:･ﾟ✧
     █████╗ ██╗  ██╗ █████╗ ██████╗ ██╗
    ██╔══██╗██║ ██╔╝██╔══██╗██╔══██╗██║
    ███████║█████╔╝ ███████║██████╔╝██║
    ██╔══██║██╔═██╗ ██╔══██║██╔══██╗██║
    ██║  ██║██║  ██╗██║  ██║██║  ██║██║
    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝
          (˶˃ᆺ˂˶) ア カ リ (˶˃ᆺ˂˶)  1.5.0 ヽ(o^.^o)ﾉ
      ✧･ﾟ: *✧･ﾟ:*  ♡ ૮ ˶ᵔ ᵕ ᵔ˶ ა ♡  *:･ﾟ✧*:･ﾟ✧
```

cliente de anime en español multiplataforma para terminal — inspirado en ani-cli ଘ(੭ˊ꒳ˋ)੭✧

---

## (｡♥‿♥｡) qué es esto

akari es un cliente de anime interactivo hecho en python. busca, selecciona y reproduce anime con subtítulos o doblaje latino directamente desde tu terminal, sin abrir el navegador. diseñado con una estética kawaii (｡•̀ᴗ-)✧, soporta múltiples fuentes concurrentes, guarda tu progreso al minuto exacto y es completamente multiplataforma (Linux, Windows, macOS, Android/Termux).

el nombre es por alguien especial. ♡(◡‿◡✿)

---

## ฅ(≧ω≦)ฅ requisitos

- python 3.10+
- reproductor de video (mpv recomendado, vlc soportado)
- yt-dlp (para extraer streams complejos)
- chafa (opcional, para ver portadas de anime en arte ASCII)

### instalación de dependencias del sistema:

**arch / endeavouros / manjaro / cachyos:**
```bash
sudo pacman -S mpv yt-dlp python chafa
```

**ubuntu / debian / mint / pop!_os:**
```bash
sudo apt install mpv python3 python3-pip python3-venv chafa
pip install yt-dlp
```

**windows:**

🐍 **1. Python 3.10+**
Descargado de [python.org](https://python.org/)
- IMPORTANTE: marcar ✅ "Add Python to PATH" durante la instalación
- Verificación: `python --version`

📦 **2. Git**
Descargado de [git-scm.com](https://git-scm.com/)
- Marcar "Git from the command line and also from 3rd-party software"
- Verificación: `git --version`

🎬 **3. mpv (reproductor de video)**
Instalado con Scoop:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
scoop bucket add extras
scoop install mpv
```
- Verificación: `mpv --version`

📚 **4. Dependencias de Python**
```powershell
pip install yt-dlp
```
Y las del proyecto:
```powershell
cd C:\ruta\a\akari-cli
pip install -e .
```

---

## ૮(˶ík꒳ì˶)ა instalación

recomendamos usar un entorno virtual (venv) para evitar conflictos con tu sistema (๑>◡<๑).

### script automático (solo linux):
```bash
git clone https://github.com/AKUUMI/akari-cli
cd akari-cli
chmod +x install.sh
./install.sh
```

### instalación manual (windows / linux / macos):
```bash
git clone https://github.com/AKUUMI/akari-cli
cd akari-cli
python -m venv .venv

# en linux/macos:
source .venv/bin/activate
# en windows:
.\.venv\Scripts\activate

pip install -e .
akari
```

---

## 🎮 uso

asegúrate de tener activo tu entorno virtual (¬‿¬). el menú interactivo te permite:

```
[b] buscar anime
[c] continuar viendo (reanuda en el minuto exacto)
[g] explorar catálogo por géneros
[f] favoritos
[h] historial completo
[q] salir
```

también puedes usar comandos directos ᕕ( ᐛ )ᕗ:
```bash
akari buscar "attack on titan"
akari historial
akari favoritos
```

---

## 🌍 compatibilidad

| sistema | estado | notas |
|---|---|---|
| arch / derivadas | (◕‿◕) | soporte nativo perfecto |
| debian / ubuntu | (◕‿◕) | soporte nativo |
| windows | (◕‿◕) | usa %APPDATA% y requiere consola con UTF-8 |
| macos | (◕‿◕) | requiere brew para mpv/chafa |
| termux (android) | (◕‿◕) | abre la app de android de vlc automáticamente |

---

## 📡 estado de las fuentes

akari realiza búsquedas concurrentes para máxima velocidad ヾ(≧ω≦*)ﾉ.

| fuente | estado | contenido |
|---|---|---|
| jkanime | (^▽^) estable | subs m3u8 directos |
| tioanime | (^▽^) estable | subs/doblaje |
| animefenix | (×_×) fuera de línea | servidor sin respuesta, desactivado temporalmente |
| animeid | (×_×) dominio comprometido | redirige fuera del servicio, desactivado por seguridad |
| monoschinos | (^▽^) estable | enfocado en latino |
| animeflv | (×_×) reproducción no disponible | devuelve episodios sin servidores, desactivado temporalmente |

---

## 🚀 roadmap

- [x] más fuentes de anime en español (TioAnime, MonosChinos, etc.) ✧(◡ ω ◡)
- [x] portadas en terminal con chafa ✧(◡ ω ◡)
- [x] guardar progreso de reproducción (minuto exacto en SQLite) ✧(◡ ω ◡)
- [x] catálogo por géneros ✧(◡ ω ◡)
- [x] soporte multiplataforma nativo para Windows ✧(◡ ω ◡)
- [ ] soporte oficial para Anime AV1 (•ˋ _ ˊ•)
- [ ] notificaciones de nuevos episodios (•ˋ _ ˊ•)
- [ ] bypass para Cloudflare en AnimeFLV (•ˋ _ ˊ•)
- [ ] paquete en AUR (akari-cli-git) (•ˋ _ ˊ•)

---

## (｡>﹏<｡) apoyar el proyecto

akari es y será siempre gratuito. si te gusta y quieres apoyar el desarrollo (café, ramen, servidores) puedes donar en [ko-fi](https://ko-fi.com/akuumi) — es completamente voluntario y no da ninguna ventaja ni acceso especial, pero te lo agradeceremos mucho ╰(◡‿◡╰).

---

## (シ_ _)シ aviso legal

akari-cli es una herramienta open-source creada con fines educativos y de entretenimiento personal ( •̯ˍ•̯ ).

este proyecto no hostea ni distribuye ningún contenido con derechos de autor.
solo actúa como cliente que parsea fuentes públicas de terceros disponibles en internet.
el uso depende de la disponibilidad y legalidad de dichas fuentes en tu país o región.
no nos hacemos responsables del contenido accedido, ni promovemos la infracción de derechos de autor.

recomendamos usar servicios legales como crunchyroll, netflix, hidive o amazon prime para apoyar a los creadores de la industria.

si eres titular de derechos y consideras que alguna fuente viola tus copyrights, contacta directamente al proveedor de la web fuente — no a este repositorio.

este proyecto es gratuito, sin fines de lucro y de uso personal/comunitario. cualquier donación es voluntaria y solo para apoyar el tiempo de desarrollo de la herramienta en código. uso bajo tu propio riesgo (￣^￣).

---

## (๑˃̵ᴗ˂̵) créditos

inspirado originalmente por la magia y simplicidad de ani-cli ヾ(＾-＾)ノ.
