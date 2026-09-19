#!/usr/bin/env bash
set -euo pipefail

INSTALL_DIR="${INSTALL_DIR:-$HOME/.local/share/HymnOS}"
VENV_DIR="${VENV_DIR:-$INSTALL_DIR/venv}"
DESKTOP_FILE="$HOME/.local/share/applications/HymnOS.desktop"
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

PKG_MANAGER=""
PKG_INSTALL_CMD=""
SYSTEM_PKGS=""

for arg in "$@"; do
    case "$arg" in
        --system-deps) INSTALL_SYSTEM_DEPS=1 ;;
        *) echo "Unknown argument: $arg" >&2; exit 1 ;;
    esac
done

detect_python() {
    if command -v python3 >/dev/null 2>&1; then
        echo "$(command -v python3)"
    elif command -v python >/dev/null 2>&1; then
        echo "$(command -v python)"
    else
        echo ""
    fi
}

detect_pkg_manager() {
    if command -v apt-get >/dev/null 2>&1; then
        PKG_MANAGER="apt"
        PKG_INSTALL_CMD="sudo apt-get update && sudo apt-get install -y --no-install-recommends"
        SYSTEM_PKGS="python3 python3-venv python3-pip libxcb-cursor0 libegl1 libgl1 libxkbcommon-x11-0 fontconfig libdbus-1-3"
    elif command -v dnf >/dev/null 2>&1; then
        PKG_MANAGER="dnf"
        PKG_INSTALL_CMD="sudo dnf install -y"
        SYSTEM_PKGS="python3 python3-pip python3-virtualenv libxcb-cursor mesa-libEGL mesa-libGL libxkbcommon-x11 fontconfig dbus-libs"
    elif command -v zypper >/dev/null 2>&1; then
        PKG_MANAGER="zypper"
        PKG_INSTALL_CMD="sudo zypper install -y"
        SYSTEM_PKGS="python3 python3-pip python3-virtualenv libxcb-cursor0 Mesa-libEGL1 Mesa-libGL1 libxkbcommon-x11-0 fontconfig libdbus-1-3"
    elif command -v pacman >/dev/null 2>&1; then
        PKG_MANAGER="pacman"
        PKG_INSTALL_CMD="sudo pacman -S --noconfirm --needed"
        SYSTEM_PKGS="python python-pip xcb-cursor mesa libxkbcommon-x11 fontconfig"
    elif command -v apk >/dev/null 2>&1; then
        PKG_MANAGER="apk"
        PKG_INSTALL_CMD="sudo apk add"
        SYSTEM_PKGS="python3 py3-pip py3-virtualenv libxcb-util-cursor mesa-gl libxkbcommon-x11 fontconfig"
    elif command -v xbps-install >/dev/null 2>&1; then
        PKG_MANAGER="xbps"
        PKG_INSTALL_CMD="sudo xbps-install -y"
        SYSTEM_PKGS="python3 python3-pip libxcb-cursor mesa libxkbcommon-x11-util fontconfig"
    elif command -v emerge >/dev/null 2>&1; then
        PKG_MANAGER="emerge"
        PKG_INSTALL_CMD="sudo emerge --ask=n --quiet"
        SYSTEM_PKGS="dev-lang/python dev-python/pip dev-python/virtualenv x11-libs/libxcb media-libs/mesa x11-libs/libxkbcommon media-libs/fontconfig"
    fi
}

install_system_deps() {
    detect_pkg_manager
    if [[ -z "$PKG_MANAGER" ]]; then
        echo "Could not detect a supported package manager." >&2
        echo "Install manually: Python 3, pip/venv support, and the PyQt6 runtime libraries." >&2
        exit 1
    fi
    echo "Installing system dependencies with $PKG_MANAGER ..."
    if ! eval "$PKG_INSTALL_CMD $SYSTEM_PKGS"; then
        echo "Warning: system package installation reported errors." >&2
        echo "Install the missing Python/Qt packages for your distro manually, then rerun without --system-deps." >&2
        exit 1
    fi
}

ensure_python_venv() {
    TMPVENV="$(mktemp -d)/venv"
    if ! "$PYTHON" -m venv "$TMPVENV" >/dev/null 2>&1; then
        rm -rf "${TMPVENV%/venv}"
        echo "Error: '$PYTHON' cannot create virtual environments." >&2
        echo "Install Python with venv support (e.g. python3-venv / python3-virtualenv) for your distro, then rerun." >&2
        exit 1
    fi
    rm -rf "${TMPVENV%/venv}"
}

check_qt_libraries() {
    missing=()
    for lib in libxcb-cursor.so.0 libEGL.so.1 libGL.so.1 libxkbcommon-x11.so.0; do
        if ! ldconfig -p 2>/dev/null | grep -qF "$lib"; then
            missing+=("$lib")
        fi
    done

    if [[ ${#missing[@]} -gt 0 ]]; then
        echo "Note: PyQt6 needs these libraries to display the window:" >&2
        printf '  - %s\n' "${missing[@]}" >&2
        echo "Rerun with './install.sh --system-deps' to install them for your distro, or install them manually." >&2
    fi
}

PYTHON="${PYTHON:-$(detect_python)}"

if [[ -n "${INSTALL_SYSTEM_DEPS:-}" ]]; then
    install_system_deps
    PYTHON="${PYTHON:-$(detect_python)}"
fi

if [[ -z "$PYTHON" ]]; then
    echo "Error: Python 3 was not found." >&2
    if [[ -z "${INSTALL_SYSTEM_DEPS:-}" ]]; then
        echo "Rerun with './install.sh --system-deps' to install Python for your distro." >&2
    fi
    exit 1
fi

ensure_python_venv
check_qt_libraries

echo "Installing HymnOS to $INSTALL_DIR ..."
mkdir -p "$INSTALL_DIR" "$HOME/.local/share/applications"

cp -r \
    "$SOURCE_DIR/main.py" \
    "$SOURCE_DIR/slideShow.py" \
    "$SOURCE_DIR/SettingsWindow.py" \
    "$SOURCE_DIR/settingsModal.py" \
    "$SOURCE_DIR/resources" \
    "$INSTALL_DIR/"

echo "Creating virtual environment..."
"$PYTHON" -m venv "$VENV_DIR"
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install PyQt6 screeninfo

cat > "$INSTALL_DIR/hymnos" <<EOF
#!/usr/bin/env bash
cd "$INSTALL_DIR"
exec "$VENV_DIR/bin/python" main.py
EOF
chmod +x "$INSTALL_DIR/hymnos"

cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Name=HymnOS
Comment=A PowerPoint type program for displaying hymns
Exec=$INSTALL_DIR/hymnos
Icon=$INSTALL_DIR/resources/gospel.png
Terminal=false
Type=Application
Categories=Utility;AudioVideo;
EOF
chmod +x "$DESKTOP_FILE"

if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$HOME/.local/share/applications" >/dev/null 2>&1 || true
fi

echo "Installation complete."
echo "Launch it from the application menu (HymnOS) or run: $INSTALL_DIR/hymnos"
echo "Uninstall by removing: $INSTALL_DIR, $DESKTOP_FILE"