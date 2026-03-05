#!/usr/bin/env python3
"""
RegataOS Welcome App — v2
Tela de boas-vindas para o RegataOS 25 "Maverick"
Inspirado no ZorinOS Tour: sidebar + conteúdo, com modo dark/light

Dependências: pip install PyQt6 PyQt6-WebEngine
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtCore import QUrl, Qt, QSize

HTML = r"""<!DOCTYPE html>
<html lang="pt-BR" data-theme="dark">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Bem-vindo ao RegataOS</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

[data-theme="dark"] {
  --bg:         #1a1a2e;
  --bg-sidebar: #16213e;
  --bg-card:    #0f3460;
  --bg-card2:   #1a1a2e;
  --border:     rgba(255,255,255,0.08);
  --text:       #e2e8f0;
  --text-muted: #94a3b8;
  --text-weak:  #64748b;
  --accent:     #e94560;
  --shadow:     0 1px 3px rgba(0,0,0,0.5);
  --shadow-md:  0 4px 12px rgba(0,0,0,0.4);
  --nav-hover:  rgba(233,69,96,0.12);
  --nav-active: rgba(233,69,96,0.18);
  --badge-bg:   rgba(233,69,96,0.2);
  --tag-new:    rgba(52,211,153,0.15);
  --tag-new-c:  #34d399;
  --tag-upd:    rgba(251,191,36,0.15);
  --tag-upd-c:  #fbbf24;
}

[data-theme="light"] {
  --bg:         #f1f5f9;
  --bg-sidebar: #ffffff;
  --bg-card:    #ffffff;
  --bg-card2:   #f8fafc;
  --border:     rgba(0,0,0,0.08);
  --text:       #1e293b;
  --text-muted: #475569;
  --text-weak:  #94a3b8;
  --accent:     #e11d48;
  --shadow:     0 1px 3px rgba(0,0,0,0.1);
  --shadow-md:  0 4px 12px rgba(0,0,0,0.08);
  --nav-hover:  rgba(225,29,72,0.07);
  --nav-active: rgba(225,29,72,0.1);
  --badge-bg:   rgba(225,29,72,0.12);
  --tag-new:    rgba(16,185,129,0.12);
  --tag-new-c:  #059669;
  --tag-upd:    rgba(217,119,6,0.12);
  --tag-upd-c:  #d97706;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Inter', system-ui, sans-serif;
  font-size: 14px;
  background: var(--bg);
  color: var(--text);
  height: 100vh;
  overflow: hidden;
  display: flex;
  transition: background 0.25s, color 0.25s;
}

/* Sidebar */
.sidebar {
  width: 220px; min-width: 220px;
  background: var(--bg-sidebar);
  border-right: 1px solid var(--border);
  display: flex; flex-direction: column;
  transition: background 0.25s;
}

.content {
  flex: 1; overflow-y: auto; scroll-behavior: smooth;
}
.content::-webkit-scrollbar { width: 4px; }
.content::-webkit-scrollbar-track { background: transparent; }
.content::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

.logo {
  padding: 24px 20px 20px;
  border-bottom: 1px solid var(--border);
  display: flex; align-items: center; gap: 12px;
}
.logo-icon {
  width: 38px; height: 38px;
  background: var(--accent);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 20px; flex-shrink: 0;
}
.logo-name { font-weight: 700; font-size: 15px; line-height: 1.2; }
.logo-ver  { font-size: 11px; color: var(--text-muted); margin-top: 1px; }

.nav { flex: 1; padding: 12px 0; overflow-y: auto; }
.nav-section {
  padding: 12px 20px 4px;
  font-size: 10px; font-weight: 600;
  letter-spacing: 0.08em; text-transform: uppercase;
  color: var(--text-weak);
}
.nav-item {
  display: flex; align-items: center; gap: 10px;
  padding: 9px 20px;
  cursor: pointer; color: var(--text-muted);
  font-size: 13.5px; font-weight: 500;
  border-left: 2px solid transparent;
  transition: all 0.15s; user-select: none;
}
.nav-item:hover { background: var(--nav-hover); color: var(--text); }
.nav-item.active {
  background: var(--nav-active); color: var(--accent);
  border-left-color: var(--accent); font-weight: 600;
}
.nav-ico { font-size: 15px; width: 18px; text-align: center; }
.nav-badge {
  margin-left: auto;
  background: var(--badge-bg); color: var(--accent);
  font-size: 10px; font-weight: 700;
  padding: 1px 6px; border-radius: 10px;
}

.sidebar-footer {
  padding: 16px 20px;
  border-top: 1px solid var(--border);
}
.theme-toggle {
  display: flex; align-items: center; gap: 8px;
  cursor: pointer; font-size: 12px;
  color: var(--text-muted); user-select: none;
}
.theme-toggle:hover { color: var(--text); }
.toggle-track {
  width: 32px; height: 18px;
  background: var(--border); border-radius: 9px;
  position: relative; transition: background 0.2s;
  border: 1px solid var(--border); flex-shrink: 0;
}
.toggle-track.on { background: var(--accent); }
.toggle-thumb {
  width: 12px; height: 12px; background: white;
  border-radius: 50%; position: absolute;
  top: 2px; left: 2px; transition: left 0.2s;
  box-shadow: 0 1px 2px rgba(0,0,0,0.3);
}
.toggle-track.on .toggle-thumb { left: 16px; }

/* Pages */
.page { display: none; }
.page.active { display: block; animation: fadeIn 0.25s ease; }
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(6px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* Hero */
.hero {
  padding: 48px 48px 36px;
  border-bottom: 1px solid var(--border);
}
.hero-eyebrow {
  font-size: 11px; font-weight: 600;
  letter-spacing: 0.1em; text-transform: uppercase;
  color: var(--accent); margin-bottom: 10px;
}
.hero-title {
  font-size: 32px; font-weight: 700;
  line-height: 1.15; margin-bottom: 12px;
}
.hero-title em { color: var(--accent); font-style: normal; }
.hero-desc {
  font-size: 14.5px; color: var(--text-muted);
  line-height: 1.7; max-width: 520px; margin-bottom: 28px;
}
.hero-actions { display: flex; gap: 10px; flex-wrap: wrap; }

/* Buttons */
.btn {
  display: inline-flex; align-items: center; gap: 7px;
  padding: 9px 20px; border-radius: 7px;
  font-family: inherit; font-size: 13.5px; font-weight: 600;
  cursor: pointer; border: none; transition: all 0.15s;
}
.btn-primary { background: var(--accent); color: white; }
.btn-primary:hover { filter: brightness(1.1); transform: translateY(-1px); box-shadow: var(--shadow-md); }
.btn-ghost {
  background: transparent; color: var(--text-muted);
  border: 1px solid var(--border);
}
.btn-ghost:hover { color: var(--text); border-color: var(--text-muted); background: var(--bg-card2); }

/* Section */
.section { padding: 36px 48px; border-bottom: 1px solid var(--border); }
.section:last-child { border-bottom: none; }
.section-label {
  font-size: 11px; font-weight: 600;
  letter-spacing: 0.08em; text-transform: uppercase;
  color: var(--text-weak); margin-bottom: 20px;
}

/* Cards */
.grid-2 { display: grid; grid-template-columns: repeat(2,1fr); gap: 12px; }
.grid-3 { display: grid; grid-template-columns: repeat(3,1fr); gap: 12px; }

.feat-card {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: 10px; padding: 18px;
  transition: box-shadow 0.15s, border-color 0.15s;
}
.feat-card:hover { box-shadow: var(--shadow-md); border-color: var(--accent); }
.feat-icon { font-size: 24px; margin-bottom: 10px; }
.feat-title { font-size: 14px; font-weight: 600; margin-bottom: 5px; }
.feat-desc { font-size: 12.5px; color: var(--text-muted); line-height: 1.55; }

/* What's new */
.new-list { display: flex; flex-direction: column; }
.new-item {
  display: flex; align-items: flex-start; gap: 16px;
  padding: 16px 0; border-bottom: 1px solid var(--border);
}
.new-item:last-child { border-bottom: none; }
.new-icon {
  width: 40px; height: 40px;
  background: var(--bg-card); border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 20px; flex-shrink: 0;
}
.new-body { flex: 1; }
.new-head { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
.new-title { font-size: 14px; font-weight: 600; }
.tag {
  font-size: 10px; font-weight: 700;
  padding: 2px 7px; border-radius: 4px;
  letter-spacing: 0.05em; text-transform: uppercase;
}
.tag-new { background: var(--tag-new); color: var(--tag-new-c); }
.tag-upd { background: var(--tag-upd); color: var(--tag-upd-c); }
.new-desc { font-size: 13px; color: var(--text-muted); line-height: 1.55; }

/* Spec table */
.spec-table { display: flex; flex-direction: column; gap: 2px; }
.spec-row {
  display: flex; align-items: center; gap: 12px;
  padding: 11px 16px;
  background: var(--bg-card); border-radius: 7px;
  border: 1px solid var(--border); font-size: 13.5px;
}
.spec-ico { font-size: 16px; width: 20px; text-align: center; }
.spec-key { color: var(--text-muted); width: 155px; flex-shrink: 0; }
.spec-val { font-weight: 500; flex: 1; }
.spec-tag { margin-left: auto; }

/* Steps */
.steps { display: flex; flex-direction: column; gap: 3px; }
.step {
  display: flex; gap: 16px;
  padding: 16px; background: var(--bg-card);
  border: 1px solid var(--border); border-radius: 10px;
  transition: border-color 0.15s;
}
.step:hover { border-color: var(--accent); }
.step-num {
  font-size: 22px; font-weight: 700;
  color: var(--accent); opacity: 0.4;
  min-width: 32px; line-height: 1; padding-top: 2px;
}
.step-body { flex: 1; }
.step-title { font-size: 14px; font-weight: 600; margin-bottom: 4px; }
.step-desc { font-size: 13px; color: var(--text-muted); line-height: 1.55; }

/* Banner */
.banner {
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: 10px; padding: 20px 24px;
  display: flex; align-items: center; gap: 16px;
  margin-bottom: 24px;
}
.banner-ico { font-size: 32px; }
.banner-body { flex: 1; }
.banner-title { font-size: 15px; font-weight: 600; margin-bottom: 4px; }
.banner-desc { font-size: 13px; color: var(--text-muted); line-height: 1.55; }

/* Bottom bar */
.bottom-bar {
  position: sticky; bottom: 0;
  background: var(--bg-sidebar); border-top: 1px solid var(--border);
  padding: 12px 48px;
  display: flex; align-items: center; justify-content: space-between;
}
.startup-check {
  display: flex; align-items: center; gap: 8px;
  cursor: pointer; font-size: 12.5px; color: var(--text-muted);
  user-select: none;
}
.startup-check:hover { color: var(--text); }
.checkbox {
  width: 16px; height: 16px;
  border: 1px solid var(--border); border-radius: 4px;
  background: var(--bg-card);
  display: flex; align-items: center; justify-content: center;
  font-size: 10px; transition: all 0.15s;
}
.checkbox.checked { background: var(--accent); border-color: var(--accent); color: white; }

/* Pills */
.pill-strip { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 14px; }
.pill {
  font-size: 12px; padding: 4px 12px;
  background: var(--bg-card); border: 1px solid var(--border);
  border-radius: 20px; color: var(--text-muted);
}
</style>
</head>
<body>

<aside class="sidebar">
  <div class="logo">
    <div class="logo-icon">⚓</div>
    <div>
      <div class="logo-name">RegataOS</div>
      <div class="logo-ver">25 "Maverick"</div>
    </div>
  </div>

  <nav class="nav">
    <div class="nav-section">Tour</div>
    <div class="nav-item active" data-page="welcome">
      <span class="nav-ico">🏠</span> Bem-vindo
    </div>
    <div class="nav-item" data-page="whats-new">
      <span class="nav-ico">✨</span> Novidades
      <span class="nav-badge">Novo</span>
    </div>
    <div class="nav-section">Recursos</div>
    <div class="nav-item" data-page="specs">
      <span class="nav-ico">🖥️</span> Sistema
    </div>
    <div class="nav-item" data-page="gaming">
      <span class="nav-ico">🎮</span> Gaming
    </div>
    <div class="nav-section">Início</div>
    <div class="nav-item" data-page="start">
      <span class="nav-ico">⚡</span> Primeiros Passos
    </div>
    <div class="nav-item" data-page="community">
      <span class="nav-ico">🌐</span> Comunidade
    </div>
  </nav>

  <div class="sidebar-footer">
    <div class="theme-toggle" id="themeToggle">
      <div class="toggle-track on" id="toggleTrack">
        <div class="toggle-thumb"></div>
      </div>
      <span id="themeLabel">Modo escuro</span>
    </div>
  </div>
</aside>

<main class="content">

  <!-- Bem-vindo -->
  <div class="page active" id="page-welcome">
    <div class="hero">
      <div class="hero-eyebrow">Linux · Gaming · Brasil</div>
      <h1 class="hero-title">Bem-vindo ao<br><em>RegataOS 25</em></h1>
      <p class="hero-desc">
        O RegataOS é um sistema Linux brasileiro focado em criadores e jogadores.
        Com base openSUSE, KDE Plasma 6 e ferramentas gaming pré-configuradas,
        é a alternativa mais completa ao Windows sem abrir mão de desempenho.
      </p>
      <div class="hero-actions">
        <button class="btn btn-primary" onclick="navigate('start')">⚡ Primeiros passos</button>
        <button class="btn btn-ghost" onclick="navigate('whats-new')">✨ Ver novidades</button>
      </div>
    </div>

    <div class="section">
      <div class="section-label">Por que RegataOS?</div>
      <div class="grid-3">
        <div class="feat-card">
          <div class="feat-icon">🎮</div>
          <div class="feat-title">Feito para Gaming</div>
          <div class="feat-desc">Steam, Game Access, Wine e Proton pré-configurados. Acesse Epic, GOG, EA, Ubisoft e mais.</div>
        </div>
        <div class="feat-card">
          <div class="feat-icon">🇧🇷</div>
          <div class="feat-title">100% Brasileiro</div>
          <div class="feat-desc">Desenvolvido no Brasil, em Português. Comunidade ativa e suporte local desde 2013.</div>
        </div>
        <div class="feat-card">
          <div class="feat-icon">🏪</div>
          <div class="feat-title">Loja Própria</div>
          <div class="feat-desc">RegataOS Store: experiência de app store no estilo mobile, reconhecida como a melhor do Linux.</div>
        </div>
        <div class="feat-card">
          <div class="feat-icon">🔒</div>
          <div class="feat-title">Base openSUSE</div>
          <div class="feat-desc">Estabilidade e confiabilidade com atualizações constantes via zypper e ferramentas YaST.</div>
        </div>
        <div class="feat-card">
          <div class="feat-icon">⚡</div>
          <div class="feat-title">KDE Plasma 6</div>
          <div class="feat-desc">Interface moderna e altamente personalizável. Versão estável mais recente do Plasma.</div>
        </div>
        <div class="feat-card">
          <div class="feat-icon">🖱️</div>
          <div class="feat-title">Fácil para Iniciantes</div>
          <div class="feat-desc">Instalação Calamares em ~12 min. Sem configuração manual. Pronto para usar no primeiro boot.</div>
        </div>
      </div>
    </div>
  </div>

  <!-- Novidades -->
  <div class="page" id="page-whats-new">
    <div class="hero">
      <div class="hero-eyebrow">Abril de 2025</div>
      <h1 class="hero-title">Novidades do<br><em>RegataOS 25 "Maverick"</em></h1>
      <p class="hero-desc">
        Linux Kernel 6.13, KDE Plasma 6.3 e novas ferramentas gaming.
        Fonte: anúncio oficial em mag.regataos.com.br.
      </p>
    </div>

    <div class="section">
      <div class="section-label">Destaques desta versão</div>
      <div class="new-list">

        <div class="new-item">
          <div class="new-icon">🐧</div>
          <div class="new-body">
            <div class="new-head">
              <span class="new-title">Linux Kernel 6.13</span>
              <span class="tag tag-new">Novo</span>
            </div>
            <div class="new-desc">
              Novo driver HID para dispositivos Kysona — exibe o status de bateria
              do mouse gaming M600. Suporte à especificação NVMe 2.1 e possibilidade
              de desativar o modo Zero RPM em GPUs Radeon RX 7000. Suporte aprimorado
              a hardware lançado em 2024/2025.
            </div>
          </div>
        </div>

        <div class="new-item">
          <div class="new-icon">🖥️</div>
          <div class="new-body">
            <div class="new-head">
              <span class="new-title">KDE Plasma 6.3</span>
              <span class="tag tag-upd">Atualizado</span>
            </div>
            <div class="new-desc">
              Escala fracionária remodelada: imagens mais nítidas em monitores HiDPI,
              reduzindo o blur em displays de alta resolução. Clonagem de painéis
              facilitada no modo de edição. Monitor do Sistema usa menos CPU e
              exibe dados mais detalhados de processador. Modo Não Perturbe exibe
              apenas o contador de notificações pendentes.
            </div>
          </div>
        </div>

        <div class="new-item">
          <div class="new-icon">🏪</div>
          <div class="new-body">
            <div class="new-head">
              <span class="new-title">RegataOS Store</span>
              <span class="tag tag-upd">Atualizado</span>
            </div>
            <div class="new-desc">
              Loja de aplicativos no estilo Android/iOS com categorias na barra lateral
              e busca instantânea. Avaliada pela imprensa especializada como a loja
              de apps mais bem apresentada do Linux.
            </div>
          </div>
        </div>

        <div class="new-item">
          <div class="new-icon">🎮</div>
          <div class="new-body">
            <div class="new-head">
              <span class="new-title">Game Access — Mais launchers</span>
              <span class="tag tag-upd">Atualizado</span>
            </div>
            <div class="new-desc">
              Suporte completo a: Amazon Games, Epic Games Store, EA App, Battle.net,
              Ubisoft Connect, Rockstar Launcher e GOG Galaxy — tudo em um só lugar,
              via wine-gcs customizado para o RegataOS.
            </div>
          </div>
        </div>

        <div class="new-item">
          <div class="new-icon">🎴</div>
          <div class="new-body">
            <div class="new-head">
              <span class="new-title">ISO com driver NVIDIA 570.x</span>
              <span class="tag tag-new">Novo</span>
            </div>
            <div class="new-desc">
              Disponível ISO separada (sufixo _NV) com o driver proprietário NVIDIA
              já incluído. Ideal para quem tem GPU GeForce e quer instalar sem
              precisar adicionar o driver depois. Consulte a lista de GPUs suportadas
              no site da NVIDIA antes de baixar.
            </div>
          </div>
        </div>

        <div class="new-item">
          <div class="new-icon">📦</div>
          <div class="new-body">
            <div class="new-head">
              <span class="new-title">Software padrão atualizado</span>
              <span class="tag tag-upd">Atualizado</span>
            </div>
            <div class="new-desc">
              Instalação padrão inclui: Firefox, OnlyOffice Suite, VLC, Steam
              e ferramentas YaST herdadas da base openSUSE. Thunderbird, GIMP
              e LibreOffice disponíveis com um clique na RegataOS Store.
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>

  <!-- Sistema -->
  <div class="page" id="page-specs">
    <div class="hero">
      <div class="hero-eyebrow">Especificações reais</div>
      <h1 class="hero-title">O sistema<br><em>por dentro</em></h1>
      <p class="hero-desc">Informações técnicas do RegataOS 25 Maverick.</p>
    </div>

    <div class="section">
      <div class="section-label">Núcleo do sistema</div>
      <div class="spec-table">
        <div class="spec-row">
          <span class="spec-ico">🏗️</span>
          <span class="spec-key">Base</span>
          <span class="spec-val">openSUSE</span>
        </div>
        <div class="spec-row">
          <span class="spec-ico">🐧</span>
          <span class="spec-key">Kernel</span>
          <span class="spec-val">Linux 6.13</span>
          <span class="spec-tag"><span class="tag tag-new">Novo</span></span>
        </div>
        <div class="spec-row">
          <span class="spec-ico">🖥️</span>
          <span class="spec-key">Desktop</span>
          <span class="spec-val">KDE Plasma 6.3</span>
          <span class="spec-tag"><span class="tag tag-upd">Atualizado</span></span>
        </div>
        <div class="spec-row">
          <span class="spec-ico">📦</span>
          <span class="spec-key">Gerenciador de pacotes</span>
          <span class="spec-val">zypper + YaST</span>
        </div>
        <div class="spec-row">
          <span class="spec-ico">💿</span>
          <span class="spec-key">Instalador</span>
          <span class="spec-val">Calamares modificado · ~12 minutos</span>
        </div>
        <div class="spec-row">
          <span class="spec-ico">🌐</span>
          <span class="spec-key">Idioma padrão</span>
          <span class="spec-val">Português do Brasil + English</span>
        </div>
        <div class="spec-row">
          <span class="spec-ico">🖥️</span>
          <span class="spec-key">Arquitetura</span>
          <span class="spec-val">x86_64 (64-bit)</span>
        </div>
        <div class="spec-row">
          <span class="spec-ico">💾</span>
          <span class="spec-key">Tamanho da ISO</span>
          <span class="spec-val">~3,8 GB</span>
        </div>
      </div>
    </div>

    <div class="section">
      <div class="section-label">Requisitos mínimos</div>
      <div class="spec-table">
        <div class="spec-row">
          <span class="spec-ico">⚙️</span>
          <span class="spec-key">Processador</span>
          <span class="spec-val">Dual-core 2 GHz 64-bit</span>
        </div>
        <div class="spec-row">
          <span class="spec-ico">🧠</span>
          <span class="spec-key">RAM</span>
          <span class="spec-val">4 GB (8 GB recomendado para gaming)</span>
        </div>
        <div class="spec-row">
          <span class="spec-ico">💾</span>
          <span class="spec-key">Armazenamento</span>
          <span class="spec-val">30 GB livres</span>
        </div>
        <div class="spec-row">
          <span class="spec-ico">🔌</span>
          <span class="spec-key">Mídia</span>
          <span class="spec-val">Pen drive USB</span>
        </div>
      </div>
    </div>

    <div class="section">
      <div class="section-label">Software pré-instalado</div>
      <div class="pill-strip">
        <span class="pill">Firefox</span>
        <span class="pill">OnlyOffice</span>
        <span class="pill">VLC</span>
        <span class="pill">Steam</span>
        <span class="pill">RegataOS Store</span>
        <span class="pill">RegataOS Game Access</span>
        <span class="pill">YaST</span>
        <span class="pill">Dolphin</span>
        <span class="pill">Konsole</span>
        <span class="pill">wine-gcs</span>
        <span class="pill">sc-controller</span>
        <span class="pill">prime-settings</span>
        <span class="pill">KDE Connect</span>
      </div>
    </div>
  </div>

  <!-- Gaming -->
  <div class="page" id="page-gaming">
    <div class="hero">
      <div class="hero-eyebrow">Plataforma Gaming</div>
      <h1 class="hero-title"><em>Gaming no Linux</em><br>do jeito certo</h1>
      <p class="hero-desc">
        Com o RegataOS Game Access, você acessa os principais launchers do mercado
        diretamente no Linux, sem configuração manual.
      </p>
    </div>

    <div class="section">
      <div class="banner">
        <div class="banner-ico">🏆</div>
        <div class="banner-body">
          <div class="banner-title">RegataOS Game Access</div>
          <div class="banner-desc">Ferramenta exclusiva que instala e gerencia launchers Windows no Linux via wine-gcs customizado:
          Epic Games, EA App, Battle.net, Ubisoft Connect, Amazon Games, GOG Galaxy e Rockstar Launcher.</div>
        </div>
      </div>

      <div class="section-label">Launchers suportados pelo Game Access</div>
      <div class="grid-2">
        <div class="feat-card">
          <div class="feat-icon">🟣</div>
          <div class="feat-title">Epic Games Store</div>
          <div class="feat-desc">Fortnite, Rocket League, jogos gratuitos semanais e títulos exclusivos da Epic.</div>
        </div>
        <div class="feat-card">
          <div class="feat-icon">🟡</div>
          <div class="feat-title">EA App</div>
          <div class="feat-desc">FIFA 18/19, The Sims 4, GRID Legends, Battlefield e outros títulos EA.</div>
        </div>
        <div class="feat-card">
          <div class="feat-icon">🔵</div>
          <div class="feat-title">Battle.net (Blizzard)</div>
          <div class="feat-desc">World of Warcraft, Diablo III e IV, Overwatch 2, Hearthstone.</div>
        </div>
        <div class="feat-card">
          <div class="feat-icon">⚫</div>
          <div class="feat-title">Ubisoft Connect</div>
          <div class="feat-desc">Assassin's Creed (série completa), Watch Dogs, Far Cry, Rainbow Six Siege.</div>
        </div>
        <div class="feat-card">
          <div class="feat-icon">🟤</div>
          <div class="feat-title">GOG Galaxy</div>
          <div class="feat-desc">Jogos DRM-free: The Witcher, Cyberpunk 2077, clássicos e independentes.</div>
        </div>
        <div class="feat-card">
          <div class="feat-icon">🔴</div>
          <div class="feat-title">Rockstar Launcher</div>
          <div class="feat-desc">GTA V, GTA San Andreas, GTA Vice City, Red Dead Redemption 2.</div>
        </div>
      </div>
    </div>

    <div class="section">
      <div class="section-label">Ferramentas gaming</div>
      <div class="spec-table">
        <div class="spec-row">
          <span class="spec-ico">🎮</span>
          <span class="spec-key">Steam</span>
          <span class="spec-val">Pré-instalado com Proton habilitado por padrão</span>
        </div>
        <div class="spec-row">
          <span class="spec-ico">🍷</span>
          <span class="spec-key">wine-gcs</span>
          <span class="spec-val">Wine customizado para o RegataOS Game Access</span>
        </div>
        <div class="spec-row">
          <span class="spec-ico">🕹️</span>
          <span class="spec-key">sc-controller</span>
          <span class="spec-val">Suporte a Steam Controller e outros gamepads</span>
        </div>
        <div class="spec-row">
          <span class="spec-ico">💻</span>
          <span class="spec-key">prime-settings</span>
          <span class="spec-val">Alternância iGPU ↔ dGPU em notebooks</span>
        </div>
        <div class="spec-row">
          <span class="spec-ico">🎴</span>
          <span class="spec-key">NVIDIA (ISO _NV)</span>
          <span class="spec-val">Driver 570.x pré-instalado na versão NV da ISO</span>
        </div>
      </div>
    </div>
  </div>

  <!-- Primeiros Passos -->
  <div class="page" id="page-start">
    <div class="hero">
      <div class="hero-eyebrow">Configuração inicial</div>
      <h1 class="hero-title">Primeiros<br><em>Passos</em></h1>
      <p class="hero-desc">Siga estes passos para aproveitar ao máximo o seu RegataOS.</p>
    </div>

    <div class="section">
      <div class="section-label">Configure o sistema</div>
      <div class="steps">
        <div class="step">
          <div class="step-num">01</div>
          <div class="step-body">
            <div class="step-title">Atualize o sistema</div>
            <div class="step-desc">Abra o Gerenciador de Atualizações do RegataOS ou execute
            <code>sudo zypper dup</code> no terminal para aplicar as últimas correções e atualizações.</div>
          </div>
        </div>
        <div class="step">
          <div class="step-num">02</div>
          <div class="step-body">
            <div class="step-title">Verifique o driver de vídeo</div>
            <div class="step-desc">Usuários NVIDIA: use o <strong>prime-settings</strong> para ativar
            o driver proprietário. Se baixou a ISO _NV, o driver 570.x já está instalado.
            AMD e Intel funcionam com Mesa nativamente.</div>
          </div>
        </div>
        <div class="step">
          <div class="step-num">03</div>
          <div class="step-body">
            <div class="step-title">Explore a RegataOS Store</div>
            <div class="step-desc">A loja possui categorias, busca e instalação com um clique.
            Instale Thunderbird, GIMP, LibreOffice, OBS, Discord, VS Code e muito mais.</div>
          </div>
        </div>
        <div class="step">
          <div class="step-num">04</div>
          <div class="step-body">
            <div class="step-title">Configure o Steam e o Game Access</div>
            <div class="step-desc">No Steam, vá em Configurações → Compatibilidade e ative o Proton
            para todos os jogos. Para launchers adicionais (Epic, EA, Ubisoft…), abra o
            <strong>RegataOS Game Access</strong>.</div>
          </div>
        </div>
        <div class="step">
          <div class="step-num">05</div>
          <div class="step-body">
            <div class="step-title">Personalize o KDE Plasma 6.3</div>
            <div class="step-desc">Clique direito no desktop para acessar as configurações de aparência.
            O Plasma 6.3 permite clonar painéis facilmente e tem escala fracionária melhorada para HiDPI.</div>
          </div>
        </div>
      </div>
    </div>

    <div class="bottom-bar">
      <label class="startup-check" id="startupLabel">
        <div class="checkbox checked" id="startupCheck">✓</div>
        Mostrar ao iniciar o sistema
      </label>
      <button class="btn btn-primary" onclick="closeApp()">Começar a usar →</button>
    </div>
  </div>

  <!-- Comunidade -->
  <div class="page" id="page-community">
    <div class="hero">
      <div class="hero-eyebrow">Suporte &amp; Comunidade</div>
      <h1 class="hero-title">Você faz parte de<br><em>uma comunidade</em></h1>
      <p class="hero-desc">O RegataOS tem suporte oficial, magazine com tutoriais e fóruns ativos em Português.</p>
    </div>

    <div class="section">
      <div class="section-label">Canais oficiais</div>
      <div class="grid-2">
        <div class="feat-card">
          <div class="feat-icon">📖</div>
          <div class="feat-title">Suporte oficial</div>
          <div class="feat-desc">support.regataos.com.br — base de conhecimento com tutoriais e guias em Português.</div>
        </div>
        <div class="feat-card">
          <div class="feat-icon">📰</div>
          <div class="feat-title">RegataOS Magazine</div>
          <div class="feat-desc">mag.regataos.com.br — notícias, tutoriais e novidades do RegataOS.</div>
        </div>
        <div class="feat-card">
          <div class="feat-icon">💾</div>
          <div class="feat-title">Download</div>
          <div class="feat-desc">get.regataos.com.br — ISOs oficiais com e sem driver NVIDIA pré-instalado.</div>
        </div>
        <div class="feat-card">
          <div class="feat-icon">🐙</div>
          <div class="feat-title">GitHub</div>
          <div class="feat-desc">github.com/regataos — código aberto. Contribute e acompanhe o desenvolvimento.</div>
        </div>
      </div>
    </div>

    <div class="section">
      <div class="section-label">Sobre o projeto</div>
      <div class="feat-card">
        <div class="feat-desc" style="font-size:13.5px;line-height:1.7">
          O RegataOS existe desde <strong>2013</strong> com objetivo de oferecer uma alternativa Linux
          acessível ao Windows, focada em jogadores e criadores. Em 2021, com o RegataOS 21 Challenger,
          o projeto adotou a base openSUSE e o KDE Plasma estável. Hoje é reconhecido internacionalmente
          como uma das distribuições Linux gaming mais polidas — premiada por reviews no FOSS Force,
          DistroWatch e imprensa especializada.
        </div>
      </div>
    </div>
  </div>

</main>

<script>
function navigate(id) {
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.page').forEach(el => el.classList.remove('active'));
  const nav = document.querySelector(`[data-page="${id}"]`);
  const page = document.getElementById(`page-${id}`);
  if (nav) nav.classList.add('active');
  if (page) { page.classList.add('active'); document.querySelector('.content').scrollTop = 0; }
}
document.querySelectorAll('.nav-item').forEach(el =>
  el.addEventListener('click', () => navigate(el.dataset.page))
);

// Tema
const html = document.documentElement;
const track = document.getElementById('toggleTrack');
const label = document.getElementById('themeLabel');
let dark = true;
document.getElementById('themeToggle').addEventListener('click', () => {
  dark = !dark;
  html.setAttribute('data-theme', dark ? 'dark' : 'light');
  track.classList.toggle('on', dark);
  label.textContent = dark ? 'Modo escuro' : 'Modo claro';
});

// Checkbox
let showOnStart = true;
document.getElementById('startupLabel').addEventListener('click', () => {
  showOnStart = !showOnStart;
  const cb = document.getElementById('startupCheck');
  cb.textContent = showOnStart ? '✓' : '';
  cb.classList.toggle('checked', showOnStart);
});

// Fechar
function closeApp() {
  document.title = '__CLOSE__';
  if (window.regataos) window.regataos.close();
}
</script>
</body>
</html>
"""


class WelcomeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bem-vindo ao RegataOS")
        self.setMinimumSize(QSize(920, 620))
        self.resize(1080, 680)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)

        self.view = QWebEngineView()
        s = self.view.settings()
        s.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        s.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        s.setAttribute(QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled, True)
        self.view.titleChanged.connect(self._on_title)
        self.view.setHtml(HTML, QUrl("about:blank"))
        layout.addWidget(self.view)

    def _on_title(self, title):
        if title == "__CLOSE__":
            self.close()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("RegataOS Welcome")
    win = WelcomeApp()
    win.show()
    screen = app.primaryScreen().availableGeometry()
    fg = win.frameGeometry()
    fg.moveCenter(screen.center())
    win.move(fg.topLeft())
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
