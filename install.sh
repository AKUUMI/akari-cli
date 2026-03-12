#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────
#  ✦ Akari — Script de instalación universal para Linux 🕊️
#  Soporta: Arch, Debian, Ubuntu, Mint, Fedora, openSUSE,
#           Kali, Manjaro, EndeavourOS, Pop!_OS, Void, Alpine
# ─────────────────────────────────────────────────────────────────

set -e

# ── Colores ───────────────────────────────────────────────────────
LAVANDA='\033[38;5;183m'
ROSA='\033[38;5;219m'
DORADO='\033[38;5;220m'
VERDE='\033[38;5;157m'
GRIS='\033[38;5;245m'
RESET='\033[0m'
BOLD='\033[1m'

# ── Banner ────────────────────────────────────────────────────────
echo ""
echo -e "${LAVANDA}    ✦ · . ˚ ✦ · . ˚ ✦ · . ˚ ✦ · . ˚ ✦ · . ˚ ✦${RESET}"
echo -e "${BOLD}   █████╗ ██╗  ██╗ █████╗ ██████╗ ██╗${RESET}"
echo -e "${BOLD}  ██╔══██╗██║ ██╔╝██╔══██╗██╔══██╗██║${RESET}"
echo -e "${BOLD}  ███████║█████╔╝ ███████║██████╔╝██║${RESET}"
echo -e "${BOLD}  ██╔══██║██╔═██╗ ██╔══██║██╔══██╗██║${RESET}"
echo -e "${BOLD}  ██║  ██║██║  ██╗██║  ██║██║  ██║███████╗${RESET}"
echo -e "${BOLD}  ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝${RESET}"
echo -e "${DORADO}        ✧  ア カ リ  ✧   instalador 🕊️${RESET}"
echo -e "${LAVANDA}    ✦ · . ˚ ✦ · . ˚ ✦ · . ˚ ✦ · . ˚ ✦ · . ˚ ✦${RESET}"
echo ""

# ── Funciones de log ──────────────────────────────────────────────
info()    { echo -e "${LAVANDA}  ✦ ${1}${RESET}"; }
ok()      { echo -e "${VERDE}  ✓ ${1}${RESET}"; }
warn()    { echo -e "${DORADO}  ⚠ ${1}${RESET}"; }
error()   { echo -e "${ROSA}  ✗ ${1}${RESET}"; exit 1; }
step()    { echo -e "\n${BOLD}${LAVANDA}  ── ${1} ──${RESET}\n"; }

# ── Detectar distro ───────────────────────────────────────────────
detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        DISTRO_ID="${ID}"
        DISTRO_LIKE="${ID_LIKE:-}"
        DISTRO_NAME="${NAME}"
    elif command -v lsb_release &>/dev/null; then
        DISTRO_ID=$(lsb_release -si | tr '[:upper:]' '[:lower:]')
        DISTRO_LIKE=""
        DISTRO_NAME=$(lsb_release -sd)
    else
        error "No se pudo detectar la distribución Linux."
    fi
}

# ── Detectar gestor de paquetes ───────────────────────────────────
detect_pkg_manager() {
    if command -v pacman &>/dev/null; then
        PKG="pacman"
    elif command -v apt-get &>/dev/null; then
        PKG="apt"
    elif command -v dnf &>/dev/null; then
        PKG="dnf"
    elif command -v zypper &>/dev/null; then
        PKG="zypper"
    elif command -v xbps-install &>/dev/null; then
        PKG="xbps"
    elif command -v apk &>/dev/null; then
        PKG="apk"
    elif command -v emerge &>/dev/null; then
        PKG="emerge"
    else
        error "Gestor de paquetes no soportado."
    fi
}

# ── Instalar dependencias del sistema ─────────────────────────────
install_system_deps() {
    step "Instalando dependencias del sistema"
    info "Distro detectada: ${DISTRO_NAME} (gestor: ${PKG})"

    case "$PKG" in
        pacman)
            # Arch, Manjaro, EndeavourOS, Garuda, etc.
            sudo pacman -Sy --noconfirm --needed mpv python python-pip python-virtualenv git ffmpeg
            ;;
        apt)
            # Debian, Ubuntu, Mint, Kali, Pop!_OS, MX Linux, etc.
            sudo apt-get update -qq
            sudo apt-get install -y mpv python3 python3-pip python3-venv git ffmpeg
            ;;
        dnf)
            # Fedora, RHEL, AlmaLinux, Rocky Linux
            sudo dnf install -y mpv python3 python3-pip git ffmpeg
            ;;
        zypper)
            # openSUSE Leap / Tumbleweed
            sudo zypper install -y mpv python3 python3-pip git ffmpeg
            ;;
        xbps)
            # Void Linux
            sudo xbps-install -Sy mpv python3 python3-pip git ffmpeg
            ;;
        apk)
            # Alpine Linux
            sudo apk add --no-cache mpv python3 py3-pip git ffmpeg
            ;;
        emerge)
            # Gentoo
            sudo emerge --ask n media-video/mpv dev-lang/python dev-vcs/git media-video/ffmpeg
            ;;
    esac

    ok "Dependencias instaladas"
}

# ── Verificar Python 3.8+ ─────────────────────────────────────────
check_python() {
    step "Verificando Python"
    PYTHON_BIN=""
    for py in python3 python; do
        if command -v "$py" &>/dev/null; then
            VER=$($py -c "import sys; print(sys.version_info >= (3,8))" 2>/dev/null)
            if [ "$VER" = "True" ]; then
                PYTHON_BIN="$py"
                PY_VERSION=$($py --version)
                ok "Encontrado: ${PY_VERSION}"
                break
            fi
        fi
    done
    [ -z "$PYTHON_BIN" ] && error "Se requiere Python 3.8 o superior."
}

# ── Configurar entorno virtual ────────────────────────────────────
setup_venv() {
    step "Configurando entorno virtual"
    INSTALL_DIR="$HOME/.local/share/akari"
    mkdir -p "$INSTALL_DIR"

    if [ ! -d "$INSTALL_DIR/.venv" ]; then
        $PYTHON_BIN -m venv "$INSTALL_DIR/.venv"
        ok "Virtualenv creado en $INSTALL_DIR/.venv"
    else
        ok "Virtualenv ya existe"
    fi

    # Actualizar pip dentro del venv
    "$INSTALL_DIR/.venv/bin/pip" install --upgrade pip -q
}

# ── Instalar Akari ────────────────────────────────────────────────
install_akari() {
    step "Instalando Akari"
    INSTALL_DIR="$HOME/.local/share/akari"
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

    "$INSTALL_DIR/.venv/bin/pip" install -e "$SCRIPT_DIR" -q
    ok "Akari instalado"
}

# ── Crear lanzador global ─────────────────────────────────────────
create_launcher() {
    step "Creando comando 'akari'"
    INSTALL_DIR="$HOME/.local/share/akari"
    BIN_DIR="$HOME/.local/bin"
    mkdir -p "$BIN_DIR"

    cat > "$BIN_DIR/akari" << EOF
#!/usr/bin/env bash
exec "$INSTALL_DIR/.venv/bin/akari" "\$@"
EOF
    chmod +x "$BIN_DIR/akari"
    ok "Lanzador creado en $BIN_DIR/akari"

    # Verificar que ~/.local/bin esté en PATH
    if ! echo "$PATH" | grep -q "$BIN_DIR"; then
        warn "~/.local/bin no está en tu PATH."
        echo ""

        # Detectar shell del usuario
        SHELL_NAME=$(basename "$SHELL")
        case "$SHELL_NAME" in
            zsh)  RC_FILE="$HOME/.zshrc" ;;
            fish) RC_FILE="$HOME/.config/fish/config.fish" ;;
            *)    RC_FILE="$HOME/.bashrc" ;;
        esac

        echo -e "${LAVANDA}  Agrega esto a tu ${RC_FILE}:${RESET}"
        echo -e "${DORADO}    export PATH=\"\$HOME/.local/bin:\$PATH\"${RESET}"
        echo ""

        read -rp "  ¿Lo agrego automáticamente? [S/n]: " RESP
        RESP="${RESP:-S}"
        if [[ "$RESP" =~ ^[Ss]$ ]]; then
            if [ "$SHELL_NAME" = "fish" ]; then
                mkdir -p "$(dirname "$RC_FILE")"
                echo 'set -gx PATH $HOME/.local/bin $PATH' >> "$RC_FILE"
            else
                echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$RC_FILE"
            fi
            ok "PATH actualizado en $RC_FILE"
            warn "Ejecuta: source ${RC_FILE}  (o abre una terminal nueva)"
        fi
    fi
}

# ── Verificar mpv ─────────────────────────────────────────────────
check_mpv() {
    step "Verificando reproductor"
    if command -v mpv &>/dev/null; then
        MPV_VER=$(mpv --version | head -1)
        ok "mpv encontrado: ${MPV_VER}"
    else
        warn "mpv no encontrado. Akari usará vlc como respaldo."
        if command -v vlc &>/dev/null; then
            ok "vlc encontrado como respaldo"
        else
            warn "Ningún reproductor encontrado. Instala mpv manualmente."
        fi
    fi
}

# ── Resumen final ─────────────────────────────────────────────────
show_summary() {
    echo ""
    echo -e "${LAVANDA}    ✦ · . ˚ ✦ · . ˚ ✦ · . ˚ ✦ · . ˚ ✦ · . ˚ ✦${RESET}"
    echo -e "${VERDE}${BOLD}  ✦ ¡Akari instalado exitosamente! 🕊️${RESET}"
    echo ""
    echo -e "${DORADO}  Para empezar:${RESET}"
    echo -e "${GRIS}    akari                     ${LAVANDA}# modo interactivo${RESET}"
    echo -e "${GRIS}    akari buscar \"naruto\"      ${LAVANDA}# búsqueda directa${RESET}"
    echo -e "${GRIS}    akari historial            ${LAVANDA}# ver historial${RESET}"
    echo ""
    echo -e "${ROSA}  Si 'akari' no funciona, ejecuta:${RESET}"
    echo -e "${GRIS}    source ~/.bashrc  (bash)${RESET}"
    echo -e "${GRIS}    source ~/.zshrc   (zsh)${RESET}"
    echo -e "${LAVANDA}    ✦ · . ˚ ✦ · . ˚ ✦ · . ˚ ✦ · . ˚ ✦ · . ˚ ✦${RESET}"
    echo ""
}

# ── Main ──────────────────────────────────────────────────────────
main() {
    detect_distro
    detect_pkg_manager
    install_system_deps
    check_python
    setup_venv
    install_akari
    create_launcher
    check_mpv
    show_summary
}

main
