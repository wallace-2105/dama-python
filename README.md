# 🔴🔵 DAMA — Python Edition

> Um clássico atemporal, reconstruído do zero com Python + Pygame.

<!-- 🎮 Coloque aqui um print ou GIF do jogo rodando -->
<!-- ![gameplay](preview.png) -->

---

## ⚔️ Sobre o jogo
<img width="959" height="505" alt="image" src="https://github.com/user-attachments/assets/38c9143e-51ee-46be-aac5-47e402de5a0e" />

Dama (Checkers) é um dos jogos de tabuleiro mais antigos e estratégicos do mundo. Aqui, ele ganha vida numa versão feita 100% em **Python**, com renderização gráfica via **Pygame** — sem frameworks prontos, sem engine externa, só lógica pura e algumas linhas de código.

Dois jogadores. Um tabuleiro. Captura obrigatória. Sem piedade.

---

## 🕹️ Como jogar

| Ação | Comando |
|---|---|
| Selecionar peça | Clique esquerdo |
| Mover peça | Clique na casa verde destacada |
| Reiniciar partida | Tecla `R` |
| Fechar o jogo | `X` da janela |

**Regras rápidas:**
- 🔴 Vermelho sempre começa
- Peças normais andam 1 casa na diagonal, pra frente
- Captura é obrigatória quando disponível — inclusive captura múltipla em sequência
- Ao alcançar a última linha do tabuleiro, a peça vira **Dama** 👑 e passa a andar em qualquer direção diagonal
- Quem ficar sem peças, perde

---

## 🚀 Rodando localmente

Pré-requisitos: **Python 3.12+**

\`\`\`bash
# Clone o repositório
git clone https://github.com/wallace-2105/dama-python.git
cd dama-python

# Instale as dependências
pip install -r requirements.txt

# Jogue!
python dama.py
\`\`\`

---

## 🛠️ Tecnologias

- **Python 3** — lógica do jogo, regras, validação de movimentos
- **Pygame** — renderização gráfica, input do mouse/teclado, loop do jogo

---

## 📈 Roadmap (próximas evoluções)

- [ ] Visual premium — sprites de peças e tabuleiro com textura
- [ ] Animações de movimento e captura
- [ ] Efeitos sonoros
- [ ] Modo contra IA (algoritmo minimax)
- [ ] Placar de partidas salvo em banco de dados
- [ ] Versão web do placar (PHP)

---

## 👤 Autor

**Wallace Coimbra**
[GitHub](https://github.com/wallace-2105)

---

<p align="center">Feito com ♟️ e muito café</p>
