#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regata Control Center — Qt WebEngine wrapper
Lança o HTML em uma janela nativa do KDE Plasma 6+ com integração Qt.
"""

import sys
import os
import subprocess
import shutil
from pathlib import Path

# ── Qt imports ──────────────────────────────────────────────────────────────
try:
    from PyQt6.QtCore    import QUrl, QObject, pyqtSlot, QTimer, Qt
    from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
    from PyQt6.QtWebEngineWidgets  import QWebEngineView
    from PyQt6.QtWebEngineCore     import QWebEngineSettings, QWebEnginePage
    from PyQt6.QtWebChannel        import QWebChannel
    from PyQt6.QtGui               import QIcon, QColor
    QT_VERSION = 6
    # PyQt6 expõe enums como atributos de classe — não aceita int puro
    NO_CONTEXT_MENU   = Qt.ContextMenuPolicy.NoContextMenu
    JS_CONSOLE_LEVELS = {
        QWebEnginePage.JavaScriptConsoleMessageLevel.InfoMessageLevel:    "INFO",
        QWebEnginePage.JavaScriptConsoleMessageLevel.WarningMessageLevel: "WARN",
        QWebEnginePage.JavaScriptConsoleMessageLevel.ErrorMessageLevel:   "ERROR",
    }
except ImportError:
    try:
        from PyQt5.QtCore    import QUrl, QObject, pyqtSlot, QTimer, Qt
        from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
        from PyQt5.QtWebEngineWidgets  import QWebEngineView, QWebEngineSettings
        from PyQt5.QtWebEngineCore     import QWebEnginePage
        from PyQt5.QtWebChannel        import QWebChannel
        from PyQt5.QtGui               import QIcon, QColor
        QT_VERSION = 5
        NO_CONTEXT_MENU   = Qt.NoContextMenu
        JS_CONSOLE_LEVELS = {0: "INFO", 1: "WARN", 2: "ERROR"}
    except ImportError:
        print("ERRO: PyQt6 ou PyQt5 com QtWebEngine não encontrado.", file=sys.stderr)
        print("Instale com: pip install PyQt6 PyQt6-WebEngine", file=sys.stderr)
        sys.exit(1)


# ── Bridge object (JavaScript ↔ Python) ─────────────────────────────────────
class RegataShellBridge(QObject):
    """Expõe runCommand() ao JavaScript."""

    @pyqtSlot(str)
    def runCommand(self, cmd: str):
        """Executa um comando KCM/shell de forma segura."""
        if not cmd:
            return

        # Whitelist de prefixos de comandos permitidos (segurança)
        ALLOWED_PREFIXES = (
            "kcmshell6 ", "kcmshell5 ",
            "plasma-open-settings", "plasma-discover",
            "pavucontrol", "skanlite", "gufw",
            "systemctl status", "ksysguard",
        )
        safe = any(cmd.startswith(p) for p in ALLOWED_PREFIXES)
        if not safe:
            print(f"[RCC] Comando bloqueado por segurança: {cmd}", file=sys.stderr)
            return

        print(f"[RCC] Executando: {cmd}")
        try:
            subprocess.Popen(
                cmd, shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
        except Exception as e:
            print(f"[RCC] Erro ao executar '{cmd}': {e}", file=sys.stderr)


# ── Custom Page — injeta bridge e tema do sistema ─────────────────────────
class RCCPage(QWebEnginePage):

    def __init__(self, channel: QWebChannel, parent=None):
        super().__init__(parent)
        self._channel = channel

    def javaScriptConsoleMessage(self, level, msg, line, source):
        label = JS_CONSOLE_LEVELS.get(level, "LOG")
        print(f"[JS {label}:{line}] {msg}")


# ── Main Window ──────────────────────────────────────────────────────────────
class RegataControlCenter(QMainWindow):

    APP_NAME    = "Regata Control Center"
    APP_VERSION = "1.0"
    MIN_W, MIN_H = 920, 640

    def __init__(self, html_path: Path):
        super().__init__()
        self.html_path = html_path
        self._setup_window()
        self._setup_webengine()
        self._setup_channel()
        self._load_page()

    # ── Window setup ────────────────────────────────────────────
    def _setup_window(self):
        self.setWindowTitle(self.APP_NAME)
        self.setMinimumSize(self.MIN_W, self.MIN_H)
        self.resize(1280, 780)

        # Try to use the Regata/KDE icon
        icon_names = ["preferences-system", "configure", "systemsettings", "regata-control-center"]
        for name in icon_names:
            icon = QIcon.fromTheme(name)
            if not icon.isNull():
                self.setWindowIcon(icon)
                break

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self._layout = layout

    # ── WebEngine setup ─────────────────────────────────────────
    def _setup_webengine(self):
        self.view = QWebEngineView()

        if QT_VERSION == 6:
            settings = self.view.settings()
            settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
            settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, False)
            settings.setAttribute(QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled, True)
        else:
            settings = self.view.settings()
            settings.setAttribute(QWebEngineSettings.JavascriptEnabled, True)
            settings.setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, True)

        self.view.setContextMenuPolicy(NO_CONTEXT_MENU)
        self._layout.addWidget(self.view)

    # ── WebChannel bridge setup ──────────────────────────────────
    def _setup_channel(self):
        self.channel = QWebChannel()
        self.bridge  = RegataShellBridge(self)
        self.channel.registerObject("bridge", self.bridge)

        self.page = RCCPage(self.channel, self.view)
        self.page.setWebChannel(self.channel)
        self.view.setPage(self.page)

    # ── Load HTML ────────────────────────────────────────────────
    def _load_page(self):
        url = QUrl.fromLocalFile(str(self.html_path.resolve()))
        self.view.load(url)

        # Inject QWebChannel JS after page loads
        self.view.loadFinished.connect(self._on_load_finished)

    def _on_load_finished(self, ok: bool):
        if not ok:
            print("[RCC] Falha ao carregar a página HTML.", file=sys.stderr)
            return

        # Detect system theme and sync
        self._sync_system_theme()

        # Inject webchannel bridge
        js = """
        (function() {
          if (typeof QWebChannel !== 'undefined') return;
          var script = document.createElement('script');
          script.src = 'qrc:///qtwebchannel/qwebchannel.js';
          script.onload = function() {
            new QWebChannel(qt.webChannelTransport, function(channel) {
              window.regataShell = channel.objects.bridge;
              console.log('[RCC] Qt bridge ready');
            });
          };
          document.head.appendChild(script);
        })();
        """
        self.page.runJavaScript(js)

    def _sync_system_theme(self):
        """Detecta tema do KDE e sincroniza com o HTML."""
        try:
            result = subprocess.run(
                ["kreadconfig6", "--group", "General", "--key", "ColorScheme",
                 "--file", str(Path.home() / ".config/kdeglobals")],
                capture_output=True, text=True, timeout=2
            )
            scheme = result.stdout.strip().lower()
            is_dark = any(w in scheme for w in ["dark", "breeze-dark", "noir", "escuro"])
        except Exception:
            is_dark = False

        if is_dark:
            self.page.runJavaScript(
                "document.documentElement.setAttribute('data-theme','dark');"
                "localStorage.setItem('rcc-theme','dark');"
            )


# ── Entry Point ──────────────────────────────────────────────────────────────
def find_html() -> Path:
    """Localiza o arquivo HTML em locais conhecidos."""
    candidates = [
        Path(__file__).parent / "regata-control-center.html",
        Path.home() / ".local/share/regata-control-center/regata-control-center.html",
        Path("/usr/share/regata-control-center/regata-control-center.html"),
    ]
    for p in candidates:
        if p.exists():
            return p
    raise FileNotFoundError(
        "regata-control-center.html não encontrado. "
        "Reinstale o Regata Control Center."
    )


def main():
    # High-DPI support
    os.environ.setdefault("QT_AUTO_SCREEN_SCALE_FACTOR", "1")

    app = QApplication(sys.argv)
    app.setApplicationName("regata-control-center")
    app.setApplicationDisplayName("Regata Control Center")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("RegataOS")
    app.setOrganizationDomain("regataos.com.br")

    try:
        html = find_html()
    except FileNotFoundError as e:
        print(f"ERRO: {e}", file=sys.stderr)
        sys.exit(1)

    window = RegataControlCenter(html)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
