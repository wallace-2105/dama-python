"""
Jogo de Dama (Checkers) - feito com Pygame
Regras: peças normais andam na diagonal 1 casa pra frente,
capturam pulando o adversário. Ao chegar na última linha, vira Dama
(pode andar pra qualquer direção diagonal).
"""

import pygame
import sys

# ---------- Configurações ----------
LARGURA_JANELA = 640
LINHAS, COLUNAS = 8, 8
TAMANHO_CASA = LARGURA_JANELA // COLUNAS

BRANCO = (245, 245, 220)
PRETO = (40, 40, 40)
VERMELHO = (200, 30, 30)
AZUL_CLARO = (60, 140, 230)
CINZA = (100, 100, 100)
DOURADO = (255, 215, 0)

FPS = 60

pygame.init()
JANELA = pygame.display.set_mode((LARGURA_JANELA, LARGURA_JANELA))
pygame.display.set_caption("Dama")


# ---------- Classe da Peça ----------
class Peca:
    PADDING = 12
    BORDA = 3

    def __init__(self, linha, coluna, cor):
        self.linha = linha
        self.coluna = coluna
        self.cor = cor  # VERMELHO ou AZUL_CLARO
        self.dama = False
        self.x = 0
        self.y = 0
        self.calcular_pos()

    def calcular_pos(self):
        self.x = TAMANHO_CASA * self.coluna + TAMANHO_CASA // 2
        self.y = TAMANHO_CASA * self.linha + TAMANHO_CASA // 2

    def virar_dama(self):
        self.dama = True

    def mover(self, linha, coluna):
        self.linha = linha
        self.coluna = coluna
        self.calcular_pos()

    def desenhar(self, janela):
        raio = TAMANHO_CASA // 2 - self.PADDING
        pygame.draw.circle(janela, CINZA, (self.x, self.y), raio + self.BORDA)
        pygame.draw.circle(janela, self.cor, (self.x, self.y), raio)
        if self.dama:
            pygame.draw.circle(janela, DOURADO, (self.x, self.y), raio // 2)


# ---------- Classe do Tabuleiro ----------
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

    def desenhar_casas(self, janela):
        janela.fill(PRETO)
        for linha in range(LINHAS):
            for coluna in range(linha % 2, COLUNAS, 2):
                pygame.draw.rect(
                    janela, BRANCO,
                    (coluna * TAMANHO_CASA, linha * TAMANHO_CASA, TAMANHO_CASA, TAMANHO_CASA)
                )

    def desenhar(self, janela):
        self.desenhar_casas(janela)
        for linha in range(LINHAS):
            for coluna in range(COLUNAS):
                peca = self.tabuleiro[linha][coluna]
                if peca != 0:
                    peca.desenhar(janela)

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


# ---------- Classe do Jogo ----------
class Jogo:
    def __init__(self, janela):
        self.janela = janela
        self._iniciar()

    def _iniciar(self):
        self.selecionada = None
        self.tabuleiro = Tabuleiro()
        self.turno = VERMELHO
        self.movimentos_validos = {}

    def atualizar(self):
        self.tabuleiro.desenhar(self.janela)
        self.desenhar_movimentos_validos(self.movimentos_validos)
        pygame.display.update()

    def resetar(self):
        self._iniciar()

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

    def desenhar_movimentos_validos(self, movimentos):
        for move in movimentos:
            linha, coluna = move
            pygame.draw.circle(
                self.janela, (20, 180, 20),
                (coluna * TAMANHO_CASA + TAMANHO_CASA // 2, linha * TAMANHO_CASA + TAMANHO_CASA // 2),
                15
            )

    def _trocar_turno(self):
        self.movimentos_validos = {}
        self.turno = AZUL_CLARO if self.turno == VERMELHO else VERMELHO

    def vencedor(self):
        return self.tabuleiro.vencedor()


def get_pos_mouse(pos):
    x, y = pos
    linha = y // TAMANHO_CASA
    coluna = x // TAMANHO_CASA
    return linha, coluna


def mostrar_mensagem(janela, texto):
    fonte = pygame.font.SysFont("arial", 48, bold=True)
    render = fonte.render(texto, True, DOURADO)
    fundo = pygame.Surface((LARGURA_JANELA, 80))
    fundo.fill(PRETO)
    fundo.set_alpha(210)
    janela.blit(fundo, (0, LARGURA_JANELA // 2 - 40))
    janela.blit(render, (LARGURA_JANELA // 2 - render.get_width() // 2, LARGURA_JANELA // 2 - 24))
    pygame.display.update()


def main():
    relogio = pygame.time.Clock()
    jogo = Jogo(JANELA)
    rodando = True
    fim_de_jogo = False

    while rodando:
        relogio.tick(FPS)

        vencedor = jogo.vencedor()
        if vencedor and not fim_de_jogo:
            fim_de_jogo = True

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if evento.type == pygame.MOUSEBUTTONDOWN and not fim_de_jogo:
                pos = pygame.mouse.get_pos()
                linha, coluna = get_pos_mouse(pos)
                if 0 <= linha < LINHAS and 0 <= coluna < COLUNAS:
                    jogo.selecionar(linha, coluna)

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:  # tecla R reinicia o jogo
                    jogo.resetar()
                    fim_de_jogo = False

        jogo.atualizar()

        if fim_de_jogo:
            nome = "VERMELHO" if vencedor == "VERMELHO" else "AZUL"
            mostrar_mensagem(JANELA, f"{nome} venceu! Pressione R para jogar de novo")

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
