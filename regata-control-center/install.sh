#!/usr/bin/env bash
#  Regata Control Center — Script de Instalação
#  Instala em ~/.local/share/regata-control-center e registra no menu do KDE

set -euo pipefail

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; BOLD='\033[1m'; NC='\033[0m'

info()    { echo -e "${BLUE}[INFO]${NC}  $*"; }
success() { echo -e "${GREEN}[OK]${NC}    $*"; }
warn()    { echo -e "${YELLOW}[AVISO]${NC} $*"; }
error()   { echo -e "${RED}[ERRO]${NC}  $*" >&2; exit 1; }

INSTALL_DIR="${HOME}/.local/share/regata-control-center"
BIN_DIR="${HOME}/.local/bin"
APP_DIR="${HOME}/.local/share/applications"
ICON_DIR="${HOME}/.local/share/icons/hicolor/scalable/apps"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "\n${BOLD}Regata Control Center — Instalador${NC}"
echo "────────────────────────────────────────"

# Verificar Python3
if ! command -v python3 &>/dev/null; then
    error "Python3 não encontrado. Instale com: sudo apt install python3"
fi
success "Python3 encontrado: $(python3 --version)"

# Verificar PyQt6 ou PyQt5 com WebEngine
HAS_PYQT=false
if python3 -c "from PyQt6.QtWebEngineWidgets import QWebEngineView" 2>/dev/null; then
    success "PyQt6 com WebEngine encontrado"
    HAS_PYQT=true
elif python3 -c "from PyQt5.QtWebEngineWidgets import QWebEngineView" 2>/dev/null; then
    success "PyQt5 com WebEngine encontrado"
    HAS_PYQT=true
fi

if [ "$HAS_PYQT" = false ]; then
    warn "PyQt6/PyQt5 com WebEngine não encontrado."
    echo -e "  Tentando instalar via pip..."
    if pip3 install PyQt6 PyQt6-WebEngine --user --quiet 2>/dev/null; then
        success "PyQt6 instalado com sucesso"
    elif pip3 install PyQt5 PyQtWebEngine --user --quiet 2>/dev/null; then
        success "PyQt5 instalado com sucesso"
    else
        warn "Instalação automática falhou. Instale manualmente:"
        echo "  pip3 install PyQt6 PyQt6-WebEngine --user"
        echo "  ou: sudo apt install python3-pyqt6-webengine"
    fi
fi

info "Criando diretórios..."
mkdir -p "$INSTALL_DIR" "$BIN_DIR" "$APP_DIR" "$ICON_DIR"
success "Diretórios criados"

info "Instalando arquivos em $INSTALL_DIR..."
cp -f "$SCRIPT_DIR/regata-control-center.html" "$INSTALL_DIR/"
cp -f "$SCRIPT_DIR/regata-control-center.py"   "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/regata-control-center.py"
success "Arquivos copiados"

info "Criando executável em $BIN_DIR..."
cat > "$BIN_DIR/regata-control-center" << 'LAUNCHER'
#!/usr/bin/env bash
exec python3 "${HOME}/.local/share/regata-control-center/regata-control-center.py" "$@"
LAUNCHER
chmod +x "$BIN_DIR/regata-control-center"
success "Executável criado: $BIN_DIR/regata-control-center"

info "Instalando ícone..."
cat > "$ICON_DIR/regata-control-center.svg" << 'SVG'
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48">
  <defs>
    <linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#5b6cf8"/>
      <stop offset="100%" style="stop-color:#7c3aed"/>
    </linearGradient>
  </defs>
  <rect width="48" height="48" rx="12" fill="url(#grad)"/>
  <path d="M24 8L10 15v9c0 8.3 5.9 16.1 14 18 8.1-1.9 14-9.7 14-18v-9L24 8z"
    fill="none" stroke="white" stroke-width="2.5" stroke-linejoin="round"/>
  <circle cx="24" cy="24" r="4" fill="white"/>
  <path d="M24 14v2M24 32v2M14 24h2M32 24h2M16.93 16.93l1.41 1.41M29.66 29.66l1.41 1.41M16.93 31.07l1.41-1.41M29.66 18.34l1.41-1.41"
    stroke="white" stroke-width="2" stroke-linecap="round"/>
</svg>
SVG
success "Ícone instalado"

info "Registrando no menu de aplicativos..."
cat > "$APP_DIR/regata-control-center.desktop" << DESKTOP
[Desktop Entry]
Version=1.0
Type=Application
Name=Regata Control Center
Name[pt_BR]=Central de Controle Regata
Comment=Centro de controle completo para KDE Plasma 6
Comment[pt_BR]=Gerencie todas as configurações do seu sistema Regata OS
Exec=${BIN_DIR}/regata-control-center
Icon=regata-control-center
Terminal=false
StartupNotify=true
StartupWMClass=regata-control-center
Categories=Settings;System;Qt;KDE;
Keywords=configurações;sistema;kde;plasma;controle;settings;control;
X-KDE-SubstituteUID=false
X-GNOME-UsesNotifications=false
MimeType=
DESKTOP

success "Arquivo .desktop criado"

info "Atualizando cache do sistema..."
if command -v update-desktop-database &>/dev/null; then
    update-desktop-database "$APP_DIR" 2>/dev/null || true
fi
if command -v gtk-update-icon-cache &>/dev/null; then
    gtk-update-icon-cache -f -t "$HOME/.local/share/icons/hicolor" 2>/dev/null || true
fi
if command -v kbuildsycoca6 &>/dev/null; then
    kbuildsycoca6 --noincremental 2>/dev/null || true
elif command -v kbuildsycoca5 &>/dev/null; then
    kbuildsycoca5 --noincremental 2>/dev/null || true
fi
success "Cache atualizado"

if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    warn "$BIN_DIR não está no seu PATH."
    echo "  Adicione ao ~/.bashrc ou ~/.profile:"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

echo ""
echo -e "${BOLD}${GREEN}✓ Instalação concluída!${NC}"
echo "────────────────────────────────────────"
echo -e "  App instalado em: ${BOLD}$INSTALL_DIR${NC}"
echo -e "  Executável:       ${BOLD}$BIN_DIR/regata-control-center${NC}"
echo -e "  Atalho no menu:   ${BOLD}$APP_DIR/regata-control-center.desktop${NC}"
echo ""
echo "  Para executar:"
echo -e "    ${BOLD}regata-control-center${NC}  (se \$HOME/.local/bin estiver no PATH)"
echo -e "    ${BOLD}python3 $INSTALL_DIR/regata-control-center.py${NC}"
echo ""
echo "  Ou procure por 'Regata Control Center' no lançador de aplicativos."
echo ""
