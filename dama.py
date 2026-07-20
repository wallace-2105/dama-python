"""
Jogo de Dama (Checkers) — feito com Pygame
Visual: Neon Futurista / Sci-Fi

Regras: peças normais andam na diagonal 1 casa pra frente,
capturam pulando o adversário. Ao chegar na última linha, vira Dama
(pode andar pra qualquer direção diagonal).
"""

import pygame
import sys
import os
import random
import math
import json
from datetime import datetime

# ═══════════════════════════════════════════════════════════════
#  CONFIGURAÇÕES DE LAYOUT
# ═══════════════════════════════════════════════════════════════

TAMANHO_CASA = 80
LINHAS, COLUNAS = 8, 8
PADDING_BOARD = 20             # espaço entre borda da janela e tabuleiro
HUD_ALTURA = 56                # faixa superior de informações
TABULEIRO_PX = TAMANHO_CASA * COLUNAS                              # 640
LARGURA_JANELA = TABULEIRO_PX + 2 * PADDING_BOARD                  # 680
ALTURA_JANELA = HUD_ALTURA + TABULEIRO_PX + 2 * PADDING_BOARD + 10 # 746
BOARD_X = PADDING_BOARD                                            # 20
BOARD_Y = HUD_ALTURA + PADDING_BOARD                               # 76

FPS = 60

# ═══════════════════════════════════════════════════════════════
#  PALETA DE CORES — NEON FUTURISTA
# ═══════════════════════════════════════════════════════════════

# Cores lógicas dos jogadores — usadas APENAS como identificadores
# internos na lógica do jogo. NÃO ALTERAR.
VERMELHO = (200, 30, 30)
AZUL_CLARO = (60, 140, 230)

# ---- Fundo ----
BG_ESCURO = (8, 8, 24)
BG_PROFUNDO = (10, 18, 36)

# ---- Tabuleiro ----
CASA_CLARA = (18, 28, 52)          # azul-escuro sutil
CASA_ESCURA = (10, 14, 30)         # quase preto-azulado
CASA_BORDA = (25, 40, 70)          # contorno sutil das casas
GRID_GLOW = (30, 60, 120, 40)      # brilho da grade

# ---- Peças (visual neon) ----
NEON_CIANO = (0, 240, 255)         # jogador VERMELHO → peça ciano
NEON_CIANO_ESCURO = (0, 140, 160)
NEON_CIANO_GLOW = (0, 200, 255, 60)

NEON_MAGENTA = (255, 0, 170)       # jogador AZUL → peça magenta
NEON_MAGENTA_ESCURO = (160, 0, 100)
NEON_MAGENTA_GLOW = (255, 0, 180, 60)

# ---- Seleção ----
NEON_BRANCO = (200, 220, 255)
SELECAO_GLOW = (255, 255, 255, 50)

# ---- Movimentos válidos ----
NEON_VERDE = (0, 255, 136)
NEON_VERDE_ESCURO = (0, 180, 100)

# ---- HUD ----
HUD_BG = (6, 6, 18)
HUD_BORDA = (20, 35, 65)
HUD_TEXTO = (180, 195, 230)
HUD_TEXTO_BRILHO = (220, 235, 255)

# ---- Acentos ----
NEON_ROXO = (123, 47, 255)
NEON_ROXO_GLOW = (100, 40, 200, 40)

# Mapeamento cor lógica → cor visual neon das peças
COR_VISUAL_PECA = {
    VERMELHO: NEON_CIANO,
    AZUL_CLARO: NEON_MAGENTA,
}

COR_VISUAL_ESCURA = {
    VERMELHO: NEON_CIANO_ESCURO,
    AZUL_CLARO: NEON_MAGENTA_ESCURO,
}

# Nomes dos jogadores para exibição
NOME_JOGADOR = {
    VERMELHO: "Ciano",
    AZUL_CLARO: "Magenta",
}

# ---- Estados do jogo ----
ESTADO_MENU = "menu"
ESTADO_JOGANDO = "jogando"
ESTADO_FIM = "fim"

# ═══════════════════════════════════════════════════════════════
#  INICIALIZAÇÃO DO PYGAME
# ═══════════════════════════════════════════════════════════════

pygame.init()
JANELA = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
pygame.display.set_caption("DAMA — Neon")

# ---- Fonte moderna ----
def carregar_fonte(tamanho, bold=False):
    """Tenta carregar fonte moderna; fallback para Segoe UI."""
    for nome in ["Segoe UI", "Calibri", "Arial", "Helvetica"]:
        try:
            f = pygame.font.SysFont(nome, tamanho, bold=bold)
            if f:
                return f
        except Exception:
            continue
    return pygame.font.SysFont(None, tamanho, bold=bold)


FONTE_TITULO = carregar_fonte(78, True)
FONTE_SUB = carregar_fonte(20)
FONTE_HUD = carregar_fonte(17)
FONTE_BOTAO = carregar_fonte(24, True)
FONTE_VITORIA = carregar_fonte(42, True)
FONTE_MINI = carregar_fonte(13)


# ═══════════════════════════════════════════════════════════════
#  PARTÍCULAS ANIMADAS
# ═══════════════════════════════════════════════════════════════

class Particula:
    """Ponto luminoso flutuante para efeitos de fundo."""
    def __init__(self, largura, altura):
        self.x = random.uniform(0, largura)
        self.y = random.uniform(0, altura)
        self.vx = random.uniform(-0.3, 0.3)
        self.vy = random.uniform(-0.2, -0.05)
        self.raio = random.uniform(1, 2.5)
        self.alpha_base = random.randint(30, 90)
        self.fase = random.uniform(0, math.pi * 2)
        self.velocidade_fase = random.uniform(0.01, 0.04)
        self.largura = largura
        self.altura = altura
        # Cor: ciano, magenta ou roxo aleatório
        cores = [NEON_CIANO, NEON_MAGENTA, NEON_ROXO, (80, 120, 200)]
        self.cor = random.choice(cores)

    def atualizar(self):
        self.x += self.vx
        self.y += self.vy
        self.fase += self.velocidade_fase
        # Wrap around
        if self.x < 0:
            self.x = self.largura
        elif self.x > self.largura:
            self.x = 0
        if self.y < 0:
            self.y = self.altura
        elif self.y > self.altura:
            self.y = 0

    def desenhar(self, janela):
        alpha = int(self.alpha_base * (0.5 + 0.5 * math.sin(self.fase)))
        alpha = max(10, min(255, alpha))
        surf = pygame.Surface((int(self.raio * 6), int(self.raio * 6)), pygame.SRCALPHA)
        centro = int(self.raio * 3)
        # Glow externo
        pygame.draw.circle(surf, (*self.cor[:3], alpha // 3), (centro, centro), int(self.raio * 2.5))
        # Core
        pygame.draw.circle(surf, (*self.cor[:3], alpha), (centro, centro), int(self.raio))
        janela.blit(surf, (int(self.x - centro), int(self.y - centro)))


# Pool de partículas global
PARTICULAS = [Particula(LARGURA_JANELA, ALTURA_JANELA) for _ in range(60)]
PARTICULAS_MENU = [Particula(LARGURA_JANELA, ALTURA_JANELA) for _ in range(100)]


# ═══════════════════════════════════════════════════════════════
#  FUNÇÕES AUXILIARES DE DESENHO
# ═══════════════════════════════════════════════════════════════

def clamp_cor(r, g, b):
    """Garante que os valores RGB fiquem entre 0 e 255."""
    return (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))


def cor_variante(cor, delta):
    """Retorna uma cor com brilho ajustado por 'delta'."""
    return clamp_cor(cor[0] + delta, cor[1] + delta, cor[2] + delta)


def lerp_cor(cor1, cor2, t):
    """Interpola linearmente entre duas cores (t: 0.0 → cor1, 1.0 → cor2)."""
    return clamp_cor(
        int(cor1[0] + (cor2[0] - cor1[0]) * t),
        int(cor1[1] + (cor2[1] - cor1[1]) * t),
        int(cor1[2] + (cor2[2] - cor1[2]) * t),
    )


# Contador global de frames para animações
frame_counter = 0


def desenhar_fundo(janela):
    """Desenha fundo gradiente escuro futurista."""
    for y in range(ALTURA_JANELA):
        t = y / ALTURA_JANELA
        r = int(BG_ESCURO[0] + (BG_PROFUNDO[0] - BG_ESCURO[0]) * t)
        g = int(BG_ESCURO[1] + (BG_PROFUNDO[1] - BG_ESCURO[1]) * t)
        b = int(BG_ESCURO[2] + (BG_PROFUNDO[2] - BG_ESCURO[2]) * t)
        pygame.draw.line(janela, (r, g, b), (0, y), (LARGURA_JANELA, y))


# Pré-gerar o fundo como surface estática
FUNDO_SURFACE = pygame.Surface((LARGURA_JANELA, ALTURA_JANELA))
desenhar_fundo(FUNDO_SURFACE)


def desenhar_particulas(janela, lista_particulas):
    """Atualiza e desenha partículas animadas."""
    for p in lista_particulas:
        p.atualizar()
        p.desenhar(janela)


# ── Casas do tabuleiro (estilo neon/glass) ─────────────────────

def criar_texturas_casas():
    """Pré-gera surfaces com estilo glassmorphism para cada casa."""
    texturas = {}

    for r in range(LINHAS):
        for c in range(COLUNAS):
            is_clara = (r + c) % 2 == 0
            cor_base = CASA_CLARA if is_clara else CASA_ESCURA

            surf = pygame.Surface((TAMANHO_CASA, TAMANHO_CASA), pygame.SRCALPHA)

            # Fundo da casa
            pygame.draw.rect(surf, (*cor_base, 200), (0, 0, TAMANHO_CASA, TAMANHO_CASA))

            # Gradiente sutil (topo levemente mais claro — efeito glass)
            grad = pygame.Surface((TAMANHO_CASA, TAMANHO_CASA // 2), pygame.SRCALPHA)
            for y in range(TAMANHO_CASA // 2):
                alpha = int(15 * (1.0 - y / (TAMANHO_CASA // 2)))
                grad.fill((100, 140, 220, alpha), (0, y, TAMANHO_CASA, 1))
            surf.blit(grad, (0, 0))

            # Borda interna sutil
            borda_cor = (*CASA_BORDA, 80) if is_clara else (*CASA_BORDA, 40)
            pygame.draw.rect(surf, borda_cor, (0, 0, TAMANHO_CASA, TAMANHO_CASA), 1)

            texturas[(r, c)] = surf

    return texturas


# ── Borda neon do tabuleiro ────────────────────────────────────

def desenhar_borda_tabuleiro(janela, tempo):
    """Desenha borda neon com glow ao redor do tabuleiro."""
    bx = BOARD_X - 3
    by = BOARD_Y - 3
    bw = TABULEIRO_PX + 6
    bh = TABULEIRO_PX + 6

    # Glow externo pulsante
    pulso = 0.6 + 0.4 * math.sin(tempo * 0.8)
    alpha_glow = int(25 * pulso)

    glow = pygame.Surface((bw + 16, bh + 16), pygame.SRCALPHA)
    pygame.draw.rect(glow, (30, 80, 180, alpha_glow), (0, 0, bw + 16, bh + 16), border_radius=4)
    janela.blit(glow, (bx - 8, by - 8))

    # Borda principal — linha neon azul
    cor_borda = lerp_cor((20, 50, 100), (40, 100, 200), pulso)
    pygame.draw.rect(janela, cor_borda, (bx, by, bw, bh), 2, border_radius=2)

    # Cantos brilhantes
    canto_tam = 12
    cor_canto = lerp_cor((40, 100, 200), (80, 160, 255), pulso)
    # Top-left
    pygame.draw.line(janela, cor_canto, (bx, by), (bx + canto_tam, by), 2)
    pygame.draw.line(janela, cor_canto, (bx, by), (bx, by + canto_tam), 2)
    # Top-right
    pygame.draw.line(janela, cor_canto, (bx + bw, by), (bx + bw - canto_tam, by), 2)
    pygame.draw.line(janela, cor_canto, (bx + bw, by), (bx + bw, by + canto_tam), 2)
    # Bottom-left
    pygame.draw.line(janela, cor_canto, (bx, by + bh), (bx + canto_tam, by + bh), 2)
    pygame.draw.line(janela, cor_canto, (bx, by + bh), (bx, by + bh - canto_tam), 2)
    # Bottom-right
    pygame.draw.line(janela, cor_canto, (bx + bw, by + bh), (bx + bw - canto_tam, by + bh), 2)
    pygame.draw.line(janela, cor_canto, (bx + bw, by + bh), (bx + bw, by + bh - canto_tam), 2)


# ── Peça Neon ──────────────────────────────────────────────────

def desenhar_peca_neon(janela, cx, cy, raio, cor_neon, cor_escura, is_dama=False, selecionada=False, tempo=0):
    """Desenha uma peça com estética neon futurista:
    glow externo + corpo escuro + anel neon + brilho especular."""

    # ── Glow externo (sempre presente, mais forte se selecionada) ──
    glow_raio = raio + (10 if selecionada else 6)
    glow_alpha = 80 if selecionada else 35
    if selecionada:
        pulso = 0.7 + 0.3 * math.sin(tempo * 3.0)
        glow_alpha = int(glow_alpha * pulso)

    glow_surf = pygame.Surface((glow_raio * 2 + 4, glow_raio * 2 + 4), pygame.SRCALPHA)
    gc = glow_raio + 2
    # Camadas de glow
    pygame.draw.circle(glow_surf, (*cor_neon[:3], glow_alpha // 4), (gc, gc), glow_raio)
    pygame.draw.circle(glow_surf, (*cor_neon[:3], glow_alpha // 2), (gc, gc), glow_raio - 4)
    pygame.draw.circle(glow_surf, (*cor_neon[:3], glow_alpha), (gc, gc), raio + 2)
    janela.blit(glow_surf, (cx - gc, cy - gc))

    # ── Glow extra branco se selecionada ──
    if selecionada:
        sel_surf = pygame.Surface((raio * 2 + 20, raio * 2 + 20), pygame.SRCALPHA)
        sc = raio + 10
        pygame.draw.circle(sel_surf, (255, 255, 255, 20), (sc, sc), raio + 8)
        janela.blit(sel_surf, (cx - sc, cy - sc))

    # ── Corpo da peça — escuro com gradiente ──
    # Base escura
    pygame.draw.circle(janela, (8, 10, 20), (cx, cy), raio)

    # Gradiente radial (corpo escuro com tom da cor neon)
    passos = 10
    cor_centro = (
        min(255, cor_escura[0] // 3 + 15),
        min(255, cor_escura[1] // 3 + 15),
        min(255, cor_escura[2] // 3 + 15),
    )
    cor_borda_interna = (
        cor_escura[0] // 5,
        cor_escura[1] // 5,
        cor_escura[2] // 5,
    )
    for i in range(passos):
        t = i / passos
        r_atual = int(raio * (1 - t * 0.85))
        if r_atual <= 0:
            break
        offset_x = int(-raio * 0.06 * t)
        offset_y = int(-raio * 0.10 * t)
        cor_atual = lerp_cor(cor_borda_interna, cor_centro, t * t)
        pygame.draw.circle(janela, cor_atual, (cx + offset_x, cy + offset_y), r_atual)

    # ── Anel neon (borda da peça) ──
    pygame.draw.circle(janela, cor_neon, (cx, cy), raio, 2)
    # Anel interno mais sutil
    pygame.draw.circle(janela, cor_escura, (cx, cy), raio - 4, 1)

    # ── Brilho especular (highlight superior) ──
    hl_surf = pygame.Surface((raio * 2, raio * 2), pygame.SRCALPHA)
    hl_w = int(raio * 0.6)
    hl_h = int(raio * 0.25)
    hl_x = int(raio * 0.35)
    hl_y = int(raio * 0.18)
    pygame.draw.ellipse(hl_surf, (255, 255, 255, 30),
                        (hl_x, hl_y, hl_w, hl_h))
    janela.blit(hl_surf, (cx - raio, cy - raio))

    # ── Ponto central luminoso ──
    pygame.draw.circle(janela, (*cor_neon[:3], 180), (cx, cy), 3)
    pygame.draw.circle(janela, (255, 255, 255), (cx, cy), 1)

    # ── Dama: anel orbital animado ──
    if is_dama:
        desenhar_anel_orbital(janela, cx, cy, raio, cor_neon, tempo)


# ── Anel Orbital para peça Dama ───────────────────────────────

def desenhar_anel_orbital(janela, cx, cy, raio, cor_neon, tempo):
    """Desenha um anel orbital animado ao redor da peça dama."""
    # Anel externo duplo
    pygame.draw.circle(janela, cor_neon, (cx, cy), raio + 1, 2)
    pygame.draw.circle(janela, cor_variante(cor_neon, -60), (cx, cy), raio + 4, 1)

    # Pontos orbitais animados (3 pontos girando)
    orbit_raio = raio + 3
    for i in range(3):
        angulo = tempo * 2.0 + i * (math.pi * 2 / 3)
        px = cx + int(orbit_raio * math.cos(angulo))
        py = cy + int(orbit_raio * math.sin(angulo))
        # Glow do ponto
        dot_surf = pygame.Surface((12, 12), pygame.SRCALPHA)
        pygame.draw.circle(dot_surf, (*cor_neon[:3], 60), (6, 6), 5)
        pygame.draw.circle(dot_surf, cor_neon, (6, 6), 2)
        pygame.draw.circle(dot_surf, (255, 255, 255), (6, 6), 1)
        janela.blit(dot_surf, (px - 6, py - 6))

    # Símbolo central "★" (hexágono pequeno)
    hex_r = raio * 0.22
    for i in range(6):
        a1 = math.pi / 3 * i + tempo * 0.5
        a2 = math.pi / 3 * (i + 1) + tempo * 0.5
        x1 = cx + int(hex_r * math.cos(a1))
        y1 = cy + int(hex_r * math.sin(a1))
        x2 = cx + int(hex_r * math.cos(a2))
        y2 = cy + int(hex_r * math.sin(a2))
        pygame.draw.line(janela, cor_neon, (x1, y1), (x2, y2), 1)


# ── HUD Futurista ─────────────────────────────────────────────

def desenhar_hud(janela, turno, pecas_vermelhas, pecas_azuis, tempo):
    """Desenha HUD minimalista neon."""
    # Fundo
    hud_surf = pygame.Surface((LARGURA_JANELA, HUD_ALTURA), pygame.SRCALPHA)
    hud_surf.fill((*HUD_BG, 230))
    janela.blit(hud_surf, (0, 0))

    # Linha inferior com glow
    pulso = 0.6 + 0.4 * math.sin(tempo * 1.2)
    cor_linha = lerp_cor((15, 30, 60), (30, 70, 140), pulso)
    pygame.draw.line(janela, cor_linha, (0, HUD_ALTURA - 1), (LARGURA_JANELA, HUD_ALTURA - 1), 1)

    # Glow sutil na linha
    glow_line = pygame.Surface((LARGURA_JANELA, 4), pygame.SRCALPHA)
    glow_line.fill((30, 70, 140, int(15 * pulso)))
    janela.blit(glow_line, (0, HUD_ALTURA - 3))

    cy = HUD_ALTURA // 2

    # ── Lado esquerdo — Ciano ──
    # Mini peça
    mini_glow = pygame.Surface((26, 26), pygame.SRCALPHA)
    pygame.draw.circle(mini_glow, (*NEON_CIANO[:3], 40), (13, 13), 12)
    pygame.draw.circle(mini_glow, NEON_CIANO, (13, 13), 8)
    pygame.draw.circle(mini_glow, (8, 10, 20), (13, 13), 6)
    pygame.draw.circle(mini_glow, NEON_CIANO, (13, 13), 6, 1)
    janela.blit(mini_glow, (14, cy - 13))
    txt_esc = FONTE_HUD.render(f"CIANO  {pecas_vermelhas}", True, NEON_CIANO)
    janela.blit(txt_esc, (44, cy - txt_esc.get_height() // 2))

    # ── Lado direito — Magenta ──
    mini_glow2 = pygame.Surface((26, 26), pygame.SRCALPHA)
    pygame.draw.circle(mini_glow2, (*NEON_MAGENTA[:3], 40), (13, 13), 12)
    pygame.draw.circle(mini_glow2, NEON_MAGENTA, (13, 13), 8)
    pygame.draw.circle(mini_glow2, (8, 10, 20), (13, 13), 6)
    pygame.draw.circle(mini_glow2, NEON_MAGENTA, (13, 13), 6, 1)
    txt_cla = FONTE_HUD.render(f"MAGENTA  {pecas_azuis}", True, NEON_MAGENTA)
    janela.blit(mini_glow2, (LARGURA_JANELA - 44 - txt_cla.get_width(), cy - 13))
    janela.blit(txt_cla, (LARGURA_JANELA - 40 - txt_cla.get_width() + 22, cy - txt_cla.get_height() // 2))

    # ── Centro — indicador de turno ──
    nome = NOME_JOGADOR[turno]
    cor_turno = COR_VISUAL_PECA[turno]
    txt_turno = FONTE_HUD.render(f"▸ {nome}", True, cor_turno)
    tx = LARGURA_JANELA // 2 - txt_turno.get_width() // 2
    janela.blit(txt_turno, (tx, cy - txt_turno.get_height() // 2))

    # Linha animada embaixo do nome do turno
    lw = txt_turno.get_width()
    underline_y = cy + txt_turno.get_height() // 2 + 2
    pygame.draw.line(janela, cor_turno, (tx, underline_y), (tx + lw, underline_y), 1)


# ── Botão Neon ────────────────────────────────────────────────

def desenhar_botao(janela, texto, cx, cy, mouse_pos=None, largura=220, altura=50):
    """Desenha um botão neon com hover glow. Retorna o Rect."""
    rect = pygame.Rect(cx - largura // 2, cy - altura // 2, largura, altura)
    hover = mouse_pos is not None and rect.collidepoint(mouse_pos)

    if hover:
        # Glow externo
        glow = pygame.Surface((largura + 20, altura + 20), pygame.SRCALPHA)
        pygame.draw.rect(glow, (0, 200, 255, 25), (0, 0, largura + 20, altura + 20), border_radius=12)
        janela.blit(glow, (rect.x - 10, rect.y - 10))

    # Fundo
    bg_surf = pygame.Surface((largura, altura), pygame.SRCALPHA)
    bg_alpha = 180 if hover else 140
    pygame.draw.rect(bg_surf, (12, 20, 40, bg_alpha), (0, 0, largura, altura), border_radius=8)
    janela.blit(bg_surf, rect.topleft)

    # Gradiente sutil no topo
    grad = pygame.Surface((largura, altura // 3), pygame.SRCALPHA)
    grad.fill((100, 180, 255, 12 if hover else 6))
    janela.blit(grad, rect.topleft)

    # Borda neon
    cor_borda = NEON_CIANO if hover else (40, 100, 180)
    pygame.draw.rect(janela, cor_borda, rect, 2, border_radius=8)

    # Texto
    cor_texto = NEON_CIANO if hover else HUD_TEXTO_BRILHO
    txt = FONTE_BOTAO.render(texto, True, cor_texto)
    janela.blit(txt, (cx - txt.get_width() // 2, cy - txt.get_height() // 2))

    return rect


# ── Tela de Menu ──────────────────────────────────────────────

def desenhar_tela_menu(janela, mouse_pos, tempo):
    """Tela futurista com partículas, título neon e botão."""
    # Fundo
    janela.blit(FUNDO_SURFACE, (0, 0))

    # Partículas
    desenhar_particulas(janela, PARTICULAS_MENU)

    # Grade decorativa sutil
    grade_surf = pygame.Surface((LARGURA_JANELA, ALTURA_JANELA), pygame.SRCALPHA)
    for x in range(0, LARGURA_JANELA, 40):
        pygame.draw.line(grade_surf, (20, 40, 80, 15), (x, 0), (x, ALTURA_JANELA))
    for y in range(0, ALTURA_JANELA, 40):
        pygame.draw.line(grade_surf, (20, 40, 80, 15), (0, y), (LARGURA_JANELA, y))
    janela.blit(grade_surf, (0, 0))

    # Moldura decorativa com cantos neon
    lx = LARGURA_JANELA // 2
    borda_rect = pygame.Rect(40, 40, LARGURA_JANELA - 80, ALTURA_JANELA - 80)
    pygame.draw.rect(janela, (25, 45, 85), borda_rect, 1, border_radius=4)

    # Cantos brilhantes
    ct = 20
    cor_canto = lerp_cor((30, 80, 160), (60, 160, 255), 0.6 + 0.4 * math.sin(tempo * 1.5))
    for (bx, by, dx, dy) in [
        (40, 40, 1, 1), (LARGURA_JANELA - 40, 40, -1, 1),
        (40, ALTURA_JANELA - 40, 1, -1), (LARGURA_JANELA - 40, ALTURA_JANELA - 40, -1, -1)
    ]:
        pygame.draw.line(janela, cor_canto, (bx, by), (bx + ct * dx, by), 2)
        pygame.draw.line(janela, cor_canto, (bx, by), (bx, by + ct * dy), 2)

    # ── Título "DAMA" ──
    cy_titulo = ALTURA_JANELA // 2 - 150

    # Glow do título
    titulo_glow = FONTE_TITULO.render("DAMA", True, (*NEON_CIANO[:3],))
    glow_surf = pygame.Surface(titulo_glow.get_size(), pygame.SRCALPHA)
    glow_surf.blit(titulo_glow, (0, 0))
    glow_surf.set_alpha(int(30 + 20 * math.sin(tempo * 1.5)))
    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
        janela.blit(glow_surf, (lx - titulo_glow.get_width() // 2 + dx,
                                 cy_titulo + dy))

    # Texto principal
    titulo = FONTE_TITULO.render("DAMA", True, NEON_CIANO)
    janela.blit(titulo, (lx - titulo.get_width() // 2, cy_titulo))

    # ── Linha decorativa com diamante ──
    ly = cy_titulo + titulo.get_height() + 18
    cor_linha = lerp_cor((20, 60, 120), (40, 120, 200), 0.5 + 0.5 * math.sin(tempo))
    pygame.draw.line(janela, cor_linha, (lx - 140, ly), (lx - 10, ly), 1)
    pygame.draw.line(janela, cor_linha, (lx + 10, ly), (lx + 140, ly), 1)
    d = 5
    pygame.draw.polygon(janela, NEON_CIANO,
                        [(lx, ly - d), (lx + d, ly), (lx, ly + d), (lx - d, ly)])

    # ── Subtítulo ──
    sub = FONTE_SUB.render("N E O N   C H E C K E R S", True, (100, 130, 180))
    janela.blit(sub, (lx - sub.get_width() // 2, ly + 16))

    # ── Peças decorativas ──
    peca_y = ly + 75
    desenhar_peca_neon(janela, lx - 70, peca_y, 22, NEON_CIANO, NEON_CIANO_ESCURO, tempo=tempo)
    desenhar_peca_neon(janela, lx + 70, peca_y, 22, NEON_MAGENTA, NEON_MAGENTA_ESCURO, tempo=tempo)

    # Vs texto
    vs_txt = FONTE_MINI.render("VS", True, (60, 80, 120))
    janela.blit(vs_txt, (lx - vs_txt.get_width() // 2, peca_y - vs_txt.get_height() // 2))

    # ── Botão "JOGAR" ──
    btn_y = ALTURA_JANELA // 2 + 130
    return desenhar_botao(janela, "▶  JOGAR", lx, btn_y, mouse_pos, 240, 52)


# ── Tela de Vitória ───────────────────────────────────────────

def desenhar_tela_vitoria(janela, vencedor, mouse_pos, tempo):
    """Overlay futurista de vitória com painel glassmorphism."""
    # Overlay escuro
    overlay = pygame.Surface((LARGURA_JANELA, ALTURA_JANELA), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    janela.blit(overlay, (0, 0))

    # Partículas sobre o overlay
    desenhar_particulas(janela, PARTICULAS)

    # Painel central glassmorphism
    pw, ph = 420, 280
    px = LARGURA_JANELA // 2 - pw // 2
    py = ALTURA_JANELA // 2 - ph // 2

    # Glow externo do painel
    glow_rect = pygame.Surface((pw + 30, ph + 30), pygame.SRCALPHA)
    cor_glow_venc = NEON_CIANO if vencedor == "VERMELHO" else NEON_MAGENTA
    pygame.draw.rect(glow_rect, (*cor_glow_venc[:3], 15), (0, 0, pw + 30, ph + 30), border_radius=16)
    janela.blit(glow_rect, (px - 15, py - 15))

    # Fundo do painel (glassmorphism)
    painel_surf = pygame.Surface((pw, ph), pygame.SRCALPHA)
    pygame.draw.rect(painel_surf, (10, 15, 30, 210), (0, 0, pw, ph), border_radius=12)
    # Gradiente glass no topo
    glass = pygame.Surface((pw, ph // 3), pygame.SRCALPHA)
    glass.fill((80, 120, 200, 10))
    painel_surf.blit(glass, (0, 0))
    janela.blit(painel_surf, (px, py))

    # Borda neon
    painel_rect = pygame.Rect(px, py, pw, ph)
    pygame.draw.rect(janela, cor_glow_venc, painel_rect, 2, border_radius=12)

    # Cantos brilhantes
    ct = 15
    pulso = 0.6 + 0.4 * math.sin(tempo * 2.0)
    cor_c = lerp_cor(cor_glow_venc, (255, 255, 255), pulso * 0.3)
    for (bx, by2, dx, dy) in [
        (px, py, 1, 1), (px + pw, py, -1, 1),
        (px, py + ph, 1, -1), (px + pw, py + ph, -1, -1)
    ]:
        pygame.draw.line(janela, cor_c, (bx, by2), (bx + ct * dx, by2), 2)
        pygame.draw.line(janela, cor_c, (bx, by2), (bx, by2 + ct * dy), 2)

    # ── Texto "VITÓRIA" ──
    titulo_txt = FONTE_VITORIA.render("VITÓRIA", True, cor_glow_venc)
    janela.blit(titulo_txt, (LARGURA_JANELA // 2 - titulo_txt.get_width() // 2, py + 25))

    # ── Nome do vencedor ──
    cor_logica = VERMELHO if vencedor == "VERMELHO" else AZUL_CLARO
    nome = NOME_JOGADOR[cor_logica]
    nome_txt = FONTE_SUB.render(f"Jogador {nome} venceu!", True, HUD_TEXTO_BRILHO)
    janela.blit(nome_txt, (LARGURA_JANELA // 2 - nome_txt.get_width() // 2, py + 80))

    # Linha decorativa
    line_y = py + 115
    pygame.draw.line(janela, (*cor_glow_venc[:3],), (px + 40, line_y), (px + pw - 40, line_y), 1)

    # Peça vencedora decorativa (com dama)
    cor_neon_venc = COR_VISUAL_PECA[cor_logica]
    cor_esc_venc = COR_VISUAL_ESCURA[cor_logica]
    desenhar_peca_neon(janela, LARGURA_JANELA // 2, line_y + 40, 22,
                       cor_neon_venc, cor_esc_venc, is_dama=True, tempo=tempo)

    # ── Botão "JOGAR NOVAMENTE" ──
    btn_y = py + ph - 48
    return desenhar_botao(janela, "▶  JOGAR NOVAMENTE", LARGURA_JANELA // 2, btn_y,
                          mouse_pos, 280, 48)


# ═══════════════════════════════════════════════════════════════
#  CLASSE DA PEÇA
#  (lógica idêntica ao original — apenas desenhar() reescrito)
# ═══════════════════════════════════════════════════════════════

class Peca:
    PADDING = 12
    BORDA = 3

    def __init__(self, linha, coluna, cor):
        self.linha = linha
        self.coluna = coluna
        self.cor = cor  # VERMELHO ou AZUL_CLARO (identificador lógico)
        self.dama = False
        self.x = 0
        self.y = 0
        self.calcular_pos()

    def calcular_pos(self):
        """Calcula posição em pixels (com offset do padding e HUD)."""
        self.x = BOARD_X + TAMANHO_CASA * self.coluna + TAMANHO_CASA // 2
        self.y = BOARD_Y + TAMANHO_CASA * self.linha + TAMANHO_CASA // 2

    def virar_dama(self):
        self.dama = True

    def mover(self, linha, coluna):
        self.linha = linha
        self.coluna = coluna
        self.calcular_pos()

    def desenhar(self, janela, selecionada=False, tempo=0):
        """Desenha a peça com estética neon futurista."""
        raio = TAMANHO_CASA // 2 - self.PADDING
        cor_neon = COR_VISUAL_PECA[self.cor]
        cor_escura = COR_VISUAL_ESCURA[self.cor]
        desenhar_peca_neon(janela, self.x, self.y, raio, cor_neon, cor_escura,
                           is_dama=self.dama, selecionada=selecionada, tempo=tempo)


# ═══════════════════════════════════════════════════════════════
#  CLASSE DO TABULEIRO
#  (lógica idêntica ao original — apenas desenhar_casas() reescrito)
# ═══════════════════════════════════════════════════════════════

class Tabuleiro:
    def __init__(self):
        self.tabuleiro = []
        self.pecas_vermelhas = self.pecas_azuis = 12
        self.damas_vermelhas = self.damas_azuis = 0
        self.criar_tabuleiro()

    def criar_tabuleiro(self):
        for linha in range(LINHAS):
            self.tabuleiro.append([])
            for coluna in range(COLUNAS):
                casa_jogavel = (linha + coluna) % 2 == 1
                if casa_jogavel and linha < 3:
                    self.tabuleiro[linha].append(Peca(linha, coluna, AZUL_CLARO))
                elif casa_jogavel and linha > 4:
                    self.tabuleiro[linha].append(Peca(linha, coluna, VERMELHO))
                else:
                    self.tabuleiro[linha].append(0)

    def desenhar_casas(self, janela, tempo):
        """Desenha o fundo, casas glassmorphism e borda neon."""
        janela.blit(FUNDO_SURFACE, (0, 0))
        desenhar_particulas(janela, PARTICULAS)
        desenhar_borda_tabuleiro(janela, tempo)
        for linha in range(LINHAS):
            for coluna in range(COLUNAS):
                x = BOARD_X + coluna * TAMANHO_CASA
                y = BOARD_Y + linha * TAMANHO_CASA
                janela.blit(TEXTURAS_CASAS[(linha, coluna)], (x, y))

    def desenhar(self, janela, selecionada=None, tempo=0):
        """Desenha casas + peças (com destaque na peça selecionada)."""
        self.desenhar_casas(janela, tempo)
        for linha in range(LINHAS):
            for coluna in range(COLUNAS):
                peca = self.tabuleiro[linha][coluna]
                if peca != 0:
                    is_sel = (selecionada is not None and peca == selecionada)
                    peca.desenhar(janela, selecionada=is_sel, tempo=tempo)

    # ── Lógica do jogo (inalterada) ───────────────────────────

    def get_peca(self, linha, coluna):
        return self.tabuleiro[linha][coluna]

    def mover(self, peca, linha, coluna):
        self.tabuleiro[peca.linha][peca.coluna], self.tabuleiro[linha][coluna] = \
            self.tabuleiro[linha][coluna], self.tabuleiro[peca.linha][peca.coluna]
        peca.mover(linha, coluna)

        if linha == 0 or linha == LINHAS - 1:
            if not peca.dama:
                peca.virar_dama()
                if peca.cor == VERMELHO:
                    self.damas_vermelhas += 1
                else:
                    self.damas_azuis += 1

    def remover(self, pecas):
        for peca in pecas:
            self.tabuleiro[peca.linha][peca.coluna] = 0
            if peca != 0:
                if peca.cor == VERMELHO:
                    self.pecas_vermelhas -= 1
                else:
                    self.pecas_azuis -= 1

    def vencedor(self):
        if self.pecas_vermelhas <= 0:
            return "AZUL"
        elif self.pecas_azuis <= 0:
            return "VERMELHO"
        return None

    def get_pecas_validas(self, peca):
        """Retorna dict {(linha, coluna): [pecas_capturadas]} com movimentos validos."""
        movimentos = {}
        esquerda = peca.coluna - 1
        direita = peca.coluna + 1
        linha = peca.linha

        if peca.cor == VERMELHO or peca.dama:
            movimentos.update(self._mover_esquerda(linha - 1, max(linha - 3, -1), -1, peca.cor, esquerda))
            movimentos.update(self._mover_direita(linha - 1, max(linha - 3, -1), -1, peca.cor, direita))
        if peca.cor == AZUL_CLARO or peca.dama:
            movimentos.update(self._mover_esquerda(linha + 1, min(linha + 3, LINHAS), 1, peca.cor, esquerda))
            movimentos.update(self._mover_direita(linha + 1, min(linha + 3, LINHAS), 1, peca.cor, direita))

        return movimentos

    def _mover_esquerda(self, start, stop, passo, cor, esquerda, pecas_capturadas=[]):
        movimentos = {}
        ultima_peca = []
        for r in range(start, stop, passo):
            if esquerda < 0:
                break

            atual = self.tabuleiro[r][esquerda]
            if atual == 0:
                if pecas_capturadas and not ultima_peca:
                    break
                elif pecas_capturadas:
                    movimentos[(r, esquerda)] = ultima_peca + pecas_capturadas
                else:
                    movimentos[(r, esquerda)] = ultima_peca

                if ultima_peca:
                    if passo == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, LINHAS)
                    movimentos.update(self._mover_esquerda(r + passo, row, passo, cor, esquerda - 1, pecas_capturadas=ultima_peca))
                    movimentos.update(self._mover_direita(r + passo, row, passo, cor, esquerda + 1, pecas_capturadas=ultima_peca))
                break
            elif atual.cor == cor:
                break
            else:
                ultima_peca = [atual]

            esquerda -= 1

        return movimentos

    def _mover_direita(self, start, stop, passo, cor, direita, pecas_capturadas=[]):
        movimentos = {}
        ultima_peca = []
        for r in range(start, stop, passo):
            if direita >= COLUNAS:
                break

            atual = self.tabuleiro[r][direita]
            if atual == 0:
                if pecas_capturadas and not ultima_peca:
                    break
                elif pecas_capturadas:
                    movimentos[(r, direita)] = ultima_peca + pecas_capturadas
                else:
                    movimentos[(r, direita)] = ultima_peca

                if ultima_peca:
                    if passo == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, LINHAS)
                    movimentos.update(self._mover_esquerda(r + passo, row, passo, cor, direita - 1, pecas_capturadas=ultima_peca))
                    movimentos.update(self._mover_direita(r + passo, row, passo, cor, direita + 1, pecas_capturadas=ultima_peca))
                break
            elif atual.cor == cor:
                break
            else:
                ultima_peca = [atual]

            direita += 1

        return movimentos


# ═══════════════════════════════════════════════════════════════
#  CLASSE DO JOGO
#  (lógica idêntica ao original — apenas métodos visuais reescritos)
# ═══════════════════════════════════════════════════════════════

class Jogo:
    def __init__(self, janela):
        self.janela = janela
        self._iniciar()

    def _iniciar(self):
        self.selecionada = None
        self.tabuleiro = Tabuleiro()
        self.turno = VERMELHO
        self.movimentos_validos = {}

    def atualizar(self, mouse_pos=None, tempo=0):
        """Redesenha tabuleiro, peças, hover, movimentos válidos e HUD."""
        self.tabuleiro.desenhar(self.janela, selecionada=self.selecionada, tempo=tempo)
        self.desenhar_hover(mouse_pos)
        self.desenhar_movimentos_validos(self.movimentos_validos, tempo)
        # Redesenha peça selecionada por cima (para o glow ficar acima dos indicadores)
        if self.selecionada:
            self.selecionada.desenhar(self.janela, selecionada=True, tempo=tempo)
        desenhar_hud(self.janela, self.turno,
                     self.tabuleiro.pecas_vermelhas, self.tabuleiro.pecas_azuis, tempo)

    def resetar(self):
        self._iniciar()

    # ── Lógica de seleção e movimento (inalterada) ────────────

    def selecionar(self, linha, coluna):
        if self.selecionada:
            resultado = self._mover(linha, coluna)
            if not resultado:
                self.selecionada = None
                self.selecionar(linha, coluna)

        peca = self.tabuleiro.get_peca(linha, coluna)
        if peca != 0 and peca.cor == self.turno:
            self.selecionada = peca
            self.movimentos_validos = self.tabuleiro.get_pecas_validas(peca)
            return True

        return False

    def _mover(self, linha, coluna):
        peca = self.tabuleiro.get_peca(linha, coluna)
        if self.selecionada and peca == 0 and (linha, coluna) in self.movimentos_validos:
            self.tabuleiro.mover(self.selecionada, linha, coluna)
            capturadas = self.movimentos_validos[(linha, coluna)]
            if capturadas:
                self.tabuleiro.remover(capturadas)
            self._trocar_turno()
        else:
            return False

        return True

    def _trocar_turno(self):
        self.movimentos_validos = {}
        self.turno = AZUL_CLARO if self.turno == VERMELHO else VERMELHO

    def vencedor(self):
        return self.tabuleiro.vencedor()

    # ── Métodos visuais (reescritos) ──────────────────────────

    def desenhar_movimentos_validos(self, movimentos, tempo=0):
        """Indica movimentos válidos com círculos neon verdes pulsantes."""
        pulso = 0.5 + 0.5 * math.sin(tempo * 4.0)

        for (linha, coluna) in movimentos:
            cx = BOARD_X + coluna * TAMANHO_CASA + TAMANHO_CASA // 2
            cy = BOARD_Y + linha * TAMANHO_CASA + TAMANHO_CASA // 2
            px = BOARD_X + coluna * TAMANHO_CASA
            py = BOARD_Y + linha * TAMANHO_CASA

            # Glow sutil sobre a casa
            glow = pygame.Surface((TAMANHO_CASA, TAMANHO_CASA), pygame.SRCALPHA)
            glow_alpha = int(15 + 10 * pulso)
            pygame.draw.rect(glow, (*NEON_VERDE[:3], glow_alpha),
                             (0, 0, TAMANHO_CASA, TAMANHO_CASA))
            self.janela.blit(glow, (px, py))

            # Círculo neon pulsante
            raio_ext = int(11 + 3 * pulso)
            circ_surf = pygame.Surface((raio_ext * 2 + 8, raio_ext * 2 + 8), pygame.SRCALPHA)
            centro = raio_ext + 4
            # Glow externo
            pygame.draw.circle(circ_surf, (*NEON_VERDE[:3], int(25 * pulso)),
                               (centro, centro), raio_ext + 2)
            # Anel
            pygame.draw.circle(circ_surf, NEON_VERDE, (centro, centro), raio_ext, 2)
            # Centro
            pygame.draw.circle(circ_surf, (*NEON_VERDE[:3], int(40 + 30 * pulso)),
                               (centro, centro), 4)
            self.janela.blit(circ_surf, (cx - centro, cy - centro))

    def desenhar_hover(self, mouse_pos):
        """Highlight neon ao passar o mouse sobre uma peça jogável."""
        if mouse_pos is None:
            return
        mx, my = mouse_pos
        coluna = (mx - BOARD_X) // TAMANHO_CASA
        linha = (my - BOARD_Y) // TAMANHO_CASA
        if 0 <= linha < LINHAS and 0 <= coluna < COLUNAS:
            peca = self.tabuleiro.get_peca(linha, coluna)
            if peca != 0 and peca.cor == self.turno and peca != self.selecionada:
                cor_hover = COR_VISUAL_PECA[self.turno]
                hover_surf = pygame.Surface((TAMANHO_CASA, TAMANHO_CASA), pygame.SRCALPHA)
                pygame.draw.rect(hover_surf, (*cor_hover[:3], 12),
                                 (0, 0, TAMANHO_CASA, TAMANHO_CASA))
                pygame.draw.rect(hover_surf, (*cor_hover[:3], 60),
                                 (0, 0, TAMANHO_CASA, TAMANHO_CASA), 1)
                self.janela.blit(hover_surf,
                                (BOARD_X + coluna * TAMANHO_CASA,
                                 BOARD_Y + linha * TAMANHO_CASA))


# ═══════════════════════════════════════════════════════════════
#  UTILIDADES
# ═══════════════════════════════════════════════════════════════

def get_pos_mouse(pos):
    """Converte posição do mouse em (linha, coluna) do tabuleiro."""
    x, y = pos
    linha = (y - BOARD_Y) // TAMANHO_CASA
    coluna = (x - BOARD_X) // TAMANHO_CASA
    return linha, coluna


# Mapeamento da cor lógica retornada por vencedor() → nome exibido no HUD
_NOME_VENCEDOR_HUD = {
    "VERMELHO": "CIANO",
    "AZUL": "MAGENTA",
}


def salvar_resultado(vencedor):
    """Salva o resultado da partida em placar-dama/placar.json.

    Cada registro contém o nome do vencedor (CIANO ou MAGENTA) e a
    data/hora formatada como string legível.
    """
    caminho = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "placar-dama",
        "placar.json",
    )

    # Garante que o diretório exista
    os.makedirs(os.path.dirname(caminho), exist_ok=True)

    # Se o arquivo não existir, cria com lista vazia
    if not os.path.exists(caminho):
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump([], f)

    # Lê o conteúdo atual
    with open(caminho, "r", encoding="utf-8") as f:
        partidas = json.load(f)

    # Adiciona novo registro
    nome_vencedor = _NOME_VENCEDOR_HUD.get(vencedor, vencedor)
    partidas.append({
        "vencedor": nome_vencedor,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    })

    # Salva a lista atualizada
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(partidas, f, ensure_ascii=False, indent=2)


# ═══════════════════════════════════════════════════════════════
#  PRÉ-GERAÇÃO DE TEXTURAS (executado uma vez na inicialização)
# ═══════════════════════════════════════════════════════════════

TEXTURAS_CASAS = criar_texturas_casas()


# ═══════════════════════════════════════════════════════════════
#  LOOP PRINCIPAL
# ═══════════════════════════════════════════════════════════════

def main():
    relogio = pygame.time.Clock()
    estado = ESTADO_MENU
    jogo = None
    vencedor_nome = None
    btn_rect = None

    while True:
        relogio.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()

        # Tempo global para animações
        global frame_counter
        frame_counter += 1
        tempo = frame_counter / FPS

        # ── Eventos ──
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if estado == ESTADO_MENU:
                    if btn_rect and btn_rect.collidepoint(evento.pos):
                        jogo = Jogo(JANELA)
                        estado = ESTADO_JOGANDO

                elif estado == ESTADO_JOGANDO:
                    linha, coluna = get_pos_mouse(evento.pos)
                    if 0 <= linha < LINHAS and 0 <= coluna < COLUNAS:
                        jogo.selecionar(linha, coluna)

                elif estado == ESTADO_FIM:
                    if btn_rect and btn_rect.collidepoint(evento.pos):
                        jogo = Jogo(JANELA)
                        estado = ESTADO_JOGANDO
                        vencedor_nome = None

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r and estado in (ESTADO_JOGANDO, ESTADO_FIM):
                    jogo = Jogo(JANELA)
                    estado = ESTADO_JOGANDO
                    vencedor_nome = None

        # ── Desenho ──
        if estado == ESTADO_MENU:
            btn_rect = desenhar_tela_menu(JANELA, mouse_pos, tempo)

        elif estado == ESTADO_JOGANDO:
            jogo.atualizar(mouse_pos, tempo)
            venc = jogo.vencedor()
            if venc:
                vencedor_nome = venc
                estado = ESTADO_FIM
                salvar_resultado(venc)

        elif estado == ESTADO_FIM:
            jogo.atualizar(mouse_pos, tempo)
            btn_rect = desenhar_tela_vitoria(JANELA, vencedor_nome, mouse_pos, tempo)

        pygame.display.update()


if __name__ == "__main__":
    main()
