
# 🛸 DAMA — Space Edition

> Um clássico atemporal, reconstruído do zero com Python + Pygame — visual futurista, e agora com placar web integrado em PHP.

<!-- 🎮 Coloque aqui um print ou GIF do jogo rodando -->
<!-- ![gameplay](preview.png) -->

---

## ⚔️ Sobre o projeto
<img width="959" height="505" alt="image" src="https://github.com/user-attachments/assets/38c9143e-51ee-46be-aac5-47e402de5a0e" />
<img width="959" height="539" alt="Captura de tela 2026-07-20 165555" src="https://github.com/user-attachments/assets/fc993da6-8c18-4f12-b2f0-34d0ec4960c3" />


Dama (Checkers) é um dos jogos de tabuleiro mais antigos e estratégicos do mundo. Aqui, ele ganha vida numa versão feita 100% em **Python**, com renderização gráfica via **Pygame** — sem frameworks prontos, sem engine externa, só lógica pura e algumas linhas de código.

Tabuleiro escuro, peças com brilho neon em **ciano** e **magenta**, e uma estética futurista/espacial que foge do visual clássico de dama.

Além do jogo, o projeto conta com um **placar web feito em PHP**, que lê os resultados das partidas salvos automaticamente pelo jogo e exibe um histórico completo, com o mesmo visual espacial.

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
- 🩵 Ciano sempre começa
- Peças normais andam 1 casa na diagonal, pra frente
- Captura é obrigatória quando disponível — inclusive captura múltipla em sequência
- Ao alcançar a última linha do tabuleiro, a peça vira **Dama** 👑 e passa a andar em qualquer direção diagonal
- Quem ficar sem peças, perde

---

## 🏆 Placar Web (PHP)

Cada partida jogada é salva automaticamente pelo jogo Python num arquivo compartilhado. Um site em **PHP** lê esse arquivo e exibe:

- Total de partidas jogadas
- Vitórias de cada cor (Ciano / Magenta)
- Histórico completo com data e hora de cada partida
- Botão para zerar o placar quando quiser começar do zero

### Como rodar o placar

```bash
cd placar-dama
php -S localhost:8000
```

Depois acesse `http://localhost:8000` no navegador.

---

## 🚀 Rodando o jogo localmente

Pré-requisitos: **Python 3.12+**

```bash
# Clone o repositório
git clone https://github.com/wallace-2105/dama-python.git
cd dama-python

# Instale as dependências
pip install -r requirements.txt

# Jogue!
python dama.py
```

---

## 📁 Estrutura do projeto

```
dama-python/
├── dama.py              # Lógica e visual do jogo (Python + Pygame)
├── requirements.txt      # Dependências do jogo
├── baixar_fonte.py       # Script auxiliar para baixar a fonte usada no jogo
└── placar-dama/
    ├── index.php         # Página principal do placar
    ├── reset.php         # Zera o histórico de partidas
    ├── style.css         # Visual espacial do placar
    └── placar.json       # Gerado automaticamente com o histórico de partidas
```

---

## 🛠️ Tecnologias

- **Python 3** — lógica do jogo, regras, validação de movimentos
- **Pygame** — renderização gráfica, input do mouse/teclado, loop do jogo
- **PHP** — leitura e exibição do placar de partidas
- **JSON** — formato usado para os dois lados (jogo e site) se comunicarem

---

## 📈 Roadmap (próximas evoluções)

- [x] Visual futurista/espacial — peças com brilho neon
- [x] Placar de partidas integrado (Python salva, PHP exibe)
- [ ] Animações de movimento e captura
- [ ] Efeitos sonoros
- [ ] Modo contra IA (algoritmo minimax)


---

## 👤 Autor

**Wallace Coimbra**
[GitHub](https://github.com/wallace-2105)

---

<p align="center">Feito com 🛸 e muito café</p>

