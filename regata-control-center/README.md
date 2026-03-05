# Regata Control Center

Central de controle completa para **KDE Plasma 6+** e **RegataOS**.

## Instalação

```bash
bash install.sh
```

O script instala automaticamente em:
- `~/.local/share/regata-control-center/` — arquivos do app
- `~/.local/bin/regata-control-center` — executável
- `~/.local/share/applications/` — entrada no menu KDE
- `~/.local/share/icons/` — ícone

## Dependências

- Python 3.8+
- PyQt6 + PyQt6-WebEngine (ou PyQt5 + PyQtWebEngine)

```bash
pip3 install PyQt6 PyQt6-WebEngine --user
# ou via pacotes do sistema:
sudo apt install python3-pyqt6-webengine
```

## Execução

```bash
regata-control-center
# ou
python3 ~/.local/share/regata-control-center/regata-control-center.py
```

## Estrutura

```
regata-control-center/
├── regata-control-center.html   # Interface web (HTML/CSS/JS)
├── regata-control-center.py     # Wrapper Qt WebEngine
├── install.sh                   # Instalador automático
└── README.md
```
