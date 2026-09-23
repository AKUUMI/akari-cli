```
      ✧･ﾟ: *✧･ﾟ:*  ♡ (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧  ♡  *:･ﾟ✧*:･ﾟ✧
     █████╗ ██╗  ██╗ █████╗ ██████╗ ██╗
    ██╔══██╗██║ ██╔╝██╔══██╗██╔══██╗██║
    ███████║█████╔╝ ███████║██████╔╝██║
    ██╔══██║██╔═██╗ ██╔══██║██╔══██╗██║
    ██║  ██║██║  ██╗██║  ██║██║  ██║██║
    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝
          (˶˃ ᵕ ˂˶) ア カ リ 1.7.0 (˶˃ ᵕ ˂˶)
      ✧･ﾟ: *✧･ﾟ:*  ♡ ૮ ˶ᵔ ᵕ ᵔ˶ ა ♡  *:･ﾟ✧*:･ﾟ✧
```

Akari es un cliente de anime en español para la terminal, inspirado en la sencillez de ani-cli. Puede buscar, reproducir y descargar episodios desde varias fuentes, mostrar portadas con Chafa y guardar tu progreso localmente. Funciona en Windows, Linux, macOS y Android mediante Termux. (｡•̀ᴗ-)✧

El nombre es por alguien especial. (◡‿◡✿)

---

## Qué necesitas

No hace falta saber programar. Solo necesitas instalar estas herramientas:

- Python 3.10 o una versión posterior.
- Git para descargar y actualizar Akari.
- mpv para reproducir los capítulos.
- Chafa si quieres ver las portadas dentro de la terminal.
- Una conexión a Internet.

`yt-dlp` y las demás librerías de Python se instalan automáticamente junto con Akari.

---

## Instalar en Windows

### 1. Instala Python

Descarga Python desde [python.org](https://www.python.org/downloads/). Durante la instalación marca la casilla `Add Python to PATH` y después continúa con la instalación normal.

Abre PowerShell y comprueba que funciona:

```powershell
python --version
```

Debe aparecer Python 3.10 o una versión posterior.

### 2. Instala Git

Descarga Git desde [git-scm.com](https://git-scm.com/download/win) y usa las opciones recomendadas del instalador.

Comprueba la instalación:

```powershell
git --version
```

### 3. Instala mpv

La forma más sencilla es usar Scoop. Copia estos comandos en PowerShell, uno por uno:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
scoop bucket add extras
scoop install mpv
```

Comprueba que mpv está disponible:

```powershell
mpv --version
```

### 4. Instala Chafa

Chafa es opcional. Akari funciona sin él, pero no mostrará las portadas en la terminal.

```powershell
winget install --id hpjansson.Chafa --exact
```

Si acabas de instalar mpv o Chafa, cierra PowerShell y vuelve a abrirlo antes de continuar.

### 5. Descarga Akari

Elige una carpeta donde quieras guardar el programa, abre PowerShell en ella y ejecuta:

```powershell
git clone https://github.com/AKUUMI/akari-cli.git
cd akari-cli
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
akari
```

La ventana mostrará el menú principal cuando todo esté listo. ヽ(・∀・)ﾉ

### Abrir Akari otro día

No necesitas instalarlo nuevamente. Abre PowerShell, entra en su carpeta y ejecuta:

```powershell
cd C:\ruta\donde\guardaste\akari-cli
.\.venv\Scripts\Activate.ps1
akari
```

Sustituye la ruta del ejemplo por la ubicación real de tu carpeta.

---

## Instalar en Linux

El instalador reconoce Arch, Debian, Ubuntu, Fedora, openSUSE, Void, Alpine y Gentoo.

```bash
git clone https://github.com/AKUUMI/akari-cli.git
cd akari-cli
chmod +x install.sh
./install.sh
```

Al terminar, sigue la indicación que aparezca en la terminal para iniciar Akari.

### Instalación manual en Linux o macOS

Instala primero Python, Git, mpv y Chafa con el gestor de paquetes de tu sistema. Después ejecuta:

```bash
git clone https://github.com/AKUUMI/akari-cli.git
cd akari-cli
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
akari
```

---

## Instalar en Termux

Instala Termux desde F-Droid y abre la aplicación. Después copia estos comandos:

```bash
pkg update
pkg install git
git clone https://github.com/AKUUMI/akari-cli.git
cd akari-cli
chmod +x install.sh
./install.sh
```

Para guardar descargas en la carpeta compartida de Android, ejecuta una vez:

```bash
termux-setup-storage
```

Android pedirá permiso para acceder a los archivos. También necesitas tener VLC instalado para reproducir capítulos desde Termux. (´･ω･`)

---

## Cómo usar Akari

El menú principal muestra estas opciones:

```text
[b] Buscar anime
[c] Continuar viendo
[d] Descargar episodios
[f] Favoritos
[h] Historial completo
[q] Salir
```

Para ver un anime:

1. Escribe `b` y presiona Enter.
2. Escribe el nombre del anime.
3. Elige un resultado escribiendo su número.
4. Escribe el número del episodio.
5. Elige qué quieres hacer.

```text
[v] Ver
[d] Descargar uno
[m] Descargar varios
[q] Volver
```

### Descargar varios capítulos

Puedes escribir una sola lista, un rango o una combinación:

```text
1-12
1,4,8
1-5,10-12
```

Akari comprobará que los episodios existan y mostrará cuántos descargará antes de pedir confirmación. Si un servidor falla, intentará con los siguientes disponibles.

Las descargas se guardan aquí:

| Sistema | Carpeta |
|---|---|
| Windows | `C:\Users\TU_USUARIO\Downloads\Akari` |
| Linux y macOS | `~/Downloads/Akari` |
| Termux | `~/storage/downloads/Akari` |

### Comandos directos

También puedes usar Akari sin entrar primero al menú:

```bash
akari buscar "attack on titan"
akari historial
akari favoritos
akari descargar "naruto" --episodios "1-3,5" --fuente JKAnime --destino "./descargas"
```

---

## Actualizar Akari

Activa el mismo entorno virtual con el que instalaste Akari y ejecuta desde cualquier carpeta:

```bash
akari update
```

El comando localiza el repositorio asociado a esa instalación, obtiene `origin/main` y avanza `main` sin crear ramas ni commits de mezcla. Después reinstala Akari y las dependencias necesarias con el mismo Python. Al terminar, vuelve a abrir `akari`.

Necesitas Git, conexión a Internet y una instalación hecha con `python -m pip install -e .`. El comando se detiene si estás en otra rama, tienes cambios locales en archivos versionados o commits propios pendientes. No borra archivos, historial, favoritos ni descargas. Git también bloquea la actualización si un archivo sin seguimiento sería sobrescrito.

Si el repositorio se actualiza pero falla la instalación de dependencias, corrige la conexión o el error mostrado y repite `akari update`.

### Primera actualización desde una versión anterior

Las versiones anteriores a 1.7.0 todavía no tienen este comando. Desde la carpeta del repositorio y con tu entorno virtual activo, ejecuta una vez:

```bash
git pull --ff-only origin main
python -m pip install -e .
```

Después podrás usar siempre `akari update`.

### Novedades de 1.7.0

- Actualización automática con `akari update`.
- Caché de 60 segundos para acelerar las fichas y búsquedas repetidas.
- Resultados paginados y opción de volver al elegir capítulos o descargas.
- Descargas desde el menú y con `akari descargar`, carpeta configurable y reanudación de archivos parciales.
- Retirada de AnimeFLV, AnimeFenix y AnimeID tras comprobar sus fallos.
- JKAnime, TioAnime y MonosChinos conservadas tras verificar resolución de video.

Consulta todos los cambios en [CHANGELOG.md](CHANGELOG.md).

---

## Estado de compatibilidad

| Sistema | Estado | Notas |
|---|---|---|
| Windows | (＾▽＾) probado | Compatible con mpv, Chafa y descargas |
| Ubuntu y Debian | (＾▽＾) probado automáticamente | Instalación mediante `install.sh` |
| Arch y derivadas | (＾▽＾) compatible | Instalación mediante `install.sh` |
| macOS | (＾▽＾) probado automáticamente | Requiere instalar mpv y Chafa por separado |
| Termux | (＾▽＾) compatible | Reproduce mediante VLC para Android |

Las pruebas automáticas se ejecutan en Windows, Ubuntu y macOS con Python 3.10 y 3.12.

---

## Estado de las fuentes

Akari consulta las fuentes activas al mismo tiempo para que las búsquedas sean rápidas. ヾ(≧▽≦*)o

| Fuente | Estado | Notas |
|---|---|---|
| JKAnime | (＾▽＾) activa | Episodios subtitulados y streams directos |
| TioAnime | (＾▽＾) activa | Varias opciones de reproducción |
| MonosChinos | (＾▽＾) activa | Contenido subtitulado y latino |
| AnimeFLV | retirada | Búsquedas sin respuesta en la revisión del 22-09-2026 |
| AnimeFenix | retirada | Conexión agotada en la revisión del 22-09-2026 |
| AnimeID | retirada | Redirige a TikTok |

Las páginas externas pueden cambiar sin aviso. Las fuentes retiradas ya no forman parte del código. La revisión comprobó búsqueda, episodios y resolución de video en las tres fuentes conservadas; algunos servidores individuales fallan.

Las respuestas correctas se reutilizan durante 60 segundos (hasta 64 páginas). Los errores no se guardan. Los resultados aparecen en páginas de diez; usa `n`, `p` y `q` para navegar. Puedes volver con `q` al elegir episodios o un lote de descargas. Las descargas conservan archivos parciales para reanudarlos al repetir la misma selección con el mismo servidor y carpeta.

---

## Solución de problemas

### `python`, `git`, `mpv` o `chafa` no se reconoce como comando

Cierra la terminal, vuelve a abrirla y prueba otra vez. Si el problema continúa, confirma que la herramienta fue instalada y añadida al `PATH`.

### PowerShell no permite activar `.venv`

Ejecuta una vez:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Después vuelve a ejecutar `.\.venv\Scripts\Activate.ps1`.

### No aparece una portada

Akari continúa funcionando aunque Chafa no esté instalado o la fuente no entregue una imagen. Comprueba la instalación con:

```bash
chafa --version
```

### Un capítulo no reproduce o no descarga

Los videos pertenecen a servicios externos. Akari intenta varias opciones, pero puede ocurrir que todas estén temporalmente caídas. Prueba nuevamente más tarde u otro resultado del mismo anime.

---

## Aviso legal

Akari CLI es una herramienta de código abierto creada con fines educativos y para uso personal.

El proyecto no aloja, copia ni distribuye videos. Solo interpreta información disponible en páginas públicas de terceros. La disponibilidad y legalidad de esas páginas depende de cada país. Usa Akari bajo tu responsabilidad y considera servicios oficiales como Crunchyroll, Netflix, HIDIVE o Amazon Prime para apoyar a los creadores.

Si eres titular de derechos, cualquier reclamación relacionada con un video debe dirigirse al sitio externo que lo aloja, no a este repositorio.

---

## Apoyar el proyecto

Akari es gratuito y ninguna donación desbloquea funciones. Si deseas apoyar voluntariamente el tiempo de desarrollo, puedes hacerlo en [Ko-fi](https://ko-fi.com/akuumi). (づ｡◕‿‿◕｡)づ

---

## Créditos

Inspirado por la magia y sencillez de ani-cli. (シ_ _)シ
