# changelog

## 1.5.0
- soporte total para Windows:
  - migración de rutas de configuración y logs a `%APPDATA%`
  - parche de codificación UTF-8 forzado para evitar crasheos por caracteres especiales en la terminal
  - comandos de sistema adaptados (`cls` para limpiar pantalla, `os.startfile` para abrir el navegador)
  - corrección de permisos en archivos temporales generados para `chafa`
  - manejo de saltos de línea (`\r\n`) corregido al interpretar salidas de `yt-dlp`
- nueva estética "Moe" y rediseño de UI:
  - banner ASCII completamente nuevo con temática kawaii (🎀✨)
  - transición de colores base-256 a códigos hexadecimales pastel (rosa, lavanda, dorado) para asegurar un renderizado perfecto en cualquier terminal
- optimización masiva de scrapers:
  - implementación de `concurrent.futures` para ejecutar búsquedas simultáneas en múltiples fuentes, eliminando los cuellos de botella
  - estructuración y preparación de nuevas fuentes (AnimeFenix, AnimeID, MonosChinos, TioAnime) con soporte para doblaje latino
- testing:
  - pruebas unitarias de `pytest` parcheadas para aislar el directorio base en entornos locales
  - validación de migraciones de la base de datos (guardado de minutos)

## 1.4.2
- opción [0] para volver desde resultados de búsqueda
- eliminar favoritos con [d+número] desde el menú de favoritos
- ver anime directo desde favoritos

## 1.4.1
- autoplay solo cuando mpv termina el video naturalmente, no al cerrar con q
- fix chafa — portadas ASCII ahora se muestran correctamente

## 1.4.0
- catálogo local por género con paginación (5 por página)
- géneros disponibles: acción, romance, comedia, terror, fantasía, shounen, seinen, shoujo, yuri, ecchi, psicológico, deportes
- portadas en ASCII con chafa si está instalado
- slugs verificados para JKAnime

## 1.3.1
- versión dinámica en el banner
- clear al salir
- log de actividad en ~/.config/akari/akari.log
- explorar por género movido al roadmap (JKAnime no soporta filtro estático)

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