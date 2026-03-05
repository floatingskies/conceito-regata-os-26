#!/bin/bash
# ============================================================
#  RegataOS Welcome App — Script de instalação
# ============================================================

set -e

echo ""
echo "  ⚓  RegataOS Welcome App — Instalador"
echo "  ======================================"
echo ""

# Verifica Python 3
if ! command -v python3 &>/dev/null; then
  echo "  ✗ Python 3 não encontrado. Instale com:"
  echo "    sudo dnf install python3"
  exit 1
fi

echo "  ✓ Python 3 encontrado: $(python3 --version)"

# Instala dependências
echo ""
echo "  → Instalando PyQt6 e PyQt6-WebEngine..."
pip3 install --user --quiet PyQt6 PyQt6-WebEngine 2>&1 | tail -3

echo ""
echo "  ✓ Dependências instaladas com sucesso!"
echo ""
echo "  → Para iniciar o app:"
echo "     python3 welcome.py"
echo ""

# Pergunta se quer executar agora
read -rp "  Deseja iniciar o app agora? [s/N] " resp
if [[ "$resp" =~ ^[Ss]$ ]]; then
  python3 "$(dirname "$0")/welcome.py"
fi
