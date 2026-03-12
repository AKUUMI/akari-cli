## 1.3.1
- versión dinámica en el banner
- clear al salir
- log de actividad en ~/.config/akari/akari.log
- explorar por género movido al roadmap (JKAnime no soporta filtro estático)

# changelog

## 1.3.0
- explorar anime por género directamente desde el menú
- info del anime antes de elegir episodio (sinopsis, estado, año, géneros)
- autoplay con cuenta regresiva de 5s cancelable con Enter
- soporte para Termux / Android — abre VLC automáticamente
- portadas en ASCII con chafa si está instalado (opcional)
- historial muestra el minuto donde quedaste

## 1.2.2
- reanudar desde el minuto exacto donde cerraste mpv
- botón [f] para agregar a favoritos desde el menú post-reproducción
- URL directa visible cuando no hay reproductor o fallan todos los servidores

## 1.2.1
- fuente única: JKAnime (streams m3u8 directos, sin depender de yt-dlp)
- animeFLV y TioAnime desactivadas temporalmente
- comando global `akari` disponible tras instalar con pip

## 1.2.0 (beta)
- scraper JKAnime corregido — búsqueda funcionando para todos los títulos
- TioAnime añadido como fuente (experimental)

## 0.1.0 (alpha)
- primera versión funcional
- JKAnime, AnimeFLV y TioAnime como fuentes
- historial SQLite, favoritos, reproductor mpv/vlc
