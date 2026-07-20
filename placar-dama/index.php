<?php
// Arquivo onde o jogo Python salva os resultados
$arquivoPlacar = __DIR__ . '/placar.json';

// Se o arquivo ainda não existe, cria vazio
if (!file_exists($arquivoPlacar)) {
    file_put_contents($arquivoPlacar, json_encode([]));
}

// Lê os resultados salvos
$conteudo = file_get_contents($arquivoPlacar);
$partidas = json_decode($conteudo, true);
if (!is_array($partidas)) {
    $partidas = [];
}

// Calcula estatísticas
$totalPartidas = count($partidas);
$vitoriasCiano = 0;
$vitoriasMagenta = 0;

foreach ($partidas as $partida) {
    if ($partida['vencedor'] === 'CIANO') {
        $vitoriasCiano++;
    } elseif ($partida['vencedor'] === 'MAGENTA') {
        $vitoriasMagenta++;
    }
}

// Ordena as partidas da mais recente pra mais antiga
$partidas = array_reverse($partidas);
?>
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Placar — Dama Space Edition</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

    <div class="fundo-estrelas"></div>

    <div class="container">
        <header>
            <h1>🛸 PLACAR — DAMA SPACE EDITION</h1>
            <p class="subtitulo">Histórico de partidas da sessão atual</p>
        </header>

        <section class="resumo">
            <div class="card-stat card-ciano">
                <span class="numero"><?= $vitoriasCiano ?></span>
                <span class="label">Vitórias Ciano</span>
            </div>
            <div class="card-stat card-total">
                <span class="numero"><?= $totalPartidas ?></span>
                <span class="label">Partidas Jogadas</span>
            </div>
            <div class="card-stat card-magenta">
                <span class="numero"><?= $vitoriasMagenta ?></span>
                <span class="label">Vitórias Magenta</span>
            </div>
        </section>

        <section class="historico">
            <h2>Histórico de Partidas</h2>

            <?php if ($totalPartidas === 0): ?>
                <p class="vazio">Nenhuma partida registrada ainda. Jogue uma partida de Dama pra ver o resultado aqui!</p>
            <?php else: ?>
                <table>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Vencedor</th>
                            <th>Data / Hora</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($partidas as $index => $partida): ?>
                            <tr>
                                <td><?= $totalPartidas - $index ?></td>
                                <td>
                                    <span class="badge badge-<?= strtolower($partida['vencedor']) ?>">
                                        <?= htmlspecialchars($partida['vencedor']) ?>
                                    </span>
                                </td>
                                <td><?= htmlspecialchars($partida['data']) ?></td>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            <?php endif; ?>
        </section>

        <form action="reset.php" method="post" onsubmit="return confirm('Tem certeza que quer zerar o placar?');">
            <button type="submit" class="botao-zerar">🗑️ Zerar Placar</button>
        </form>

        <footer>
            <p>Atualize a página após cada partida pra ver o resultado mais recente.</p>
        </footer>
    </div>

</body>
</html>
