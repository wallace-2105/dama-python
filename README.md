# Dama em Python (Pygame)

Jogo de Dama (Checkers) 2 jogadores, mesmo teclado/mouse, feito em Python com Pygame.

<!-- Coloque aqui um print ou GIF do jogo rodando -->
<!-- ![preview](preview.png) -->

## Funcionalidades

- Tabuleiro 8x8 com peças vermelhas e azuis
- Movimento na diagonal com validação de regras
- Captura obrigatória de peças adversárias (inclusive captura múltipla em sequência)
- Promoção a "Dama" ao alcançar a última linha
- Detecção de vitória
- Reiniciar partida a qualquer momento (tecla R)

## Como rodar

```bash
pip install -r requirements.txt
python3 dama.py
```

## Como jogar

- Clique em uma peça da sua cor pra selecionar
- Os movimentos possíveis aparecem marcados em verde no tabuleiro
- Clique na casa verde pra mover
- Vermelho começa jogando
- Pressione **R** a qualquer momento pra reiniciar a partida

## Tecnologias

- Python 3
- Pygame

## Possíveis melhorias futuras

- Modo contra IA (minimax)
- Placar salvo em banco de dados
- Sons de movimento e captura
